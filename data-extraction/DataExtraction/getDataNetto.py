import os
import asyncio
from pyppeteer import launch
import pymongo
from pyppeteer import errors
import pyppeteer
from pyppeteer.page import ConsoleMessage
from DataExtraction import config, helper
from random import randint
from datetime import datetime
import logging

# Mongo DB connection
conn = config.MONGO_URL
client = pymongo.MongoClient(conn)
db = client[config.MONGO_DB]
netto_col = db.netto_data_col_2
logs_col = db.data_ext_logs_col

logFile = 'Netto.log'
logging.basicConfig(filename=logFile, level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

## === Best Practices ====
# 1. Visit the website in intervals of 10 min or more
# 2. Use proxy servers
# 3. Use fingerprint rotation with headless browser
# 4 Use Scrapy frameworks
# 5. Change headers in request

vendor = 'Netto'
browser = None

async def getCategories(page):
    logging.info('====== Getting to all categories ======')
    #await helper.waitingTime(page)
    await page.waitForSelector('.sub-navigation__inner__list')
    # Gets basic information on each item
    categories = await page.evaluate(f"""() => {{
        var categories = []
        document.querySelectorAll('.sub-navigation__inner__list li').forEach(category => {{
            element = {{}}
            element.link = category.querySelector('a').href
            element.name = category.querySelector('a').innerText
            categories.push(element)
        }})
        return categories;
    }}""")
    logging.info(f'Categories: {categories}')
    return categories

async def readElements(category,page):
    logging.info(f'====== Reading elements {category}======')
    await page.goto(category["link"])
    await helper.waitingTime(page)
    nav = {}
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
    for i in range(0,(int(nav["lastPage"])+1)):
        logging.info(f' ======= Reading page {i}/{nav["lastPage"]} ========')
        # open initial URL
        if(i > 0):
            await page.goto(f'{nav["page"]}/{i}')
            await helper.waitingTime(page)
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
                newItem.vendor = 'Netto'
                newItem.status = true
                newItem.insert_dt = Date.now()
                newItem.category = '{category["name"]}'
                if(newItem.product_title != '')
                    items.push(newItem)
                }})
                return items
            }}""")
            # Insert elements into Mongo
            if(len(items) > 0 ):
                netto_col.insert_many(items)
                logging.info(f'Total items: {len(items)} inserted into Mongo')
            print('================')
        except errors.TimeoutError:
            logging.exception(f'{category} has with no items')
            pass




async def main():
    ''' Reading basic product information to retrieve categories and all links for second stage'''
    logging.info(f'%(asctime) ====== Starting {vendor} Basic extractor ====== \n === Opening browser ===')
    browser = await launch()
    page = await browser.newPage()

    initial_URL = 'https://www.netto-online.de/lebensmittel/c-N01'

    # Starts with the following link:
    logging.info('- Openning Netto website')
    await page.goto(initial_URL)
    await helper.waitingTime(page)
    # Accept cookies
    logging.info('- Accepting cookies')
    await page.waitForSelector('#CybotCookiebotDialog')
    await page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')

    categories = await getCategories(page)
    [await readElements(category,page) for category in categories]

    await browser.close()


async def details():
    ''' Reading individual product to extract its details'''
    logging.info(f'====== Starting {vendor} Detailed extractor ====== \n === Opening browser ===')
    # Load documents from mongo
    totalDocs = netto_col.count_documents({"detailedInfo.processed": None })
    logging.info(f'Total documents with no details: {totalDocs}')
    # Read products with missing details
    no_tabs = 30
    logging.info(f'{no_tabs} tabs configured for the browser')
    # Get all results
    for i in range(1,totalDocs+1):
        numPage = no_tabs *(i-1)
        logging.info(f' ------- Reading skip: {numPage} limit: {no_tabs} --------')
        logging.info(f'Reading products...')
        browser = await launch(headless=True)
        page = await browser.newPage()
        initial_URL = 'https://www.netto-online.de/lebensmittel/c-N01'
        await page.goto(initial_URL)
        await helper.waitingTime(page)
        # Accept cookies
        logging.info(f'=== Acccepting cookies ===')
        await page.waitForSelector('#CybotCookiebotDialog')
        await page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        # validate if there are still products that need detailed information
        if(netto_col.count_documents({"detailedInfo.processed": None }) == 0):
            logging.info(f'No more products to process')
            break
        for product in netto_col.find({"detailedInfo.processed": None }).skip(numPage).limit(no_tabs):
            page = await browser.newPage()
            await readDetails(page, product)
        await asyncio.sleep(1)
        logging.info(f'Products have been saved')
        logging.info(f'-------- Closing browser -----------')
        await browser.close()


async def readDetails(page, product):
    ''' Extracting detailed information for each product with basic information (from stage 1 of data processing)'''

    page = await browser.newPage()
    webPage = product["details"]
    logging.info(f'===== Visiting {webPage} ====== ')
    try:
        await page.goto(webPage)
        await helper.waitingTime(page)
        await page.waitForSelector('.detail-page__common-infos')
    except errors.TimeoutError:
        logging.error(f'page crashed! ... Trying to reloading it... ')
        await page.reload()
        # page = await browser.newPage()
        # webPage = product["details"]
        # logging.info(f'===== Visiting again {webPage} ====== ')
        # await page.goto(webPage)


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
    #await page.close()
    #logging.info(f'{product["product_title"]} added')
    netto_col.save(product)

def loadBasicInfo():
    asyncio.get_event_loop().run_until_complete(main())

def loadDetailedInfo():
    asyncio.get_event_loop().run_until_complete(details())


if __name__ == "__main__":
    loadBasicInfo()
    #loadDetailedInfo()
    logging.info(f"- Pipeline finished")