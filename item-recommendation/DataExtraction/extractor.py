import asyncio
import logging
from os import path, listdir
from pyppeteer import launch
import json

class Extractor:

  def __init__(self, log_path):
    '''
    Constructor that takes log_path as argument specifying the logging location
    '''
    logging.basicConfig(filename=log_path, filemode="w", format="%(asctime)s - %(message)s")
    self.info = logging.info

  def formatter(self, string, params, fstart="/***", fend="***/"):
    '''
    @ToBeDeprecated
    Helper function that replaces content of JS file with value from params by searching for the index number
    Default: /***0***/ is replaced by 0th element in params array
             /***1***/ is replaced by 1st element in params array
    '''
    for i, val in enumerate(params):
      f = fstart + str(i) + fend
      if isinstance(val, str):
        val = '\"' + val + '\"'
      string = string.replace(f, val)
    return string

  async def executeJS(self, filepath, name, params=[]):
    '''
    @CoreFunction
    Execute any specific JS scripts that is required for data collection
    '''
    fullPath = path.join(filepath, name)
    print(f'Reading script from path {fullPath}')
    script = ''
    with open(fullPath) as reader:
      script = reader.read()
    script = self.formatter(script, params)
    print(f'Executing script {name}')
    data = await self.page.evaluate(script)
    return data

  async def setup(self, headless=True, autoClose=True):
    '''
    Launches the browser by default in headless and autoclose mode
    '''
    browser = await launch(headless=headless, autoClose=autoClose)
    self.page = await browser.newPage()

  async def gotoPage(self, url, wait_selector=False):
    '''
    @CoreFunction
    Make the launched browser open a specific URL and wait for a selector is specified
    '''
    print(f'Opening URL: {url}')
    await self.page.goto(url)
    # also wait for selector 
    if(wait_selector):
      await self.page.waitForSelector(wait_selector)

  async def acceptCookies(self, wait_selector, click_button, next_wait_selector=False):
    '''
    @CoreFunction
    Accept the cookies by clicking the cookie button after waiting for cookie modal to load completely
    '''
    print('Accepting cookies')
    await self.page.waitForSelector(wait_selector)
    await self.page.click(click_button)
    if(next_wait_selector):
      await self.page.waitForSelector(next_wait_selector)

  async def getListItems(self, selector_object):
    '''
    @CoreFunction
    Get the list of items from the webpage 
    '''
    print('Fetching list item values')
    listItems = await self.page.querySelectorAll(selector_object['selector'])
    list_values = []
    for item in listItems:
      data = {}
      property_data = await self.getItemProperties(selector_object, item)
      list_values.append(property_data)
    return list_values

  async def getItemProperties(self, selector_object, item):
    '''
    @CoreFunction
    Get selected item properties from the selector object
    '''
    if 'children' in selector_object:
      content = {}
      for item_property in selector_object['children']:
        child_item = await item.querySelector(item_property['selector'])
        if child_item is not None:
          tag = item_property['tag']
          if item_property['tag'] == 'innerHTML':
            content[tag] = child_item.innerHTML
          else:
            content[tag] = (await (await child_item.getProperty(item_property['property'])).jsonValue())
      return content

  async def gotoNextPage(self, selector, page_count=False):
    '''
    @CoreFunction
    Click on the next page button to go to next page as required
    '''
    if not page_count:
      print('Going to next page')
    else:
      print('Going to page: ' + str(page_count))
    # End function if this method timesout
    try:
      await self.page.waitForSelector(selector)
    except:
      return False
    await self.page.querySelector(selector)
    await asyncio.wait([
      self.page.click(selector),
      self.page.waitForNavigation(),
    ])
    return True


async def main():
  extractor = Extractor('logfile')
  await extractor.setup(headless=False)
  all_data = []
  # Load all configurations such as Kaufland, Netto, Rewe, Aldi and so on
  for filename in listdir('./DataExtraction/config'):
    # Read each configuration file from store it as JSON
    with open(path.join('./DataExtraction/config', filename)) as filedata:
      instructions = json.loads(filedata.read())
      # Goto homepage and wait for cookieModal
      await extractor.gotoPage(instructions['homepage'], instructions['cookieModal'])
      # Click cookie accept button once cookieModal is loaded
      await extractor.acceptCookies(instructions['cookieModal'], instructions['cookieButton'], instructions['paginationButton'])
      page = 1
      while(True):
        # For each page, get list of card items and extract data from each card item
        data = await extractor.getListItems({
          'selector': instructions['parentSelector'],
          'children': instructions['children']
        })
        print(data[0])
        all_data += data
        # Go to next page by clicking on the next page button
        status = await extractor.gotoNextPage('.m-pagination__link[aria-label="Seite Weiter"]', page)
        # If next page button is disabled, break the loop as all data is extracted
        if not status:
          break
        page +=1

asyncio.get_event_loop().run_until_complete(main())
