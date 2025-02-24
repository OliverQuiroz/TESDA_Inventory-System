import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/HomePage.vue';
import Login from '@/views/LoginPage.vue';
import ScanPage from '@/views/ScanPage.vue';

const routes = [
  { path: '/', redirect: '/login' }, // Redirect root to login
  { path: '/login', name: 'Login', component: Login },
  { path: '/home', name: 'Home', component: Home },
  { path: '/scan', name: 'Scan', component: ScanPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
