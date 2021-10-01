import random
import pymongo
from bson.objectid import ObjectId
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority");
db = client["vendors_data_db"]
users_collection = db["users_col"]
bookmark_collection = db["bookmarks_col"]
products_collection = db["product_col"]

userIds = []
productIds = []

for user in users_collection.find({},{ "_id": 1}):
    userIds.append(str(user['_id']))

for product in products_collection.find({},{ "_id": 1}):
    productIds.append(str(product['_id']))    

for userId in userIds:
    numberOfProducts = random.randint(1,5);
    randomProductIds = random.choices(productIds, k=numberOfProducts);	
    print("TYPE ",type(randomProductIds));
    mydict = { "userId": userId, "status": "1","insert_dt" : datetime.today().replace(microsecond=0),"products": randomProductIds,"update_dt":None }
    bookmark_collection.insert_one(mydict);
