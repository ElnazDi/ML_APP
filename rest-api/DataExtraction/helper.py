from datetime import datetime
from random import randint

def insertLogs(vendor, col, subcategory, no_rows, status, type='', step=''):
    ''' Insert logs to detect any problem in the data extraction execution'''
    logs = {}
    logs['vendor'] = vendor
    try:
        logs['category'] = (subcategory['category'] if subcategory['category'] is not None else subcategory['name'])
        logs['subcategory'] = (subcategory['name'] if subcategory['name'] is not None else '')
        logs['subcategory_url'] = (subcategory['url'] if subcategory['url'] is not None else '')
    except:
        logs['category'] = ''
        logs['subcategory'] = ''
        logs['subcategory_url'] = ''
    logs['no_rows'] = no_rows
    logs['status'] = status
    logs['type'] = type
    logs['step'] = step
    logs['insert_dt'] = datetime.today()
    col.insert_one(logs)
    return

async def waitingTime(page):
    ''' Waits a random number of seconds to simulate human interaction on the website'''
    waitTime = randint(1,10) * 1000
    print(f"<< Waiting {waitTime / 1000} secs >>")
    await page.waitFor(waitTime)
    return
    

def setValueForPropertyJS(func_js, param_js, property_js, attr_js):
    '''Attemps to read the value of DOM element and sets a default if it not found
    Params:
    1. func_js => Function to use in JS.
    2. param_js => DOM element specified by the function.
    3. property_js => product property to save the data once it's returned.
    4. attr_js => DOM attribute where the value is located.
    Returns the string object representation in JS that holds the value we're reading on the webpage
    '''
    js_code = f""" temp_result = item.{func_js}('{param_js}')[0]
    if(typeof temp_result !== 'undefined')
        item_dict['{property_js}'] = temp_result.{attr_js}
    else
        item_dict['{property_js}'] = ''
    """
    return js_code
