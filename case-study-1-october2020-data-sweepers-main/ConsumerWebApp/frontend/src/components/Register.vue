<template>
  <div>
    <PreAuthNavBar/>
    <div class="ui segment register">
      <h1>Register</h1>
      <Notification />
      <form class="ui form" v-on:submit.prevent>
        <div class="field">
          <label>Username</label>
          <input type="text" name="username" placeholder="Username" v-model="username" required>
        </div>
        <div class="field">
          <label>Password</label>
          <input type="password" name="password" placeholder="Password" v-model="password" required>
        </div>
        <div class="field">
          <label>Re-enter Password</label>
          <input type="password" name="password" placeholder="Re-enter Password" v-model="password2" required>
        </div>
        <div class="field">
          <label for="gender">Gender</label>
          <select class="ui dropdown">
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="field">
          <label for="phone">Phone</label>
          <input type="text" placeholder="Enter phone number" v-model="phone"/>
        </div>
        <div class="field">
          <label for="email">Email</label>
          <input type="email" placeholder="Enter email id" v-model="email"/>
        </div>
        <div class="field">
          <label for="country">Country</label>
          <input type="text" placeholder="Enter country of origin" v-model="country"/>
        </div>
        <div class="field">
          <label for="dob">Date of Birth</label>
          <input type="date" v-model="dob"/>
        </div>
        <div class="field">
          <div class="ui checkbox">
            <input type="checkbox" v-model="terms">
            <label>I agree to the Terms and Conditions</label>
          </div>
        </div>
        <button class="ui button" @click="register">Sign Up</button>
        <button class="ui button" @click="() => this.$store.commit('showLogin')">Login</button>
      </form>
    </div>
  </div>  
</template>

<script>
import PreAuthNavBar from './shared/PreAuthNavBar.vue';
import Notification from './shared/Notification.vue';

export default {
  name: 'Register',
  props: {
    displayRegister: Boolean,
  },
  created(){
    this.$store.commit('hideNotification');
  },
  data() {
    return {
      username: '',
      password: '',
      password2: '',
      gender: '',
      phone: '',
      country: '',
      email: '',
      dob: '',
      terms: false,
    }
  },
  components: {
    PreAuthNavBar,
    Notification,
  }, 
  methods: {
    register() {
      if(this.password !== this.password2){
        this.$store.commit('displayNotification', {
          type: 'error',
          message: 'Passwords don\'t match',
        });
      } else if (this.password.length < 8) {
        this.$store.commit('displayNotification', {
          type: 'error',
          message: 'Password must be minimum 8 characters long',
        });
      } else {
        this.$store.dispatch('register', {
          username: this.username,
          password: this.password,
          password2: this.password2,
          gender: this.gender,
          phone: this.phone,
          email: this.email,
          country: this.country,
          dob: this.dob
        })
      }
    }
  }
}
</script>

<style scoped>
.register{
  margin: 5% auto;
  padding: 3%;
  border-radius: 5%;
  width: 40%;
}
.register h1 {
  text-align: center;
}
</style>