() => {
                
  var results = []
  var items = document.getElementsByClassName('item')
  
  // iterate over the whole list of items on the webpage
  results = items.map((item) => {
      var data = {}      
      // Get Product Details
      data['product_details'] = item.querySelector('a')[0] ? item.querySelector('a')[0].href : ''
      // Get Product Title
      data['product_title'] = item.querySelector('.product__title')[0] ? item.querySelector('.product__title')[0].innerText : ''      
      // Get Product Labels
      data['product_label'] = item.querySelector('.product-labels')[0] ? item.querySelector('.product-labels')[0].innerText : ''
      // Get Image src
      data['product_image'] = item.querySelector('img')[0] ? item.querySelector('img')[0].src : ''
      // Get Product Rating
      data['product_rating'] = item.querySelector('_rating')[0] ? item.querySelector('_rating')[0].getAttribute("data-rating") : ''      
      // Get Product Price
      data['product_price'] = item.querySelector('.price')[0] ? item.querySelector('.price')[0].innerText : ''
      // Get Product Base Price
      data['product_base_price'] = item.querySelector('.product__base-price')[0] ? item.querySelector('.product__base-price')[0].getElementsByTagName("span")[0].innerText : ''      
      // Get Product Informationlink
      data['product_information'] = item.querySelector('.product__delivery-info')[0] ? item.querySelector('.product__delivery-info')[0].innerText : ''
      // Get Product Category                        
      data['product_category'] = /***0***/
      // Get Product Subcategory                        
      data['product_subcategory'] = /***1***/
      // Get Product Ingredients
      data['product_ingredients'] = ''
      // Get Product Brand/seller
      data['product_brand'] = ''
      // Get Product Discount
      data['product_discount'] = ''      
      // Set Product Vendor
      data['product_vendor'] = /***2***/
      // Set Extraction Date
      data['product_insert_dt'] = /***3***/
      return data
   });
  
  return results
}