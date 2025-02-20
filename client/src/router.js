import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/HomePage.vue";
import Scan from "@/views/ScanPage.vue";


const routes = [
  { path: "/", component: Home },
  { path: "/scan", component: Scan },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
