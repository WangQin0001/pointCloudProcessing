import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store'

// 懒加载组件
const Login = () => import('@/views/Login.vue');
const Home = () => import('@/views/Home.vue');
const Register = () => import('@/views/Register.vue');
// const NotFound = () => import('@/views/404.vue'); // 假设你有一个404组件

Vue.use(VueRouter);

const routes = [
  { path: '/', redirect: { name: 'Login' } },
  { path: '/user/login', component: Login, name: 'Login' },
  { path: '/user/register', component: Register, name: 'Register' },
  { path: '/home', component: Home, name: 'Home' },
  // { path: '*', component: NotFound }, // 404 页面，确保这条是路由列表中的最后一条
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.getIsAuthenticated; // 从 Vuex 的 getters 中获取登录状态

  if (!isAuthenticated && to.name !== 'Login' && to.name !== 'Register') {
    // 如果用户未登录，并且目标路由不是登录页或注册页，则重定向到登录页
    next({ name: 'Login' });
  } else if (isAuthenticated && (to.name === 'Login' || to.name === 'Register')) {
    // 如果用户已登录，并且目标路由是登录页或注册页，则重定向到主页
    next({ name: 'Home' });
  } else {
    // 如果没有需要重定向的，确保一定要调用 next()
    next();
  }
});




export default router;
