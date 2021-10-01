const createError = require('http-errors');
const express = require('express');
const path = require('path');
const logger = require('morgan');
const cors = require('cors');

const mongoose = require('mongoose');
mongoose.connect('mongodb+srv://datasweepers:d4t4sw33p3rs@clustervendors.zfzwq.mongodb.net/vendors_data_db?retryWrites=true&w=majority');

const registerRouter = require('./routes/register');
const loginRouter = require('./routes/login');
const productsRouter = require('./routes/products');
const bookmarkRouter = require('./routes/bookmark');
const cartRouter = require('./routes/cart');
const recommendationRouter = require('./routes/recommendation');
const cartHistoryRouter = require('./routes/cartHistory');

const app = express();

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/register', registerRouter);
app.use('/login', loginRouter);
app.use('/products', productsRouter);
app.use('/bookmark', bookmarkRouter);
app.use('/cart', cartRouter);
app.use('/recommendations', recommendationRouter);
app.use('/cartHistory', cartHistoryRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.send('error');
});

module.exports = app;
