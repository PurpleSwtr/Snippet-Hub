<template>
  <RouterLink
    :to="`/technology/${name}`"
    class="flex flex-col items-center text-center bg-white dark:bg-gray-800 p-6 rounded-lg border border-gray-200 dark:border-gray-700 cursor-pointer transition-colors hover:border-indigo-500 duration-200 overflow-hidden"
  >
    <div class="mb-4">
      <PrimeIcon
      v-if="icon"
      :icon="icon"
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
  </RouterLink>
</template>

<script setup lang="ts">
defineProps<{
  name: string
  icon?: string
  description?: string
}>()
</script>
