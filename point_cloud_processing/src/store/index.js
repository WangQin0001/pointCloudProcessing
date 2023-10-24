// store.js
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        point1: new Float32Array(3),
        point2: new Float32Array(3),
        isAuthenticated: JSON.parse(sessionStorage.getItem('isAuthenticated') || "false"), // 注意 sessionStorage 中的数据是字符串格式
    },
    // 用于更新状态
    mutations: {
        setPoint1(state, point) {
            state.point1 = point;
        },
        setPoint2(state, point) {
            state.point2 = point;
        },
        setIsAuthenticated(state, isAuthenticated){
            state.isAuthenticated = isAuthenticated;
            sessionStorage.setItem('isAuthenticated', isAuthenticated);//确保刷新页面后登录状态不变
        },
    },

    //用于获取状态
    getters:{
        getIsAuthenticated: state => {
            return state.isAuthenticated;
        }
    }
});

