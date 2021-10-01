import random
import pymongo
from bson.objectid import ObjectId
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority");
db = client["vendors_data_db"]
users_collection = db["users_col"]
carts_collection = db["carts_col"]
products_collection = db["product_col"]

userIds = []
productIds = []

for user in users_collection.find({},{ "_id": 1}):
    userIds.append(str(user['_id']))

for product in products_collection.find({},{ "_id": 1}):
    productIds.append(str(product['_id']))    

for userId in userIds:
    numberOfProducts = random.randint(1,10);
    randomProductIds = random.choices(productIds, k=numberOfProducts);	
    randProdArray = [];
    for randomProduct in randomProductIds:
        qty = random.randint(1,3);
        buy = ["0","1"];
        products = {"qty":qty,"productId":randomProduct, "bought":random.choice(buy)}
        randProdArray.append(products)

    mydict = { "userId": userId, "status": "1","insert_dt" : datetime.today().replace(microsecond=0),"products":randProdArray,"update_dt":None }
    carts_collection.insert_one(mydict);
