from faker import Faker
import pymongo
import numpy as np
fake = Faker()
import bcrypt

passwd = b'123456'

salt = bcrypt.gensalt(rounds=10)
hashed = bcrypt.hashpw(passwd, salt)
client = pymongo.MongoClient("mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority");
db = client["vendors_data_db"]
collection = db.users_col
for x in range(200):
    gender = np.random.choice(["Male", "Female"], p=[0.5, 0.5])
    firstName= fake.first_name_male() if gender=="Male" else fake.first_name_female(),
    lastName= fake.last_name_male() if gender=="Male" else fake.last_name_female(),
    phone = fake.phone_number();
    email = firstName[0]+"."+lastName[0]+"@gmail.com";
    dob = fake.date();
    # gender = fake.randomElement(["Male","Female","Others"]);
    country = fake.country();
    mydict = { "firstName": firstName[0], "lastName": lastName[0],"gender" : gender,"phone": phone, "email":email,"password":hashed.decode("utf-8"),"countryOfOrigin": country,"dateOfBirth":dob }
    collection.insert_one(mydict);
     
