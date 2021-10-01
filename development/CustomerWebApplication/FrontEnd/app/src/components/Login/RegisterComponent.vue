<template>
  <div class="container register">
    <div class="mb-3">
      <h3 class="text-center">Sign Up</h3>
      <hr>
    </div>
    <div class="mb-3">
      <input type="text" class="form-control" id="name" placeholder="Name">
    </div>
    <div class="mb-3">
      <input type="email" class="form-control" id="emailAddress" placeholder="Email address">
    </div>
    <div class="mb-3">
      <input type="password" class="form-control" id="password" placeholder="Password">
    </div>
    <div class="mb-3">
      <input type="password" class="form-control" id="cpassword" placeholder="Confirm Password">
    </div>
    <div class="mb-3 form-check">
      <input type="checkbox" class="form-check-input" id="exampleCheck1">
      <label class="form-check-label" for="exampleCheck1">I agree to the terms and conditions</label>
    </div>
    <div class="mb-3 d-grid col-11 mx-auto">
      <button type="button" class="btn btn-success">Register</button>
    </div>    
  </div>
</template>

<script>
export default{
  name: 'Register'
}
</script>

<style scoped>
.register{
  margin-top:15vh;
  max-width: 400px;
}
</style>