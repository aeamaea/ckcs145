const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const Coeffs = require('./models/coeffmodel');
const Contacts = require('./models/contactmodel');

// console.log(taskRouter);
dotenv.config();

const app = express();

// https://stackoverflow.com/questions/4529586/render-basic-html-view

// this is for express 3.0.0/3.10.0
app.set('views', __dirname + '/views');
app.engine('html', require('ejs').renderFile);

// this is for express 3.4+ as per link above
app.set('view engine', 'ejs');

// middleware
app.use(cors());
app.use(express.json());
// app.use('/tasks', taskRouter);
// app.use('/jwfoods', jwRouter);
app.use(express.static('views'));
// apparently I need body-parser so I can get 
// to the form variables in post variables (wut?)
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: true }));


// connect to mongoose
// notice I don't use db anywhere it's 
// just there to catch the output of connection attempt
// in case I need to console.log() it.
mongoose.connect(process.env.DB_CONN_STR);
const db = mongoose.connection;

// -----------------
// routes
// -----------------

// Get the main page
app.get('/', (req,res) => {
    res.render('company1.1.html');
});

// add contact
app.post('/add_contact', async(req,res) => {
    // make a new coeffs object
    const contact = new Contacts({
        name: req.body.name,
        email: req.body.email,
        comments: req.body.comments
    });
    console.log(contact);
    // put it in the backend
    try {
        const newContact = await contact.save();
        console.log("newContact: ", newContact);
        res.status(201).json({status:"added contact"});
    } catch(err){
        res.status(500).json({error: err.message});
    }
})
// just get the form values and stuff them in the database
// but delete the current document first :: aeam
// this will eventually be called by the /admin route.

app.get('/update_coeffs', async (req, res) => {
    res.render('update_coeffs.html')
})

app.post('/update_coeffs', async(req,res)=> {
    try{
        // just remove whatever's in there
        // seems to work for an empty Coeffs collection as well. 
        let delete_result = await Coeffs.deleteMany({});

        // make a new coeffs object
        const coeffs = new Coeffs({
            weight_coeff: req.body.weight_coeff,
            distance_coeff: req.body.distance_coeff
        });
    
        // put it in the backend
        try {
            const newCoeff = await coeffs.save();
            res.status(201).json(newCoeff);
        } catch(err){
            res.status(500).json({create_message: err.message});
        }
    }catch(err){
        res.status(500).json({delete_message: err.message});
    }

});


app.post('/calc_charges', async(req, res) => {

    // get the weight and distance that the user entered.
    // console.log(req.body);
    weight = parseFloat(req.body.weight);
    distance = parseFloat(req.body.distance);
    //console.log(req.body.weight,req.body.distance);
    // init the vars we're going to get from the 
    // mongo backend.
    let db_weight_coeff = 0.0;
    let db_distance_coeff = 0.0;

    try {
        const coeffs = await Coeffs.find().lean();
        db_weight_coeff = parseFloat(coeffs[0].weight_coeff);
        db_distance_coeff = parseFloat(coeffs[0].distance_coeff);
        console.log(db_weight_coeff,db_distance_coeff);
        // calculate delivery charges.
        let delivery_cost = weight * db_weight_coeff + distance * db_distance_coeff;
        res.json({"delivery_cost":delivery_cost});
        
    } catch(err) {
        res.status(500).json({message: err.message});
    }
});

// =====================================================
// admin interface :: login/logout/modify coeffs routes
// =====================================================

app.get('/login', (req,res) => {
    res.render('login.html');
});

// start the appserver
app.listen(3000);
