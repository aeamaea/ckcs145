const express = require('express');
const jwrouter = express.Router();

// this exports the Coeffs module containing the jwfoods
// Schema
const Coeffs = require('../models/coeffmodel');

// get all coeefs
// note that the route is the same ie /tasks/
// but method is GET

jwrouter.get('/', async(req, res) => {
    try {
        const coeffs = await Coeffs.find().lean();
        let weight = parseFloat(coeffs[0].weight_coeff);
        let distance = parseFloat(coeffs[0].distance_coeff);
        console.log(weight,distance);
        //res.json({"weight":weight,"distance":distance});
        
    } catch(err) {
        res.status(500).json({message: err.message});
    }
});

jwrouter.post('/calc_charges', async(req, res) => {

    // get the weight and distance that the user entered.
    console.log(req.body);
    weight = parseFloat(req.body.weight);
    distance = parseFloat(req.body.distance);
    console.log(req.body.weight,req.body.distance);
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
        let delivery_charges = weight * db_weight_coeff + distance * db_distance_coeff;
        res.json({"delivery_charges":delivery_charges});
        
    } catch(err) {
        res.status(500).json({message: err.message});
    }
});


// Create a task
// to create a task we just post to the same URL
// same URL /tasks/ but method is POST and vars are coming
// via the variables :: aeam

// I think for purposes of jwfoods, it would be good to 
// just remove the current document and create a new one with 
// the new values. :D -- aeam --
jwrouter.post('/', async(req, res) => {
    const coeffs = new Coeffs({
        weight_coeff: req.body.weight_coeff,
        distance_coeff: req.body.distance_coeff
    });

    try {
        const newCoeff = await coeffs.save();
        res.status(201).json(newCoeff);
    } catch(err){
        res.status(500).json({message: err.message});
    }
});

// middleware for our /:id route
async function getCoeff(req, res, next) {
    let coeff;
    try{
        task = await Coeffs.findById(req.params.id);
        if(task == null){
            return res.status(404).json({message: 'Task not found'});
        }
    } catch (err) {
        return res.status(500).json({message: err.message})
    }
    res.task = task;
    next();
}

// Get a specific task by 'ID' 
// the lambda we're passing is the "next() function in getTask() btw"
jwrouter.get('/:id', getCoeff, (req, res) => {
    res.json(res.task);
});

// Update a specific task by "ID"
jwrouter.patch('/:id', getCoeff, async(req,res) => {
    if(req.body.title != null){
        res.task.title = req.body.title;
    }
    if(req.body.description != null){
        res.task.description = req.body.description;
    }
    try{
        const updateTask = await res.task.save();
        res.json(updateTask);
    }catch(err){
        res.status(400).json({message:err.message});
    }
});

// Delete a task by Id

jwrouter.delete('/:id', getCoeff, async(req,res) => {
    try{
        await res.task.remove();
        res.json({message: "deleted"});
    }catch(err){
        res.status(500).json({message: err.message});
    }
});

module.exports = jwrouter;