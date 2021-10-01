const express = require('express');
const router = express.Router();
const CartModel = require('../models/cart');

var auth = require('../middleware/auth');

router.get('/', auth, function(req, res, next){
  CartModel.find({
    userId: req.token.id,
    active: false,
  }).then((products) => {
    const cartProducts = products.map(product => {
      return {
        productId: product.productId,
        quantity: product.quantity,
        id: product._id,
        deleted: product.deleted,
        created: product.created,
        modified: product.modified,
        removed: product.removed,
      }
    })
    res.status(200).send({
      message: 'Sucessfully fetched cart history',
      products: cartProducts,
    })
  }).catch((err) => {
    res.status(500).send({
      message: 'Unable to fetch cart history',
    })
    console.log(err)
  })
})

module.exports = router;