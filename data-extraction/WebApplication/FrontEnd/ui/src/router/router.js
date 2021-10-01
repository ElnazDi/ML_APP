import Vue from 'vue';
import Router from 'vue-router';

import AuthPage from '../auth/AuthPage.vue';
import HomePage from '../home/home/HomePage.vue';
import CartPage from '../home/cart/CartPage.vue';
import BookmarkPage from '../home/bookmark/BookmarkPage.vue';

Vue.use(Router);

export default new Router({
  routes: [{
    path: '/auth',
    name: 'Auth',
    component: AuthPage,
  }, {
    path: '/home',
    name: 'Home',
    component: HomePage,
  }, {
    path: '/cart',
    name: 'Cart',
    component: CartPage,
  }, {
    path: '/bookmark',
    name: 'Bookmark',
    component: BookmarkPage,
  }],
});
