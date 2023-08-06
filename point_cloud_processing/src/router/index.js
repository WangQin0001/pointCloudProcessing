import Vue from 'vue'
import VueRouter from 'vue-router'

import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Register from "../views/Register.vue";

Vue.use(VueRouter)

const routes = [
  { path: '', redirect: '/login' },
  { path: '/', redirect: '/login' },

  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/home', component: Home },

]

const router = new VueRouter({
  mode:'history',
  routes
})

export default router