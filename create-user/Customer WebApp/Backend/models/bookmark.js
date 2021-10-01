const mongoose = require("mongoose");


/*
@Schema  Bookmark
*/
const BookmarkSchema=mongoose.Schema( {
    userId:
    {
        type:String,
        required:true

    },
    productId:
    {
        type:String,
        required:true

    },
    status:
    {
        type:Boolean,
        default:true
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

const Bookmark = mongoose.model("Bookmark", BookmarkSchema);

/*
@Model   Products
*/
class Bookmarks{
    
    constructor(){
        console.log('Bookmarks Constructor');
    }
    
    // @desc:   Fetch all active bookmarks
    // @params: 
    // @return: Array of products, containing the basic information to display
    async getAll(userId) {
        var result = await Bookmark.find({ status: true, userId : userId },'productId');
        return result;
    }

    // @desc:   Add a new bookmark
    // @params: user Id, product Id
    // @return: Flag indicating db operation
    async add(userId, productId){
        try{
            var newBookmark = new Bookmark();
            newBookmark.userId = userId;
            newBookmark.productId = productId;
            // Validate if bookmark already exists
            var validate = await Bookmark.findOne({userId : userId, productId: productId },'productId status');
            if(validate === null){
                await newBookmark.save()
                return 1;
            }
            else{
                // if already exists, just activate it once again
                newBookmark.status = !validate.status;
                newBookmark.update_dt = Date.now();
                await newBookmark.save();
                return 0;
            }
        }
        catch(e){
            console.log("Problem in the DB: " + e);
            return -1;
        }        
    }

    // @desc:   Delete a bookmark for a particular user
    // @params: user Id, cart name
    // @return: flag indicating db operation
    async delete(userId, productId){
        try{
            //Validate if cart is deleted already
            var validate = await Bookmark.findOne({userId : userId, productId: productId, status:false },'productId status');
            if(validate == null){
                await Bookmark.updateOne({userId : userId, productId: productId }, {status:false, update_dt: Date.now() },{upsert:true});
                console.log(`Soft deleted from DB`);
                return true;  
            }
            console.log(`Bookmark already deleted in DB`);
            return false;
        }
        catch(e){
            console.log("Problem in the DB: " + e);
            return false
        }        
    }
}

module.exports = new Bookmarks();
