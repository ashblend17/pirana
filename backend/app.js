const express = require('express');
const app = express();
const cors = require('cors');
const db = require('./db/init');
const router = express.Router();
require('dotenv').config();

app.use(cors());
app.use(express.json());

// db();
app.get('/', (req, res) => {
    res.send('Hello pirates!');
});