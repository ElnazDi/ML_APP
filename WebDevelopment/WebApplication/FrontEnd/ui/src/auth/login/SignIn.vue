<template>
  <div class="container-fluid">
    <div class="row d-flex justify-content-center" style="margin-bottom: 8%; margin-top: 7%;">
      <div class="col-md-4 col-md-offset-4 col-sm-6 col-sm-offset-3 backsecond">
        <div class="backcolor">

          <h3 Style="color:#43d36e;">Log In</h3>

            <div class="col-md-12 col-sm-12 textup" style="padding-top: 0%;">
                <label for="username" style="color: aliceblue;">Username:</label>
                <input type="email" class="form-control" placeholder="Username"
                v-model="username" style="color: black;" id="username" required>
            </div>

            <div class="col-md-12 col-sm-12 textup" style="padding-top: 0%;">
                <label for="password" style="color: aliceblue;">Password:</label>
                <input type="password" class="form-control" placeholder="Password"
                v-model="password" style="color: black;" id="password" required>
            </div>

            <div class="col-md-12 col-sm-12 textup">
                <a href="#"><button type="btn" class="btn-signup form-control"
                  @click="login">
                  Sign In</button></a><br>
                <p align="center" style="font-size:13px; color:white;">Don't Have a Account ?
                <a href="#" @click="displayRegister"
                  style="color:#43d36e;; font-weight:bold;">Sign Up</a></p>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignIn',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    displayRegister() {
      this.$store.commit('displayLogin', false);
    },
    login() {
      console.log(this.username);
      console.log(this.password);
      this.$store.commit('login', {
        username: this.username,
        password: this.password,
        callback: () => {
          this.$router.push({ name: 'Home' });
        },
      });
    },
  },
};
</script>

<style scoped>

</style>
