const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const UserModel = require('../models/user');
const jwt = require('jsonwebtoken');

/* Login existing user */
router.post('/', function(req, res, next) {
  UserModel.findOne({ username: req.body.username })
    .then((data) => {
      if(!data)
        res.status(404).send({
          message: 'Username / Password is incorrect',
        })
      else {
        bcrypt.compare(req.body.password, data.password).then((result) => {
          if(!result)
            res.status(404).send({
              message: 'Username / Password is incorrect',
            })
          //TODO: Extract secret key to configuration file
          const token = jwt.sign({
            id: data._id
          }, 'SECRETKEYGOESHERE', (err, token) => {
            if(err)
              console.log(error);
            res.status(200).send({
              token: token,
            });
          });
        });
      }
    })

});

module.exports = router;
