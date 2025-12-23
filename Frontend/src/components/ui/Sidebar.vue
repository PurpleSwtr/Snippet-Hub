<script setup lang="ts">
import { onMounted } from 'vue'
import { useTechnologyStore } from '@/stores/technology'
import { useRoute } from 'vue-router'

const technologyStore = useTechnologyStore()
const route = useRoute()

onMounted(() => {
  technologyStore.fetchTechnologies()
})


const getIconPath = (iconName: string) => {
  return `/icons/all/${iconName}`
}
</script>

<template>
  <aside class="w-2/10 border-r border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50 h-full overflow-y-auto flex flex-col">
    <UScrollArea
    class="w-full h-full"
    >
    <div class="p-4 flex-1">
      <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 px-2">
        Меню
      </h3>
    </div>
    <div class="p-4 flex-1">
      <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 px-2">
        Technologies
      </h3>

      <div v-if="technologyStore.isLoading" class="space-y-2 px-2">
         <USkeleton class="h-8 w-full" v-for="i in 2" :key="i" />
         <USkeleton class="h-8 max-w-3/4"/>
      </div>

      <nav v-else class="space-y-1">
        <UButton
          v-for="tech in technologyStore.technologies"
          :key="tech.id"
          :to="`/technology/${tech.name}`"
          :label="tech.name"

          variant="ghost"
          color="gray"
          block
          class="justify-start text-left"
          :class="{ 'bg-gray-100 dark:bg-gray-800 text-primary-500': route.path === `/technology/${tech.name}` }"
        >
          <template #leading>

            <img
              v-if="tech.icon"
              :src="getIconPath(tech.icon)"
              :alt="tech.name"
              class="w-5 h-5 object-contain"
            />

            <UIcon
              v-else
              name="i-heroicons-cube"
              class="w-5 h-5 text-gray-400"
            />

          </template>
        </UButton>
      </nav>

      <div v-if="technologyStore.error" class="text-red-500 text-sm mt-2 px-2">
        {{ technologyStore.error }}
      </div>
    </div>

  </UScrollArea>
  </aside>
</template>
