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
            <h2 class="ui dividing header">Cart</h2>
          </div>
          <div class="row">
            <table class="ui fixed table" v-if="cartProductsByKaufland.length > 0">
              <thead>
                <tr>
                  <th colspan="9"><h3>Kaufland</h3></th>
                </tr>
                <tr>
                  <th class="center aligned"> Product name</th>
                  <th class="center aligned">Image</th>
                  <th class="right aligned"> UnitPrice x</th>
                  <th> Quantity</th>
                  <th>Increase</th>
                  <th>Reduce</th>
                  <th>Remove</th>
                  <th>Mark</th>
                  <th class="center aligned"> Total price</th>
                </tr>
              </thead>
              <tbody>
                <CartProduct v-for="product in displayCartProductsByKaufland" 
                  :key="product.id"
                  :productId="product.productId"
                  :title="product.title"
                  :quantity="product.quantity"
                  :unitPrice="product.price"
                  :totalPrice="Number.parseFloat(product.quantity * product.price).toFixed(2)"
                  :vendor="product.vendor"
                  :image="product.image"/>
              </tbody>
              <tr>
                <td colspan="8">
                  <Pagination
                    :context='"Cart"'
                    :fieldName='"kaufland"'
                    :length='cartProductsByKaufland.length'
                    :itemsPerPage='itemsPerPage'
                    @pageChanged='pageChanged'/>
                </td>
              </tr>
              <tr class="single line">
                <td colspan="8">
                  <h3 class="right aligned">Total</h3>
                </td>
                <td class="center aligned">
                  <span class="total-price">€ {{ totalPriceOfKauflandCart }} /-</span>
                </td>
              </tr>
            </table>

            <table class="ui fixed table" v-if="cartProductsByAldi.length > 0">
              <thead>
                <tr>
                  <th colspan="9"><h3>Aldi</h3></th>
                </tr>
                <tr>
                  <th class="center aligned"> Product name</th>
                  <th class="center aligned">Image</th>
                  <th class="right aligned"> UnitPrice x</th>
                  <th> Quantity</th>
                  <th>Increase</th>
                  <th>Reduce</th>
                  <th>Remove</th>
                  <th>Mark</th>
                  <th class="center aligned"> Total price</th>
                </tr>
              </thead>
              <tbody>
                <CartProduct v-for="product in displayCartProductsByAldi" 
                  :key="product.id"
                  :productId="product.productId"
                  :title="product.title"
                  :quantity="product.quantity"
                  :unitPrice="product.price"
                  :totalPrice="Number.parseFloat(product.quantity * product.price).toFixed(2)"
                  :vendor="product.vendor"
                  :image="product.image"/>
              </tbody>
              <tr>
                <td colspan="8">
                  <Pagination
                    :context='"Cart"'
                    :fieldName='"aldi"'
                    :length='cartProductsByAldi.length'
                    :itemsPerPage='itemsPerPage'
                    @pageChanged='pageChanged'/>
                </td>
              </tr>
              <tr class="single line">
                <td colspan="8">
                  <h3 class="right aligned">Total</h3>
                </td>
                <td class="center aligned">
                  <span class="total-price">€ {{ totalPriceOfAldiCart }} /-</span>
                </td>
              </tr>
            </table>

            <table class="ui fixed table" v-if="cartProductsByNetto.length > 0">
              <thead>
                <tr>
                  <th colspan="9"><h3>Netto</h3></th>
                </tr>
                <tr>
                  <th class="center aligned"> Product name</th>
                  <th class="center aligned">Image</th>
                  <th class="right aligned"> UnitPrice x</th>
                  <th> Quantity</th>
                  <th>Increase</th>
                  <th>Reduce</th>
                  <th>Remove</th>
                  <th>Mark</th>
                  <th class="center aligned"> Total price</th>
                </tr>
              </thead>
              <tbody>
                <CartProduct v-for="product in displayCartProductsByNetto" 
                  :key="product.id"
                  :productId="product.productId"
                  :title="product.title"
                  :quantity="product.quantity"
                  :unitPrice="product.price"
                  :totalPrice="Number.parseFloat(product.quantity * product.price).toFixed(2)"
                  :vendor="product.vendor"
                  :image="product.image"/>
              </tbody>
              <tr>
                <td colspan="8">
                  <Pagination
                    :context='"Cart"'
                    :fieldName='"netto"'
                    :length='cartProductsByNetto.length'
                    :itemsPerPage='itemsPerPage'
                    @pageChanged='pageChanged'/>
                </td>
              </tr>
              <tr class="single line">
                <td colspan="8">
                  <h3 class="right aligned">Total</h3>
                </td>
                <td class="center aligned">
                  <span class="total-price">€ {{ totalPriceOfNettoCart }} /-</span>
                </td>
              </tr>
            </table>

          </div>
          <div class="row">
            <div class="ui clearing segment">
              <h3 class="ui right floated header"><span class="total-price">Grand Total : &nbsp; € {{ totalPriceOfCart }} /-</span></h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilterBar from '../shared/filter/FilterBar.vue';
import CartProduct from '../shared/CartProduct.vue';
import Pagination from '../shared/Pagination.vue';

export default {
  name: 'AllCarts',
  created(){
    this.$store.dispatch('fetchListInCart');
  },
  components: {
    FilterBar,
    CartProduct,
    Pagination
  },
  data() {
    return {
      itemsPerPage: 3,
      page: {
        kaufland: 1,
        aldi: 1,
        netto: 1
      },
    }
  },
  computed: {
    cartProductsByKaufland(){
      let subset = this.$store.getters.displayCartProducts;
      subset = subset.filter(product => product.vendor.toLowerCase() == "kaufland")
      if(!this.$store.getters.getFilters['kaufland'])
        return []
      return subset;
    },
    cartProductsByAldi(){
      let subset = this.$store.getters.displayCartProducts;
      subset = subset.filter(product => product.vendor.toLowerCase() == "aldi")
      if(!this.$store.getters.getFilters['aldi'])
        return []
      return subset;
    },
    cartProductsByNetto(){
      let subset = this.$store.getters.displayCartProducts;
      subset = subset.filter(product => product.vendor.toLowerCase() == "netto")
      if(!this.$store.getters.getFilters['netto'])
        return []
      return subset;
    },
    displayCartProductsByKaufland(){
      let subset = this.cartProductsByKaufland;
      subset = subset.slice((this.page.kaufland - 1) * this.itemsPerPage, this.page.kaufland * this.itemsPerPage);
      return subset; 
    },
    displayCartProductsByAldi(){
      let subset = this.cartProductsByAldi;
      subset = subset.slice((this.page.aldi - 1) * this.itemsPerPage, this.page.aldi * this.itemsPerPage);
      return subset; 
    },
    displayCartProductsByNetto(){
      let subset = this.cartProductsByNetto;
      subset = subset.slice((this.page.netto - 1) * this.itemsPerPage, this.page.netto * this.itemsPerPage);
      return subset; 
    },
    totalPriceOfKauflandCart(){
      const subset = this.cartProductsByKaufland
      let price = 0;
      subset.forEach(product => price += (product.price * product.quantity))
      return Number.parseFloat(price).toFixed(2);
    },
    totalPriceOfAldiCart(){
      const subset = this.cartProductsByAldi
      let price = 0;
      subset.forEach(product => price += (product.price * product.quantity))
      return Number.parseFloat(price).toFixed(2);
    },
    totalPriceOfNettoCart(){
      const subset = this.cartProductsByNetto
      let price = 0;
      subset.forEach(product => price += (product.price * product.quantity))
      return Number.parseFloat(price).toFixed(2);
    },
    totalPriceOfCart() {
      const kaufland = Number(this.totalPriceOfKauflandCart)
      const aldi = Number(this.totalPriceOfAldiCart)
      const netto = Number(this.totalPriceOfNettoCart)
      return Number.parseFloat(kaufland + aldi + netto).toFixed(2);
    }
  },
  methods: {
    pageChanged(data) {
      if(data.context == "Cart" && data.field == "kaufland")
        this.page['kaufland'] = data.page;
      else if(data.context == "Cart" && data.field == "aldi")
        this.page['aldi'] = data.page;
      else if(data.context == "Cart" && data.field == "netto")
        this.page['netto'] = data.page;
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