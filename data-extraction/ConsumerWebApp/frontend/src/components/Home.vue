<template>
  <div>
    <PostAuthNavBar 
      @goto="gotoTab"
      :active="activeTab"/>
    <div class="content-value">
      <AllProducts v-if="activeTab == 'home'"/>
      <AllCarts v-if="activeTab == 'cart'"/>
      <AllCartHistory v-if="activeTab == 'cartHistory'"/>
      <AllBookmarks v-if="activeTab == 'bookmark'"/>
      <AllRecommendations v-if="activeTab == 'recommendations'"/>
    </div>
  </div>
</template>

<script>
import PostAuthNavBar from './shared/PostAuthNavBar.vue';
import AllProducts from './Home/AllProducts.vue';
import AllCarts from './Home/AllCarts.vue';
import AllCartHistory from './Home/AllCartHistory.vue';
import AllBookmarks from './Home/AllBookmarks.vue';
import AllRecommendations from './Home/AllRecommendations.vue';

export default {
  name: 'Home',
  components: {
    PostAuthNavBar,
    AllProducts,
    AllCarts,
    AllCartHistory,
    AllBookmarks,
    AllRecommendations,
  },
  created(){
    this.$store.commit('hideNotification');
  },
  data() {
    return {
      activeTab: 'home',
    }
  },
  methods: {
    gotoTab(tab) {
      if(tab === 'logout')
        this.$store.commit('logoutUser');
      this.activeTab = tab;
    }
  }
}  
</script>

<style scoped>
  .content-value {
    margin-top: 30px;
  }
</style>