import os
import sys

sys.path.append('/opt/airflow')

import asyncio
from pyppeteer import launch
import pymongo
from pyppeteer import errors
from config import configuration, helper
from datetime import datetime
import logging


class KauflandExtractor():

    def __init__(self) -> None:
        # Mongo DB connection
        self.conn = configuration.MONGO_URL
        self.client = pymongo.MongoClient(self.conn)
        self.db = self.client[configuration.MONGO_DB]
        self.kaufland_col = self.db.kaufland_data
        self.etl_config = self.db.etl_config
        self.initial_URL = 'https://filiale.kaufland.de/sortiment/das-sortiment.html'
        self.offers_URL = 'https://filiale.kaufland.de/angebote/aktuelle-woche.html'
        self.vendor = 'Kaufland'
        self.categories = []
        self.browser = None
        self.noTabs = 10
        self.start_process = datetime.now()
        logFile = f'{self.vendor}.log'
        logging.basicConfig(filename=logFile, level=logging.INFO,
            format='%(asctime)s:%(levelname)s:%(message)s')

    async def initBrowser(self):
        ''' Init a new browser to open links from vendor'''
        try:
            self.browser = await launch(options={'args':['--no-sandbox', '--disable-setuid-sandbox']},headless=True)
            page = await self.browser.newPage()
            # Starts with the following link:
            logging.info('- Openning Kaufland website > Lebensmittel')
            await page.goto(self.initial_URL)
            await helper.waitingTime(page)
            # Accept cookies
            logging.info('- Accepting cookies')
            await page.waitForSelector('.cookie-alert-extended-modal')
            await page.click('.cookie-alert-extended-button')
            await page.close()
            logging.info('-Browser ready')
        except:
            logging.exception('Problem opening browser in initBrowser!!')

    async def closeBrowser(self):
        try:
            await self.browser.close()
        except:
            logging.exception(f'Problem while closing the browser!!')
            pass

    async def readCategories(self):
        ''' Read all categories that Kaufland offers on its website'''
        try:
            # if the process didn't have any error, read categories for the first time
            if(self.etl_config.count_documents({"vendor":self.vendor}) == 0):
                logging.info('===== Reading all categories')
                await self._readCategoryLinks()
                logging.info('===== Writing categories')
                log_process = {}
                log_process["vendor"] = self.vendor
                log_process["execution_dt"] = self.start_process
                log_process["categories"] = self.categories
                if(len(self.categories) > 0):
                    self.etl_config.insert_one(log_process)
                    logging.info('===== Categories inserted')
                else:
                    raise Exception(f'Empty Categories in {self.vendor} Extractor')
            else: # in case of re-run
                self.categories = [categories["categories"] for categories in self.etl_config.find({"categories.visited":False,"vendor":self.vendor})]
                logging.info(f'===== Existing categories')

        except:
            logging.exception('Problem loading categories readCategories!!')

    async def _readCategoryLinks(self):
        ''' Scraps the category links from Kaufland website'''
        try:
            await self.initBrowser()
            logging.info(f'====== Starting: Getting to all categories ======')
            page = await self.browser.newPage()
            await page.goto(self.initial_URL)
            #await helper.waitingTime(page)
            await page.waitForSelector('.m-accordion__list')
            # Gets basic information on each item
            logging.info(f'====== Replacing categories ======')
            categories = await page.evaluate(f"""() => {{
                var categories = []
                document.querySelectorAll('.m-accordion__item--level-2').forEach(category => {{
                        category_desc = category.querySelector('a').innerText
                        category.querySelectorAll('.m-accordion__item--level-3').forEach(subcategory => {{
                            element = {{}}
                            element.category = category_desc
                            element.link = subcategory.querySelector('a').href
                            element.name = subcategory.querySelector('a').innerText
                            element.visited = false
                            element.lastVisitedLink = ''
                            element.lastVisitedPage = 0
                            element.maxPags = 0
                            if(!category_desc.startsWith('\\n'))
                                categories.push(element)
                        }})
                    }})
                return categories;
            }}""")
            #logging.info(f'{categories}')
            self.categories = categories
            await self.closeBrowser()
            logging.info(f'====== Finishing: Getting to all categories ======')
        except errors.TimeoutError:
            logging.exception('Selector not found in _readCategoryLinks')
        except errors.PyppeteerError:
            logging.exception('Pyppeteer Error in _readCategoryLinks')

    async def _readBasicData(self, category):
        ''' Read  all categories that cotains products for this vendor'''
        logging.info(f'====== Reading elements for {category} ======')
        nav = category["link"]
        # read url and last page for pagination
        try:
            page = await self.browser.newPage()
            currentPage = 0
            while(True):
            # Scrape the webpage
                await page.goto(nav)
                #await helper.waitingTime(page)
                await page.waitForSelector('.o-overview-list__list-item')
                logging.info('- Readig items')
                items = await page.evaluate(f"""() => {{

                    function validate(element, src = 0) {{
                        if (element == undefined)
                            return ''
                        if (src == 0)
                            return element.innerText
                        else if (src == 1)
                            return element.src
                        return element.href
                    }}

                    var items = []
                    document.querySelectorAll('.o-overview-list__list-item').forEach(function (item) {{
                        newItem = {{}}
                        newItem.image = validate(item.querySelector(".o-overview-list__list-item img.a-image-responsive"), 1)
                        newItem.brand = validate(item.querySelector(".o-overview-list__list-item h5.m-offer-tile__subtitle"))
                        newItem.product_title = validate(item.querySelector(".o-overview-list__list-item h4.m-offer-tile__title"))
                        newItem.content = validate(item.querySelector(".o-overview-list__list-item div.m-offer-tile__quantity"))
                        newItem.price_per_unit = validate(item.querySelector(".o-overview-list__list-item div.m-offer-tile__basic-price"))
                        newItem.discount = validate(item.querySelector(".o-overview-list__list-item div.a-pricetag__discount"))
                        newItem.old_price = validate(item.querySelector(".o-overview-list__list-item div.a-pricetag__old-price"))
                        newItem.current_price = validate(item.querySelector(".o-overview-list__list-item .a-pricetag__price"))
                        newItem.details = validate(item.querySelector("a.m-offer-tile__link"), 2)
                        newItem.vendor = '{self.vendor}'
                        newItem.category = '{category["category"]}'
                        newItem.subcategory = '{category["name"]}'
                        newItem.status = true
                        //newItem.insert_dt = new Date()
                        items.push(newItem)
                    }});
                    return items;
                }}""")
                # Adding products into Mongo
                logging.info(f'Inserting {len(items)} documents into Mongo')
                if(len(items) > 0 ):
                    for item in items:
                        item["insert"] = self.start_process
                        self.kaufland_col.insert_one(item)
                    currentPage += 1
                    # Updates the last link read by the process
                    self.etl_config.update_one({"categories.name":category["name"],
                                                "vendor":self.vendor},
                                                {"$set":
                                                    {"categories.$.link":nav,
                                                    "categories.$.lastVisitedLink":nav,
                                                    "categories.$.lastVisitedPage":currentPage
                                                    }})
                    logging.info(f'Category updated {category}')
                    logging.info(f'Total items: {len(items)} inserted into Mongo')
                # Read next page
                nav = await page.evaluate(f"""() => {{
                    return document.querySelector('.m-pagination__item--next a').href
                }}""")
        except errors.ElementHandleError:
            logging.info(f'End of pagination and updating Mongo for {category["name"]}')
            self.etl_config.update_one({"categories.name":category["name"]},
                                            {"$set":
                                                {"categories.$.link":nav,
                                                "categories.$.lastVisitedLink":nav,
                                                "categories.$.lastVisitedPage":currentPage,
                                                "categories.$.visited":True
                                                }})
            logging.info(f'Category updated {category}')
        except errors.PageError:
            # Updates the last link read by the process
            self.etl_config.update_one({"categories.name":category["name"]},
                                        {"$set":
                                            {"categories.$.link":nav,
                                            "categories.$.lastVisitedLink":nav,
                                            "categories.$.lastVisitedPage":currentPage
                                            }})
            logging.info(f'Page error in {category["category"]} while reading {category["lastVisitedLink"]} in page {category["lastVisitedPage"]}')


    async def readBasicData(self):
        ''' Init a new browser to open links from vendor'''
        logging.info('==== Reading all categories that have not been visited yet')
        self.categories = [categories["categories"] for categories in self.etl_config.find({"categories.visited":False,"vendor":self.vendor})]
        self.categories = self.categories[0]
        logging.info(f'===== Opening Browser for {len(self.categories)} categories')
        try:
            await self.initBrowser()
            logging.info(f'-------- Opening browser -----------')
        except:
            raise Exception('Problem opening the browser')
        for category in self.categories:
            if category["visited"] is not True:
                try:
                    await self._readBasicData(category)
                except:
                    logging.exception(f'Problem reading basic data for {category}. Moving onto the next one')
                    pass
        try:
            await self.closeBrowser()
            logging.info(f'-------- Closing browser -----------')
        except:
            raise Exception('Problem opening the browser')

    async def _readDetails(self, product):
        ''' Extracting detailed information for each product with basic information (from stage 1 of data processing)'''
        try:
            page = await self.browser.newPage()
            webPage = product["details"]
            logging.info(f' =============== Visiting {webPage}')
            #await helper.waitingTime(page)
            await page.goto(webPage)
            await page.waitForSelector('.page__content')
            # Gets detailed information on each item
            item = await page.evaluate(f"""() => {{
                function validate(element, src = 0) {{
                    if (element == undefined)
                        return ''
                    if (src == 0)
                        return element.innerText
                    else if (src == 1)
                        return element.src
                    return element.href
                }}
                newItem = {{}}
                imgs = []
                newItem.image = validate(document.querySelector(".a-image-responsive"), 1)
                document.querySelectorAll(".o-product-gallery img").forEach((img) => {{imgs.push(img.src)}})
                newItem.thumbnail_img = imgs
                newItem.product_title = validate(document.querySelector(".t-assortment-detail__title"))
                newItem.product_description = validate(document.querySelector("div#section-description p"))
                newItem.product_properties = validate(document.querySelector(".t-assortment-detail__properties"))
                newItem.ingredients = validate(document.querySelector("div#section-composition p"))
                newItem.prep_instruction = validate(document.querySelector("div#section-preparationInstructions p"))
                newItem.hints = validate(document.querySelector("div#section-hints p"))
                newItem.manufacturer = validate(document.querySelector("div#section-producer p"))
                newItem.processed = true
                return newItem;

            }}""")
            product["detailedInfo"] = item
            product["updated"] = self.start_process
            self.kaufland_col.save(product)
        except errors.PageError:
            self.etl_config.insert_one({"details":webPage,"loaded":False,"insert":self.start_process})
            logging.exception(f'Problem loadding {webPage} !')

    async def readDetails(self):
        ''' Reading individual product to extract its details'''
        logging.info(f'====== Starting {self.vendor} Detiled extractor ======')

        totalDocs = self.kaufland_col.count_documents({"detailedInfo.processed": None })
        logging.info(f'Total documents with no details: {totalDocs}')

        # Read products with missing details
        logging.info(f'{self.noTabs} tabs configured for the browser')

        # Get all results
        for i in range(1,totalDocs+1):
            numPage = self.noTabs *(i-1)
            logging.info(f' ------- Reading skip: {numPage} limit: {self.noTabs} --------')
            logging.info(f'Reading products...')
            try:
                await self.initBrowser()
                logging.info(f'-------- Opening browser -----------')
            except:
                raise Exception('Problem opening the browser')
            # validate if there are still products that need detailed information
            if(self.kaufland_col.count_documents({"detailedInfo.processed": None }) == 0):
                logging.info(f'No more products to process')
                break
            for product in self.kaufland_col.find({"detailedInfo.processed": None }).skip(numPage).limit(self.noTabs):
                try:
                    await self._readDetails(product)
                    await asyncio.sleep(0.05)
                    logging.info(f'Products have been saved')
                except:
                    logging.exception(f'{product["product_title"]} has a problem reading its details. Moving onto the next products')
                    pass
            try:
                await self.closeBrowser()
                logging.info(f'-------- Closing browser -----------')
            except:
                raise Exception('Problem closing the browser')


    def etlReadCategories(self):
        asyncio.get_event_loop().run_until_complete(self.readCategories())

    def etlBasicInfo(self):
        asyncio.get_event_loop().run_until_complete(self.readBasicData())

    def etlDetailedInfo(self):
        asyncio.get_event_loop().run_until_complete(self.readDetails())

if __name__ == "__main__":
    #loadBasicInfo()
    kaufland = KauflandExtractor()
    kaufland.etlBasicInfo()
    logging.info(f"- Pipeline finished")