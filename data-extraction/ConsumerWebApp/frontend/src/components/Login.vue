<template>
  <div>
    <PreAuthNavBar/>
    <div class="ui segment login">
      <h1>Login</h1>
      <Notification />
      <form class="ui form" v-on:submit.prevent>
        <div class="field">
          <label>Username</label>
          <input type="text" name="username" placeholder="Username" v-model="username">
        </div>
        <div class="field">
          <label>Password</label>
          <input type="password" name="password" placeholder="Password" v-model="password">
        </div>
        <div class="field">
          <div class="ui checkbox">
            <input type="checkbox" v-model="terms"/>
            <label>I agree to the Terms and Conditions</label>
          </div>
        </div>
        <button class="ui button" @click="login">Sign In</button>
        <button class="ui button" @click="goToRegister">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
import PreAuthNavBar from './shared/PreAuthNavBar.vue';
import Notification from './shared/Notification.vue';

export default {
  name: 'Login',
  created(){
    this.$store.commit('hideNotification');
  },
  data() {
    return {
      username: '',
      password: '',
      terms: false,
    };
  },
  components: {
    PreAuthNavBar,
    Notification,
  },
  methods: {
    login() {
      this.$store.dispatch('login', {
        username: this.username,
        password: this.password
      });      
    },
    goToRegister() {
      this.$store.commit('showRegister');
    }
  }
}  
</script>

<style scoped>
.login {
  margin: 5% auto;
  padding: 3%;
  border-radius: 5%;
  width: 40%;
}
.login h1 {
  text-align: center;
}
</style>