const jwt = require('jsonwebtoken');

module.exports = (req, res, next) => {
  if(!req.headers || !req.headers.authorization)
    res.status(500).send({
      message: 'Internal server error'
    });
  else {
    const token = req.headers.authorization;
    jwt.verify(token, 'SECRETKEYGOESHERE', function(err, decoded){
      if(err)
        res.status(500).send({
          message: 'Unable to login',
        })
      req.token = decoded;
      next();
    });
  }
}