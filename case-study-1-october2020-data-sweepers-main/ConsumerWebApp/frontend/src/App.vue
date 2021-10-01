<template>
  <div id="app">
    <Login v-if="!loggedIn && displayLogin"/>
    <Register v-if="!loggedIn && !displayLogin"/>
    <Home v-if="loggedIn"/>
  </div>
</template>

<script>
import Login from './components/Login.vue';
import Register from './components/Register.vue';
import Home from './components/Home.vue';

export default {
  name: 'App',
  created(){
    this.$store.commit('fetchCredFromLocalStorage');
  },
  components: {
    Login,
    Register,
    Home,
  }, 
  computed: {
    loggedIn(){
      return this.$store.state.auth.loggedIn;
    },
    displayLogin(){
      return this.$store.state.auth.displayLogin;
    }
  },
  beforeDestory(){
    this.$store.commit('saveCredToLocalStorage');
  }
}
</script>
