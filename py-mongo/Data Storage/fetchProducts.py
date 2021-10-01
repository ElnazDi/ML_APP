import pymongo
from pymongo import MongoClient
import ssl
import connection

# function to translate german text
def translate(product):
    from googletrans import Translator
    translator = Translator()

    text_lang = translator.detect(text=product)

    if text_lang.lang != 'de':
        translated_text = translator.translate(product, dest='de')
        product = translated_text.text

    return product


def find_products(product_category,collection):
    # displaying the cheapest products first
    prods = collection.find({"$text": {"$search":product_category}}).sort([("product_price", pymongo.ASCENDING)])    # prods = collection.find(query).sort([("product_price", pymongo.ASCENDING)])
    # print(collection.count_documents(query))
    return prods


def fetch_products(product_name):
    # Mongo DB connection
    mongo_uri = connection.MONGO_URL
    client = MongoClient(mongo_uri,ssl_cert_reqs=ssl.CERT_NONE)
    db = client.vendors_data_db
    collection_names = ['kaufland_data_col','netto_data_col']
    products = []
    product_name = translate(product_name)

    for collection_name in collection_names:
        collection = db[collection_name]
        collection.create_index([('product_title', 'text'),('product_ingredients', 'text')])
        product_collection = find_products(product_name,collection)
        products.append(product_collection)

    for product_vec in products:
        for product in product_vec:
            print(product)




fetch_products(product_name='coffee')




