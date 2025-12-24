<template>
  <UPage>
    <div class="space-y-6">

      <div class="grid grid-cols-2 justify-between gap-2">
        <UInput
          v-model="form.name"
          placeholder="Название"
          color="gray"
        />
        <UInput
          v-model="form.description"
          placeholder="Короткое описание"
          color="gray"
        />
      </div>
      <div class="h-auto">
        <UTextarea
          v-model="form.about"
          class="w-full"
          placeholder="Подробное описание"
          color="gray"
          autoresize
          :rows="5"
          :ui="{ base: 'overflow-hidden' }"
        />
      </div>

      <IconSelector v-model="form.icon" />

      <div class="flex justify-center items-center pt-5">
        <div class="flex justify-center w-full">
          <UButton
            icon="i-heroicons-plus"
            size="xl"
            color="neutral"
            variant="subtle"
            class="cursor-pointer w-full"
            :loading="isLoading"
            @click="handleSubmit"
          >
            Создать технологию
          </UButton>
        </div>
      </div>

    </div>
  </UPage>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useTechnologyStore } from '@/stores/technology';
import IconSelector from '@/components/builder/IconSelector.vue'

const techStore = useTechnologyStore();
const toast = useToast();

const isLoading = ref(false);

const form = reactive({
  name: '',
  description: '',
  about: '',
  icon: ''
});

async function handleSubmit() {
  if (!form.name || !form.description) {
    toast.add({
      title: 'Ошибка',
      description: 'Заполните хотя бы название и краткое описание.',
      color: 'red'
    });
    return;
  }

  isLoading.value = true;

  try {
    await techStore.createTechnology({
      name: form.name,
      description: form.description,
      about: form.about,
      icon: form.icon
    });

    toast.add({
      title: 'Успешно!',
      description: `Технология ${form.name} создана.`,
      color: 'green'
    });

    form.name = '';
    form.description = '';
    form.about = '';
    form.icon = '';

  } catch (error: any) {
    toast.add({
      title: 'Ошибка сервера',
      description: error.message || 'Не удалось создать технологию.',
      color: 'red'
    });
  } finally {
    isLoading.value = false;
  }
}
</script>
