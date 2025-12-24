<template>
  <UPage>

    <div class="space-y-10">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Tech-Snippets
          </h1>
          <p class="text-gray-500 dark:text-gray-400 mt-2">
            Выберите технологию на боковой панели, чтобы просмотреть ее сниппеты.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <TechCard
        v-for="tech in technologyStore.technologies"
        :key="tech.id"
        :name="tech.name"
        :icon="tech.icon"
        :description="tech.description"
        />
      </div>

    </div>
  </UPage>
</template>

<script setup lang="ts">
import { useTechnologyStore } from '@/stores/technology'
import TechCard from '@/components/TechCard.vue'
const technologyStore = useTechnologyStore()
</script>
