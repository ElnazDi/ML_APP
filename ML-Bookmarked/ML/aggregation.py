import pymongo
import config
from bson.objectid import ObjectId


conn = config.MONGO_URL
client = pymongo.MongoClient(conn)
db = client["Vendors_data_db"]
collection1 = db.users_col
collection2 = db.bookmarks_col
collection3 = db.aggregated_collection


data = list(collection1.aggregate([

    {"$lookup": {
        "from": "bookmarks_col",
        "localField": "user_id",
     "foreignField": "userId",
     "as": "aggregate"
     }

     },
]))


collection3.insert_many(data)
print(f'{len(data)} is the number of movies inserted in the aggregated_collection')
