import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import BuilderView from '@/views/BuilderView.vue'
import TechnologyView from '@/views/TechnologyView.vue'
import SettingsView from '@/views/SettingsView.vue'
import ChatView from '@/views/ChatView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/builder',
      name: 'builder',
      component: BuilderView
    },
    {
      path: '/technology/:name',
      name: 'technology',
      component: TechnologyView
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView
    },
    {
      path: '/agent',
      name: 'agent',
      component: ChatView
    },
  ],
})

export default router
