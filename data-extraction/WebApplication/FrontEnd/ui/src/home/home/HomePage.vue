<template>
  <div class="home">
    <NavBar :authenticated='true'/>
    <div class="row">
      <div class="col-sm-2" style="align-items: center;">
        <FilterBar/>
      </div>
      <div class="col-sm-10">
        <div class="row">
          <!-- Search bar and notification -->
          <Notification/>
        </div>
        <div class="row">
          <SearchBar/>
        </div>
        <div class="row">
          <div class="container">
            <ProductList/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilterBar from '../../shared/filter/FilterBar.vue';
import ProductList from '../products/ProductList.vue';
import NavBar from '../../shared/navbar/NavBar.vue';
import Notification from '../../shared/notification/Notification.vue';
import SearchBar from '../../shared/search/SearchBar.vue';

export default {
  name: 'HomePage',
  components: {
    FilterBar,
    ProductList,
    NavBar,
    Notification,
    SearchBar,
  },
};
</script>

<style scoped>

</style>
