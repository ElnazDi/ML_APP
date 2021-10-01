import os
import asyncio
from pyppeteer import launch
import pymongo
from pyppeteer import errors
import config
import helper
from datetime import datetime

# Mongo DB connection
conn = config.MONGO_URL
client = pymongo.MongoClient(conn)
db = client[config.MONGO_DB]
rewe_col = db.rewe_data_col
logs_col = db.data_ext_logs_col

## === Best Practices ====
# 1. Visit the website in intervals of 10 min or more
# 2. Use proxy servers
# 3. Use fingerprint rotation with headless browser
# 4 Use Scrapy frameworks 
# 5. Change headers in request

vendor = 'Rewe'
browser = None

async def main():
    try:
        browser = await launch()
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
    
    
        print('Navigating to all articles')
        # 1- 89 pages
        for pag in range(40,90):
            # Load inital webpage
            webPage = f'https://filiale.kaufland.de/sortiment/das-sortiment.pageIndex={pag}.html'
            print(webPage)
            await helper.waitingTime(page)
            await page.goto(webPage)
            await page.waitForSelector('.o-overview-list__list-item')
            print('- Readig items')
            try:
                # Gets basic information on each item
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
                        newItem.status = true
                        newItem.insert_dt = Date.now()
                        items.push(newItem)
                    }});
                    return items;

                }}""")
                # Inserts the elements into Mongo
                rewe_col.insert_many(items)
                
            except errors.ElementHandleError as e:
                print(e)
            print(f'end Page {pag}')
           
        await browser.close()
    except e:
        print(e)
        await browser.close()
    

async def details():
    print('Getting products details')
    print('=== Opening browser === ')
    browser = await launch()
    page = await browser.newPage()
    initial_URL = 'https://filiale.kaufland.de/sortiment/das-sortiment.html'    
    
    await page.goto(initial_URL)
    await helper.waitingTime(page)
    
    # Accept cookies
    print('- Accepting cookies')
    await page.waitForSelector('.cookie-alert-extended-modal')
    await page.click('.cookie-alert-extended-button')
    
    # Load documents from mongo
    pageSize = 50
    for i in range (1,15):
        print(f'Loading {i} pagination')
        skipNum = pageSize * (i-1)
        results = rewe_col.find({"detailedInfo.processed": None }).skip(skipNum).limit(pageSize)
        [await readDetails(product, page) for product in results]
        

async def readDetails(product, page):
    webPage = product["details"]
    print(f'Visiting {webPage}')
    await helper.waitingTime(page)
    await page.goto(webPage)
    await page.waitForSelector('.t-assortment-detail__title')
    print(f'- Readig item {product}')
    # Gets basic information on each item
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
    print(item)
    product["detailedInfo"] = item
    rewe_col.save(product)
    print('Saved to DB')

    



asyncio.get_event_loop().run_until_complete(details())


print(f"- Pipeline finished")