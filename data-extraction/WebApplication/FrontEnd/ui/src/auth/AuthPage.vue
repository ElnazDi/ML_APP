<template>
  <div class="auth">
    <NavBar :brandName='brandName'/>
    <div class="auth-inner">
      <Notification/>
      <SignIn v-if="showLogin"/>
      <SignUp v-if="!showLogin"/>
    </div>
  </div>
</template>

<script>
import NavBar from '../shared/navbar/NavBar.vue';
import SignIn from './login/SignIn.vue';
import SignUp from './register/SignUp.vue';
import Notification from '../shared/notification/Notification.vue';

export default {
  name: 'AuthPage',
  components: {
    NavBar,
    Notification,
    SignIn,
    SignUp,
  },
  computed: {
    showLogin() {
      return this.$store.state.showLogin;
    },
  },
};
</script>

<style scoped>

</style>
