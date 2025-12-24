import { defineStore } from "pinia";
import { ref } from 'vue'
import type { Tag } from "@/types/tag";

export const useTagStore = defineStore('tags', () => {
  const tags = ref<Tag[]>([])
  const isLoading = ref(false)

  async function fetchTags() {
    isLoading.value = true
    try {
      const response = await fetch('http://localhost:8000/api/v1/tags/')
      if (response.ok) {
        tags.value = await response.json()
      }
    } catch (e) {
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function createTag(payload: { name: string, color?: string }) {
    isLoading.value = true
    try {
      const response = await fetch('http://localhost:8000/api/v1/tags/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Ошибка создания тега')
      }

      const newTag = await response.json()
      tags.value.push(newTag)
      return newTag
    } finally {
      isLoading.value = false
    }
  }

  return {
    tags,
    isLoading,
    fetchTags,
    createTag
  }
})
