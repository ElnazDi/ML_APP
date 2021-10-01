const { Router } = require("express");
const express = require("express");
const userRouter = express.Router();
const { Users, User } = require('../models/user');
const bcrypt = require("bcryptjs");
const configFile = require('./../config.json');

const UsersInstance = new Users();


const jwt = require("jsonwebtoken");


/*
    @route: http://localhost:8000/users/login
    @desc:  Login
    @params: 
*/
userRouter.post("/login", async (req, res) => {
  const {
    email,
    password
  } = req.body;
  try {
    var data = await UsersInstance.get(email);

    console.log(req.body);

    if ((data === undefined) | (data == "undefined")) {
      status = configFile["No_Content_Code"];
      message = "No email found";
    }
    if (data) {
      const validPassword = await bcrypt.compare(
        req.body.password,
        data.password
      );

      if (validPassword) {
        console.log("here were");

        // Generate an access token
        const accessToken = jwt.sign(
          { userId: data._id, role: data.role },
          configFile["accessTokenSecret"]
        );
        res.json({
          accessToken,
        });
      } else {
        res.status(configFile["Unauthorized_Code"]).json({ error: "Invalid Password" });
      }
    }
  } catch (err) {
    console.error(err);
    res.status(configFile["Internal_Server_Error_Code"]).json({ error: "Internal problem error" });
  }
});

/* Checks a password
 * @param {string} password  - The first password
 * @param {string} password2 - The repeated password
 * @return {array} errors    - An array of all the erros 
 *                             which ocurred (empty when sucessful)
 */
function checkPassword(password, password2) {
    // check passwords
    if (password !== password2) {
        var msg = "Passwords do not match";
        console.log(msg);
        return msg;
    }
    // check password length
    if (password.length < 6) {
        var msg = "Passwords should be minimum of 6 characters";
        console.log(msg);
        return msg;
    }
    return "";

}

function checkMandatoryFields(user){
    if (
        !user.firstName ||
        !user.email ||
        !user.password ||
        !user.password2 ||
        !user.phone ||
        !user.countryOfOrigin ||
        !user.dateOfBirth ||
        !user.gender
      ){
          console.log("Please fill in all the fields");
        return "Please fill in all the fields";

      }
      return "";
}

/*
    @route: http://localhost:8000/users/register
    @desc:  Regiser a new user
    @params:
    @body: first Name, last Name, email, password, gender, phone, dateOfBirth
*/
userRouter.post("/register", async (req, res) => {
  const {
    firstName,
    lastName,
    email,
    password,
    password2,
    gender,
    phone,
    countryOfOrigin,
    dateOfBirth,
  } = req.body;

  let errors = [];

  // check required fields
  var errorMsg = checkMandatoryFields(req.body);
 if (errorMsg != ""){
    errors.push({ msg:  errorMsg});

 }
  // check password
  errorMsg =  checkPassword(password, password2);
  if (errorMsg != ""){
    errors.push({ msg:  errorMsg});
 }
  if (errors.length !== 0) {

    res.status(configFile["Bad_Request"]).json({ error: errors[0].msg });

  } else {
    await UsersInstance.get(email)
    .then((user) => {
      if (user) {
        res.status(configFile["Unauthorized_Code"]).json({ error: "Email already exists" });

      } else {
        const newUser = new User({
          firstName,
          lastName,
          email,
          password,
          gender,
          countryOfOrigin,
          dateOfBirth,
          phone,
        });

        // Encrypt password
        bcrypt.genSalt(10, (err, salt) =>
          bcrypt.hash(newUser.password, salt, (err, hash) => {
            if (err) throw err;
            //set hashed passwFord
            newUser.password = hash;

            //save user
            UsersInstance.add(newUser)
              .then(() => {
                res.status(200).json({ status: 'success' });
              })
              .catch((err) => console.log(err));
          })
        );
      }
    })
    .catch((err) => res.status(configFile["Internal_Server_Error_Code"]).json({ error: "Internal problem error" }));
  }
});

module.exports = userRouter;
