<template>
  <div class="row card" style="background-color:rgba(255, 255, 255, 0.726); ">
    <!-- Card Header -->
    <!-- @detail_url -->
    <!-- <a href="#"> -->
      <div class="row card-header">
        <div class="col-10" >
          <!-- @product_title -->
          <h4>{{ title }}</h4>
        </div>
        <div class="col-2">
          <!-- @bookmark -->
          <i class="far fa-bookmark"></i>
          <i class="fas fa-bookmark"></i>
        </div>
      </div>
      <!-- Image -->
      <div class="row">
        <img class="card-img-top img-product"
        :src="image"
        alt="Card image">
      </div>
      <!-- Product information -->
      <div class="row card-body">
          <!-- left column -->
          <div class="col-6">
            <div class="row panel">
              <!-- @current_price -->
              <span class="text">Price:</span>
              <strong class="value">{{ price }}</strong>
            </div>
            <div class="row panel">
              <!-- @discount -->
              <span class="text">Discount: </span>
              <strong class="value">{{ discount }}</strong>
            </div>
            <div class="row panel">
              <!-- @old_price -->
              <span class="text">Old Price: </span>
              <strong class="value">{{ oldPrice }}</strong>
            </div>
            <div class="row panel">
              <!-- @price_per_unit -->
              <span class="text">Content: </span>
              <strong class="value">{{ content }}</strong>
            </div>
            <div class="row panel">
              <!-- @content_quantity -->
              <span class="text">Quantity: </span>
              <strong class="value">{{ quantity }}</strong>
            </div>
          </div>
          <!-- right column -->
          <div class="col-6">
            <div class="row panel">
              <!-- @brand -->
              <span class="text">Brand: </span>
              <strong class="value">{{ brand }}</strong>
            </div>
            <div class="row panel">
              <!-- @product_vendor -->
              <span class="text">Vendor: </span>
              <strong class="value">{{ vendor }}</strong>
            </div>
          </div>
      </div>
    <!-- </a> -->
      <!-- Footer -->
      <div class="row divider">
          <div class="col-6">
            <input class="input-qty" type="number" id="qty" value="1"
              placeholder="1" name="qty" min="1" max="10">
          </div>
          <div class="col-6">
            <div class="dropdown">
              <button class="btn btn-secondary dropdown-toggle"
              type="button" id="dropdownMenuButton"
              data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Add to Cart
              </button>
              <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <a class="dropdown-item" href="#">Default Cart</a>
              </div>
            </div>
          </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'ProductCard',
  props: {
    title: String,
    image: String,
    price: String,
    discount: String,
    oldPrice: String,
    content: String,
    quantity: String,
    brand: String,
    vendor: String,
  },
};
</script>

<style scoped>
</style>
