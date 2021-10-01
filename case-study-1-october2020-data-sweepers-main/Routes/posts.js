const express = require('express');
const router =express.Router();
const Post=require('../models/Post')



// Server codes


//ROUTES

router.get('/id/add',async(req,res)=>{    
    try{
        const posts = await Post.find();
        res.json(posts);
        
        
    }catch(err){
        
        res.json({message:err});  
    }
});

/*
router.get('/id/add',async(req,res)=>{    
    try{
        var data=[];
        var data = Post.find(reqs.params.userId);
        var status = 200;
        var message = 'Carts retrieved successfully';

        if(data === undefined | data == 'undefined' | data.length == 0){
            status = No_Content_Code;
            message = 'No content found';
        }
        
        }catch(err){
        console.error(err);
        status = Internal_Server_Error_Code;
        message = 'Internal problem error';
        

        }return res.json({
        'status': status,
        'data': data,
        'message': message});
});

*/


router.post('/id',async(req,res)=>{
    //console.log(req.body);
    const post = new Post({
        userId:req.body.userId,
        products:req.body.products,
        status:req.body.status

    });

    try{
    const savedPost=await post.save();
        res.json(savedPost);
    }catch(err){
        res.json({message: err});
    }    
});

router.get('/:bookmarksId',async(req,res)=>{
    try{
    //console.log(req.params.addId)
    const post= await Post.findById(req.params.bookmarksId);
    res.json(post);
    
    }catch(err){
        res.json({message: err});
    }
});


router.delete('/:bookmarksId',async(req,res)=>{
    try{   
    const removebookmark = await Post.remove({_id:req.params.bookmarksId});
    res.json(removebookmark); 
    }catch(err){
        res.json({message:err});
    }
});

module.exports= router;
