const express = require("express");
const cartRouter = express.Router();
const Carts = require("../models/cart")
const configFile = require('./../config.json');
const auth = require('../middleware/auth');


/*
    @route: http://localhost:8000/cart/carts
    @desc:  Fetch all active existing carts from a particular user
    @params:    
    @body:      UserID*
*/
cartRouter.get('/carts', auth, async (req, res) => {
    
    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Carts retrieved successfully';

    // Handling errors
    try{
        var data = await Carts.getAll(req.userId);
        // If there are no results
        if(data === undefined | data == 'undefined' | data.length == 0){
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
    @route:     http://localhost:8000/cart/CartName
    @desc:      Details of specific cart from user
    @params:    Cart ID
    @body:      UserID
*/
cartRouter.get('/:id', auth, async (req, res) => {
    
    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];;
    var message = 'Cart retrieved successfully';

    // Handling errors
    try{
        var data = await Carts.getCart(req.userId, req.params.id);
        // If there are no result
        if(data === undefined | data == 'undefined' | data.length == 0){
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
    @route:     http://localhost:8000/cart/CartName/delete
    @desc:      Delete a cart for a paritcular user
    @params:    Cart Name
    @body:      UserID
*/
cartRouter.get('/:id/delete', auth, async (req, res) => {
    
    // Default response data
    var data = req.params.id;
    var userId = req.userId;
    var status = configFile["Accepted_Code"];;
    var message = 'Cart deleted successfully';
    console.log(`Delete ${data} for ${userId}`)
    
    // Handling errors
    try{
        if(!await Carts.delete(userId, data)){
            status = configFile["Not_Implemented_Code"];
            message = 'Cart not deleted';
        }
    } catch(err){
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
    @route:     http://localhost:8000/cart/CartName/add
    @desc:      Add a new cart for a paritcular user
    @params:    Cart Name
    @body:      UserID
*/
cartRouter.get('/:id/add', auth,  async (req, res) => {
    console.log('Add cart rout')
    // Default response data
    var data = req.params.id;
    var status = configFile["Accepted_Code"];;
    var message = 'Cart created successfully';

     // Handling errors
     try{
        const createdCartFlag = await Carts.add(req.userId, data)
        if(createdCartFlag == 0){
            status = configFile["Not_Implemented_Code"];
            message = 'Cart already exists';
        }
        else if(createdCartFlag == -1){
            status = configFile["Internal_Server_Error_Code"];
            message = 'Internal problem error';
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
    @route:     http://localhost:8000/cart/CartNameTest/add/60eb79fc369a318801384b60/2
    @desc:      Add a new product in a cart for a paritcular user
    @params:    Cart Name, Product Id, Quantity
    @body:      UserID
*/
cartRouter.get('/:cartName/add/:productId/:qty', auth, async (req, res) => {
    
    // Default response data
    const cartName = req.params.cartName;
    const productId = req.params.productId;
    const qty = req.params.qty;
    var data = '';
    var status = configFile["Accepted_Code"];;
    var message = 'Product added successfully';

     // Handling errors
     try{
        const createdCartFlag = await Carts.addProduct(req.userId, cartName, productId, qty);
        if(createdCartFlag == 0){
            status = configFile["Not_Implemented_Code"];
            message = 'Product enabled again';
        }
        else if(createdCartFlag == -1){
            status = configFile["Internal_Server_Error_Code"];
            message = 'Internal problem error';s
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
    @route:     http://localhost:8000/cart/CartNameTest/delete/60eb79fc369a318801384b60
    @desc:      Delete a cart for a paritcular user
    @params:    Cart Name
    @body:      UserID
*/
cartRouter.get('/:cartName/delete/:productId', auth, async (req, res) => {
    
    // Default response data
    const cartName = req.params.cartName;
    const productId = req.params.productId;
    const qty = req.params.qty;
    var data = '';
    var status = configFile["Accepted_Code"];;
    var message = 'Product deleted successfully';
    
    // Handling errors
    try{
        if(!await Carts.deleteProduct(req.userId, cartName, productId)){
            status = configFile["Not_Implemented_Code"];
            message = 'Product not deleted';
        }
    } catch(err){
        console.error(err);
        status = configFile["Internal_Server_Error_Code"];
        message = 'Internal problem error';
    }
    
    // Send final response 
    return res.json({
        'status': status,
        'message': message});
});


module.exports = cartRouter;



