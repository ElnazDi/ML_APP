<template>
  <div class="container-fluid">

    <div class="row d-flex justify-content-center">
      <div class="col-md-4 col-md-offset-4 col-sm-6 col-sm-offset-3 backsecond">
        <div class="backcolor">

        <h3 Style="color:#43d36e;">Register</h3>

          <!--First Name-->
            <div class="col-md-12 col-sm-12 textup custom_padding">
              <label for="firstname" style="color: aliceblue;">First Name:</label>  <br>
              <input type="text" class="form-control" placeholder="First Name"
              v-model="firstname" style="color: black;" id="firstname" required>
            </div>

          <!--Last Name-->
            <div class="col-md-12 col-sm-12 textup custom_padding">
            <label for="lastname" style="color: aliceblue;">Last Name:</label>  <br>
            <input type="text" class="form-control" placeholder="Last Name"
            v-model="lastname" style="color: black;" id="lastname" required>
            </div>

          <!-- Gender -->
            <div class="col-md-12 col-sm-12 textup custom_padding">
            <label for="gender" style="color: aliceblue;">Gender:</label>  <br>
            <select name="gender" id="gender" class="form-control"
            v-model="gender" required>
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Others">Others</option>
            </select>
            </div>

          <!-- Date of Birth -->
            <div class="col-md-12 col-sm-12 textup custom_padding" >
            <span style="color: aliceblue;">Date of Birth</span>
            <input type="date" class="form-control"
            v-model="dateOfBirth" style="color: black;" required>
            </div>

          <!-- Place of Birth-->
            <div class="col-md-12 col-sm-12 textup custom_padding">
              <label for="country" style="color: aliceblue;">Nationality:</label>
              <select id="country" name="country"
              v-model="placeOfBirth" class="form-control" required>
                <option value="Country 1">Country 1</option>
                <option value="Country 2">Country 2</option>
              </select>
            </div>

            <!--Phone Number-->
            <div class="col-md-12 col-sm-12 textup custom_padding" >
            <label for="phone" style="color: aliceblue;">Phone number:</label>
            <input type="tel" class="form-control" placeholder="777-44-225" id="phone"
            v-model="phoneNumber" name="phone" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}" required>
            </div>

            <!--Email/Username-->
            <div class="col-md-12 col-sm-12 textup custom_padding">
            <label for="email" style="color: aliceblue;">Email:</label>
            <input type="email" class="form-control" placeholder="Email"
            v-model="email" style="color: black;" id="email" required>
            </div>

            <!--Password-->
            <div class="col-md-12 col-sm-12 textup custom_padding">
            <label for="password" style="color: aliceblue;">Password:</label>
            <input type="password" class="form-control" placeholder="Password"
            v-model="password" style="color: black;" id="password" required>
            </div>

            <!--Password 2-->
            <div class="col-md-12 col-sm-12 textup custom_padding">
            <label for="password2" style="color: aliceblue;">Repeat Password:</label>
            <input type="password" class="form-control" placeholder="Repeat Password"
            v-model="repeatPassword" style="color: black;" id="password2" required>
            </div>

            <div class="col-md-12 col-sm-12 textup">
            <a href="#"><button type="btn" class="btn-signup form-control"
              @click='register'>
              Sign Up</button></a><br>
            <p align="center" style="font-size:13px; color:white;">Already Have a Account ?
              <a href="#" @click='displayLogin'
                style="color:#43d36e;; font-weight:bold;">Sign In</a></p>
            </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignUp',
  data() {
    return {
      firstname: '',
      lastname: '',
      gender: '',
      dateOfBirth: '',
      placeOfBirth: '',
      phoneNumber: '',
      email: '',
      password: '',
      repeatPassword: '',
    };
  },
  methods: {
    displayLogin() {
      this.$store.commit('displayLogin', true);
    },
    register() {
      const data = {
        firstName: this.firstname,
        lastName: this.lastname,
        gender: this.gender,
        dateOfBirth: this.dateOfBirth,
        countryOfOrigin: this.placeOfBirth,
        phone: this.phoneNumber,
        email: this.email,
        password: this.password,
        password2: this.repeatPassword,
      };
      this.$store.commit('register', data);
      console.log(data);
    },
  },
};
</script>

<style scoped>
</style>
