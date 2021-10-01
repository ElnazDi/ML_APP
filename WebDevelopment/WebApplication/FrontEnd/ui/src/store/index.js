import Vue from 'vue';
import Vuex from 'vuex';

import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    showLogin: false,
    products: [],
    page: 1,
    webtoken: '',
    authenticated: false,
    bookmarks: [],
    carts: [],
    notificationMessage: 'Added to cart successfully',
    displayNotification: true,
    notificationType: 'Success', // One of 3 types 'Error', 'Info' or 'Success'
    dummy: false,
    vendorFilter: {
      aldi: true,
      rewe: true,
      kaufland: true,
      netto: true,
    },
  },
  mutations: {
    displayLogin(state, value) {
      state.showLogin = value;
    },
    login(state, data) {
      // Fetch webtoken from backend after login
      axios({
        method: 'post',
        url: 'http://localhost:8000/users/login',
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          email: data.username,
          password: data.password,
        },
      }).then((result) => {
        state.webtoken = result.accessToken;
        state.authenticated = true;
        data.callback();
      }).catch((err) => {
        state.notificationMessage = err.response.data.error;
        state.displayNotification = true;
        state.notificationType = 'Error';
      });
    },
    register(state, data) {
      // Register user
      axios.post('http://localhost:8000/users/register', data)
        .then(() => console.log('Success'))
        .catch((err) => console.log(err));
      console.log(state, data);
    },
    updateProducts(state, products) {
      state.products = [...products];
    },
    updateCarts(state, carts) {
      state.carts.push(carts);
    },
    updateBookmarks(state, bookmarks) {
      state.carts.push(bookmarks);
    },
    // bookmarkProduct(state, bookmark) {

    // },
    // unbookmarkProduct(state, bookmark) {
    //   // remove bookmark
    // },
    addProductToCart() {
      // use state.products or state.carts or state.page to make changes
    },
    removeProductFromCart() {

    },
    hideNotification(state) {
      state.notificationMessage = '';
      state.notificationType = '';
      state.displayNotification = false;
    },
    updateFilters(state, vendor) {
      state.vendorFilter[vendor] = !state.vendorFilter[vendor];
    },
  },
  actions: {
    fetchListOfProducts({ state, commit }) {
      // Fetch list of products based on page number
      axios.get(`http://localhost:8000/product/products/${state.page}`)
        .then((result) => {
          commit('updateProducts', result.data.data);
          console.log(state.products);
        });
    },
  },
  getters: {
    listOfBookmarks(state) {
      // Fetch list of all bookmark products
      return state.bookmarks;
    },
    listOfCarts() {

    },
    detailsOfProduct() {

    },
    listOfProductsInCart() {
      // use state.products.filter() with cart field set to value
    },
    displayNotification(state, type) {
      if (state.displayNotification && type === state.notificationType) {
        return { status: true, message: state.notificationMessage };
      }
      return { status: false };
    },
  },
});

// use this.$store.commit('method', params) to call and pass data
// use this.$store.getters.methodName to fetch data
//

/*
// /login
// req: username, password
// res: { status: Success/Failure, data: { token }, message: "Failure message" }

// /register
// req: name, password, username, date of birth, phone number
// res: { status: Success/Failure, message: "Failure message" }

// /products/:pageNumber
// res: {status: Success/Failure,
data: { products: [product1, product2 ...] }, message: "failure message"}

// /product/:id
// res: {status: Success/Failure,
data: { details of product }, message: "failure message"}

// /bookmarks
// token
// res: {status: Success/Failure,
data: { bookmarks: [product1, product2 ...] }, message: "failure message"}

// /bookmark/:id/delete
// token
// res: {status: Success/Failure, message: ""}

// /bookmark/:id/add
// token Authorization: Basic ""
// res: {status: Success/Failure, message: ""}

// /carts (id, name)
// token
// res: message {status: Success/Failure,
data: { carts: [cart1 id, cart2 id] }, message: "failure message"}

// /cart/:id
// token
// res: message {status: Success/Failure,
 data: { name: '', products: [product1, product2...]},
  message: "failure message"}

// /cart/add
// token
// req: cart name
// res: message {status: Success/Failure,
data: id of cart, message: "failure message"}

// /cart/:id/delete
// token
// res: message {status: Success/Failure, message: ""}

// /cart_update/:id/add/:product_id
// token
// res: message {status: Success/Failure, message: ""}

// /cart_update/:id/delete/:product_id
// token
// res: message {status: Success/Failure, message: ""}
*/
