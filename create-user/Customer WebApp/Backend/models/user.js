const mongoose = require("mongoose");

const UserSchema = mongoose.Schema({
    firstName:{
    type: String,
    required:true
    },

    lastName:{
        type: String
        },

    email:{
        type: String,
        required:true
    },

    password:{
        type: String,
        required:true
    },
    gender:{
        type: String,
        enum : ['Male','Female','Others'],     
        required:true
    },
    phone:{
        type: String,
        required:true
    },
    countryOfOrigin:{
        type: String,
        required:true
    },
    status:{
        type: Boolean
        },

    dateOfBirth:{
        type: Date,
        required:true
    },

},
{ collection: "users_col" }

)


const User = mongoose.model('User',UserSchema);    
class Users{
    
    constructor(){
        console.log('Users Constructor');
    }

//     // Fetch all active existing users 
//     async getAll() {
//         const result = await this.collection.find({"status":"Active"},
//             {projection:{"firstName":1,"lastName":1,"email":1,"gender":1,
//             "nationality":1,"dateOfBirth":1}
            
//         }).toArray();
//         return result;
//     }

    // Get specific user
    async get(email){
        try{
             var result = await User.findOne({email:email}) 
            return result;
        }
        catch(e){
            console.log("Problem in adding the user to DB: " + e);
            return e;
        }
    }
    
    // // Get active users by nationailty
    // async getUsersPerCountry(country) {
    //     const result = await Users.find({ "$and" :[{ "nationality" : country }, 
    //                                                 { "status" : "Active" }] 
    //                                             },
    //                                             {projection:{"firstName":1,"lastName":1,"email":1,"gender":1,
    //                                             "nationality":1,"dateOfBirth":1}
    //                                         }).toArray();
    //     return result;
    // }

    // Add a new user 
    async add(user){
        try{
            console.log("Adding new user");
            await User.create(user);
            return true;
        }
        catch(e){
            console.log("Problem in adding the user to DB: " + e);
            return false
        }
        
    }
}

module.exports = { 
    Users,
    User
 };
