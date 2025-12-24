import { defineStore } from "pinia";
import { ref } from 'vue'
import type { Snippet, SnippetCreate } from "@/types/snippet";

export const useSnippetStore = defineStore('snippets', () => {
  const snippets = ref<Snippet[]>([])
  const activeTechId = ref<number | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchSnippets(techId: number) {
    activeTechId.value = techId
    isLoading.value = true
    snippets.value = []

    try {
      const response = await fetch(`http://localhost:8000/api/v1/snippets/${techId}`)
      if (!response.ok) throw new Error('Ошибка загрузки сниппетов')
      snippets.value = await response.json()
    } catch (err: any) {
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  async function createSnippet(payload: SnippetCreate) {
    isLoading.value = true
    try {
      const response = await fetch('http://localhost:8000/api/v1/snippets/new_snippet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!response.ok) throw new Error('Ошибка создания сниппета')

      const newSnippet = await response.json()
      if (activeTechId.value === payload.technology_id) {
        snippets.value.push(newSnippet)
      }
      return newSnippet
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function updateSnippet(id: number, payload: Partial<SnippetCreate>) {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:8000/api/v1/snippets/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!response.ok) throw new Error('Ошибка обновления сниппета')

      const updatedSnippet = await response.json()

      const index = snippets.value.findIndex(s => s.id === id)
      if (index !== -1) {
        snippets.value[index] = updatedSnippet
      }
      return updatedSnippet
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function deleteSnippet(id: number) {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:8000/api/v1/snippets/${id}`, {
        method: 'DELETE',
      })

      if (!response.ok) throw new Error('Ошибка удаления сниппета')

      snippets.value = snippets.value.filter(s => s.id !== id)
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    snippets,
    activeTechId,
    isLoading,
    error,
    fetchSnippets,
    createSnippet,
    updateSnippet,
    deleteSnippet
  }
})
