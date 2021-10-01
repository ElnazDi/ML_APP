<template>
  <nav class="navbar navbar-primary bg-primary">
    <div class="container-fluid">
      <span class="navbar-brand mb-0 h1">Project O</span>
      <div class="row g-3">
        <div class="col-sm-5">
          <input type="text" class="form-control" placeholder="Username" aria-label="username" v-model="username">
        </div>
        <div class="col-sm-5">
          <input type="password" class="form-control" placeholder="Password" aria-label="password" v-model="password">
        </div>
        <div class="col-sm-2">
          <button class="btn btn-success" type="submit" @click="logIn">{{ button }}</button>
        </div>
      </div>
    </div>
  </nav>  
</template>

<script>
export default {
  name: 'PageHeader',
  data(){
    return {
      loggedIn: false,
      username: '',
      password: '',
      button: 'Log In'
    }
  },
  methods: {
    logIn(){
      //make HTTP request and check if user credentials are valid
      this.button = 'Wrong!'
      setTimeout(() => {
        this.button = 'Log In'
      },2000)
      this.username = ''
      this.password = ''
    },
  }
}  
</script>

<style>

</style>