import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: null,
    },
    getters: {
        getUser: (state) => state.user,
        isAuthenticated: (state) => !!state.user,
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
    },
    actions: {
        fetchUser({commit}, userData) {
            commit("setUser", userData);
        },
    },
});
