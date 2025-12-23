<template>
  <div class="flex flex-col items-center text-center bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer transition-colors hover:border-primary-500">

    <div class="mb-4">
      <img
        v-if="icon"
        :src="`/icons/all/${icon}`"
        :alt="name"
        class="w-20 h-20 object-contain"
      />
      <UIcon
        v-else
        name="i-heroicons-cube"
        class="w-20 h-20 text-gray-400"
      />
    </div>

    <h3 class="text-xl font-bold text-gray-900 dark:text-white">
      {{ name }}
    </h3>

  </div>
</template>

<script setup lang="ts">
defineProps<{
  name: string
  icon?: string
  description?: string
}>()
</script>
