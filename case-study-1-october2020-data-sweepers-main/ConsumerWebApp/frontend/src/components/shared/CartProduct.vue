<template>
  <tr>
    <td class="center aligned">
      <h3 class="ui center aligned header">{{ title }}</h3>
    </td>
    <td class="center aligned">
      <img :src="image" class="cart-image"/>
    </td>
    <td class="right aligned">
      <span class="unit-price">€ {{ unitPrice }}</span>&nbsp; x
    </td>
    <td>
      <span class="quantity">{{ quantity }}</span>
    </td>
    <td class="single line">
      <div class="field">
        <button class="ui icon basic blue button" @click="incrementProduct" title="Add product quantity">
          <i class="big blue plus square outline icon"></i>
        </button>              
      </div>
    </td>
    <td class="single line">
      <div class="field">
        <button :class="decrementClass" @click="decrementProduct" title="Reduce product quatity">
          <i class="big white minus square outline icon"></i>
        </button>
      </div>
    </td>
    <td class="single line">
      <div class="field">
        <button class="ui icon red basic button" @click="removeProduct" title="Remove product">
          <i class="big red times circle outline icon"></i>
        </button>
      </div>
    </td>
    <td class="single line">
      <div class="field">
        <button class="ui icon green basic button" @click="boughtProduct" title="Mark product as bought">
          <i class="big green check circle outline icon"></i>
        </button>
      </div>
    </td>
    <td class="single line center aligned">
      <span class="total-price">€ {{ totalPrice }}</span>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'CartProduct',
  props: {
    quantity: Number,
    unitPrice: Number,
    totalPrice: Number,
    title: String,
    vendor: String,
    productId: String,
    image: String,
  },
  methods: {
    incrementProduct(){
      this.$store.dispatch('incrementProductInCart', {
        productId: this.productId,
      })
    },
    decrementProduct(){
      this.$store.dispatch('decrementProductInCart', {
        productId: this.productId,
      })
    },
    removeProduct() {
      this.$store.dispatch('removeProductFromCart', {
        productId: this.productId,
      })
    },
    boughtProduct(){
      this.$store.dispatch('boughtProductInCart', {
        productId: this.productId,
      })
    },
  },
  computed: {
    decrementClass(){
      const buttonClass = ["ui", "icon", "basic", "orange", "button"]
      if (this.quantity == 1)
        buttonClass.push('disabled')
      return buttonClass
    }
  }
}
</script>

<style scoped>
.unit-price {
  font-weight: 500;
  font-size: 1.1em;
}
.quantity {
  font-size: 1.5em;
  font-style: italic;
}
.total-price {
  font-weight: 600;
  font-size: 1.5em;
}
.cart-image{
  height: 100px;
  width: auto;
  margin-left: auto;
  margin-right: auto;
}
</style>