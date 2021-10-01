import os
import asyncio
from pyppeteer import launch
import pymongo
from pyppeteer import errors
from pyppeteer.page import ConsoleMessage
from DataExtraction import config, helper
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

logFile = 'Aldi.log'
logging.basicConfig(filename=logFile, level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

## === Best Practices ====
# 1. Visit the website in intervals of 10 min or more
# 2. Use proxy servers
# 3. Use fingerprint rotation with headless browser
# 4 Use Scrapy frameworks
# 5. Change headers in request

vendor = 'Aldi'
browser = None

async def getCategories(page):
    print('====== Getting to all categories ======')
    await helper.waitingTime(page)
    await page.waitForSelector('.parbase')
    # Gets basic information on each item
    categories = await page.evaluate(f"""() => {{
        var categories = []
        document.querySelectorAll('.wrapRichText p a').forEach(node => {{
            category = {{}}
            if(node.innerText != '' && node.innerText != 'Zur Übersicht'){{
                category.link = node.href
                category.name = node.innerText
                categories.push(category)
            }}
        }})
        return categories;
    }}""")
    print(categories)
    return categories

async def readElements(category,page):
    print('====== Reading elements ======')
    await page.goto(category["link"])
    await helper.waitingTime(page)
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
        print(f' ===== Pagination found. Pags: {nav} ====== ')
    except:
        print('No pagination')

    # Read basic details
    print(f' ======= Reading basic details {category["name"]} ========')
    try:
        await helper.waitingTime(page)
        #await page.waitForSelector('.product-list')
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
                newItem.vendor = 'Aldi'
                newItem.status = true
                newItem.insert_dt = Date.now()
                newItem.category = '{category["name"]}'
                if (newItem.product_title != '') {{
                    items.push(newItem)
                    //console.log("=======================")
                }}
            }})
            return items

        }}""")
        print('Inserting data into Mongo')
        # Insert elements into Mongo
        print(f'Total items: {len(items)}')
        if(len(items) > 0 ):
            aldi_col.insert_many(items)
            print('Inserted into Mongo')
        print('================')
    except errors.TimeoutError:
        print('Page with no items')
        pass




async def main():
    browser = await launch()
    page = await browser.newPage()

    initial_URL = 'https://www.aldi-sued.de/de/produkte/produktsortiment.html'

    # Starts with the following link:
    print('- Openning Aldi website')
    await page.goto(initial_URL)
    await helper.waitingTime(page)
    # Accept cookies
    print('- Accepting cookies')
    await page.waitForSelector('#c-modal')
    await page.click('.js-privacy-accept')

    categories = await getCategories(page)
    [await readElements(category,page) for category in categories]

    await browser.close()


async def details():
    ''' Reading individual product to extract its details'''
    logging.info(f'====== Starting {vendor} Detiled extractor ====== \n === Opening browser ===')
    totalDocs = aldi_col.count_documents({"detailedInfo.processed": None })
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
        initial_URL = 'https://www.aldi-sued.de/de/produkte/produktsortiment.html'
        await page.goto(initial_URL)
        await helper.waitingTime(page)
        # Accept cookies
        logging.info('- Accepting cookies')
        await page.waitForSelector('#c-modal')
        await page.click('.js-privacy-accept')
        # validate if there are still products that need detailed information
        if(aldi_col.count_documents({"detailedInfo.processed": None }) == 0):
            logging.info(f'No more products to process')
            break
        for product in aldi_col.find({"detailedInfo.processed": None }).skip(numPage).limit(no_tabs):
            page = await browser.newPage()
            await readDetails(page, product)
        await asyncio.sleep(1)
        logging.info(f'Products have been saved')
        logging.info(f'-------- Closing browser -----------')
        await browser.close()

async def readDetails(page, product):
    ''' Extracting detailed information for each product with basic information (from stage 1 of data processing)'''
    webPage = product["details"]
    logging.info(f'{product["product_title"]} with link {webPage}')
    await page.goto(webPage)
    await page.waitForSelector('.pdp_h1')
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
    # update record in Mongo Collection
    aldi_col.save(product)



def loadBasicInfo():
    asyncio.get_event_loop().run_until_complete(main())

def loadDetailedInfo():
    asyncio.get_event_loop().run_until_complete(details())


if __name__ == "__main__":
    #loadBasicInfo()
    loadDetailedInfo()
    logging.info(f"- Pipeline finished")