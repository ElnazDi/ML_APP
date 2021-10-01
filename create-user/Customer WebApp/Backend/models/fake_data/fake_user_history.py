import datetime
import calendar
import random
import numpy
import pymongo
import pandas as pd
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority");
db = client["vendors_data_db"]
users_collection = db["users_col"]
carts_collection = db["carts_col_test"]
products_collection = db["product_col"]

products = []
for product in products_collection.find({},{ "_id": 1}):
    products.append(str(product['_id']))    

users = []
for user in users_collection.find({},{ "_id": 1}):
    users.append(str(user['_id']))



def generate_random_time(month,yr):
  day = generate_random_day(month,yr)
  if random.random() < 0.5:
    date = datetime.datetime(yr, month, day,2,00)
  else:
    date = datetime.datetime(yr, month, day,6,00)
  time_offset = numpy.random.normal(loc=0.0, scale=180)
  final_date = date + datetime.timedelta(minutes=time_offset)
  removed_dt = final_date + datetime.timedelta(days=1)
  return final_date.strftime("%m/%d/%y %H:%M:%S"),removed_dt.strftime("%m/%d/%y %H:%M:%S")

def generate_random_day(month,year):
  day_range = calendar.monthrange(year,month)[1]
  return random.randint(1,day_range)


if __name__ == '__main__':
  for month in range(1,13):
    if month <= 10:
      orders_amount = int(numpy.random.normal(loc=1200, scale=40))
    elif month == 11:
      orders_amount = int(numpy.random.normal(loc=2000, scale=30))
    else: # month == 12
      orders_amount = int(numpy.random.normal(loc=2600, scale=30))

    product_list = [product for product in products]

    print(orders_amount)

    year = [2017,2018,2019,2020]
    yr = random.choice(year)
    while orders_amount > 0:
      orderDate,removed_dt = generate_random_time(month,yr)
      userId = random.choice(users)
      numberOfProducts = random.randint(1,10);
      products_selected = [];
      for i in range(numberOfProducts):
        product_choice = random.choice(product_list)
        qty = random.randint(1,3);
        buy = [0,1];
        singleProduct = {"qty":qty,"productId":product_choice, "bought":random.choice(buy)}
        products_selected.append(singleProduct)
      orders_amount -= 1
      mydict = { "userId": userId, "status": 1,"insert_dt" : orderDate,"products":products_selected,"removed_dt":removed_dt,"update_dt":None }
      carts_collection.update_one({
        'userId': userId,
        'status':1
        },{
        '$set': {
            'status':0
        }});


      carts_collection.insert_one(mydict);


    month_name = calendar.month_name[month]

    print(f"{month_name} {yr} Complete")