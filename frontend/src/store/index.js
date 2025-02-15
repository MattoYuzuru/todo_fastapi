import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

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
        clearUser(state) {
            state.user = null;
        }
    },
    actions: {
        async fetchUser({commit}) {
            const token = localStorage.getItem("token");
            if (!token) {
                commit("clearUser");
                return;
            }

            try {
                const response = await axios.get("http://localhost:8000/users/me/", {
                    headers: {Authorization: `Bearer ${token}`}
                });
                commit("setUser", response.data);
            } catch (error) {
                console.error("Error fetching user:", error);
                commit("clearUser");
                localStorage.removeItem("token");
            }
        },
        logout({commit}) {
            localStorage.removeItem("token");
            commit("clearUser");
        }
    }
});
