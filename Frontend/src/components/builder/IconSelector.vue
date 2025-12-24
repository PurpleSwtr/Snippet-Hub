<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const props = defineProps<{
  modelValue: string // v-model binding
}>()

const emit = defineEmits(['update:modelValue'])

const icons = ref<string[]>([])
const search = ref('')
const isLoading = ref(false)

onMounted(async () => {
  isLoading.value = true
  try {
    const res = await fetch('http://localhost:8000/api/v1/icons/namelist/all')
    if (res.ok) {
      icons.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
})

const filteredIcons = computed(() =>
  icons.value.filter(icon => icon.toLowerCase().includes(search.value.toLowerCase()))
)

const selectIcon = (icon: string) => {
  emit('update:modelValue', icon)
}
</script>

<template>
  <div class="space-y-2">
    <!-- <UInput
      v-model="search"
      icon="i-heroicons-magnifying-glass"
      placeholder="Поиск иконки..."
      size="sm"
    /> -->

    <div class="border border-gray-200 dark:border-gray-700 rounded-md p-2 h-128 overflow-y-auto bg-gray-50 dark:bg-gray-900">
      <div v-if="isLoading" class="text-center text-sm text-gray-500 py-4">Загрузка...</div>

      <div v-else class="grid grid-cols-8 sm:grid-cols-8 gap-2">
        <button
          v-for="icon in filteredIcons"
          :key="icon"
          type="button"
          @click="selectIcon(icon)"
          class="aspect-square flex items-center justify-center p-1 rounded hover:bg-white dark:hover:bg-gray-800 border border-transparent hover:border-primary-500 transition-all"
          :class="{'bg-white dark:bg-gray-800 border-primary-500 ring-1 ring-primary-500': modelValue === icon}"
          :title="icon"
        >
          <img :src="`/icons/all/${icon}`" class="w-24 h-24 object-contain" loading="lazy" />
        </button>
      </div>

      <div v-if="!isLoading && filteredIcons.length === 0" class="text-center text-xs text-gray-500 mt-2">
        Ничего не найдено
      </div>
    </div>

    <!-- <div v-if="modelValue" class="text-xs text-gray-500">
      Выбрано: <span class="font-mono text-primary-500">{{ modelValue }}</span>
    </div> -->
  </div>
</template>
