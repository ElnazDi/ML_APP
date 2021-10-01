const mongoose = require("mongoose");
const ObjectId = require("mongodb").ObjectId;


/*
@Schema  Products
*/
const ProductSchema = mongoose.Schema(
    {
        detail_url: {
        type: String
      },
      image: {
        type: String
      },
      brand: {
        type: String
      },
      product_title: {
        type: String
      },
      content_quantity: {
        type: String
      },
      price_per_unit: {
        type: String
      },
      discount: {
        type: String
      },
      old_price: {
        type: String
      },
      current_price: {
        type: String
      },
      product_img_thumb: {
        type: String
      },
      product_description: {
        type: String
      },    
      product_properties: {
        type: String
      },    
      product_ingredients: {
        type: String
      },    
      product_instructions: {
        type: String
      },    
      product_hints: {
        type: String
      },    
      product_manufacturer: {
        type: String
      },    
      product_vendor: {
        type: String
      }
      /*,    
      status: {
        type: Boolean,
        default: true
      },
      insert_dt: {
        type: Date,
        default: Date.now,
      },
      update_dt: {
        type: Date,
        default: null,
      }
      */
    },
    { collection: "stg_product_col" }
);
  

const Product = mongoose.model("Product", ProductSchema);

/*
@Model   Products
*/
class Products{

    constructor(){
        console.log('Products Constructor');
        this.pageSize = 20;

    }

    // @desc:   Fetch all active products with discounts
    // @params: Page Size, Page Number
    // @return: Array of products, containing the basic information to display
    async getDiscounts(pageNum) {
        var skips = this.pageSize * (parseInt(pageNum) - 1);
        var result = await Product.find({discount:{$regex : ".*%.*"}},
            'detail_url image brand product_title content_quantity price_per_unit discount old_price current_price product_vendor'
        ).skip(skips).limit(this.pageSize);
        return result;
    }
    
    // @desc:   Fetch all active products for filter 'Kaufland'
    // @params: Page Number
    // @return: Array of products, containing the basic information to display
    async getKauflandProducts(pageNum) {
      var skips = this.pageSize * (parseInt(pageNum) - 1);
      var result = await Product.find({product_vendor:"Kaufland"},
          'detail_url image brand product_title content_quantity price_per_unit discount old_price current_price product_vendor'
      ).skip(skips).limit(this.pageSize);
      return result;
  }

  // @desc:   Fetch all active products for filter 'Netto'
  // @params: Page Number
  // @return: Array of products, containing the basic information to display

  async getNettoProducts(pageNum) {
    var skips = this.pageSize * (parseInt(pageNum) - 1);
    var result = await Product.find({product_vendor:"Netto"},
        'detail_url image brand product_title content_quantity price_per_unit discount old_price current_price product_vendor'
    ).skip(skips).limit(this.pageSize);
    return result;
}


    // @desc:   Fetch all active products for all the vendors
    // @params: Page Size, Page Number
    // @return: Array of products, containing the basic information to display
    async getAll(pageNum,queryParam) {
        var skips = this.pageSize * (parseInt(pageNum) - 1);
      if (queryParam != " "){
        ProductSchema.index({'$**': 'text'});
        const result = await Product.find({$text: {$search: queryParam}},
          'detail_url image brand product_title content_quantity price_per_unit discount old_price current_price product_vendor'
      ).skip(skips).limit(this.pageSize);
      return result;

      }else{
        const result = await Product.find({},
          'detail_url image brand product_title content_quantity price_per_unit discount old_price current_price product_vendor'
            ).skip(skips).limit(this.pageSize);
              return result;

          }
    }

    // @desc:   Fetch single products to see its detailed information
    // @params: product Id
    // @return: Single products with all its details
    async get(productId) {
        const result = await Product.findOne({"_id": ObjectId(productId)});
        return result;
    }
}

module.exports = new Products();
