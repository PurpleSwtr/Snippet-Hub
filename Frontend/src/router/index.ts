import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import BuilderView from '@/views/BuilderView.vue'
import TechnologyView from '@/views/TechnologyView.vue'
import SettingsView from '@/views/SettingsView.vue'
import ChatView from '@/views/ChatView.vue'
import CreateTechView from '@/views/CreateTechView.vue'
import CreateTagView from '@/views/CreateTagView.vue'

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
    {
      path: '/create_technology',
      name: 'create_technology',
      component: CreateTechView
    },
    {
      path: '/create_tag',
      name: 'create_tag',
      component: CreateTagView
    },
  ],
})

export default router
