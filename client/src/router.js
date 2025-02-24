import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import ScanPage from '@/views/ScanPage.vue';
import LoginPage from '@/views/LoginPage.vue';  

const routes = [
  { path: '/', component: HomePage },
  { path: '/scan', component: ScanPage },
  { path: '/login', component: LoginPage },  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
