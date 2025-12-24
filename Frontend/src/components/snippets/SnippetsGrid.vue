<template>
  <div v-if="isLoading" class="space-y-4">
    <USkeleton class="h-24 w-full" v-for="n in 3" :key="n" />
  </div>

  <div v-else-if="snippets.length > 0" class="grid grid-cols-3 gap-4">
    <SnippetCard
      v-for="snippet in snippets"
      :key="snippet.id"
      :snippet="snippet"
    />
  </div>

  <div v-else class="text-center text-gray-500 py-10">
    Сниппетов пока нет
  </div>
</template>

<script setup lang="ts">
import SnippetCard from './Card/SnippetCard.vue';

defineProps<{
  snippets: any[]
  isLoading: boolean
}>()
</script>
