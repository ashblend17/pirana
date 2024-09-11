require('dotenv').config();
const cors = require('cors');
const express = require('express');
const app = express();
const mongoose = require('mongoose');
const semester = require('./model/semester.js');
const db = require('./db/init');
const cook = require('./app');
app.use(cors());
app.use(express.json());
const port = process.env.PORT || 3000;
const IP = process.env.IP || 'localhost';

mongoose.connect(process.env.mongo_connect).then(() => console.log('connected to mnogodb database')).catch((e) => console.log('error connecting to database',e));

app.get('/sem', (req, res) => {
    res.send({'Hello World!' : 'Welcome to the Cook API - sem'});
});

app.get('/stu', (req, res) => {
    res.send({'Hello World!' : 'Welcome to the Cook API - stu'});
});

app.get('/cou', (req, res) => {
    res.send({'Hello World!' : 'Welcome to the Cook API - cou'});
});


app.get('/sem', async(req, res) => {
    const {student_id} = req.body;
    try
    {
        const sem = await semester.find({"student_id": student_id}).exec();
        console.log(sem);
        res.send(sem);
    }
    catch(e)
    {
        console.log('cannnot find',e);
    }
});


app.listen(port, IP, () => {
    console.log(`Server running at http://${IP}:${port}`);
});