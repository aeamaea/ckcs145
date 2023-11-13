const express = require('express');
const router = express.Router();

const Task = require('../models/task');

// get all tasks
// note that the route is the same ie /tasks/
// but method is GET

router.get('/', async(req, res) => {
    try {
        const tasks = await Task.find();
        res.json(tasks);
    } catch(err) {
        res.status(500).json({message: err.message});
    }
});

// Create a task
// to create a task we just post to the same URL
// same URL /tasks/ but method is POST and vars are coming
// via the variables :: aeam

router.post('/', async(req, res) => {
    const task = new Task({
        title: req.body.title,
        description: req.body.description
    });

    try {
        const newTask = await task.save();
        res.status(201).json(newTask);
    } catch(err){
        res.status(500).json({message: err.message});
    }
});

// middleware for our /:id route
async function getTask(req, res, next) {
    let task;
    try{
        task = await Task.findById(req.params.id);
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
router.get('/:id', getTask, (req, res) => {
    res.json(res.task);
});

// Update a specific task by "ID"
router.patch('/:id', getTask, async(req,res) => {
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

router.delete('/:id', getTask, async(req,res) => {
    try{
        await res.task.remove();
        res.json({message: "deleted"});
    }catch(err){
        res.status(500).json({message: err.message});
    }
});

module.exports = router;