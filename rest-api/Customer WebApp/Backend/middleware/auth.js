const jwt = require("jsonwebtoken");
const configFile = require('./../config.json');

module.exports = function(req,res,next){
    // Reads the authorization element in the request
    const authHeader = req.headers.authorization;
    // Decode token to extract user from it and store it in request
    if (authHeader) {
        const token = authHeader.split(" ")[1];
        jwt.verify(token, configFile["accessTokenSecret"], (err, user) => {
            if (err) {
                return res.sendStatus(configFile["Forbidden_Code"]);
            }
            // Set userId from user in DB
            req.userId = user.userId;
            console.log(`Request user: ${req.userId}`);
            next();
        });
    } else {
        res.sendStatus(configFile["Unauthorized_Code"]);
        // Redirect to login
        res.redirect("users/login");
    }

}
