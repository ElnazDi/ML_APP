const mongoose = require('mongoose');

const ContentBaseRecommendation = mongoose.model('Content_Base_Recommendation', {
  productId: String,
  recommendedProducts: Array,
})

module.exports = ContentBaseRecommendation;