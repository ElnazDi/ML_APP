import asyncio
import logging
from os import path
from pyppeteer import launch


class Extractor:
  
  def __init__(self, log_path):
    logging.basicConfig(filename=log_path, filemode="w", format="%(asctime)s - %(message)s")
    self.info = logging.info

  def formatter(self, string, params, fstart="/***", fend="***/"):
    for i, val in enumerate(params):
      f = fstart + str(i) + fend
      if isinstance(val, str):
        val = '\"' + val + '\"'
      string = string.replace(f, val)
    return string

  async def setup(self):
    browser = await launch(headless=False, autoClose=False)
    self.page = await browser.newPage()

  async def gotoPage(self, url, wait_selector=False):
    print(f'Opening URL: {url}')
    await self.page.goto(url)
    if(wait_selector):
      await self.page.waitForSelector(wait_selector)

  async def acceptCookies(self, wait_selector, click_button, next_wait_selector=False):
    print('Accepting cookies')
    await self.page.waitForSelector(wait_selector)
    await self.page.click(click_button)
    if(next_wait_selector):
      await self.page.waitForSelector(next_wait_selector)

  async def getListItems(self, selector_object):
    print('Fetching list item values')
    data = await self.getListChildrenItems(selector_object, self.page)
    return data

  async def getListChildrenItems(self, selector_object, item):
    listItems = await item.querySelectorAll(selector_object['selector'])
    list_values = []
    for item in listItems:
      data = {}
      property_data = await self.getItemProperties(selector_object, item)
      list_values.append(property_data)
    return list_values

  async def getItemProperties(self, selector_object, item):
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

  async def executeJS(self, filepath, name, params=[]):
    fullPath = path.join(filepath, name)
    print(f'Reading script from path {fullPath}')
    script = ''
    with open(fullPath) as reader:
      script = reader.read()
    script = self.formatter(script, params)
    print(f'Executing script {name}')
    data = await self.page.evaluate(script)
    return data


async def main():
  extractor = Extractor('logfile')
  await extractor.setup()
  all_data = []
  await extractor.gotoPage('https://filiale.kaufland.de/sortiment/das-sortiment.html', '.cookie-alert-extended-modal') #
  await extractor.acceptCookies('.cookie-alert-extended-modal', '.cookie-alert-extended-button', '.m-pagination__link[aria-label="Seite Weiter"]')
  page = 1
  while(True):
    data = await extractor.getListItems({
      'selector': '.m-offer-tile__container',
      'children': [{
        'selector': '.a-image-responsive',
        'tag': 'imgSrc',
        'property': 'src'
      }, {
        'selector': '.a-pricetag__price',
        'tag': 'price',
        'property': 'innerHTML'
      }, {
        'selector': '.m-offer-tile__subtitle',
        'tag': 'brand',
        'property': 'innerHTML'
      }, {
        'selector': '.m-offer-tile__title',
        'tag': 'title',
        'property': 'innerHTML'
      }, {
        'selector': '.m-offer-tile__quantity',
        'tag': 'quantity',
        'property': 'innerHTML'
      }, {
        'selector': '.m-offer-tile__basic-price',
        'tag': 'basePrice',
        'property': 'innerHTML'      
      }]      
    })
    print(data[0])
    all_data += data
    status = await extractor.gotoNextPage('.m-pagination__link[aria-label="Seite Weiter"]', page)
    if not status:
      break
    page +=1

asyncio.get_event_loop().run_until_complete(main())
