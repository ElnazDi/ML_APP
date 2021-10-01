var express = require("express");
var mongoose = require("mongoose");
const cors = require('cors');
const configFile = require("./config.json");

// initializing the port
const PORT = process.env.PORT || 8000;

// Init app
const app = express();

async function start() {
    // Init app and DB connection
    mongoose.connect(
        configFile["uri"],
        { useNewUrlParser: true, useUnifiedTopology: true },
        () => {
        console.log("Connected to DB");
        }
    );
    //await MongoDB.init();
    app.use(cors());
    app.use(express.json());
    app.use(require("body-parser").urlencoded({ extended: false }));
    require('dotenv').config()
    //Set up the routes
    app.use("/cart", require("./routes/cart"));
    app.use("/product", require("./routes/product"));
    app.use("/bookmark", require("./routes/bookmark"));
    app.use('/users',require('./routes/users'));    
    app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    });
}
start();
