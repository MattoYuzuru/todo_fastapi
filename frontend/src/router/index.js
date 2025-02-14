import Vue from 'vue';
import Router from 'vue-router';
import UserRegister from '../components/UserRegister.vue';
import UserLogin from '../components/UserLogin.vue';
import UserAccount from "../components/UserAccount.vue";
import HomePage from '../components/HomePage.vue';
import TodoDetails from '../components/TodoDetails.vue';
import TodoList from "../components/TodoList.vue";
import AddTodo from "../components/AddTodo.vue";

Vue.use(Router);

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomePage
    },
    {
        path: '/register',
        name: 'Register',
        component: UserRegister
    },
    {
        path: '/login',
        name: 'Login',
        component: UserLogin
    },
    {
        path: '/todos/create',
        name: 'CreateTodo',
        component: AddTodo
    },
    {
        path: '/todos/all/',
        name: 'TodoList',
        component: TodoList,
        props: true
    },
    {
        path: '/todos/:id',
        name: 'TodoDetails',
        component: TodoDetails,
        props: true
    },
    {
        path: '/users/me/',
        name: 'UserAccount',
        component: UserAccount,
        props: true
    }
];

const router = new Router({
    mode: 'history',
    routes
});

export default router;
