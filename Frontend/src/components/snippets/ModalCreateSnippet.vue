<template>
  <UModal
  v-model:open="isModalOpen"
  title="Создание нового сниппета"
  close-icon="i-heroicons-x-mark"
  :ui="{ footer: 'justify-end', content: 'max-w-3xl' }"
  >
  <UButton
    icon="i-heroicons-plus"
    size="xl"
    color="neutral"
    variant="subtle"
    class="cursor-pointer"
    @click="isModalOpen = true"
  >
    Новый сниппет
  </UButton>
    <template #body>
      <div class="h-77 m-4">
        <div class="grid grid-cols-2 gap-4 pb-4">
          <UInput
            v-model="newSnippetForm.title"
            placeholder="Название"
            required
            class="w-full"
            color="gray"
          />
          <USelectMenu
            placeholder="Тип сниппета"
            required
            v-model="selectedValue"
            :icon="selectedValue?.icon || 'i-heroicons-question-mark-circle'"
            :items="snippetTypes"
            class="w-full"
            :search-input="false"
          />
        </div>
        <USelectMenu
        v-model="tagsValue"
        icon="i-heroicons-tag"
        size="md"
        :items="tagsItems"
        class="w-full"
        multiple
        placeholder="Выберите тэги"
        create-item
        @create="onTagCreate"
        />
        <div class="mt-4">
          <UTextarea
            v-model="newSnippetForm.content"
            placeholder="Введите текст или код..."
            required
            :rows="10"
            class="w-full mb-7"
            color="gray"
            size="sm"
            autoresize
            :ui="{
              base: 'w-full font-mono text-sm [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]'
            }"
          />
        </div>
      </div>
    </template>

    <template #footer="{ close }">
      <UButton
        label="Отправить"
        color="neutral"
        variant="subtle"
        class="cursor-pointer"
        :loading="isLoading"
        @click="handleSubmit"
      />
    </template>
  </UModal>
</template>

<script setup lang="ts">
import { SnippetType } from '@/types/snippet';
import type { SelectMenuItem } from '@nuxt/ui';
import { reactive, ref } from 'vue';
import { useSnippetStore } from '@/stores/snippets';

const tagsItems = ref([])
const tagsValue = ref()

const props = defineProps<{
  technologyId: number
}>();

const snippetStore = useSnippetStore();
const toast = useToast();

const isLoading = ref(false);
const isModalOpen = ref(false);

function onTagCreate(item: string) {
  tagsItems.value.push(item)
  tagsValue.value = item
}

function createSnippetTypeItems(): SelectMenuItem[] {
  const meta = {
    [SnippetType.CODE]: { label: 'Код', icon: 'i-heroicons-code-bracket-square' },
    [SnippetType.MARKDOWN]: { label: 'Markdown', icon: 'i-heroicons-document-text' },
    [SnippetType.ARCHIVE]: { label: 'Архив', icon: 'i-heroicons-archive-box' },
    [SnippetType.LINK]: { label: 'Ссылка', icon: 'i-heroicons-link' },
    [SnippetType.PROMPT]: { label: 'Промпт', icon: 'i-heroicons-chat-bubble-left-right' }
  };
  return Object.values(SnippetType).map(type => ({
    label: meta[type].label,
    value: type,
    icon: meta[type].icon
  }));
}

const snippetTypes = createSnippetTypeItems();
const selectedValue = ref<SelectMenuItem>();

const newSnippetForm = reactive({
  title: '',
  content: '',
});

async function handleSubmit() {
  if (!newSnippetForm.title || !newSnippetForm.content || !selectedValue.value || !tagsValue.value) {
    toast.add({
      title: 'Ошибка валидации',
      description: 'Пожалуйста, заполните все поля.',
      color: 'warning',
      icon: 'i-heroicons-exclamation-triangle'
    });
    return;
  }

  isLoading.value = true;

  try {
    await snippetStore.createSnippet({
      title: newSnippetForm.title,
      content: newSnippetForm.content,
      snippet_type: selectedValue.value.value,
      technology_id: props.technologyId
    });

    newSnippetForm.title = '';
    newSnippetForm.content = '';
    selectedValue.value = undefined;
    isModalOpen.value = false;

    toast.add({
      title: 'Готово!',
      description: 'Сниппет успешно создан.',
      color: 'success',
      icon: 'i-heroicons-check-circle'
    });

  } catch (e: any) {
    console.error('Ошибка сохранения:', e);

    toast.add({
      title: 'Что-то пошло не так...',
      description: 'Ваш запрос не выполнен. Возможно, сниппет с таким названием уже существует.',
      icon: 'i-heroicons-wifi',
      color: 'error'
    });
  } finally {
    isLoading.value = false;
  }
}
</script>
