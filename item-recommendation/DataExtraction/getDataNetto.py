import os
import asyncio
from pyppeteer import launch
import pymongo
from pyppeteer import errors
import config
import helper
from random import randint
from datetime import datetime

# Mongo DB connection
conn = config.MONGO_URL
client = pymongo.MongoClient(conn)
db = client[config.MONGO_DB]
netto_col = db.netto_data_col
logs_col = db.data_ext_logs_col

## === Best Practices ====
# 1. Visit the website in intervals of 10 min or more
# 2. Use proxy servers
# 3. Use fingerprint rotation with headless browser
# 4 Use Scrapy frameworks 
# 5. Change headers in request

vendor = 'Netto'
browser = None


async def readSubcategories(page, category):
    ''' Get all links for each category'''
    # Open each link to get all the products after wating 1 sec (to simulate kind of human site interaction)
    
    
    # Open link inside this category
    await page.goto(category['url'])
    print('- Setting up waiting time')
    await helper.waitingTime(page)
    
    # Expand all categories (if any) in the current web page
    print('- Expanding all categories')

    await helper.waitingTime(page)
    # ==== Open links for one page =====
    print('- Collecting subcategories')
    subcategories = []
    try:
        subcategories = await page.evaluate(f"""() => {{
                    var subcategories = []
                    var subcategories_links = document.getElementsByClassName('sub-navigation__inner__list')[0].getElementsByTagName('a')
                    Array.from(subcategories_links).forEach(function(link){{
                        subcategory = {{}}
                        subcategory['name'] = link.innerText
                        subcategory['url'] = link.href
                        subcategory['category'] = '{category['name']}'
                        if((typeof link.href != 'undefined') && (link.href != '')){{
                            subcategories.push(subcategory)
                        }}                   
                    }})
                    return subcategories
                }}""")
        print(subcategories)
        print(type(subcategories))
        print(f"- Reading products for each Subcategory")
        # Read all pages for each subcategory
        [await getProductsInfo(page=page, subcategory=subcategory) for subcategory in subcategories]
    except errors.ElementHandleError as e:
        print(e)
        helper.insertLogs(vendor = vendor, 
                            col = logs_col,
                            subcategory=category, 
                            no_rows=0, 
                            status='Error', 
                            type=e, 
                            step=readSubcategories.__name__)

    

async def getProductsInfo(page,subcategory):
    ''' Opens each subcategory page to extract products' information'''
    
    # ***** Pagination is pending *******
    # Reading just the first page
    
    await helper.waitingTime(page)

    
    await page.goto(subcategory['url'])

    
    # Get items for each category
    items = []
    print(f"- Get products in this subcategory: {subcategory['name']}")
    try:
        items = await page.evaluate(f"""() => {{
                
                var results = []
                var items = document.getElementsByClassName('product-list')[0].getElementsByClassName('product-list__item')
                
                // iterate over the whole list of items on the webpage
                Array.from(items).forEach(function(item){{

                    // Dictionary as main data structure for each product 
                    var item_dict = {{}}
                    // Temporary result for each property
                    var temp_result
                    
                    // Get Product Details
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__action__button', property_js='product_details', attr_js='href')}

                    // Get Product Title
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__title__inner', property_js='product_title', attr_js='innerText')}
                    
                    // Get Product Labels
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__min-order', property_js='product_label', attr_js='innerText')}
                    
                    // Get Image src
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__image', property_js='product_image', attr_js='src')}

                    // Get Product Rating
                    rating_full = item.getElementsByClassName('rating product__rating')[0]
                    rating_half = item.getElementsByClassName('rating product__rating')[0]
                    if(rating_full != undefined){{
                        stars = rating_half.getElementsByClassName('full').length
                        item_dict['product_rating'] = stars
                    }}
                    if(rating_half != undefined){{
                        stars = rating_half.getElementsByClassName('half').length / 2
                        item_dict['product_rating'] += stars
                        
                    }}
                    
                    // Get Product Price
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__current-price--digits-before-comma', property_js='product_price', attr_js='innerText')}
                    
                    // Get Product Base Price
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__base-price', property_js='product_base_price', attr_js='innerText')}
                    
                    // Get Product Informationlink
                    temp_result = ''

                    // Get Product Category                        
                    item_dict['product_category'] = '{subcategory['category']}'

                    // Get Product Subcategory                        
                    item_dict['product_subcategory'] = '{subcategory['name']}'

                    // Get Product Ingredients
                    item_dict['product_ingredients'] = ''

                    // Get Product Brand/seller
                    item_dict['product_brand'] = ''

                    // Original price
                    old_price = item.getElementsByClassName('product__old-price')[0]
                    if(typeof old_price != 'undefined'){{
                        old_price = old_price.getElementsByTagName('span')[0]
                        if(typeof old_price != 'undefined')
                            item_dict['product_original_price'] = old_price.innerText
                    }}
                    else
                        item_dict['product_original_price'] = ''

                    // Get Product Discount
                    item_dict['product_discount'] = temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__percent-saving__text', property_js='product_discount', attr_js='innerText')}

                    // Set Product Vendor
                    item_dict['product_vendor'] = '{vendor}'

                    // Set Extraction Date
                    item_dict['product_insert_dt'] = '{datetime.today()}'

                    results.push(item_dict)
                    }});
                
                return results
            }}""")
        # ************************************************
        # Click on each element (if available) to get its ingredients
        # for item in items:
        #     if(item['product_details' != '']):
        #         await page.goto(item['product_details'])
        # *************************************************

        # Add thumbnail details only as batch into MongoBD (for deugging)
        print(f"- Inserting data into Mongo")
        print(f"First product: {items[0]}")
        print(f"Number of products: {len(items)}")
        print(f" Category: {subcategory['category']} | Subcategory: {subcategory['name']}")
        
        # Insert data into Mongo and add logs
        try:
            netto_col.insert_many(items)
            helper.insertLogs(vendor = vendor, 
                                col = logs_col,
                                subcategory=subcategory, 
                                no_rows=len(items), 
                                status='Successful')
        except:
            helper.insertLogs(vendor = vendor, 
                                col = logs_col,
                                subcategory=subcategory, 
                                no_rows=len(items), 
                                status='Error', 
                                type='MongoDB', 
                                step='insert_many')

    except errors.ElementHandleError as e:
        print(e)
        helper.insertLogs(vendor = vendor,
                            col = logs_col,
                            subcategory=subcategory, 
                            no_rows=0, 
                            status='Error', 
                            type=e, 
                            step=getProductsInfo.__name__)
            
    

async def main():
    browser = await launch()
    page = await browser.newPage()
    
    initial_URL = 'https://www.netto-online.de/lebensmittel/c-N01'

    # Starts with the following link:
    print('- Openning Kaufland website > Lebensmittel')
    await page.goto(initial_URL)
    
    # Accept cookies
    print('- Accepting cookies')
    await page.waitForSelector('#CybotCookiebotDialog')
    await page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')

    
    print('- Readig categories')
    # Get all categories with {name:link} key-pair values
    try:
        categories = await page.evaluate(f"""() => {{
            var categories = []
            var webpage_categories = document.getElementsByClassName('sub-navigation__inner__list')[0].getElementsByTagName('a')
            Array.from(webpage_categories).forEach(function(c){{
                category = {{}}
                if((typeof c === 'undefined'))
                    return
                else {{
                    category['name'] = c.innerText
                    category['url'] = c.href
                    categories.push(category)
                }}
            }})
            return categories
        }}""")
        print(categories)
        print(type(categories))
        # Read all pages for each subcategory
        [await readSubcategories(page=page,category=category) for category in categories if (category['name'] != 'Cremesso' and category['name'] != 'Wurst & Fleisch')]
    
    except errors.ElementHandleError as e:
        print(e)
        helper.insertLogs(vendor = vendor, 
                            col = logs_col,
                            subcategory=None, 
                            no_rows=0, 
                            status='Error', 
                            type=e, 
                            step=getProductsInfo.__name__)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())


print(f"- Pipeline finished")