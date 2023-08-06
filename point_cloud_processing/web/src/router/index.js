import Vue from 'vue'
import VueRouter from 'vue-router'

import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
// import pcd from '../components/pcd.vue'

Vue.use(VueRouter)

const routes = [
  { path: '', redirect: '/login' },
  { path: '/', redirect: '/login' },

  { path: '/login', component: Login },
  { path: '/home', component: Home },
]

const router = new VueRouter({
  routes
})

export default router