#!/usr/bin/env python
# coding: utf-8

# In[413]:


from sklearn.metrics import confusion_matrix
from sklearn import metrics
from datetime import timedelta, date
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import pymongo
from datetime import datetime


# In[414]:


data = pd.read_csv('cartClassData.csv')
productEncodings = pd.read_csv('productIds.csv')
uIdEncodings = pd.read_csv('userIds.csv')
timestamp = pd.read_csv('timestamp.csv')


# In[402]:


client = pymongo.MongoClient(
    "mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority")
db = client["vendors_data_db"]
rec_collection = db["cart_history_recommendations"]


# In[415]:


print(set(data['category']))


# In[416]:


productEncodings.info()


# In[370]:


uIdEncodings.info()


# In[371]:


timestamp.info()


# In[372]:


data.info()


# In[417]:


timestamp['lastBoughtTime'] = pd.to_datetime(timestamp['lastBoughtTime'])


# In[418]:


features = list(zip(data['userId'], data['productId']))


# In[419]:


# Import train_test_split function

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(
    features, data['category'], test_size=0.03)  # 70% training and 30% test


# In[420]:


uID_unique = set(data['userId'])


# In[421]:


pID_unique = set(data['productId'])


# In[422]:


model = KNeighborsClassifier(n_neighbors=8)


# In[423]:


# accuracy
model.fit(X_train, y_train)
y_pred = model.predict(X_test)


# In[424]:


def fetchDate(modified_dt, category):
    startDays = 0
    endDays = 0
    if category == 1:
        startDays = 0
        endDays = 5
    elif category == 2:
        startDays = 5
        endDays = 10
    elif category == 3:
        startDays = 10
        endDays = 15
    elif category == 4:
        startDays = 15
        endDays = 20
    elif category == 5:
        startDays = 20
        endDays = 25
    elif category == 6:
        startDays = 25
        endDays = 30
    else:
        startDays = 30
        endDays = 35
    todt = modified_dt + timedelta(days=endDays)
    fromdt = modified_dt + timedelta(days=startDays)

    return todt, fromdt


# In[412]:


# Train the model using the training sets
model.fit(X_train, y_train)
for uid in uID_unique:
    for pid in pID_unique:
        y_pred = model.predict([[uid, pid]])
        userId = uIdEncodings[uIdEncodings['index'] == uid].iloc[0].userId

        pId = productEncodings[productEncodings['index']
                               == pid].iloc[0].productId
        moddt = timestamp[(timestamp['userId'] == uid) & (
            timestamp['productId'] == pid)].lastBoughtTime
        if moddt.any():
            for date in moddt:
                todt, fromdt = fetchDate(date, y_pred[0])
                dict = {'userId': userId, 'productId': pId,
                        "from": fromdt, "to": todt}
                rec_collection.insert_one(dict)


# In[425]:


# Model Accuracy, how often is the classifier correct?
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))


# In[397]:


accuracy = (y_test == y_pred).sum() / float(len(y_test))
accuracy
