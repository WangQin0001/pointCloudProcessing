import Vue from 'vue'
import ElementUI, { Message } from 'element-ui'; // 引入Message
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import router from './router'
import store from "./store/index";

Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.prototype.$message = Message; // 将Message方法添加到Vue的原型上

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
