// store.js
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        point1: new Float32Array(3),
        point2: new Float32Array(3),
    },
    mutations: {
        setPoint1(state, point) {
            state.point1 = point;
        },
        setPoint2(state, point) {
            state.point2 = point;
        },
    },
});