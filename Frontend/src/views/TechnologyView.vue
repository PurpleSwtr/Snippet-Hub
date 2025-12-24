<template>
  <UPage>
    <div v-if="currentTech" class="space-y-6">
      <div class="flex items-center justify-between border-b border-gray-200 dark:border-gray-800 pb-4">

        <div class="flex items-center gap-4">
          <UModal
          :title="currentTech.name"
          close-icon="i-lucide-arrow-right"
          :ui="{ content: 'max-w-2xl' }"
          >
            <PrimeIcon
            :icon="currentTech.icon"
            @click="isModalAboutOpen = true"
            class="hover:cursor-pointer"
            ></PrimeIcon>

            <template #body>
              <div class="h-full w-full" >
                <p>{{ currentTech.about }}</p>
              </div>
            </template>
          </UModal>
          <div>
            <h1 class="text-3xl font-bold">{{ currentTech.name }}</h1>
            <p class="text-gray-500">{{ currentTech.description }}</p>
          </div>
        </div>
        <ModalCreateSnippet
        v-if="currentTech"
        :technology-id="currentTech.id" />
      </div>

      <div v-if="snippetStore.isLoading" class="space-y-4">
        <USkeleton class="h-24 w-full" v-for="n in 3" :key="n" />
      </div>

      <div v-else-if="snippetStore.snippets.length > 0" class="grid grid-cols-3 gap-4">
        <UCard v-for="snippet in snippetStore.snippets" :key="snippet.id" class="relative">
          <template #header>
            <div class="font-bold">{{ snippet.title }}</div>
          </template>
          <div class="text-sm whitespace-pre-wrap font-mono bg-gray-50 dark:bg-gray-900 p-2 rounded-md">
            {{ snippet.content }}
          </div>
        </UCard>
      </div>

      <div v-else class="text-center text-gray-500 py-10">
        Сниппетов пока нет
      </div>
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
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useTechnologyStore } from '@/stores/technology'
import { useSnippetStore } from '@/stores/snippets'
import ModalCreateSnippet from '@/components/snippets/ModalCreateSnippet.vue'

const route = useRoute()
const techStore = useTechnologyStore()
const snippetStore = useSnippetStore()

const isModalAboutOpen = ref(false)

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
