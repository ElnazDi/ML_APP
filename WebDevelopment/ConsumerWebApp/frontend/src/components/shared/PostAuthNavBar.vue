<template>
  <div class="ui inverted segment">
    <div class="ui inverted pointing grey menu">
      <a :class="homeClass" @click="() => goto('home')">
        <i class="shopping basket icon"></i>
        ShopSmart
        <i class="mouse pointer icon"></i>
      </a>
      <a :class="recommendationClass" @click="() => goto('recommendations')">
        Recommendations &nbsp;
        <i class="clock icon"></i>
      </a>
      <a :class="cartClass" @click="() => goto('cart')">
        Cart &nbsp;
        <i class="shopping cart icon"></i>
      </a>
      <a :class="cartHistoryClass" @click="() => goto('cartHistory')">
        History &nbsp;
        <i class="history icon"></i>
      </a>
      <a :class="bookmarkClass" @click="() => goto('bookmark')">
        Bookmark &nbsp;
        <i class="bookmark icon"></i>
      </a>
      <div class="right menu">
        <a class="ui item" @click="() => goto('logout')">
          Logout &nbsp;
          <i class="sign-out icon"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostAuthNavBar',
  props: {
    active: String,
  },
  computed: {
    homeClass() {
      if(this.active === 'home')
        return ['item', 'home', 'active']
      return ['item', 'home'];
    },
    recommendationClass() {
      if(this.active === 'recommendations')
        return ['item', 'active']
      return ['item']
    },
    cartClass() {
      if(this.active === 'cart')
        return ['item', 'active']
      return ['item'];
    },
    cartHistoryClass() {
      if(this.active === 'cartHistory')
        return ['item', 'active']
      return ['item'];
    },
    bookmarkClass() {
      if(this.active === 'bookmark')
        return ['item', 'active']
      return ['item'];
    }
  },
  methods: {
    goto(tab){
      this.$emit('goto', tab);
    }
  }
}
</script>

<style>
.home {
  font-size: 115%;
  font-style: italic;
}
</style>