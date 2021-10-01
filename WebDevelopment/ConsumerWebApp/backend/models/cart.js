const mongoose = require('mongoose');

const Cart = mongoose.model('Cart', {
  userId: String,
  productId: String,
  active: Boolean,
  deleted: Boolean,
  quantity: Number,
  created: Date,
  modified: Date,
  removed: Date,
})

module.exports = Cart;