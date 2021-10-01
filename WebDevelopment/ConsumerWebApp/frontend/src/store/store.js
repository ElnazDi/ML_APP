import Vue from 'vue';
import Vuex from 'vuex';

import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    allProducts: [],
    cartHistoryRecommendedProducts: [],
    genericRecommendedProducts: [],
    bookmarkRecommendedProducts: [],
    bookmarkedProducts: [],
    cartProducts: [],
    cartHistoryProducts: [],
    vendorNames: ['kaufland', 'rewe', 'aldi', 'lidl', 'netto'],
    vendorFilter: {
      kaufland: true,
      aldi: true,
      netto: true,
    },
    notify: {
      display: false,
      type: 'error',
      message: '',
      timeout: null,
    },
    auth: {
      loggedIn: false,
      displayLogin: true,
      token: ''
    },
  },
  getters: {

    getAllProducts(state) {
      return state.allProducts ? state.allProducts : [];
    },

    getFilters(state){
      return state.vendorFilter;
    },

    getLengthOfAllProducts(state){
      return state.allProducts.length;
    },

    displayBookmarkedProducts(state) {
      state.bookmarkedProducts.forEach(productId => {
        const productObj = state.allProducts.filter(product => product._id == productId);
        productObj.bookmarked = true;
      })
      let subset = state.allProducts.filter(product => state.vendorFilter[product.vendor.toLowerCase()]);
      subset = subset.filter(product => product.bookmarked === true)
      return subset;
    },

    getCartHistoryRecommendedProducts(state) {
      const productList = [];
      state.allProducts.forEach(product => {
        state.cartHistoryRecommendedProducts.forEach(rProduct => {
          if (product._id == rProduct.productId)
            productList.push(product);
        })
      })
      return productList;
    },

    getGenericRecommendedProducts(state){
      const productList = [];
      console.log(state.genericRecommendedProducts);
      state.genericRecommendedProducts.forEach(rProduct => {
        const index = state.allProducts.findIndex(product => product._id == rProduct.productId)
        if(index > -1)
          productList.push(state.allProducts[index]);
      })
      return productList;
    },

    getBookmarkRecommendedProducts(state){
      const productList = [];
      state.allProducts.forEach(product => {
        state.bookmarkRecommendedProducts.forEach(rProduct => {
          if (product._id == rProduct)
            productList.push(product);
        })
      })
      return productList;
    },

    displayCartProducts(state) {
      return state.cartProducts;
    },

    getCartHistoryProducts(state){      
      return state.cartHistoryProducts;
    },

    showRecommendedProducts(state) {
      return state.cartHistoryRecommendedProducts.length > 0;
    },
    
    totalPriceOfCart(state) {
      let subset = state.cartProducts.filter(product => state.vendorFilter[product.vendor.toLowerCase()]);
      let price = 0;
      subset.forEach(product => price += (product.quantity * product.price))
      return Number.parseFloat(price).toFixed(2);
    },

  },
  actions: {
    
    fetchListOfProducts({ state, commit }) {
      axios('http://localhost:3000/products', {
        method: 'get',
        headers: {
          Authorization: state.auth.token,
        }, 
      })
      .then((result) => {
        // Add bookmarked field which is populated in next call
        commit('updateProducts', result.data.products);
        commit('saveDataToLocalStorage', {
          name: 'allProducts',
          value: state.allProducts
        });
      })
      .catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      })
    },

    fetchBookmarkedProducts({ state, commit }) {
      axios('http://localhost:3000/bookmark', {
        method: 'get',
        headers: {
          Authorization: state.auth.token,
        }
      })
      .then((result) => {
        console.log("Fetching bookmarked products")
        console.log(result);
        commit('setupBookmarkList', {
          products: result.data.products,
        })
      })
      .catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      })
    },

    fetchCartHistoryRecommendedProducts({ state, commit }) {
      axios('http://localhost:3000/recommendations/cartHistory', {
        method: 'get',
        headers: {
          Authorization: state.auth.token,
        }
      })
      .then((result) => {
        commit('setupCartHistoryRecommendationList', {
          products: result.data.products,
        })
      })
      .catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      })
    },

    fetchGenericRecommendedProducts({ state, commit }) {
      axios('http://localhost:3000/recommendations/generic', {
        method: 'get',
        headers: {
          Authorization: state.auth.token,
        }
      })
      .then((result) => {
        console.log("Fetching generic recommended products");
        commit('updateGenericRecommendedProducts', result.data.products);
      })
      .catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      })
    },

    fetchBookmarkRecommendedProducts({ state, commit }) {
      axios('http://localhost:3000/recommendations/bookmark', {
        method: 'get',
        headers: {
          Authorization: state.auth.token,
        }
      })
      .then((result) => {
        console.log("Fetching bookmark recommended products");
        console.log(result);
        commit('updateBookmarkRecommendedProducts', result.data.products);
        // commit('updateGenericRecommendedProducts', result.data.products);
      })
      .catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      })
    },

    fetchListInCart({state, commit}){
      axios('http://localhost:3000/cart', {
          method: 'get',
          headers: {
            Authorization: state.auth.token,
          }
        })
        .then((result) => {
          commit('setupCartProducts', result.data.products);
        })
        .catch((err) => {
          commit('displayNotification', {
            type: 'error',
            message: err.message,
          })
        })
    },

    fetchListInCartHistory({ state, commit }){
      axios('http://localhost:3000/cartHistory', {
        method: 'get',
        headers: {
          Authorization: state.auth.token,
        }
      })
      .then((result) => {
        commit('setupCartHistoryProducts', result.data.products);
      })
      .catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })        
      })
    },

    login({ state, commit }, { username, password }) {
      axios.post('http://localhost:3000/login', {
        username: username,
        password: password,
      }).then(result => {
        state.auth.token = result.data.token;
        state.auth.loggedIn = true;
        commit('saveCredToLocalStorage')
      })
      .catch(err => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      });
    },

    register({ commit }, { username, password, password2, gender, email, phone, country, dob }) {
      axios.post('http://localhost:3000/register', {
        username,
        password,
        password2,
        gender,
        email,
        phone,
        country,
        dob,
      }).then((result) => {
        commit('displayNotification', {
          type: 'success',
          message: result.data.message,
        })
      }).catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      })
    },

    bookmarkProduct({ commit, state }, { id }){
      axios('http://localhost:3000/bookmark', {
        method: 'post',
        headers: {
          Authorization: state.auth.token,
        },
        data: {
          id
        },
      }).then((result) => {
        commit('displayNotification', {
          type: 'success',
          message: result.data.message,
        });
      }).catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      })
    },

    unbookmarkProduct({ commit, state }, { id }){
      axios('http://localhost:3000/bookmark', {
        method: 'delete',
        headers: {
          Authorization: state.auth.token,
        },
        data: {
          id
        },
      }).then((result) => {
        commit('unbookmarkFromList', { id })
        commit('displayNotification', {
          type: 'success',
          message: result.data.message,
        })
      }).catch((err) => {
        commit('displayNotification', {
          type: 'error',
          message: err.message,
        })
      })
    },

    incrementProductInCart({ commit, state }, { productId }) {
      axios('http://localhost:3000/cart/increment', {
        method: 'post', 
        headers: {
          Authorization: state.auth.token,
        },
        data: {
          productId
        }
      }).then((result) => {
        commit('updateCart', result.data.data);
      }).catch(err => {
        console.log(err)
        commit('displayNotification', err.message);
      })
    },

    decrementProductInCart({ commit, state }, { productId }) {
      axios('http://localhost:3000/cart/decrement', {
        method: 'post', 
        headers: {
          Authorization: state.auth.token,
        },
        data: {
          productId
        }
      }).then((result) => {
        commit('updateCart', result.data.data);
      }).catch(err => {
        console.log(err)
        commit('displayNotification', err.message);
      })
    },

    removeProductFromCart({ commit, state }, { productId }) {
      axios('http://localhost:3000/cart', {
        method: 'delete', 
        headers: {
          Authorization: state.auth.token,
        },
        data: {
          productId
        }
      }).then((result) => {
        commit('removeFromCart', result.data.data);
      }).catch(err => {
        console.log(err)
        commit('displayNotification', err.message);
      })
    },

    boughtProductInCart({ commit, state }, { productId }) {
      axios('http://localhost:3000/cart/bought', {
        method: 'post',
        headers: {
          Authorization: state.auth.token,
        },
        data: {
          productId
        }
      }).then((result) => {
        commit('removeFromCart', result.data.data);
      }).catch(err => {
        commit('displayNotification', err.message);
      })
    }

  },
  mutations: {

    fetchDataFromLocalStorage(state, data){
      console.log("fetching values from local storage");
      const values = window.localStorage.getItem(data.name);
      console.log(values);
      state[data.name] = JSON.parse(values);
    },

    saveDataToLocalStorage(state, data){
      const dataToStore = JSON.stringify(data.value);
      window.localStorage.setItem(data.name, dataToStore);
    },

    fetchCredFromLocalStorage(state){
      console.log('Fetching cred from local storage')
      const token = window.localStorage.getItem('token');
      console.log(token);
      if(token){
        state.auth.token = token;
        state.auth.displayLogin = false;
        state.auth.loggedIn = true;
      } else {
        state.auth.token = '';
        state.auth.displayLogin = true;
        state.auth.loggedIn = false;
      }
    },

    saveCredToLocalStorage(state){
      console.log(state.auth.token);
      window.localStorage.setItem('token', state.auth.token);
    },

    showLogin (state) {
      state.auth.displayLogin = true;
    },

    showRegister (state) {
      state.auth.displayLogin = false;
    },

    logoutUser (state) {
      state.auth.token = '';
      state.auth.loggedIn = false;
      window.localStorage.setItem('token', '');
    },

    displayNotification (state, { type, message }) {
      state.notify.message = message;
      state.notify.type = type;
      state.notify.display = true;
      state.notify.timeout = setTimeout(() => {
        state.notify.message = '';
        state.notify.display = false;
      }, 5000);
    },

    hideNotification (state) {
      clearTimeout(state.notify.timeout);
      state.notify.message = '';
      state.notify.type = 'info';
      state.notify.display = false;
    },

    toggleVendorFilter (state, { vendor }) {
      state.vendorFilter[vendor] = !state.vendorFilter[vendor];
    },

    setupBookmarkList (state, { products }) {
      state.bookmarkedProducts = products;
      state.allProducts.filter((product) => products.includes(product._id))
        .forEach((product) => product.bookmarked = true);
    },

    setupCartHistoryRecommendationList(state, { products }) {
      state.cartHistoryRecommendedProducts = products;
    },

    unbookmarkFromList (state, { id }) {
      const index = state.bookmarkedProducts.indexOf(id);
      state.bookmarkedProducts.splice(index, 1);
      state.allProducts.filter((product) => product._id == id)
        .forEach((product) => product.bookmarked = false);
    },

    setupProducts (state) {
      state.allProducts = [];
    },

    updateProducts (state, products) {
      products.forEach(product => product.bookmarked = false);
      //set bookmarked fields to true
      state.allProducts = products;
    },

    setupCartProducts (state, cartProducts) {
      state.cartProducts = [];
      cartProducts.forEach(cartProduct => {
        const index = state.allProducts.findIndex((product) => product._id == cartProduct.productId);
        if(index == -1)
          console.log(`${cartProduct.productId} is not found`);
        else {
          cartProduct['title'] = state.allProducts[index]['title'];
          cartProduct['price'] = state.allProducts[index]['price'];
          cartProduct['vendor'] = state.allProducts[index]['vendor'];
          cartProduct['image'] = state.allProducts[index]['image'];
          state.cartProducts.push(cartProduct);
        }
      })
      console.log(state.cartProducts);
    },

    setupCartHistoryProducts (state, cartHistoryProducts) {
      state.cartHistoryProducts = [];
      cartHistoryProducts.forEach(cartProduct => {
        const index = state.allProducts.findIndex((product) => product._id == cartProduct.productId);
        if(index > -1){
          cartProduct['title'] = state.allProducts[index]['title'];
          cartProduct['price'] = state.allProducts[index]['price'];
          cartProduct['vendor'] = state.allProducts[index]['vendor'];
          cartProduct['image'] = state.allProducts[index]['image'];
          if(cartProduct.deleted)
            cartProduct['date'] = new Date(cartProduct['removed'])
          else
            cartProduct['date'] = new Date(cartProduct['modified'])
          cartProduct['totalPrice'] = Number.parseFloat(cartProduct['price'] * cartProduct['quantity']).toFixed(2);
          state.cartHistoryProducts.push(cartProduct);
        }
      })
    },

    updateCart (state, cartProduct) {
      const index = state.allProducts.findIndex((product) => product._id == cartProduct.productId);
      cartProduct['title'] = state.allProducts[index]['title'];
      cartProduct['price'] = state.allProducts[index]['price'];
      cartProduct['vendor'] = state.allProducts[index]['vendor'];
      const cartProductIndex = state.cartProducts.findIndex(product => product.productId == cartProduct.productId)
      if(cartProductIndex == -1)
        state.cartProducts.push(cartProduct)
      else{
        state.cartProducts[cartProductIndex].quantity = cartProduct.quantity;
      }
    },

    updateGenericRecommendedProducts(state, recommendedProducts) {
      // for(const recommendedProduct in recommendedProducts){
      //   const index = state.allProducts.findIndex((product) => product._id == recommendedProduct.productId);
      //   if(index > -1){
      //     state.genericRecommendedProducts.push(state.allProducts[index]);
      //   }
      // }
      state.genericRecommendedProducts = recommendedProducts;
    },

    updateBookmarkRecommendedProducts(state, recommendedProducts) {
      state.bookmarkRecommendedProducts = recommendedProducts;
    },

    removeFromCart(state, cartProduct) {
      const cartProductIndex = state.cartProducts.findIndex(product => product.productId == cartProduct.productId)
      state.cartProducts.splice(cartProductIndex, 1);
    },

  }
});