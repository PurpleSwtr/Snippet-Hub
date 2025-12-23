<script setup lang="ts">
const links = [
  { label: 'Builder', to: '/', icon: 'i-heroicons-wrench-screwdriver' },
  { label: 'Templates', to: '/templates', icon: 'i-heroicons-document-duplicate' },
  { label: 'Settings', to: '/settings', icon: 'i-heroicons-cog-6-tooth' }
]
</script>

<template>
  <header class="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
    <UContainer class="flex justify-between items-center h-16">
      <div class="flex items-center gap-2">
        <UIcon name="i-heroicons-cube-transparent" class="w-8 h-8 text-primary-500" />
        <h1 class="text-xl font-bold text-gray-900 dark:text-white">Tech-Docs</h1>
      </div>

      <nav class="flex gap-4">
        <UButton
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          :icon="link.icon"
          variant="ghost"
          color="gray"
          :label="link.label"
        />
      </nav>

      <div class="flex items-center gap-2">
        <UColorModeButton class="hover:cursor-pointer"/>
        <UButton icon="i-heroicons-user" color="gray" variant="ghost" />
      </div>
    </UContainer>
  </header>
</template>
