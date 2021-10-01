const mongoose = require("mongoose");
//const MongoBot = require('./mongo');
const ObjectId = require("mongodb").ObjectId;

/*
@Schema  Carts
*/
const CartSchema = mongoose.Schema(
  {
    cartName: {
      type: String,
      require: true,
    },
    userId: {
      type: String,
      require: true,
    },
    status: {
      type: Boolean,
      default: true,
    },
    insert_dt: {
      type: Date,
      default: Date.now,
    },
    update_dt: {
      type: Date,
      default: null,
    },
    products: [{ qty: Number, productId: String }],
  },
  { collection: "carts_col" }
);

/*
@Model   Carts
*/
const Cart = mongoose.model("Cart", CartSchema);

class Carts {
  constructor() {
    console.log("Carts Constructor");
  }

  // @desc:   Fetch all active existing carts from a particular user
  // @params: user Id
  // @return: Array of carts, containing the products for each one
  async getAll(userId) {
    var result = await Cart.find({ status: true, userId : userId },'cartName products');
    return result;
  }

  // @desc:   Fetch all active existing carts from a particular user
  // @params: user Id, cart name
  // @return: Cart object containing all its products
  async getCart(userId, cartName) {
    var result = await Cart.findOne({userId : userId, cartName: cartName },'CartName products');
    return result;
  }

  // @desc:   Add a new cart for a particular user
  // @params: user Id, cart name
  // @return: flag indicating db operation
  async add(userId, cartName) {
    try {
      const cart = new Cart({
        cartName: cartName,
        userId: userId
      });
      // Validate if cart name already exists
      var validate = await Cart.findOne({userId : userId, cartName: cartName },'CartName products status');
      if(validate === null){
        console.log('Add cart');
        await cart.save()
        return 1;
      }
      else{
        console.log('Update cart')
        cart.status = !validate.status;
        cart.update_dt = Date.now();
        await cart.save();
        return 0;
      }
      
    } catch (e) {
      console.log("Problem in the DB: " + e);
      return -1;
    }
  }

  // @desc:   Delete a cart for a particular user
  // @params: user Id, cart name
  // @return: flag indicating db operation
  async delete(userId, cartName) {
    try{
      //Validate if cart is deleted already
      var validate = await Cart.findOne({userId : userId, cartName: cartName, status:false },'cartName products');
      if(validate == null){
        await Cart.updateOne({userId : userId, cartName: cartName }, {status:false, update_dt: Date.now() },{upsert:true});
        console.log(`Soft deleted from DB`);
        return true;  
      }
      console.log(`Cart already deleted in DB`);
      return true;
    }      
    catch(e){
      console.log("Problem in the DB: " + e);
      return false;
    }
  }

  // @desc:   Add a new product in a specific cart for a particular user
  // @params: user Id, cart name, product Id, qnt
  // @return: flag indicating db operation
  async addProduct(userId, cartName, productId, qty) {
    try {
      const product = {
        qty: qty,
        productId: productId
      };
      // Validate if cart name already exists
      var cart = await Cart.findOne({userId : userId, cartName: cartName},'cartName status products');
      // Check if product already exists in current cart
      const result = cart.products.find( product => product.productId === productId );
      if(result === undefined){
        cart.products.push(product);
        cart.update_dt = Date.now()
        await cart.save();
        console.log('Product added to cart')
        return 1;
      }
      console.log('Product already added to cart');
      return 0;
      
    } catch (e) {
      console.log("Problem in the DB: " + e);
      return -1;
    }
  }



  // @desc:   Delete a product from a cart for a particular user
  // @params: user Id, cart name, product Id
  // @return: flag indicating db operation
  async deleteProduct(userId, cartName, productId) {
    try{
      // Validate if cart name already exists
      var cart = await Cart.findOne({userId : userId, cartName: cartName},'cartName status products');
      // Check if product already exists in current cart
      var index = cart.products.findIndex(product => product.productId === productId);
      // Remove product
      if(index > -1){
        cart.products.splice(index,1);
        await cart.save();
      }
      return true;
    }      
    catch(e){
      console.log("Problem in the DB: " + e);
      return false;
    }
  }

}

module.exports = new Carts();
