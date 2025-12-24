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

  return {
    tags,
    isLoading,
    fetchTags
  }
})
