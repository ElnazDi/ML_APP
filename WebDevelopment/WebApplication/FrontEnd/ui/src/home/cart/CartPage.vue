<template>
  <div class="cart">
    <NavBar authenticated='true'/>
    <div class="page">
      <div class="col-sm-3" style="padding-left: 7%; align-items: center;">
        <FilterBar/>
      </div>
      <div class="col-sm-9">
        <div class="container">
          <ProductList/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProductList from '../products/ProductList.vue';
import NavBar from '../../shared/navbar/NavBar.vue';
import FilterBar from '../../shared/filter/FilterBar.vue';

export default {
  name: 'CartPage',
  components: {
    FilterBar,
    ProductList,
    NavBar,
  },
  props: {
    brandName: String,
  },
};
</script>

<style scoped>

</style>
