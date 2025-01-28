import {createStore} from 'vuex';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

const store = createStore({
    state: {
        user: null,
        todos: [],
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setTodos(state, todos) {
            state.todos = todos;
        },
    },
    actions: {
        async fetchTodos({commit}) {
            const response = await axios.get('/todos/all');
            commit('setTodos', response.data);
        },
        async loginUser({commit}, {username, password}) {
            const response = await axios.post('/users/login', {username, password});
            commit('setUser', response.data);
        },
    },
});

export default store;
