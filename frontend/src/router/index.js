import {createRouter, createWebHistory} from 'vue-router';
import Home from '@/views/Home.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import Pomodoro from '@/views/Pomodoro.vue';

const routes = [
    {path: '/', name: 'Home', component: Home},
    {path: '/login', name: 'Login', component: Login},
    {path: '/register', name: 'Register', component: Register},
    {path: '/pomodoro', name: 'Pomodoro', component: Pomodoro},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
