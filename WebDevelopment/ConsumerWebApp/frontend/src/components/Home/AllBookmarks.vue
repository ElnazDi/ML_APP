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
            <h2 class="ui dividing header">Bookmarked Products</h2>
          </div>
          <div class="row">
            <Notification/>
          </div>
          <div class="row">
            <div class="ui cards">
              <Product v-for="product in displayBookmarkedProducts" :key="product.title"
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
            <Pagination 
              :context='"Bookmarks"'
              :fieldName='"none"'
              :length='bookmarkedProducts.length'
              :itemsPerPage='itemsPerPage'
              @pageChanged='pageChanged'/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilterBar from '../shared/filter/FilterBar.vue';
import Notification from '../shared/Notification.vue';
import Product from '../shared/Product.vue';
import Pagination from '../shared/Pagination.vue';

export default {
  name: 'AllBookmarks',
  created() {
    this.$store.dispatch('fetchBookmarkedProducts');
  },
  components: {
    FilterBar,
    Notification,
    Product,
    Pagination,
  },
  data(){
    return {
      page: 1,
      itemsPerPage: 10
    }
  },
  computed: {
    bookmarkedProducts(){
      return this.$store.getters.displayBookmarkedProducts;
    },
    displayBookmarkedProducts(){
      let subset = this.$store.getters.displayBookmarkedProducts;
      subset = subset.slice((this.page - 1) * this.itemsPerPage, this.page * this.itemsPerPage);
      return subset;
    }
  },
  methods: {
    pageChanged(data){
      this.page = data.page;
    }
  }
}
</script>