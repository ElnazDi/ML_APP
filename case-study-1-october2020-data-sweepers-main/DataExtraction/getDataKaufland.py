import os
import asyncio
from pyppeteer import launch
import pymongo
from pyppeteer import errors
from DataExtraction import config, helper
#import config
#import helper
from datetime import datetime
import logging

# Mongo DB connection
conn = config.MONGO_URL
client = pymongo.MongoClient(conn)
db = client[config.MONGO_DB]
kaufland_col = db.kaufland_data_col_2
logs_col = db.data_ext_logs_col

logFile = 'Kaufland.log'
logging.basicConfig(filename=logFile, level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')


## === Best Practices ====
# 1. Visit the website in intervals of 10 min or more
# 2. Use proxy servers
# 3. Use fingerprint rotation with headless browser
# 4 Use Scrapy frameworks
# 5. Change headers in request

vendor = 'Kaufland'
browser = None


async def getCategories(page):
    print('====== Getting to all categories ======')
    #await helper.waitingTime(page)
    await page.waitForSelector('.m-accordion__list')
    # Gets basic information on each item
    categories = await page.evaluate(f"""() => {{
        var categories = []
        document.querySelectorAll('.m-accordion__item--level-2').forEach(category => {{
                category_desc = category.querySelector('a').innerText
                category.querySelectorAll('.m-accordion__item--level-3').forEach(subcategory => {{
                    element = {{}}
                    element.category = category_desc
                    element.link = subcategory.querySelector('a').href
                    element.name = subcategory.querySelector('a').innerText
                    if(!category_desc.startsWith('\\n'))
                        categories.push(element)
                }})
            }})
        return categories;
    }}""")
    #print(categories)
    return categories


async def readElements(category,page):
    print('====== Reading elements ======')
    print(category)
    nav = category["link"]
    # read url and last page for pagination
    try:
        while(True):
        # Scrape the webpage
            await page.goto(nav)
            await helper.waitingTime(page)
            await page.waitForSelector('.o-overview-list__list-item')
            print('- Readig items')
            # Gets basic information on each item
            # scroll = await page.evaluate(f"""() => {{
            #     function Sleep(milliseconds) {{
            #         return new Promise(resolve => setTimeout(resolve, milliseconds));
            #     }}

            #     async function scrollDown(){{
            #       	for (i = 0; i< 11; i++){{
            #           window.scrollBy(0, 800);
            #           await Sleep(2000);
            #         }}

            #     }}
            #     await scrollDown();
            #     return true

            # }}""")
            # print(scroll)

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
                    newItem.vendor = 'Kaufland'
                    newItem.category = '{category["category"]}'
                    newItem.subcategory = '{category["name"]}'
                    newItem.status = true
                    newItem.insert_dt = Date.now()
                    items.push(newItem)
                }});
                return items;

            }}""")
            # Inserts the elements into Mongo
            print(f'Inserting {len(items)} documents into Mongo')
            kaufland_col.insert_many(items)
            # Read next page
            nav = await page.evaluate(f"""() => {{
                return document.querySelector('.m-pagination__item--next a').href
            }}""")

    except:
        print('End of pagination')
        pass # There's only one


async def main():
    #try:
    browser = await launch(headless=True)
    page = await browser.newPage()

    initial_URL = 'https://filiale.kaufland.de/sortiment/das-sortiment.html'

    # Starts with the following link:
    print('- Openning Kaufland website > Lebensmittel')
    await page.goto(initial_URL)
    await helper.waitingTime(page)
    # Accept cookies
    print('- Accepting cookies')
    await page.waitForSelector('.cookie-alert-extended-modal')
    await page.click('.cookie-alert-extended-button')

    print('===== Reading all categories')
    links = await getCategories(page)
    [await readElements(link, page) for link in links]



async def details():
    ''' Reading individual product to extract its details'''
    logging.info(f'====== Starting {vendor} Detiled extractor ====== \n === Opening browser ===')
    totalDocs = kaufland_col.count_documents({"detailedInfo.processed": None })
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
        initial_URL = 'https://filiale.kaufland.de/sortiment/das-sortiment.html'
        await page.goto(initial_URL)
        await helper.waitingTime(page)
        # Accept cookies
        logging.info('- Accepting cookies')
        await page.waitForSelector('.cookie-alert-extended-modal')
        await page.click('.cookie-alert-extended-button')
        # validate if there are still products that need detailed information
        if(kaufland_col.count_documents({"detailedInfo.processed": None }) == 0):
            logging.info(f'No more products to process')
            break
        for product in kaufland_col.find({"detailedInfo.processed": None }).skip(numPage).limit(no_tabs):
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
    logging.info(f' =============== Visiting {webPage}')
    await helper.waitingTime(page)
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
        newItem.insert_dt = Date.now()
        return newItem;

    }}""")
    product["detailedInfo"] = item
    #await page.close()
    kaufland_col.save(product)






def loadBasicInfo():
    asyncio.get_event_loop().run_until_complete(main())

def loadDetailedInfo():
    asyncio.get_event_loop().run_until_complete(details())


if __name__ == "__main__":
    #loadBasicInfo()
    loadDetailedInfo()
    logging.info(f"- Pipeline finished")