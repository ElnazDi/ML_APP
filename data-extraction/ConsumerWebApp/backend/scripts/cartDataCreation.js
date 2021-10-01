// const faker = require('faker');
const mongoose = require('mongoose');
mongoose.connect('mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority');
// mongoose.connect('mongodb://localhost:27017/smartshop')

const UserModel = require('../models/user');
const ProductModel = require('../models/product');
const CartModel = require('../models/cart');

function returnRandomProducts(products, threshold){
  const listOfProducts = []
  for(const product of products){
    const val = Math.random();
    if(val > threshold)
      listOfProducts.push(product);
  }
  console.log(listOfProducts.length);
  return listOfProducts;
}

function generateCartData({ userId, productId, start, end, delta, stdDev}) {
  const data = []
  while(start < end) {
    const created = new Date(start);
    created.setSeconds(created.getSeconds() - (Math.random() * 4 * 24 * 3600) - 3600)
    const deleted = Math.random() < 0.1 ? true : false;
    const cartObject = {
      userId,
      productId,
      active: false,
      quantity: Math.floor(Math.random() * 3) + 1,
      created,
    }
    if(deleted) {
      cartObject['deleted'] = true;
      cartObject['removed'] = new Date(start);
    } else {
      cartObject['deleted'] = false;
      cartObject['modified'] = new Date(start);
    }
    data.push(cartObject);
    start.setDate(start.getDate() + delta + (Math.random() - 0.5) * 2 * (stdDev + 1))
  }
  if(Math.random() > 0.5)
    data.push({
      userId,
      productId,
      active: true,
      quantity: 1,
      created: end
    })
  return data;
}

async function generateData() {
  const productsDB = await ProductModel.find({}).limit(1000).exec();
  let products = productsDB.map((product) => product._id.toString())

  console.log(`Fetched product list`)

  for(let i = 0; i < 20; i++){
    const usersDB = await UserModel.find({}).skip(i * 50).limit(50).exec();
    let users = usersDB.map((user) => user._id.toString())
  
    console.log(`Fetched users list`)
  
    for(const user of users){
      for(const product of returnRandomProducts(products, 0.97)){
        const delta = Math.floor(Math.random() * 12) + 3;
        const startDate = new Date("Mar 01 2021");
        startDate.setDate(startDate.getDate() + Math.random() * 120);
        const endDate = new Date();
        endDate.setDate(endDate.getDate() - Math.random() * 60);
        const dataObject = {
          userId: user,
          productId: product,
          start: startDate,
          end: endDate,
          delta, 
          stdDev: Math.floor((delta * (Math.random() / 3)) + 2)
        }
        const dataToPush = generateCartData(dataObject);
        if(dataToPush.length > 100){
          console.log(`${start}, ${end}, ${delta}, ${stdDev}`)
        } else {
          await CartModel.create(dataToPush)
            .then(() => { console.log (`Successfully pushed ${dataToPush.length} records for User: ${user} with Product: ${product}`) })
            .catch((err) => console.log(err));
        }        
      }
    }
  }
}

async function run() {
  await generateData();
}

run().catch(error => error.stack);