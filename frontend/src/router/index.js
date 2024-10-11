import { createRouter, createWebHistory } from 'vue-router';
import filmdetails from '../views/filmdetails.vue';
import Index from '../views/Index.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Index
  },
  {
    path: '/filmdetails/:id',
    name: 'filmdetails',
    component: filmdetails
  }  
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;

