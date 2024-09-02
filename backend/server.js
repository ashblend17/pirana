require('dotenv').config();
const cors = require('cors');
const express = require('express');
const app = express();
const mongoose = require('mongoose');
const db = require('./db/init');
const cook = require('./app');
app.use(cors());
app.use(express.json());
const port = process.env.PORT || 4000;
const IP = process.env.IP || 'localhost';
mongoose.connect(process.env.mongo_connect);

app.get('/:id', (req, res) => {
    mongoose.
});

app.listen(port, IP, () => {
    console.log(`Server running at http://${IP}:${port}`);
});