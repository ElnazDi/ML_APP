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

class AldiExtractor():

    def __init__(self) -> None:
        # Mongo DB connection
        self.conn = configuration.MONGO_URL
        self.client = pymongo.MongoClient(self.conn)
        self.db = self.client[configuration.MONGO_DB]
        self.aldi_col = self.db.aldi_data
        self.etl_config = self.db.etl_config
        self.initial_URL = 'https://www.aldi-sued.de/de/produkte/produktsortiment.html'
        self.vendor = 'Aldi'
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
            self.browser = await launch(
                                        executablePath= '/home/airflow/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome',
                                        headless=True,
                                        options={'args':['--no-sandbox', '--disable-setuid-sandbox']}
                                    )
            page = await self.browser.newPage()
            # Starts with the following link:
            logging.info('- Openning Aldi website')
            await page.goto(self.initial_URL)
            await helper.waitingTime(page)
            # Accept cookies
            logging.info('- Accepting cookies')
            await page.waitForSelector('#c-modal')
            await page.click('.js-privacy-accept')
            await page.close()
            logging.info('-Browser ready')
        except:
            logging.exception('Problem opening browser in initBrowser!!')
            return

    async def closeBrowser(self):
        try:
            await self.browser.close()
        except:
            logging.exception(f'Problem while closing the browser!!')
            pass

    async def readCategories(self):
        ''' Read all categories that Aldi offers on its website'''
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
        ''' Scraps the category links from Aldi website'''
        try:
            await self.initBrowser()
        except:
            logging.exception('Problem in browser')
            return
        try:
            logging.info(f'====== Starting: Getting to all categories ======')
            page = await self.browser.newPage()
            await page.goto(self.initial_URL)
            await helper.waitingTime(page)
            await page.waitForSelector('.parbase')
            # Gets basic information on each item
            logging.info(f'====== Replacing categories ======')
            categories = await page.evaluate(f"""() => {{
                var categories = []
                document.querySelectorAll('.wrapRichText p a').forEach(node => {{
                    category = {{}}
                    if(node.innerText != '' && node.innerText != 'Zur Übersicht'){{
                        category.link = node.href
                        category.name = node.innerText
                        category.visited = false
                        category.lastVisitedLink = ''
                        category.lastVisitedPage = 0
                        categories.push(category)
                    }}
                }})
                return categories;
            }}""")
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
        try:
            await page.waitForSelector('.container-full')
            nav = await page.evaluate(f"""() => {{
                function sleep(ms) {{
                    return new Promise(resolve => setTimeout(resolve, ms));
                }}

                async function pag(npage, pageNumber, el){{
                    while (npage < pageNumber){{
                        await sleep(4000)
                        el.click()
                        npage = el.getAttribute("data-npage")
                        pageNumber = el.getAttribute("data-pagenumber")
                    }}
                }}

                var el = document.querySelector('#showMore')
                var npage = el.getAttribute("data-npage")
                var pageNumber = el.getAttribute("data-pagenumber")
                //Small validation to read a few pages
                //if(pageNumber > 10) pageNumber=10
                pag(npage, pageNumber,el)
                return pageNumber

            }}""")
            logging.info(f' ===== Pagination found. Pags: {nav} ====== ')
        except:
            logging.info('No pagination')

        try:
            #await helper.waitingTime(page)
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
                document.querySelectorAll('.item').forEach(item => {{
                    newItem = {{}}
                    newItem.image = validate(item.querySelector(".at-product-images_img"), 1)
                    //newItem.brand = validate(item.querySelector(".default"))
                    newItem.product_title = validate(item.querySelector(".product-title"))
                    newItem.content = validate(item.querySelector(".additional-product-info"))
                    //newItem.price_per_unit = validate(item.querySelector(".de"))
                    //newItem.discount = validate(item.querySelector(".default"))
                    newItem.old_price = validate(item.querySelector(".price_before"))
                    newItem.current_price = validate(item.querySelector(".price"))
                    newItem.details = validate(item.querySelector("a"), 2)
                    badges = []
                    item.querySelectorAll(".card_badges img").forEach((img) => {{
                        badges.push(img.src)
                    }})
                    newItem.badges = badges
                    newItem.vendor = '{self.vendor}'
                    newItem.status = true
                    newItem.category = '{category["name"]}'
                    newItem.subcategory = '{category["name"]}'
                    if (newItem.product_title != '') {{
                        items.push(newItem)
                        //console.log("=======================")
                    }}
                }})
                return items

            }}""")
            # Adding products into Mongo
            logging.info(f'Inserting {len(items)} documents into Mongo')
            # Insert elements into Mongo
            if(len(items) > 0 ):
                for item in items:
                    item["insert"] = self.start_process
                    self.aldi_col.insert_one(item)

                    # Updates the last link read by the process
                self.etl_config.update_one({"categories.name":category["name"],
                                            "vendor":self.vendor},
                                            {"$set":
                                                {"categories.$.link":category["link"],
                                                "categories.$.lastVisitedLink":category["link"],
                                                "categories.$.lastVisitedPage":nav,
                                                "categories.$.visited":True
                                                }})
                logging.info(f'Total items: {len(items)} inserted into Mongo')
                print('================')

        except errors.TimeoutError:
            self.etl_config.update_one({"categories.name":category["name"]},
                                            {"$set":
                                                {"categories.$.link":category["link"],
                                                "categories.$.lastVisitedLink":category["link"],
                                                "categories.$.lastVisitedPage":nav
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
            logging.exception('Problem in browser')
            return
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
        logging.info(f'{product["product_title"]} with link {webPage}')
        try:
            await page.goto(webPage)
            #await helper.waitingTime(page)
            await page.waitForSelector('.pdp_h1')
        except errors.TimeoutError:
            logging.exception(f'page crashed! ... Trying to reloading it... ')
            page.goto(webPage)
            return
        try:
            # Gets detailed information on each item
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
                newItem.image = validate(document.querySelector(".zoom-ico-image img"), 1)
                imgs = []
                var temp = []
                document.querySelectorAll(".slick-slide").forEach((img) => {{ imgs.push(img.getAttribute('data-srcset-sm')) }})
                newItem.thumbnail_img = imgs
                newItem.product_title = document.querySelector(".target_product_name").innerText
                temp = []
                document.querySelectorAll(".product-description").forEach(x => temp.push(validate(x)))
                newItem.product_description = temp.join(' ')
                newItem.product_properties = validate(document.querySelector(".tab-content-container li"))
                /*
                temp = []
                document.querySelectorAll(".food-labeling__text p").forEach(x => temp.push(validate(x)))
                newItem.ingredients = temp.join(' ')
                temp = []
                document.querySelectorAll(".food-labeling__table-wrapper table").forEach(x => temp.push(validate(x)))
                newItem.nutritional_info = temp.join(' ')
                newItem.prep_instruction = validate(document.querySelector(".default"))
                newItem.hints = validate(document.querySelector(".default"))
                newItem.manufacturer = validate(document.querySelector(".brand-image-box img"), 3)
                */
                newItem.processed = true
                newItem.insert_dt = Date.now()
                return newItem;

            }}""")
            product["detailedInfo"] = item
            product["updated"] = self.start_process
            self.aldi_col.save(product)
        except errors.TimeoutError:
            self.etl_config.insert_one({"details":webPage,"loaded":False,"insert":self.start_process})
            logging.exception(f'Problem loadding {webPage} !')

    async def readDetails(self):
        ''' Reading individual product to extract its details'''
        logging.info(f'====== Starting {self.vendor} Detiled extractor ======')

        totalDocs = self.aldi_col.count_documents({"detailedInfo.processed": None })
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
                logging.exception('Problem in browser')
                break
            # validate if there are still products that need detailed information
            if(self.aldi_col.count_documents({"detailedInfo.processed": None }) == 0):
                logging.info(f'No more products to process')
                break
            for product in self.aldi_col.find({"detailedInfo.processed": None }).skip(numPage).limit(self.noTabs):
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
    aldi = AldiExtractor()
    aldi.etlReadCategories()
    #loadDetailedInfo()
    logging.info(f"- Pipeline finished")