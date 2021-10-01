const express = require('express');
const router = express.Router();
const CartHistoryRecommendationModel = require('../models/cartHistoryRecommendation');
const GenericRecommendationModel = require('../models/genericRecommendation');
const ContentBaseRecommendationModel = require('../models/contentBaseRecommendation');
const BookmarkModel = require('../models/bookmark');

const auth = require('../middleware/auth');

router.get('/cartHistory', auth, function(req, res, next){
  CartHistoryRecommendationModel.find({
    userId: req.token.id,
    // from: { $lt: (new Date()) },
    // to: { $gt: (new Date()) }
  }).then(products => {
    res.status(200).send({
      message: 'Successfully retrieved recommendation for user',
      products
    })
  }).catch(err => {
    console.log(err);
    res.status(500).send({
      message: 'Error while retrieving recommendation for user',
    })
  })
});

router.get('/generic', auth, function(req, res, next){
  GenericRecommendationModel.find({}).then(products => {
    res.status(200).send({
      message: 'Successfully retrieved generic recommendations',
      products
    })
  }).catch(err => {
    console.log(err);
    res.status(500).send({
      message: 'Error while retrieving generic recommendations',
    })
  })
})

router.get('/bookmark', auth, function(req, res, next){
  const recommendedProductIds = [];
  BookmarkModel.find({
    userId: req.token.id,
    active: true
  }).then(bookmarks => {
    const promises = [];
    for(const index in bookmarks){
      promises.push(ContentBaseRecommendationModel.findOne({
        productId: bookmarks[index].productId,
      }).then((doc) => {
        if(doc) {
          for(const id in doc.recommendedProducts){
            recommendedProductIds.push(doc.recommendedProducts[id])
          }
        }
      }).catch(err => console.log(err)))
    }
    Promise.all(promises).then(() => {
      const products = Array.from(new Set(recommendedProductIds));
      res.status(200).send({
        message: 'Succesfully fetched recommendations based on bookmark',
        products
      })
      console.log('Fetched all products');
    }).catch(err => console.log(err))
  })
})

module.exports = router;