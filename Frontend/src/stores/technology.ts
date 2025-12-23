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

      if (!response.ok) {
        throw new Error('Ошибка при загрузке технологий')
      }

      const data = await response.json()
      technologies.value = data
      console.log(technologies.value);

    } catch (err: any) {
      error.value = err.message
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  return {
    technologies,
    isLoading,
    error,
    fetchTechnologies
  }
})
