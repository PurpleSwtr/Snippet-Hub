<template>
  <UPage>
    <div v-if="currentTech" class="space-y-6">
      <TechnologyHeader :tech="currentTech" />
      <SnippetsGrid
        :snippets="snippetStore.snippets"
        :isLoading="snippetStore.isLoading"
      />
    </div>

    <div v-else-if="techStore.isLoading" class="py-10 text-center">
      Загрузка технологии...
    </div>

    <div v-else class="py-10 text-center text-red-500">
      Технология не найдена
    </div>
  </UPage>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useTechnologyStore } from '@/stores/technology'
import { useSnippetStore } from '@/stores/snippets'
import TechnologyHeader from '@/components/technology/TechnologyHeader.vue'
import SnippetsGrid from '@/components/snippets/SnippetsGrid.vue'

const route = useRoute()
const techStore = useTechnologyStore()
const snippetStore = useSnippetStore()

const currentTech = computed(() =>
  techStore.technologies.find(t => t.name === route.params.name)
)

const loadData = async () => {
  if (techStore.technologies.length === 0) {
    await techStore.fetchTechnologies()
  }

  if (currentTech.value) {
    await snippetStore.fetchSnippets(currentTech.value.id)
  }
}

onMounted(() => {
  loadData()
})

watch(() => route.params.name, () => {
  loadData()
})
</script>
