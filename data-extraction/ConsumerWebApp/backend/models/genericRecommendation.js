const mongoose = require('mongoose');

const GenericRecommendation = mongoose.model('Generic_Recommendation', {
  productId: String,
  description: String,
  from: Date,
  to: Date,
})

module.exports = GenericRecommendation;