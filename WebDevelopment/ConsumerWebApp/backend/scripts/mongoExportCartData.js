const moment = require('moment');
const mongoose = require('mongoose');
const fs = require('fs');
mongoose.connect('mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority');

const CartModel = require('../models/cart');

function encoder(object, encodedObject = {}, maxKey=0){
  for(key in object){
    if(!encodedObject[key]){
      encodedObject[key] = maxKey;
      maxKey += 1;
    }
  }
  return {
    encodedObject,
    maxKey
  }
}

function generateEncoderFiles(encoderObject, filename, firstString){
  const csv_file = [firstString]
  for(key in encoderObject){
    csv_file.push(`${key}, ${encoderObject[key]}`)
  }
  fs.writeFileSync(filename, csv_file.join('\n') + '\n');
}

function generateDataFiles(data, encodedUserId, encodedProductId, filename){
  const csv_data = [];
  for(user in data){
    const userId = encodedUserId.encodedObject[user]
    for(product in data[user]){
      const productId = encodedProductId.encodedObject[product]
      for(let val of convertToCount(data[user][product])) {
        csv_data.push(`${userId}, ${productId}, ${val}`)
      }
    }
  }
  fs.writeFileSync(filename, csv_data.join('\n') + '\n')
}

function generateClassDataFiles(data, encodedUserId, encodedProductId, filename){
  const csv_data = ['userId, productId, category'];
  for(user in data){
    const userId = encodedUserId.encodedObject[user]
    for(product in data[user]){
      const productId = encodedProductId.encodedObject[product]
      for(let val of convertToCount(data[user][product])) {
        let category = 7;
        if(val <= 5)
          category = 1;
        else if(val <= 10)
          category = 2;
        else if(val <= 15)
          category = 3;
        else if(val <= 20)
          category = 4;
        else if(val <= 25)
          category = 5;
        else if(val <= 30)
          category = 6;        
        csv_data.push(`${userId}, ${productId}, ${category}`)
      }
    }
  }
  fs.writeFileSync(filename, csv_data.join('\n') + '\n')
}

function generateLastTimeStampFile(data, encodedUserId, encodedProductId, filename){
  const csv_data = ['userId, productId, lastBoughtTime'];
  for(user in data){
    const userId = encodedUserId.encodedObject[user]
    for(product in data[user]){
      const productId = encodedProductId.encodedObject[product]
      let val = new Date(data[user][product].pop()).toISOString();
      csv_data.push(`${userId}, ${productId}, ${val}`);
    }
  }
  fs.writeFileSync(filename, csv_data.join('\n') + '\n')
}

function convertToCount(array){
  if(array.length == 1)
    return []
  else {
    const diff = [];
    array.sort((a, b) => a - b);
    for(let i = 1; i < array.length; i++){
      const firstDate = moment(new Date(array[i - 1]));
      const secondDate = moment(new Date(array[i]));
      const difference = secondDate.diff(firstDate, 'days');
      diff.push(difference)
    }
    return diff;
  }
}

const data = {};
const promises = [];
let encodedProductId = {
  encodedObject: {},
  maxKey: 0,
};
let encodedUserId = {
  encodedObject: {},
  maxKey: 0,
};

async function run(){
  for(let i = 0; i < 50; i++){
    await CartModel.find({ 
      active: false,
      deleted: false,
    }).skip(i * 10000).limit(10000).then((docs) => {
      for(let i = 0; i < docs.length; i++){
        if(!data[docs[i]['userId']])
          data[docs[i]['userId']] = {}
        if(!data[docs[i]['userId']][docs[i]['productId']])
          data[docs[i]['userId']][docs[i]['productId']] = []
        data[docs[i]['userId']][docs[i]['productId']].push(docs[i]['modified'])
      }
      encodedUserId = encoder(data, encodedUserId.encodedObject, encodedUserId.maxKey);
      for(user in data){
        encodedProductId = encoder(data[user], encodedProductId.encodedObject, encodedProductId.maxKey);
      }
    })
    .catch(err => console.log(err))
  }
  generateEncoderFiles(encodedProductId.encodedObject, '../data/productIds.csv', 'productId, index');
  generateEncoderFiles(encodedUserId.encodedObject, '../data/userIds.csv', 'userId, index');
  generateDataFiles(data, encodedUserId, encodedProductId, '../data/cartData.csv');
  generateClassDataFiles(data, encodedUserId, encodedProductId, '../data/cartClassData.csv');
  generateLastTimeStampFile(data, encodedUserId, encodedProductId, '../data/timestamp.csv');
  mongoose.disconnect();
  // execute the python process which reads the data and generates recommendations
}

run().catch(error => error.stack);