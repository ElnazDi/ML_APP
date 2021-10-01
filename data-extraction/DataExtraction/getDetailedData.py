import os
import asyncio
from pyppeteer import browser, launch
import pymongo
from pyppeteer import errors
from pyppeteer.page import ConsoleMessage
import config
import helper
from random import randint
from datetime import datetime
import concurrent.futures
from functools import partial
import logging

# Mongo DB connection
conn = config.MONGO_URL
client = pymongo.MongoClient(conn)
db = client[config.MONGO_DB]
aldi_col = db.aldi_data_col_2
logs_col = db.data_ext_logs_col

logFile = 'Aldi2.log'
logging.basicConfig(filename=logFile, level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

vendor = 'Aldi'

class Crawler():

    def __init__(self):
        self.no_pages = 10
        self.pages = []
        self.main_url = 'https://www.aldi-sued.de/de/produkte/produktsortiment.html'

    async def initBrowser(self):
        self.browser = await launch(headless=True)
        page = await self.browser.newPage()
        await page.goto(self.main_url)
        await helper.waitingTime(page)
        # Accept cookies
        logging.info('- Accepting cookies')
        await page.waitForSelector('#c-modal')
        await page.click('.js-privacy-accept')
        print('browser ready!')

    async def createPages(self):
        try:
            self.pages = [await self.browser.newPage() for _ in range(self.no_pages)]
        except errors.TimeoutError:
            print('Error creating the pages')
            self.pages = []

    async def closePages(self):
        for _ in range(self.no_pages):
            await self.browser.pages[_].close()
            print(f'Closing page {_}')


    async def readPage(self, product, page_index):
        asyncio.sleep(2)# self.browser.pages[page_index]




async def details():
    logging.info(f'====== Starting {vendor} Detiled extractor ====== \n === Opening browser ===')
    # Load documents from mongo
    totalDocs = aldi_col.count_documents({"detailedInfo.processed": None })
    logging.info(f'Total documents with no details: {totalDocs}')
    # Read products with missing details
    processedProducts = readDetails(browser, aldi_col.find({"detailedInfo.processed": None }))
    # Save into Mongo
    async for product in processedProducts:
        aldi_col.save(product)


async def readDetails(browser, products):
    for product in products:
        page = await browser.newPage()
        webPage = product["details"]
        logging.info(f' =============== Visiting {webPage}')
        page = await browser.newPage()
        await page.goto(webPage)
        await page.waitForSelector('.pdp_h1')
        # Gets basic information on each item
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
        await page.close()
        yield product





# def loadBasicInfo():
#     asyncio.get_event_loop().run_until_complete(main())

def loadDetailedInfo():
    asyncio.get_event_loop().run_until_complete(details())


if __name__ == "__main__":
    crawler = Crawler()
    crawler.initBrowser()
    crawler.createPages()
    asyncio.sleep(4)
    crawler.closePages()

    #loadBasicInfo()
    #loadDetailedInfo()
    logging.info(f"- Pipeline finished")