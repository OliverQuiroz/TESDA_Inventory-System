// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/HomePage.vue';
import Login from '@/views/LoginPage.vue';
import ScanPage from '@/views/ScanPage.vue';
import LoginPage from '@/views/LoginPage.vue';

const routes = [
  { 
    path: '/', 
    component: LoginPage, 
    // We hide the navbar on this route
    meta: { hideNavbar: true } 
  },
  { 
    path: '/home', 
    component: HomePage, 
    meta: { requiresAuth: true } 
  },
  { 
    path: '/scan', 
    component: ScanPage, 
    meta: { requiresAuth: true } 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// NAVIGATION GUARD
router.beforeEach(async (to, from, next) => {
  // If the route requires authentication
  if (to.meta.requiresAuth) {
    // Quick check: localStorage
    const isAuthenticatedLocal = localStorage.getItem('isAuthenticated');

    // Optional: check with your Django server
    let isReallyAuthenticated = false;
    try {
      const response = await fetch('http://127.0.0.1:8000/api/check-auth/', {
        credentials: 'include',
      });
      const data = await response.json();
      isReallyAuthenticated = data.isAuthenticated;
    } catch (error) {
      console.error('check-auth failed:', error);
    }

    if (isAuthenticatedLocal && isReallyAuthenticated) {
      next();
    } else {
      // If not authenticated, go back to login
      next('/');
    }
  } else {
    // If route does NOT require auth, proceed
    next();
  }
});

export default router;
