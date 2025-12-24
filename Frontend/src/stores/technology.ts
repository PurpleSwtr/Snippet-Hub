import { defineStore } from "pinia";
import { ref } from 'vue'
import type { Technology } from "@/types/technology";

export const useTechnologyStore = defineStore('technology', () => {
  const technologies = ref<Technology[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchTechnologies() {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch('http://localhost:8000/api/v1/technology/')
      if (!response.ok) throw new Error('Ошибка при загрузке технологий')
      technologies.value = await response.json()
    } catch (err: any) {
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  async function createTechnology(payload: { name: string; description: string; icon: string; about: string }) {
    isLoading.value = true
    try {
      const response = await fetch('http://localhost:8000/api/v1/technology/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Ошибка создания')
      }

      const newTech = await response.json()
      technologies.value.push(newTech)
      return newTech
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    technologies,
    isLoading,
    error,
    fetchTechnologies,
    createTechnology
  }
})
