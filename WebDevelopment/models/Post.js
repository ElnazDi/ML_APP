const mongoose=require('mongoose');
const PostSchema=mongoose.Schema( {

    userId:
    {
        type:String,
        required:true

    },

    /*productId:
    {
        type:String,
        required:true
    },*/

    products: 
    [{ qty: Number, productId: String }],
    
    status:
    {
        type:String,
        required:true
    },

    insert_dt:
    {
        type:Date,
        default:Date.now
    },

    update_dt:

    {
        type:Date,
        default:null 
    }

    
},{
    collection:'bookmarks_col'
});

module.exports=mongoose.model('bookmarks_col',PostSchema);