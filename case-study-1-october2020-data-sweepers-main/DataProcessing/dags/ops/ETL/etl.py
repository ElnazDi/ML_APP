import pymongo
from datetime import date, datetime
import re
import logging
import os
import sys

from config import configuration
from bson.objectid import ObjectId



''' Reading data from independent vendor collections for data pre processing'''
class ETLProcess:

    def __init__(self) -> None:

        # Mongo DB connection
        conn = configuration.MONGO_URL
        client = pymongo.MongoClient(conn)
        self.db = client[configuration.MONGO_DB]

        # Mongo collections
        self.vendors = ["kaufland_data","netto_data","aldi_data"]
        self.staging = "stg_products"
        self.product = "products_2"
        self.historical = "products_hist_2"
        self.errors = 'errors'
        self.incomplete = 'incomplete'
        self.start_time = datetime.now()

        # data collections
        self.carts= 'carts'

        # logger configuration
        self.logFile = 'ETL.log'
        logging.basicConfig(filename=self.logFile, level=logging.INFO,
            format='%(asctime)s:%(levelname)s:%(message)s')


    def mergeData(self):
        ''' Merging data from independent vendor collections into staging for processing'''
        logging.info('Reading data from vendors...')
        for vendor in self.vendors:
            # Get products with full information
            total = self.db[vendor].count_documents({"detailedInfo":{"$ne":None}})
            logging.info(f'Collection: {vendor} | Total of documents: {total}')
            processed_docs = self.db[vendor].find({"detailedInfo":{"$ne":None}}).limit(50)
            logging.info(f'Preparing to save data into Mongo...')
            try:
                for doc in processed_docs:
                    doc["processed"] = self.start_time
                    self.db[self.staging].insert_one(doc)
                logging.info(f'Inserting data for {vendor} was successful!')
            except:
                logging.exception(f'Problem inserting into Mongo in {vendor}')

    def dataCleaning(self):
        ''' Cleaning data rules'''
        # Read all elements tht have not been cleaned
        products = self.db[self.staging].find({"cleaned":None})
        logging.info(f'Preparing to save data into Mongo...')
        try:
            # Apply data quality rules and save into Mongo
            stg = self._dataCleaning(products)
            for product in stg:
                logging.info(f'{product}')
                self.db[self.staging].replace_one({"product_title":product["title"]},product, upsert=True)
            logging.info(f'Data cleaning stage finished')
        except:
            logging.exception(f'There was a problem  with the data cleaning process')

    def _dataCleaning(self, products):
        ''' Define standard structure for every doocument and apply data cleaning rules for each one'''
        for doc in products:
            document = {}
            # Reading Basic Info
            document["hash_id"] = hash(doc["product_title"] + doc["vendor"]) # Product ID: Product Title + Vendor
            document["title"] = doc["product_title"]
            document["vendor"] = doc["vendor"]
            try:
                document["image"] = doc["detailedInfo"]["image"]
            except KeyError:
                document["image"] = None
            try:
                document["brand"] = doc["brand"]
            except KeyError:
                document["brand"] = None
            document["quantity"] = doc["content"]
            document["price"] = self._replaceComma(doc["current_price"])
            try:
                if('Aldi' in doc["vendor"]): # Aldi -> Content
                    document["unitPrice"] = self._extractQuantityAndPrice(doc["content"])
                else: # Netto| Kaufland -> Price per Unit
                    document["unitPrice"] = self._extractQuantityAndPrice(doc["price_per_unit"])
                if(document["unitPrice"] == 0):
                    document["unitPrice"] = document["price"]
            except KeyError:
                document["unitPrice"] = None
            try:
                if('Aldi' in doc["vendor"]):# Aldi -> Content
                    document["unitPriceQuantity"] = self._extractQuantityAndPrice(doc["content"], quantity=True)
                else: # Netto| Kaufland -> Price per Unit
                    document["unitPriceQuantity"] = self._extractQuantityAndPrice(doc["price_per_unit"], quantity=True)
                if(document["unitPriceQuantity"] == '' or document["unitPriceQuantity"] is None):
                    document["unitPriceQuantity"] = document["quantity"]
            except KeyError:
                document["unitPriceQuantity"] = None
            try:
                document["discount"] = self._replaceNoDiscount(doc["discount"])
            except KeyError:
                document["discount"] = None
            document["oldPrice"] = self._replaceComma(doc["old_price"])
            document["offerDuration"] = None
            try:
                document["category"] = self._trimSpaces(doc["category"])
            except KeyError:
                document["category"] = None
            try:
                document["subcategory"] = self._removeNumProducts(doc["subcategory"])
            except KeyError:
                document["subcategory"] = None
            try:
                document["badges"] = [badge for badge in doc["badges"] if badge is not None]
            except KeyError:
                document["badges"] = None
            # Reading Detailed Info
            try:
                document["thumbnailImgs"] = [img for img in doc["detailedInfo"]["thumbnail_img"] if img is not None]
            except KeyError:
                document["thumbnailImgs"] = None
            try:
                document["description"] = self._trimSpaces(doc["detailedInfo"]["product_description"])
            except KeyError:
                document["description"] = None
            try:
                document["properties"] = self._trimSpaces(doc["detailedInfo"]["product_properties"])
            except KeyError:
                document["properties"] = None
            try:
                document["ingredients"] = self._trimSpaces(doc["detailedInfo"]["ingredients"])
            except KeyError:
                document["ingredients"] = None
            try:
                document["preparationInstruction"] = doc["detailedInfo"]["prep_instruction"]
            except KeyError:
                document["preparationInstruction"] = None
            try:
                document["hints"] = doc["detailedInfo"]["hints"]
            except KeyError:
                document["hints"] = None
            try:
                document["manufacturer"] = doc["detailedInfo"]["manufacturer"]
            except KeyError:
                document["manufacturer"] = None
            try:
                document["nutritionalValues"] = self._trimSpaces(doc["detailedInfo"]["nutritional_info"])
            except KeyError:
                document["nutritionalValues"] = None
            document["originalLink"] = doc["details"]
            # Control to see which products don't have any price
            if(document["price"] == 0):
                document["status"] = False
            else:
                document["status"] = True
            document["cleaned"] = True
            document["insert"] = doc["insert"]
            document["updated"] = self.start_time
            document["processed"] = doc["processed"]
            yield document


    def removeProductsWithoutPrice(self):
        ''' Remove products with no price from the lastest product list '''
        logging.info(f'Transfering products with no price the the {self.errors} collection')
        total = self.db[self.staging].count_documents({"price":0.0})
        if(total > 0):
            self.db[self.errors].insert_many(list(self.db[self.staging].find({"price":0.0})))
            self.db[self.staging].delete_many({"price":0.0})
            logging.info(f'Process Done!')
        else:
            logging.info(f'There are no products with empty price')

    def updateProductTitle(self):
        products = self.db[self.product].find({})
        #documents = self.db[self.carts].count_documents({'title':None})
        print(f'Updating documents')
        [self.db[self.carts].update_many({"productId":product["_id"]},
                                            {"$set":{"title": product["title"]}}) for product in products]


    def moveHistoricalData(self):
        ''' Transfer current products into historical data collection'''
        # Loading batch
        total = self.db[self.product].count_documents({})
        logging.info(f'Transfering data from {self.product} to {self.historical} \n Collection: {self.product} | Total of documents: {total}')
        logging.info(f'Reading data...')
        for product in self.db[self.product].find({"status":True}):
            product["status"] = False
            product["updated"] = self.start_time
            self.db[self.historical].insert_one(product)
        logging.info(f'Data successfully inserted. Initiating data transfer...')
        self.emptyCol(self.product)
        logging.info(f'Empy collection...')
        logging.info('Transfer successful!')

    def _removeNumProducts(self, field):
        ''' Remove number of products next to each subcategory for products in Kaufland'''
        try:
            return self._trimSpaces(field.split('(')[0])
        except:
            return self._trimSpaces(field)

    def emptyCol(self, col):
        ''' Drop specified collection'''
        logging.info(f'Collection {col} deleted')
        self.db[col].drop()

    def _extractQuantityAndPrice(self, field, quantity=False):
        ''' Extract Quantity and Quantity Price from the product title'''
        # Kaufland 100 g = 0,58 € & Aldi Packung (100 g = € 0,21 )
        try:
            if('(' in field): # Aldi
                if(not quantity): # quantityPrice
                    priceQuantity = self._replaceComma(field.split('=')[1].replace('€','').replace(')','')) # get priceQuantity
                    return float(priceQuantity)
                else: # Quantity
                    quantity = field.split('=')[0].replace('(','').rstrip() # get quantity
                    return quantity
            else: # Kaufland
                if(not quantity): # quantityPrice
                    priceQuantity = self._replaceComma(field.split('=')[1].replace('€','')) # get priceQuantity
                    return float(priceQuantity)
                else: # Quantity
                    quantity = field.split('=')[0].rstrip() # get quantity
                    return quantity
        except:
            try:# Netto –.89 / kg
                if(not quantity): # quantityPrice
                    priceQuantity = field.split('/')[0].split('–')[1] # get priceQuantity
                    return float(priceQuantity)
                else:
                    quantity = field.split('/')[1].rstrip() # get quantity
                    rx = re.findall('[\d]*[.]*[\d]*', quantity)
                    try:
                        return  rx[0] + quantity
                    except IndexError:
                        return '1' + quantity
            except:
                if (quantity):
                    return None
                else:
                    return 0


    def _replaceNoDiscount(self,field):
        ''' Only save numbers with percentages -00.00% and remove any text found in the discount field '''
        rx = re.findall('[-]*[\d]*[.]*[\d]+[ ]*%?', field)
        try:
            return  float(rx[0].replace('%',''))
        except IndexError:
            return 0.0

    def _replaceComma(self, field):
        ''' Extract only the following pattern: 00.00 and replace , by . '''
        if(field == "nur" or field == ''):
            return 0
        rx = re.findall('[\d]*[.|,]*[\d]+', field.replace(',','.'))
        try:
            return  float(rx[0])
        except IndexError:
            return 0.0

    def _trimSpaces(self, field):
        ''' Replace characters like \t \n and remove any white space in the string'''
        pattern = r'[\t\n\b]+'
        # Replace all occurrences of character s with an empty string
        final_field = re.sub(pattern, '', field.rstrip() )
        return final_field

    def moveCurrentProducts(self):
        ''' Move current products from stg to products '''
        logging.info('Moving current products')
        products = self.db[self.staging].find({"cleaned":True})
        for product in products:
            self.db[self.product].insert_one(product)
        logging.info(f'Process done! Cleaning stg tables')
        self.emptyCol(self.staging)
        logging.info(f'Process done!')


    def tempTransfer(self):
        ''' Temporal transfer for defined collection'''
        logging.info(f'Moving data from {self.final} to {self.product} ')
        products = self.db[self.final].find({})
        for doc in products:
            document = {}
            # Reading Basic Info
            document["title"] = doc["title"]
            document["brand"] = doc["brand"]
            document["price"] = doc["price"]
            document["quantity"] = doc["quantity"]
            document["discount"] = doc["discount"]
            document["image"] = doc["image"]
            document["vendor"] = doc["vendor"]
            document["unitPrice"] = doc["current_price"] # Need to fix with a new data rule!
            document["oldPrice"] = doc["oldPrice"]
            document["unitPriceQuantity"] = doc["unitPriceQuantity"] # Need to fix with a new data rule!
            document["vendor"] = doc["vendor"]
            document["offerDuration"] = doc["offerDuration"]
            document["category"] = doc["category"]
            document["subcategory"] = doc["subcategory"]
            document["badges"] = doc["badges"]
            document["thumbnailImgs"] = doc["thumbnailImgs"]
            document["description"] = doc["description"]
            document["properties"] = doc["properties"]
            document["ingredients"] = doc["ingredients"]
            document["preparationInstruction"] = doc["preparationInstruction"]
            document["hints"] = doc["hints"]
            document["manufacturer"] = doc["manufacturer"]
            document["nutritionalValues"] = doc["nutritionalValues"]
            # Control
            document["status"] = True
            document["created"] = doc["insert"]
            document["modified"] = doc["processed"]
            self.db[self.product].insert_one(document)
