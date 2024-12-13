import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/echo',
    name: 'Echo',
    component: () => import('@/views/Echo.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
