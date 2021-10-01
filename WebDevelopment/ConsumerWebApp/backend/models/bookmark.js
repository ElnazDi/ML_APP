const mongoose = require('mongoose');

const Bookmark = mongoose.model('Bookmark', {
  userId: String,
  productId: String,
  active: Boolean,
  created: Date,
  modified: Date,
})

module.exports = Bookmark;