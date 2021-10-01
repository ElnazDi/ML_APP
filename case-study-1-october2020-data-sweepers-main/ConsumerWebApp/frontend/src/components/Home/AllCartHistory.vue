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
            <h2 class="ui dividing header">Purchase history</h2>
          </div>
          <div class="row">
            <table class="ui fixed table" v-if="kauflandCartHistoryProducts.length > 0">
              <thead>
                <tr>
                  <th colspan="7"><h3>Kaufland</h3></th>
                </tr>
                <tr>
                  <th class="center aligned"> Product name</th>
                  <th class="center aligned">Image</th>
                  <th class="right aligned"> UnitPrice x</th>
                  <th> Quantity</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th class="center aligned"> Total price</th>
                </tr>
              </thead>
              <tbody>
                <CartHistoryProduct v-for="product in displayKauflandCartHistoryProducts" 
                  :key="product.id"
                  :productId="product.productId"
                  :title="product.title"
                  :quantity="product.quantity"
                  :unitPrice="product.price"
                  :totalPrice="product.totalPrice"
                  :deleted="product.deleted"
                  :dateChanged="product.date"
                  :vendor="product.vendor"
                  :image="product.image"/>
                <tr>
                  <td colspan="7">
                    <Pagination 
                      :context='"CartHistory"'
                      :fieldName='"kaufland"'
                      :length='kauflandCartHistoryProducts.length'
                      :itemsPerPage='itemsPerPage'
                      @pageChanged='pageChanged'/>
                  </td>
                </tr>
              </tbody>
            </table>

            <table class="ui fixed table" v-if="aldiCartHistoryProducts.length > 0">
              <thead>
                <tr>
                  <th colspan="7"><h3>Aldi</h3></th>
                </tr>
                <tr>
                  <th class="center aligned"> Product name</th>
                  <th class="center aligned">Image</th>
                  <th class="right aligned"> UnitPrice x</th>
                  <th> Quantity</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th class="center aligned"> Total price</th>
                </tr>
              </thead>
              <tbody>
                <CartHistoryProduct v-for="product in displayAldiCartHistoryProducts" 
                  :key="product.id"
                  :productId="product.productId"
                  :title="product.title"
                  :quantity="product.quantity"
                  :unitPrice="product.price"
                  :totalPrice="product.totalPrice"
                  :deleted="product.deleted"
                  :dateChanged="product.date"
                  :vendor="product.vendor"
                  :image="product.image"/>
                <tr>
                  <td colspan="7">
                    <Pagination 
                      :context='"CartHistory"'
                      :fieldName='"aldi"'
                      :length='aldiCartHistoryProducts.length'
                      :itemsPerPage='itemsPerPage'
                      @pageChanged='pageChanged'/>
                  </td>
                </tr>
              </tbody>
            </table>

            <table class="ui fixed table" v-if="nettoCartHistoryProducts.length > 0">
              <thead>
                <tr>
                  <th colspan="7"><h3>Netto</h3></th>
                </tr>
                <tr>
                  <th class="center aligned"> Product name</th>
                  <th class="center aligned">Image</th>
                  <th class="right aligned"> UnitPrice x</th>
                  <th> Quantity</th>
                  <th>Status</th>
                  <th>Date</th>
                  <th class="center aligned"> Total price</th>
                </tr>
              </thead>
              <tbody>
                <CartHistoryProduct v-for="product in displayNettoCartHistoryProducts" 
                  :key="product.id"
                  :productId="product.productId"
                  :title="product.title"
                  :quantity="product.quantity"
                  :unitPrice="product.price"
                  :totalPrice="product.totalPrice"
                  :deleted="product.deleted"
                  :dateChanged="product.date"
                  :vendor="product.vendor"
                  :image="product.image"/>
                <tr>
                  <td colspan="7">
                    <Pagination 
                      :context='"CartHistory"'
                      :fieldName='"netto"'
                      :length='nettoCartHistoryProducts.length'
                      :itemsPerPage='itemsPerPage'
                      @pageChanged='pageChanged'/>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilterBar from '../shared/filter/FilterBar.vue';
import CartHistoryProduct from '../shared/CartHistoryProduct.vue';
import Pagination from '../shared/Pagination.vue';

export default {
  name: 'AllCartHistory',
  created(){
    this.$store.dispatch('fetchListInCartHistory');
    // this.data = this.$store.getters.displayCartHistoryProductsByVendor
  },
  data() {
    return {
      itemsPerPage: 3,
      data: [],
      page: {
        kaufland: 1,
        aldi: 1,
        netto: 1
      },
    }
  },
  components: {
    FilterBar,
    CartHistoryProduct,
    Pagination,
  },
  computed: {
    kauflandCartHistoryProducts(){
      let subset = this.$store.getters.getCartHistoryProducts;
      console.log(subset);
      if(!this.$store.getters.getFilters['kaufland'])
        return []
      subset = subset.filter(product => product.vendor.toLowerCase() == 'kaufland')
      return subset;
    },
    aldiCartHistoryProducts(){
      let subset = this.$store.getters.getCartHistoryProducts;
      if(!this.$store.getters.getFilters['aldi'])
        return []
      subset = subset.filter(product => product.vendor.toLowerCase() == 'aldi')
      return subset;
    },
    nettoCartHistoryProducts(){
      let subset = this.$store.getters.getCartHistoryProducts;
      if(!this.$store.getters.getFilters['netto'])
        return []
      subset = subset.filter(product => product.vendor.toLowerCase() == 'netto')
      return subset;
    },
    displayKauflandCartHistoryProducts(){
      let subset = this.kauflandCartHistoryProducts;
      subset = subset.slice((this.page.kaufland - 1) * this.itemsPerPage, this.page.kaufland * this.itemsPerPage)
      return subset;
    },
    displayAldiCartHistoryProducts(){
      let subset = this.aldiCartHistoryProducts;
      subset = subset.slice((this.page.aldi - 1) * this.itemsPerPage, this.page.aldi * this.itemsPerPage)
      return subset;
    },
    displayNettoCartHistoryProducts(){
      let subset = this.nettoCartHistoryProducts;
      subset = subset.slice((this.page.netto - 1) * this.itemsPerPage, this.page.netto * this.itemsPerPage)
      return subset;
    },
  },
  methods: {
    pageChanged(data) {
      if(data.context == "CartHistory")
        this.page[data.field] = data.page;
      console.log(this.page)
      console.log(data);
    }
  }
}
</script>

<style scoped>
.total-price {
  font-weight: 700;
  font-size: 1.6em;
  font-style: italic;
}
.ui.clearing.segment > .header {
  margin-right: 1%;
}
</style>