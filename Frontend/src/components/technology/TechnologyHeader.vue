<template>
  <div class="flex items-center justify-between border-b border-gray-200 dark:border-gray-800 pb-4">
    <div class="flex items-center gap-4">
      <TechnologyAboutModal :tech="tech" />
      <div>
        <h1 class="text-3xl font-bold">{{ tech.name }}</h1>
        <p class="text-gray-500">{{ tech.description }}</p>
      </div>
    </div>
    <ModalCreateSnippet
      v-if="tech"
      :technology-id="tech.id" />
  </div>
</template>

<script setup lang="ts">
import ModalCreateSnippet from '@/components/snippets/ModalCreateSnippet.vue'
defineProps<{
  tech: any
}>()
</script>
