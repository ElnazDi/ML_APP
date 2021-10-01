const express = require('express');
const router = express.Router();
const BookmarkModel = require('../models/bookmark');

var auth = require('../middleware/auth');

router.post('/', auth, function(req, res, next){
  const bookmark = new BookmarkModel({
    userId: req.token.id,
    productId: req.body.id,
    created: (new Date()),
    active: true,
  });
  console.log(req.body.id);
  bookmark.save().then((doc) => {
    console.log(doc);
    res.status(200).send({
      message: 'Successfully bookmarked product'
    })
  }).catch((err) => {
    console.log(err);
    res.status(500).send({
      message: 'Internal Server Error'
    })
  })
})

router.delete('/', auth, function(req, res, next){
  BookmarkModel.findOneAndUpdate({
    userId: req.token.id,
    productId: req.body.id,
    active: true,
  }, {
    modified: (new Date()),
    active: false,
  }).then((doc) => {
    if(doc)
      res.status(200).send({
        message: 'Successfully unbookmarked product'
      });
    else
      res.status(400).send({
        message: 'Bookmark not found'
      });
  }).catch((err) => {
    res.status(500).send({
      message: 'Internal Server Error'
    })  
  })
})

router.get('/', auth, function(req, res, next){
  BookmarkModel.find({
    userId: req.token.id,
    active: true,
  }).then((bookmarkedDocs) => {
    const products = bookmarkedDocs.map(product => {
      return product.productId;
    });
    res.status(200).send({
      products,
    });
  }).catch((err) => {
    console.log(err);
    res.status(500).send({
      message: 'Unable to fetch bookmarked products',
    });
  });
})

module.exports = router;
