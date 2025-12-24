<template>
  <UPage>
    <div class="flex justify-center items-center min-h-[50vh]">
      <UCard class="w-full max-w-md">
        <template #header>
          <h2 class="text-xl font-bold flex items-center gap-2">
            <UIcon name="i-heroicons-tag" class="text-indigo-500" />
            Создать новый тег
          </h2>
        </template>

        <form @submit.prevent="handleSubmit" class="space-y-4">

          <UFormGroup label="Название тега" required>
            <UInput
              v-model="form.name"
              placeholder="Например: python, bug, feature"
              icon="i-heroicons-hashtag"
              autofocus
              class="w-full"
            />
          </UFormGroup>

          <UButton
            type="submit"
            block
            size="lg"
            color="indigo"
            variant="subtle"
            :loading="isLoading"
          >
            Создать
          </UButton>
        </form>
      </UCard>
    </div>
  </UPage>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useTagStore } from '@/stores/tags'

const tagStore = useTagStore()
const toast = useToast()

const isLoading = ref(false)
const form = reactive({
  name: '',
  color: ''
})

async function handleSubmit() {
  if (!form.name.trim()) {
    toast.add({ title: 'Ошибка', description: 'Введите название тега', color: 'red' })
    return
  }

  isLoading.value = true
  try {
    await tagStore.createTag({
      name: form.name,
      color: form.color || undefined
    })

    toast.add({ title: 'Успешно', description: `Тег #${form.name} создан`, color: 'green' })

    form.name = ''
    form.color = ''
  } catch (e: any) {
    toast.add({ title: 'Ошибка', description: e.message, color: 'red' })
  } finally {
    isLoading.value = false
  }
}
</script>
