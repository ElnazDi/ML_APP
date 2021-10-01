const { MongoClient } = require('mongodb');
const configFile = require('./../config.json');
const parseJson = require('parse-json');


class MongoBot {
    
    constructor() {
        console.log('MongoBot constructor');
        this.client = new MongoClient(configFile["uri"],  {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        
    }

    async init() {
        console.log('MongoBot Init');
        await this.client.connect();
        this.db = this.client.db(configFile["dbName"]);
    }
  }
  
  // When we create an instance and expose it, nodejs uses its cache to store this value, which is what we want as a Singleton
  module.exports = new MongoBot();
  