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
kaufland_col = db.kaufland_data_col
logs_col = db.data_ext_logs_col

## === Best Practices ====
# 1. Visit the website in intervals of 10 min or more
# 2. Use proxy servers
# 3. Use fingerprint rotation with headless browser
# 4 Use Scrapy frameworks 
# 5. Change headers in request

vendor = 'Kaufland'
browser = None

async def readSubcategories(page, category):
    ''' Get all links for each category'''
    # Open each link to get all the products after wating 1 sec (to simulate kind of human site interaction)    
    
    # Open link inside this category
    await page.goto(category['url'])
    print('- Setting up waiting time')
    await helper.waitingTime(page)
    
    # Expand all categories (if any) in the current web page
    try:
        print('- Expanding all categories')
        await page.click('.rd-tile--additional')
    except TimeoutError as e:
        print(e)
        print('This category does not have more subcategories')
    except errors.PageError as e:
        print(e)
        print('This category does not have more subcategories')
        

    await helper.waitingTime(page)
    # ==== Open links for one page =====
    print('- Collecting subcategories')
    subcategories = []
    try:
        subcategories = await page.evaluate(f"""() => {{
                    var subcategories = []
                    var subcategories_links = document.getElementsByClassName('rd-category-tiles')[0].getElementsByTagName('a')
                    subcategories_links.forEach(function(link){{
                        subcategory = {{}}
                        subcategory['name'] = link.getElementsByClassName('rd-tile__title')[0].innerText
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
    print(f"- Get elements in this subcategory")
    try:
        items = await page.evaluate(f"""() => {{
                
                var results = []
                var items = document.getElementsByClassName('item')
                
                // iterate over the whole list of items on the webpage
                items.forEach(function(item){{

                    // Dictionary as main data structure for each product 
                    var item_dict = {{}}
                    // Temporary result for each property
                    var temp_result
                    
                    // Get Product Details
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByTagName',param_js='a', property_js='product_details', attr_js='href')}

                    // Get Product Title
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__title', property_js='product_title', attr_js='innerText')}
                    
                    // Get Product Labels
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product-labels', property_js='product_label', attr_js='innerText')}
                    
                    // Get Image src
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByTagName',param_js='img', property_js='product_image', attr_js='src')}

                    // Get Product Rating
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='_rating', property_js='product_rating', attr_js='getAttribute("data-rating")')}
                    
                    // Get Product Price
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='price', property_js='product_price', attr_js='innerText')}
                    
                    // Get Product Base Price
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__base-price', property_js='product_base_price', attr_js='getElementsByTagName("span")[0].innerText')}
                    
                    // Get Product Informationlink
                    temp_result = {helper.setValueForPropertyJS(func_js='getElementsByClassName',param_js='product__delivery-info', property_js='product_information', attr_js='innerText')}

                    // Get Product Category                        
                    item_dict['product_category'] = '{subcategory['category']}'

                    // Get Product Subcategory                        
                    item_dict['product_subcategory'] = '{subcategory['name']}'

                    // Get Product Ingredients
                    item_dict['product_ingredients'] = ''

                    // Get Product Brand/seller
                    item_dict['product_brand'] = ''

                    // Get Product Discount
                    item_dict['product_discount'] = ''
                    
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
        print(f"Number of products: {len(items)}")
        print(f" Category: {subcategory['category']} | Subcategory: {subcategory['name']}")
        
        # Insert data into Mongo and add logs
        try:
            kaufland_col.insert_many(items)
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
        await browser.close()
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
    
    initial_URL = 'https://www.kaufland.de/lebensmittel/'    

    # Starts with the following link:
    print('- Openning Kaufland website > Lebensmittel')
    await page.goto(initial_URL)
    
    # Accept cookies
    print('- Accepting cookies')
    await page.waitForSelector('.cookie-alert-extended-modal')
    await page.click('.cookie-alert-extended-button')
    
    
    print('- Readig categories')
    # Get all categories with {name:link} key-pair values
    try:
        categories = await page.evaluate(f"""() => {{
            var categories = []
            var webpage_categories = document.getElementsByClassName('rd-category-tree__list-item')
            webpage_categories.forEach(function(c){{
                category = {{}}
                a_tag = c.getElementsByTagName('a')[0]
                console.log(a_tag)
                if((typeof a_tag === 'undefined'))
                    return
                else {{
                    category['name'] = a_tag.innerText
                    category['url'] = a_tag.href
                    categories.push(category)
                }}
            }})
            return categories
        }}""")
        print(categories)
        print(type(categories))
        # Read all pages for each subcategory
        [await readSubcategories(page=page,category=category) for category in categories]
        
    
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

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())


print(f"- Pipeline finished")