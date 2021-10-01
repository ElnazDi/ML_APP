<template>
  <!-- Navigation -->
  <div class="row">
    <div class="container-fluid">
      <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
        <!-- Brand/logo -->
        <a class="navbar-brand" href="#" style="margin-left: 3%;">
          <img src="img/logo.png" alt="logo" style="width:250px;">
        </a>

        <!-- Links -->
        <ul class="navbar-nav" v-if="authenticated">
          <li class="nav-item active" >
            <a class="nav-link" href="#">Home</a>
          </li>
        </ul>

        <ul class="navbar-nav" v-if="authenticated">
          <li class="nav-item" >
            <a class="nav-link" href="#">Carts</a>
          </li>
        </ul>

        <ul class="navbar-nav" v-if="authenticated">
          <li class="nav-item" >
            <a class="nav-link" href="#">Bookmarks</a>
          </li>
        </ul>

        <div style="padding-left: 75%;" v-if="authenticated">
          <ul class="navbar-nav">
            <li class="nav-item" >
              <a class="nav-link" href="#" @click='authButtonClicked'>
                <i class="fa fa-user fa-lg"></i>
                Logout
              </a>
            </li>
          </ul>
        </div>

      </nav>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BrandBar',
  props: {
    authenticated: Boolean,
  },
  methods: {
    authButtonClicked() {
      console.log('authentication button of user clicked');
    },
  },
};
</script>

<style scoped>

</style>
