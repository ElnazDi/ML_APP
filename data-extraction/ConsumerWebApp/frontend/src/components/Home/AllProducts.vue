<template>
  <div class="ui grid">
    <div class="row">
      <div class="three wide column">
        <div class="ui segment">
          <FilterBar/>
        </div>
      </div>
      <div class="thirteen wide column">  
        <div class="ui segment">
          <div class="row">
            <Notification />
          </div>
          <div class="row">
            <h2 class="ui dividing header">All Products</h2>
            <div class="ui fluid icon input">
              <i class="search icon"></i>
              <input type="text" placeholder="Search..." v-model="searchField">
            </div>
          </div>
          <div class="row">
            <div class="ui cards">
              <Product v-for="product in listOfProducts" :key="product.title"
                :id="product._id"
                :title="product.title"
                :brand="product.brand"
                :price="product.price"
                :quantity="product.quantity"
                :discount="product.discount"
                :image="product.image"
                :unitPrice="product.unitPrice"
                :unitPriceQuantity="product.unitPriceQuantity"
                :oldPrice="product.oldPrice"
                :vendor="product.vendor"
                :bookmarked="product.bookmarked"/>
            </div>
          </div>
          <div class="row">
            <div class="items">
              <div class="empty"></div>
              <Pagination 
                context='allProducts'
                :itemsPerPage='itemsPerPage'
                fieldName='page'
                :length='data.length'
                @pageChanged='pageChanged'/>
            </div>
          </div>
        </div>
      </div>
    </div>    
  </div>
</template>

<script>
import Product from '../shared/Product.vue';
import Notification from '../shared/Notification.vue';
import FilterBar from '../shared/filter/FilterBar.vue';
import Pagination from '../shared/Pagination.vue';

export default {
  name: 'AllProducts',
  created(){
    this.$store.commit('fetchDataFromLocalStorage', { name: 'allProducts' });
    this.$store.dispatch('fetchListOfProducts');
    this.data = this.$store.getters.getAllProducts;
    this.filter = this.$store.getters.getFilters;
  },
  data() {
    return {
      itemsPerPage: 5,
      data: [],
      page: 1,
      filter: {},
      searchField: ''
    }
  },
  components: {
    Product,
    Notification,
    FilterBar,
    Pagination,
  },
  computed: {
    listOfProducts(){
      let subset = this.data;
      console.log(this.data[0]);
      if(this.searchField != '')
        subset = subset.filter(product => product.title.includes(this.searchField));
      subset = subset.filter(product => this.filter[product.vendor.toLowerCase()] == true);
      return subset.slice((this.page - 1) * this.itemsPerPage, this.page * this.itemsPerPage);
    }
  },
  methods: {
    pageChanged(data) {
      if(data.context == 'allProducts')
        this.page = data.page;
    }
  }
}
</script>

<style>
.row{
  margin-bottom: 20px;
}
.items {
  display: flex;
}
.items > .empty {
  flex: 1;
}
.item > :not(.empty) {
  flex: 1;
}
</style>