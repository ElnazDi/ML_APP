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

class NettoExtractor():

    def __init__(self) -> None:
        # Mongo DB connection
        self.conn = configuration.MONGO_URL
        self.client = pymongo.MongoClient(self.conn)
        self.db = self.client[configuration.MONGO_DB]
        self.netto_col = self.db.netto_data
        self.etl_config = self.db.etl_config
        self.initial_URL = 'https://www.netto-online.de/lebensmittel/c-N01'
        self.vendor = 'Netto'
        self.categories = []
        self.browser = None
        self.noTabs = 12
        self.start_process = datetime.now()
        logFile = f'{self.vendor}.log'
        logging.basicConfig(filename=logFile, level=logging.INFO,
            format='%(asctime)s:%(levelname)s:%(message)s')


    async def initBrowser(self):
        ''' Init a new browser to open links from vendor'''
        try:
            self.browser = await launch(headless=True, options={'args':['--no-sandbox', '--disable-setuid-sandbox']})
            page = await self.browser.newPage()
            # Starts with the following link:
            logging.info('- Openning Netto website')
            await page.goto(self.initial_URL)
            await helper.waitingTime(page)
            # Accept cookies
            logging.info('- Accepting cookies')
            logging.info('- Accepting cookies')
            await page.waitForSelector('#CybotCookiebotDialog')
            await page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
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
        ''' Scraps the category links from Netto website'''
        try:
            await self.initBrowser()
            logging.info(f'====== Starting: Getting to all categories ======')
            page = await self.browser.newPage()
            await page.goto(self.initial_URL)
            #await helper.waitingTime(page)
            await page.waitForSelector('.sub-navigation__inner__list')
            # Gets basic information on each item
            logging.info(f'====== Replacing categories ======')
            categories = await page.evaluate(f"""() => {{
                var categories = []
                document.querySelectorAll('.sub-navigation__inner__list li').forEach(category => {{
                    element = {{}}
                    element.link = category.querySelector('a').href
                    element.name = category.querySelector('a').innerText
                    element.visited = false
                    element.lastVisitedLink = ''
                    element.lastVisitedPage = 0
                    categories.push(element)
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
        page = await self.browser.newPage()
        await page.goto(category["link"])
        nav = {}
        # Load navigation
        try:
            await page.waitForSelector('.pagination')
            nav = await page.evaluate(f"""() => {{
                pags = {{}}
                var elements = document.querySelectorAll('.tc-search-pagination')
                var temp =  elements[elements.length -1].querySelector('a').href.split('/')
                pags.lastPage = temp.pop()
                pags.page = temp.join('/')
                return pags
            }}""")
            logging.info(f' ===== Pags: {nav["lastPage"]} {nav["page"]} ====== ')
        except:
            nav["lastPage"] = 1
            logging.info('No pagination')
        nav["page"] = category["link"]
        logging.info(f'Pagination found {nav["page"]}/{nav["lastPage"]} ')

        # Pagination
        flagError = False
        for i in range(0,(int(nav["lastPage"])+1)):
            logging.info(f' ======= Reading page {i}/{nav["lastPage"]} ========')
            # open initial URL
            if(i > 0):
                await page.goto(f'{nav["page"]}/{i}')
                #await helper.waitingTime(page)
            try:
                await page.waitForSelector('.product-list')
                items = await page.evaluate(f"""() => {{

                    function validate(element, src = 0) {{
                        if (element == undefined)
                            return ''
                        if (src == 0)
                            return element.innerText
                        else if (src == 1)
                            return element.src
                        else if (src == 3)
                            return element.alt
                        return element.href
                    }}

                    items = []
                    document.querySelectorAll('.product-list .product-list__item').forEach(item => {{
                    newItem = {{}}
                    newItem.image = validate(item.querySelector(".product__image"), 1)
                    //newItem.brand = validate(item.querySelector(".default"))
                    newItem.product_title = validate(item.querySelector(".product__title__inner"))
                    newItem.content = validate(item.querySelector(".product__min-order"))
                    newItem.price_per_unit = validate(item.querySelector(".product__base-price"))
                    newItem.discount = validate(item.querySelector(".product__percent-saving__text"))
                    newItem.old_price = validate(item.querySelector(".product__old-price"))
                    newItem.current_price = validate(item.querySelector(".js-productile-price"))
                    newItem.details = validate(item.querySelector(".product"), 2)
                    newItem.vendor = '{self.vendor}'
                    newItem.category = '{category["name"]}'
                    newItem.subcategory = '{category["name"]}'
                    newItem.status = true
                    //newItem.insert_dt = Date.now()
                    if(newItem.product_title != '')
                        items.push(newItem)
                    }})
                    return items
                }}""")
                # Adding products into Mongo
                logging.info(f'Inserting {len(items)} documents into Mongo')
                if(len(items) > 0 ):
                    for item in items:
                        item["insert"] = self.start_process
                        self.netto_col.insert_one(item)

                        # Updates the last link read by the process
                    self.etl_config.update_one({"categories.name":category["name"],
                                                "vendor":self.vendor},
                                                {"$set":
                                                    {"categories.$.link":nav["page"],
                                                    "categories.$.lastVisitedLink":nav["page"],
                                                    "categories.$.lastVisitedPage":i
                                                    }})

                    logging.info(f'Total items: {len(items)} inserted into Mongo')
                print('================')

            except errors.PageError:
                # Updates the last link read by the process
                flagError = True
                self.etl_config.update_one({"categories.name":category["name"]},
                                            {"$set":
                                                {"categories.$.link":nav["page"],
                                                "categories.$.lastVisitedLink":nav["page"],
                                                "categories.$.lastVisitedPage":i
                                                }})
                logging.info(f'Page error in {category["category"]} while reading {category["lastVisitedLink"]} in page {category["lastVisitedPage"]}')
                pass
        # If there was no error
        if(flagError is not True):
            logging.info(f'End of pagination and updating Mongo for {category["name"]}')
            self.etl_config.update_one({"categories.name":category["name"]},
                                            {"$set":
                                                {"categories.$.link":nav["page"],
                                                "categories.$.lastVisitedLink":nav["page"],
                                                "categories.$.lastVisitedPage":i,
                                                "categories.$.visited":True
                                                }})
            logging.info(f'Category updated {category}')

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
        page = await self.browser.newPage()
        webPage = product["details"]
        logging.info(f' =============== Visiting {webPage}')
        try:
            await page.goto(webPage)
            #await helper.waitingTime(page)
            await page.waitForSelector('.detail-page__common-infos')
        except errors.TimeoutError:
            logging.exception(f'page crashed! ... Trying to reloading it... ')
            page = await self.browser.newPage()
            await page.goto(webPage)
            #await helper.waitingTime(page)
            await page.waitForSelector('.detail-page__common-infos')
            return

        # Gets basic information on each item
        try:
            item = await page.evaluate(f"""() => {{

                function validate(element, src = 0) {{
                            if (element == undefined)
                                return ''
                            if (src == 0)
                                return element.innerText
                            else if (src == 1)
                                return element.src
                            else if (src == 3)
                                return element.alt
                            return element.href
                }}

                newItem = {{}}
                newItem.image = validate(document.querySelector(".productImage"), 1)
                imgs = []
                var temp = []
                document.querySelectorAll(".ImageApp img").forEach((img) => {{ imgs.push(img.src) }})
                newItem.thumbnail_img = imgs
                newItem.product_title = document.querySelector(".tc-pdp-productname").innerText
                temp = []
                document.querySelectorAll(".detail-page-section__description-wrapper__description p").forEach(x => temp.push(validate(x)))
                newItem.product_description = temp.join(' ')
                newItem.product_properties = validate(document.querySelector(".default"))
                temp = []
                document.querySelectorAll(".food-labeling__text p").forEach(x => temp.push(validate(x)))
                newItem.ingredients = temp.join(' ')
                temp = []
                document.querySelectorAll(".food-labeling__table-wrapper table").forEach(x => temp.push(validate(x)))
                newItem.nutritional_info = temp.join(' ')
                newItem.prep_instruction = validate(document.querySelector(".default"))
                newItem.hints = validate(document.querySelector(".default"))
                newItem.manufacturer = validate(document.querySelector(".brand-image-box img"), 3)
                newItem.processed = true
                newItem.insert_dt = Date.now()
                return newItem;

            }}""")
            product["detailedInfo"] = item
            product["updated"] = self.start_process
            self.netto_col.save(product)
        except errors.TimeoutError:
            self.etl_config.insert_one({"details":webPage,"loaded":False,"insert":self.start_process})
            logging.exception(f'Problem loadding {webPage} !')
            return

    async def readDetails(self):
        ''' Reading individual product to extract its details'''
        logging.info(f'====== Starting {self.vendor} Detiled extractor ======')

        totalDocs = self.netto_col.count_documents({"detailedInfo.processed": None })
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
            if(self.netto_col.count_documents({"detailedInfo.processed": None }) == 0):
                logging.info(f'No more products to process')
                break
            for product in self.netto_col.find({"detailedInfo.processed": None }).skip(numPage).limit(self.noTabs):
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
    netto = NettoExtractor()
    netto.etlReadCategories()
    #loadDetailedInfo()
    logging.info(f"- Pipeline finished")