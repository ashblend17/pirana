require('dotenv').config();
const connect_uri = process.env.mongo_connect;
const db = require('mongoose');
module.exports = function init()
{
    try{
        const database = db.connect(connect_uri);
        console.log('Connected to the database');
    }
    catch(err){
        console.log('Error connecting to the database');
    }
};