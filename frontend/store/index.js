import axios from 'axios';

export default {
    state: {
        token: null,
    },
    mutations: {
        setToken(state, token) {
            state.token = token;
        },
    },
    actions: {
        async login({commit}, {username, password}) {
            const response = await axios.post('/users/login', {username, password});
            commit('setToken', response.data.access_token);
        },
    },
};
