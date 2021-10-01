// const LocalStrategy = require('passport-local').Strategy;
// const mongoose = require('mongoose');
// const bcrypt = require('bcryptjs');

// //Load user 
// const User = require('../models/user');
// module.exports = function(passport){
//     passport.use(
//         new LocalStrategy({userNameField :'email'},(email,password,done) =>{
//         User.findOne({email:email})
//         //match email
//         .then(user =>   {
//             if (!user){
//                 return done(null,false,{"message": "email is not registered"});
//             }

//         //match password
//         bcrypt.compare(password ,user.password,(err,isMatch) =>{
//             if (err) throw err;

//             if (isMatch){
//                 return done(null,user)
//             }else{
//                 return done(null,false,{"message": "password incorrect"});

//             }
//         });    


//         })
//         .catch(err => console.log(err));
//         })
//     );

//     passport.serializeUser((user, done) => {
//         done(null, user.id);
//       });
      
//       passport.deserializeUser((id, done) => {
//         User.findById(id, function(err, user) {
//           done(err, user);
//         });
//       });
// }
