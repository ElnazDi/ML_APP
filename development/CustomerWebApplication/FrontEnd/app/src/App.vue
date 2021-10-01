<template>
  <div>
    <login v-if="!loggedIn"/>
    <home v-if="loggedIn"/>
  </div>
</template>

<script>
import Login from './components/Login/Page.vue'
import Home from './components/Home/Page.vue'

export default {
  name: 'App',
  components: {
    Login,
    Home
  },
  data(){
    return {
      loggedIn: false
    }
  }
}
</script>

<style></style>
