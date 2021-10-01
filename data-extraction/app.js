
const express =require('express');
const app = express();
const mongoose = require('mongoose');
const bodyParser  = require('body-parser');
const cors = require('cors');
require('dotenv/config');


//Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({
  extended: true
}));



//Import Routes (kinda using middleware)
const postsRoute = require('./routes/posts');
//app.use('/post',postsRoute)
app.use('/bookmarks',postsRoute)


//connect to database
mongoose.connect(process.env.DB_CONNECTION,
    { useUnifiedTopology: true },
    ()=>console.log('Connected to db')
);

//listen to server
app.listen(3000);
