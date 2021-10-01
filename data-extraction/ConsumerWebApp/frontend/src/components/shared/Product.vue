<template>
  <div class="ui card">
    <div class="image product-image-div">
      <img class="product-image-img" :src="image"/>
    </div>
    <div class="content">
      <div class="right floated meta" v-if="Number(discount)">{{ discount }}<i class="percent icon"></i></div>
      <div class="header" href="#">{{ title }}</div> 
      <div class="description">
        <p>Brand: {{ brand }}</p>
        <p>Vendor: {{ vendor }}</p>
        <p>Price: {{ price }}</p>
        <p>Quantity: {{ quantity }}</p>
        <p>Unit Price: {{ unitPrice + ' / ' + unitPriceQuantity }}</p>
        <p>Old Price: {{ oldPrice }}</p>
      </div>
    </div>
    <div class="extra content">
      <div class="ui two icon buttons">
        <div class="ui icon basic button" title="Add to cart" @click="addToCart">
          <i class="blue cart plus icon"></i>
        </div>
        <div class="ui icon basic button" title="Add to bookmark" @click="bookmarkProduct">
          <i class="green bookmark outline icon" v-if="!bookmarked"></i>
          <i class="green bookmark icon" v-if="bookmarked"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Product',
  props: {
    id: String,
    title: String,
    image: String,
    brand: String,
    price: Number,
    quantity: String,
    unitPrice: Number,
    unitPriceQuantity: String,
    oldPrice: Number,
    discount: Number,
    vendor: String,
    bookmarked: Boolean,
  },
  methods: {
    addToCart() {
      this.$store.dispatch('incrementProductInCart', {
        productId: this.id,
      });
    },
    bookmarkProduct() {
      if(this.bookmarked)
        this.$store.dispatch('unbookmarkProduct', {
          id: this.id,
        });
      else
        this.$store.dispatch('bookmarkProduct', {
          id: this.id,
        });
    }
  }
}
</script>

<style scoped>
.ui.card > .image:not(.ui) > img, .ui.cards > .card > .image:not(.ui) > img {
  height: 200px;
  width: auto;
  margin-left: auto;
  margin-right: auto;
}
</style>