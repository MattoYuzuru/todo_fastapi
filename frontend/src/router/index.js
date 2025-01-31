import Vue from 'vue';
import Router from 'vue-router';
import UserRegister from '../components/UserRegister.vue';
import UserLogin from '../components/UserLogin.vue';
import HomePage from '../components/HomePage.vue';
import AddToDo from '../components/AddTodo.vue';
import TodoDetails from '../components/TodoDetails.vue';

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
        name: 'CreateToDo',
        component: AddToDo
    },
    {
        path: '/todos/:id',
        name: 'TodoDetails',
        component: TodoDetails,
        props: true
    }
];

const router = new Router({
    mode: 'history',
    routes
});

export default router;
