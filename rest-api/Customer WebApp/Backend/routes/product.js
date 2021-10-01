const express = require("express");
const productRouter = express.Router();
const Products = require("./../models/products")
const configFile = require('./../config.json');

/*
    @route: http://localhost:8000/product/discounts/1
    @desc:  Fetch all products with discounts
    @params: Page Size, Page Number   
    @body:
*/
productRouter.get("/discounts/:pageNum",  async (req, res, next) => {

    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Products retrieved successfully';

    // Handling errors
    try {
        data = await Products.getDiscounts(req.params.pageNum);
        // If there are no results
        if(data === undefined | data == 'undefined'){
            status = configFile["No_Content_Code"];
            message = 'No content found';
        }
    } catch (err) {
        console.error(err);
        status = configFile["Internal_Server_Error_Code"];
        message = 'Internal problem error';
    }
    
    // Send final response 
    return res.json({
        'status': status,
        'pageNumber':req.params.pageNum,
        'data': data,
        'message': message});
});


/*
    @route: http://localhost:8000/product/products/1
    @desc:  Fetch all products
    @params: Page Size, Page Number
    @body:
*/
productRouter.get('/products/:pageNum', async (req, res, next) => {
    query = " ";
    if ( req.query.search){
        query = req.query.search
    }

    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Products retrieved successfully';

    try {
        data = await Products.getAll(req.params.pageNum,query);
        // If there are no results
        if(data === undefined | data == 'undefined'){
            status = configFile["No_Content_Code"];;
            message = 'No content found';
        }
    } catch (err) {
        console.error(err);
        status = configFile["Internal_Server_Error_Code"];
        message = 'Internal problem error';
    }    

    // Send final response 
    return res.json({
        'status': status,
        'pageNumber':req.params.pageNum,
        'data': data,
        'message': message});
});

/*
    @route: http://localhost:8000/product/60ebe14f43b340c26e6736ee
    @desc:  Fetch details of a product
    @params: Product Id    
    @body:
*/
productRouter.get('/:productId', async (req, res) => {

    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Product retrieved successfully';

    try {
        data = await Products.get(req.params.productId);
        // If there are no results
        if(data === undefined | data == 'undefined'){
            status = configFile["No_Content_Code"];;
            message = 'No content found';
        }
        
    } catch (err) {
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
    @route: http://localhost:8000/product/kaufland/1
    @desc:  Filtering the products for kaufland only
    @params: Page Number   
    @body:
*/

productRouter.get('/kaufland/:pageNum', async (req, res) => {

    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Product retrieved successfully';

    try {
        data = await Products.getKauflandProducts(req.params.pageNum);
        // If there are no results
        if(data === undefined | data == 'undefined'){
            status = configFile["No_Content_Code"];;
            message = 'No content found';
        }
        
    } catch (err) {
        console.error(err);
        status = configFile["Internal_Server_Error_Code"];
        message = 'Internal problem error';
    }
    // Send final response 
    return res.json({
        'status': status,
        'data': data,
        'pageNumber':req.params.pageNum,
        'message': message});  
});


/*
    @route: http://localhost:8000/product/Netto/1
    @desc:  Filtering the products for Netto only
    @params: Page Number   
    @body:
*/

productRouter.get('/Netto/:pageNum', async (req, res) => {

    // Default response data
    var data = []
    var status = configFile["Accepted_Code"];
    var message = 'Product retrieved successfully';

    try {
        data = await Products.getNettoProducts(req.params.pageNum);
        // If there are no results
        if(data === undefined | data == 'undefined'){
            status = configFile["No_Content_Code"];;
            message = 'No content found';
        }
        
    } catch (err) {
        console.error(err);
        status = configFile["Internal_Server_Error_Code"];
        message = 'Internal problem error';
    }
    // Send final response 
    return res.json({
        'status': status,
        'data': data,
        'pageNumber':req.params.pageNum,
        'message': message});  
});


  


// Expose router to use in app
module.exports = productRouter;



