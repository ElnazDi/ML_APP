const mongoose = require('mongoose');

const Product = mongoose.model('Product', {
  title: String,
  brand: String,
  price: Number,
  quantity: String,
  discount: Number,
  image: String,
  unitPrice: Number,
  unitPriceQuantity: String,
  oldPrice: Number,
  vendor: String,
});

module.exports = Product;