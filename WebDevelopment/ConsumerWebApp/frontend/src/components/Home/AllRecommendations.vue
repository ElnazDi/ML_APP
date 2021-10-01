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
            <h2 class="ui dividing header">Products in demand</h2>
            <div class="ui cards" v-if="genericRecommendations.length > 0">
              <Product v-for="product in GenericRecommendationsPage" :key="product.title"
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
              <Pagination
                :context='"OverallRecommendations"'
                :fieldName='"None"'
                :length='genericRecommendations.length'
                :itemsPerPage='itemsPerPage'
                @pageChanged='pageChanged'/>

            </div>
          </div>
          <div class="row">
            <h2 class="ui dividing header">Products you might like to buy</h2>
            <div class="ui cards" v-if="cartHistoryRecommendations.length > 0">
              <Product v-for="product in CartHistoryRecommendationsPage" :key="product.title"
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
              <Pagination 
                :context='"CartHistoryRecommendations"'
                :fieldName='"None"'
                :length='cartHistoryRecommendations.length'
                :itemsPerPage='itemsPerPage'
                @pageChanged='pageChanged'/>
            </div>
          </div>
          <div class="row" >
            <h2 class="ui dividing header">Good value products</h2>
            <div class="ui cards" v-if="bookmarkRecommendations.length > 0">
              <Product v-for="product in BookmarkRecommendationsPage" :key="product.title"
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
              <Pagination 
                :context='"BookmarkRecommendations"'
                :fieldName='"None"'
                :length='bookmarkRecommendations.length'
                :itemsPerPage='itemsPerPage'
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
  name: 'AllRecommendations',
  created(){
    this.$store.dispatch('fetchCartHistoryRecommendedProducts');
    this.$store.dispatch('fetchGenericRecommendedProducts');
    this.$store.dispatch('fetchBookmarkRecommendedProducts');
    this.cartHistoryRecommendations = this.$store.getters.getCartHistoryRecommendedProducts;
    this.genericRecommendations = this.$store.getters.getGenericRecommendedProducts;
    this.bookmarkRecommendations = this.$store.getters.getBookmarkRecommendedProducts;
  },
  data() {
    return {
      itemsPerPage: 5,
      cartHistoryRecommendations: [],
      genericRecommendations: [],
      bookmarkRecommendations: [],
      pageOverall: 1,
      pageCartHistory: 1,
      pageBookmark: 1,
    }
  },
  components: {
    Product,
    Notification,
    FilterBar,
    Pagination,
  },
  computed: {
    CartHistoryRecommendationsPage(){
      return this.cartHistoryRecommendations.slice((this.pageCartHistory - 1) * this.itemsPerPage, this.pageCartHistory * this.itemsPerPage);
    },
    GenericRecommendationsPage(){
      return this.genericRecommendations.slice((this.pageOverall - 1) * this.itemsPerPage, this.pageOverall * this.itemsPerPage);
    },
    BookmarkRecommendationsPage(){
      return this.bookmarkRecommendations.slice((this.pageBookmark - 1) * this.itemsPerPage, this.pageBookmark * this.itemsPerPage);
    }
  },
  methods: {
    pageChanged(data) {
      if(data.context == 'OverallRecommendations')
        this.pageOverall = data.page;
      else if(data.context == 'CartHistoryRecommendations')
        this.pageCartHistory = data.page;
      else if(data.context == 'BookmarkRecommendations')
        this.pageBookmark = data.page;
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