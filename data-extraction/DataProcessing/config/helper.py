import asyncio
from datetime import datetime
from random import randint

def validate():
    return f"""
        function validate(element, src = 0) {{
            if (element == undefined)
                return ''
            if (src == 0)
                return element.innerText
            else if (src == 1)
                return element.src
            return element.href
        }}
    """


async def waitingTime(page):
    ''' Waits a random number of seconds to simulate human interaction on the website'''
    waitTime = randint(1,10) * 1000
    print(f"<< Waiting {waitTime / 1000} secs >>")
    #asyncio.sleep(waitTime / 1000)
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
