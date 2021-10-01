const moment = require('moment');
const mongoose = require('mongoose');
mongoose.connect('mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority');

const UserModel = require('../models/user');
const CartModel = require('../models/cart');

// Users - age, nationality


UserModel.find({}).then((users) => {
  const data = {};
  const now = moment(new Date());
  for(const user in users) {
    if(!data[user.country])
      data[user.country] = {}
    const dateOfBirth = new Date(user.dateOfBirth);
    console.log(dateOfBirth);
    // console.log(now.diff(dateOfBirth, 'years'))
  }
}).catch(err => console.log(err))

