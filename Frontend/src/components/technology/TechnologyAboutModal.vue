<!-- components/technology/TechnologyAboutModal.vue -->
<template>
  <UModal
    :title="tech.name"
    close-icon="i-lucide-arrow-right"
    :ui="{ content: 'max-w-2xl' }"
    v-model="isOpen"
  >
    <PrimeIcon
      :icon="tech.icon"
      @click="isOpen = true"
      class="hover:cursor-pointer"
    />

    <template #body>
      <div class="h-full w-full">
        <p>{{ tech.about }}</p>
      </div>
    </template>
  </UModal>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  tech: any
}>()

const isOpen = ref(false)
</script>
