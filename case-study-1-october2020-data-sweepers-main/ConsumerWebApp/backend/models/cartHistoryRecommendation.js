const mongoose = require('mongoose');

const CartHistoryRecommendation = mongoose.model('Cart_History_Recommendation', {
  userId: String,
  productId: String,
  created: Date,
  from: Date,
  to: Date,
})

module.exports = CartHistoryRecommendation;