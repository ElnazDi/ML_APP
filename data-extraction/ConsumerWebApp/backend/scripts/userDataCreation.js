const faker = require('faker');
const bcrypt = require('bcrypt');
const mongoose = require('mongoose');
mongoose.connect('mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority');
// mongoose.connect('mongodb://localhost:27017/smartshop')

const UserModel = require('../models/user');

const password = '$2b$10$8q4IbzexLp9O6Sa22t1beON84IQw1Cwbkq95lPOKhzh5R8IfDa/O6'; //Test@123

const promises = [];

function returnGender() {
  if(Math.random() < 0.05) {
    return "Other";
  } else if(Math.random() < 0.525){
    return "Female";
  }
  return "Male";
}

for(let i = 0; i < 1000; i++) {
  const user = new UserModel({
    username: faker.internet.userName(),
    password,
    gender: returnGender(),
    phone: faker.phone.phoneNumber(),
    email: faker.internet.email(),
    country: faker.address.country(),
    dateOfBirth: (new Date(faker.date.between('1950-01-01', '2000-01-01'))).toISOString(),
  })
  console.log(user);
  promises.push(user.save())
}

Promise.all(promises).then(() => {
  mongoose.disconnect();
}).catch(() => {
  mongoose.disconnect();
})
