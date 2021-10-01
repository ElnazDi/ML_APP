const express = require('express');
const router = express.Router();
const CartModel = require('../models/cart');

var auth = require('../middleware/auth');

router.post('/increment', auth, function(req, res, next){
  CartModel.findOne({
    userId: req.token.id,
    productId: req.body.productId,
    active: true,
  }).then(product => {
    if (product) {
      CartModel.updateOne({
        userId: req.token.id,
        productId: req.body.productId,
        active: true,
      }, {
        quantity: product.quantity + 1,
        modified: (new Date()),
      }).then(() => {
        const data = {
          id: product._id,
          productId: product.productId,
          quantity: product.quantity + 1,
        }
        console.log(data)
        res.status(200).send({
          'message': 'Successfully added product to cart',
          data,
        })    
      }).catch(err => {
        res.status(500).send({
          'message': 'Error occurred while updating product in cart'
        })
      })
    } else {
      // No product found, create a new product in cart
      const newProductInCart = new CartModel({
        userId: req.token.id,
        productId: req.body.productId,
        active: true,
        quantity: 1,
        deleted: false,
        created: (new Date()),
      })
      newProductInCart.save().then(savedProduct => {
        res.status(200).send({
          message: 'Successfully saved product in cart',
          data: {
            id: savedProduct._id,
            productId: savedProduct.productId,
            quantity: savedProduct.quantity
          }
        })
      }).catch(err => {
        res.status(500).send({
          message: 'Error occurred while adding new product to cart'
        })
      })
    }
  }).catch(err => {
    console.log(err)
    res.status(500).send({
      'message': 'Error occurred while saving product to cart'
    })
  })
});

router.post('/decrement', auth, function(req, res, next){
  CartModel.findOne({
    userId: req.token.id,
    productId: req.body.productId,
    active: true,
  }).then(product => {
    if (product){
      CartModel.updateOne({
        userId: req.token.id,
        productId: req.body.productId,
        active: true,
      }, {
        quantity: product.quantity - 1,
        modified: (new Date()),
      }).then(() => {
        const data = {
          id: product._id,
          productId: product.productId,
          quantity: product.quantity -1,
        }
        res.status(200).send({
          message: 'Successfully decremented the product by 1 quantity',
          data,
        })
      }).catch(err => {
        res.status(500).send({
          message: 'Error occurred while decrementing the product quantity'
        })
      })
    }
  }).catch(() => {
    res.status(500).send({
      message: 'Error occurred while decrementing the product quantity',
    })
  })
});

router.post('/bought', auth, function(req, res, next){
  CartModel.findOneAndUpdate({
    userId: req.token.id,
    productId: req.body.productId,
    active: true,
  }, {
    userId: req.token.id,
    productId: req.body.productId,
    active: false,
    modified: (new Date())
  }).then(() => {
    res.status(200).send({
      message: 'Successfully updated product in cart',
      data: {
        productId: req.body.productId,
      }
    });
  }).catch((err) => {
    res.status(500).send({
      message: 'Error while removing product form cart',
    })
  })
})

router.delete('/', auth, function(req, res, next){
  CartModel.findOneAndUpdate({
    userId: req.token.id,
    productId: req.body.productId,
    active: true,
  }, {
    userId: req.token.id,
    productId: req.body.productId,
    active: false,
    deleted: true,
    removed: (new Date())
  }).then(() => {
    res.status(200).send({
      message: 'Successfully removed product from cart',
      data: {
        productId: req.body.productId,
      }
    });
  }).catch((err) => {
    res.status(500).send({
      message: 'Error while removing product form cart',
    })
  })
})

router.get('/', auth, function(req, res, next){
  CartModel.find({
    userId: req.token.id,
    active: true,
  }).then((products) => {
    const cartProducts = products.map(product => {
      return {
        productId: product.productId,
        quantity: product.quantity,
        id: product._id,
      }
    })
    res.status(200).send({
      products: cartProducts,
    })
  }).catch(() => {
    res.status(500).send({
      message: 'Unable to fetch the products in the cart',
    })
  })
})

module.exports = router;