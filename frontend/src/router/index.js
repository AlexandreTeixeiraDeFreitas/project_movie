import { createRouter, createWebHistory } from 'vue-router';
import FilmDetails from '../views/FilmDetails.vue';
import Index from '../views/Index.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Index
  },
  {
    path: '/film/:id',
    name: 'FilmDetails',
    component: FilmDetails,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
