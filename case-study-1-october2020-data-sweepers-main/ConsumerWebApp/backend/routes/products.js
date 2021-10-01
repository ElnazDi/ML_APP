const express = require('express');
const router = express.Router();
const ProductModel = require('../models/product');
const BookmarkModel = require('../models/bookmark');0

var auth = require('../middleware/auth');

router.get('/', auth, function(req, res, next){
  // const { skip, limit } = req.body
  ProductModel.find({})
  .limit(2500)
  .then((docs) => {
      res.status(200).send({
        products: docs,
      });
    }).catch((err) => {
        console.log(err);
        res.status(500).send({
          'message': 'Unable to fetch list of products',
        });
    });
});

module.exports = router;