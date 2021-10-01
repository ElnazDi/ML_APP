<template>
  <div class="products">
    <div v-for="product in this.listOfProducts" :key="product.title">
      <ProductCard
        :title="product.product_title"
        :image="product.image"
        :brand="product.brand"
        :price="product.current_price"
        :oldPrice="product.old_price"
        :vendor="product.product_vendor"
        :content="product.price_per_unit"
        :quantity="product.content_quantity"
        :discount="product.discount"/>
    </div>
  </div>
</template>

<script>
import ProductCard from './ProductCard.vue';

export default {
  name: 'ProductList',
  created() {
    this.$store.dispatch('fetchListOfProducts');
  },
  components: {
    ProductCard,
  },
  data() {
    return {
      vendorFilter: this.$store.state.vendorFilter,
      display_products: [],
    };
  },
  watch: {
    listOfProducts() {
      console.log('Executing computed');
      const { products } = this.$store.state;
      this.display_products = products;
      products.filter((product) => this.vendorFilter.includes(product.product_vendor));
      return this.display_products;
    },
  },
};
</script>

<style scoped>

</style>
