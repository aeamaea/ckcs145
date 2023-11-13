const mongoose = require('mongoose');

const ContactSchema = new mongoose.Schema({
    name: {
        type: String
    },
    email: {
        type: String,
    },
    comments: {
        type: String
    }
});
const Contacts = mongoose.model('Contacts', ContactSchema);

module.exports = Contacts;