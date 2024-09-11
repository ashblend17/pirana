const mongoose = require('mongoose');

const semSch = new mongoose.Schema({
    _id:{type:String},
    semester_id: {type:String},
    student_id:{type:String},
    sgpa: {type:String}
});

module.exports = mongoose.model('semester', semSch);