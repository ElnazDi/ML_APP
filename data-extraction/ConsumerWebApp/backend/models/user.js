const mongoose = require('mongoose');

const User = mongoose.model('User', {
  username: String,
  password: String,
  gender: String,
  phone: String,
  email: String,
  country: String,
  dateOfBirth: String,
});

module.exports = User;