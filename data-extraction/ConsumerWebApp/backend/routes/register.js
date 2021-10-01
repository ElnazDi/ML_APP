const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const UserModel = require('../models/user');

/* Register new user */
router.post('/', function(req, res, next) {
  bcrypt.hash(req.body.password, 10, function(err, hash){
    if(err)
      res.status(500).send({
        message: 'Server error occurred',
      })
    const user = new UserModel({
      username: req.body.username,
      password: hash,
      gender: req.body.gender,
      phone: req.body.phone,
      email: req.body.email,
      country: req.body.country,
      dateOfBirth: req.body.dob,
    });
    UserModel.findOne({
      username: req.body.username
    }).then((data) => {
      if(data)
        res.status(400).send({
          message: 'Username already exists!'
        })
      user.save().then(() => {
        res.status(200).send({
          'message': "Successfully saved user"
        });
      }).catch(() => {
        res.status(500).send({
          'message': 'Server error occurred'
        })
      })
    })
  })
});

module.exports = router;
