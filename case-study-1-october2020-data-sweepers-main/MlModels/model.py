import pymongo
from datetime import date, datetime
import re
import concurrent.futures
import sys
import os
sys.path.append('/home/paolo/Documents/Github/case-study-1-october2020-data-sweepers')
from DataExtraction import config

# ============ Configuration ====================
# Mongo DB connection
conn = config["MONGO_URL"]
client = pymongo.MongoClient(conn)
db = client[config["MONGO_DB"]]

# Mongo collections
kaufland_stg = "kaufland_data_col"
vendors = ["kaufland_data_col","netto_data_col","aldi_data_col"]
staging = "stg_product_col"
products = "product_col"
bookmarks = "bookmarks_col"

# batch configuration
nBatch = 100


def printInfo(document):
    print(f'Title: {document["_id"]} \t Price: {document["current_price"]} \t Discount: {document["discount"]} \t Vendor: {document["vendor"]} \t Old Price: {document["old_price"]}')



# ============ Count Analysis ====================
# 1. Vendors STG
for vendor in vendors:
    total = db[vendor].count_documents({})
    print(f'Results for {vendor}: {total}')
    missing = db[vendor].count_documents({"detailedInfo":None})
    print(f'Results without detailed info for {vendor}: {missing}')
    print("Complete Data: "+"{:.2%}".format(missing/total))
    print("Missing Data: "+"{:.2%}".format(1-(missing/total)))
    print(f'============')

# 2. Products STG
results = db[staging].count_documents({})
print(f'Results for {staging}: {results}')
print(f'============')

# 3. Products STG
results = db[products].count_documents({})
print(f'Results for {products}: {results}')
print(f'============')


# ============ Category Analysis ====================
for vendor in vendors:
    results = db[vendor].aggregate([
        # {
        # "$match": {"vendor":"Kaufland"}
        # },
        {
        "$group": { "_id": "$category", "count": { "$sum": 1 } }
        },
        {
        "$sort" : { "count" : -1, "_id": 1 }
        }
    ])
    print(f'Results for Categories in {vendor}:')
    [print(result) for result in results]
    print('=================')

# 2. Product
results = db[products].aggregate([
    # {
    # "$match": {"vendor":"Kaufland"}
    # },
    {
    "$group": { "_id": "$category", "count": { "$sum": 1 } }
    },
    {
    "$sort" : { "count" : -1, "_id": 1 }
    }
])
print(f'Results for Categories in {products}:')
[print(result) for result in results]
print('=================')

# ============ STG Analysis ====================
# for vendor in vendors:
#     results = db[vendor].distinct("category")
#     print(f'Results for {vendor}:')
#     [print(result) for result in results]
#     print(f'============')


# # ============ STG Analysis ====================
# results = db[staging].distinct("category")
# print(f'Results for {staging}:')
# [print(result) for result in results]
# print(f'============')

# # ============ Prod Analysis ====================
# results = db[products].distinct("category")
# print(f'Results for {products}:')
# [print(result) for result in results]
# print(f'============')


# #results = db[kaufland_stg].distinct("category")
# #[print(result) for result in results]


# # ============ Create synthetic data for discount prices ====================
# # Read all products with discounts
# # results = db[products].count_documents({"$and":[{"status":True}, {"discount":{"$lt":0}}]})
# # [printInfo(product) for product in results]



# # ============ Reading data ====================
# # Read all the bookmarks for users
# # total = db[products].count_documents({"status":True})
# # print('======================================')
# # print(f'Collection: {products} | Total of documents: {total}')

# # total = db[bookmarks].count_documents({"status":"1"})
# # print('======================================')
# # print(f'Collection: {bookmarks} | Total of documents: {total}')
# # print('======================================')



# # ============ Exploratory Data Analysis ====================

# #  How many discounts each vendor has?
# # Which products have a discount?
# # result = db[products].aggregate(
# #     [
# #      { "$match": { "discount": {"$lt": 0} } },
# #      { "$sort": { "discount": -1}}
# #    ]
# #     )
# # print('Products with discounts:')
# # [printInfo(product) for product in result]


# # Which products have a discount?
# # result = db[products].aggregate(
# #     [
# #      { "$match": { "discount": {"$lt": 0} } },
# #      { "$sort": { "discount": -1}}
# #    ]
# #     )
# # print('Products with discounts:')
# # [printInfo(product) for product in result]

