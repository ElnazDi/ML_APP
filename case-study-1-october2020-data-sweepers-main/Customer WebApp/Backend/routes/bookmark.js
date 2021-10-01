const express = require("express");
const bookmarkRouter = express.Router();
const Bookmarks = require('../models/bookmark');
const configFile = require('./../config.json');
const auth = require('../middleware/auth');

/*
    @route:         http://localhost:8000/bookmark/bookmarks
    @desc:          Fetch all active existing bookmarks from a particular user
    @params:    
    @authorization: UserID
*/
bookmarkRouter.get('/bookmarks', auth, async (req, res) => {
    
    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Bookmarks retrieved successfully';

    // Handling errors
    try{
        console.log(`User Id from middleware: ${req.userId}`);
        var data = await Bookmarks.getAll(req.userId);
        // If there are no results
        if(data === undefined | data == 'undefined'){
            status = configFile["No_Content_Code"];
            message = 'No content found';
        }
    } catch(err){
        console.error(err);
        status = configFile["Internal_Server_Error_Code"];
        message = 'Internal problem error';
    }
    
    // Send final response 
    return res.json({
        'status': status,
        'data': data,
        'message': message});
});


/*
    @route:         http://localhost:8000/bookmark/60eb79fc369a318801384b60/add
    @desc:          Add a new bookmark for a specific product
    @params:        Product Id
    @authorization: UserID
*/
bookmarkRouter.get('/:productId/add', auth,  async (req, res) => {

    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Bookmark added successfully';

    // Handling errors
    try {
        const flagNewBookark = await Bookmarks.add(req.userId, req.params.productId);
        // If there are no results
        if(flagNewBookark == 0){
            status = configFile["No_Content_Code"];
            message = 'Bookmark enabled again';
        }
        else if(flagNewBookark == -1){
            status = configFile["Internal_Server_Error_Code"];
            message = 'Internal problem error';
        }
    } catch (err) {
        console.error(err);
        status = configFile["Internal_Server_Error_Code"];
        message = 'Internal problem error';
    }
    
    // Send final response 
    return res.json({
        'status': status,
        'message': message});
});

/*
    @route:         http://localhost:8000/bookmark/60eb79fc369a318801384b60/delete
    @desc:          Remove a bookmark
    @params:        Product Id
    @authorization: UserID
*/
bookmarkRouter.get('/:productId/delete',auth, async (req, res) => {
    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Bookmark deleted successfully';

    // Handling errors
    try {
        // If there are no results
        if(!await Bookmarks.delete(req.userId, req.params.productId)){
            status = configFile["No_Content_Code"];
            message = 'Bookmark already deleted';
        }
    } catch (err) {
        console.error(err);
        status = configFile["Internal_Server_Error_Code"];
        message = 'Internal problem error';
    }
    
    // Send final response 
    return res.json({
        'status': status,
        'message': message});
});



module.exports = bookmarkRouter;



