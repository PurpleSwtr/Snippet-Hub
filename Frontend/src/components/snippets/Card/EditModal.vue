<template>
  <div>
    <UModal
      v-model="isModalOpen"
      title="Редактирование сниппета"
      close-icon="i-heroicons-x-mark"
      :ui="{ footer: 'justify-between', content: 'max-w-3xl' }"
    >
      <UIcon
        name="i-heroicons-pencil-square"
        class="h-5 w-5 hover:scale-110 duration-300 hover:cursor-pointer hover:text-indigo-400"
        @click="openModal"
      />

      <template #body>
        <div class="h-77 m-4">
          <div class="grid grid-cols-2 gap-4 pb-4">
            <UInput
              v-model="form.title"
              placeholder="Название"
              required
              class="w-full"
              color="gray"
            />
            <USelectMenu
              placeholder="Тип сниппета"
              required
              v-model="selectedType"
              :icon="selectedType?.icon || 'i-heroicons-question-mark-circle'"
              :items="snippetTypes"
              class="w-full"
              :search-input="false"
            />
          </div>

          <USelectMenu
            v-model="tagsValue"
            icon="i-heroicons-tag"
            size="md"
            :items="availableTags"
            class="w-full"
            multiple
            placeholder="Выберите тэги"
            searchable
            creatable
            @create="onTagCreate"
          >
            <template #label>
              <span v-if="tagsValue.length" class="truncate">{{ tagsValue.join(', ') }}</span>
              <span v-else class="text-gray-500">Выберите тэги</span>
            </template>
          </USelectMenu>

          <div class="mt-4">
            <UTextarea
              v-model="form.content"
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

      <template #footer>
        <div class="flex justify-between w-full">
          <UButton
            label="Удалить"
            color="red"
            variant="ghost"
            icon="i-heroicons-trash"
            class="cursor-pointer"
            :loading="isLoading"
            @click="handleDelete"
          />

          <div class="flex gap-2">
            <UButton
              label="Отмена"
              color="gray"
              variant="ghost"
              @click="isModalOpen = false"
            />
            <UButton
              label="Сохранить"
              color="neutral"
              variant="subtle"
              class="cursor-pointer"
              :loading="isLoading"
              @click="handleUpdate"
            />
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useSnippetStore } from '@/stores/snippets';
import { useTagStore } from '@/stores/tags';
import { SnippetType } from '@/types/snippet';
import type { Snippet } from '@/types/snippet';
import type { SelectMenuItem } from '@nuxt/ui';

const props = defineProps<{
  snippet: Snippet
}>();

const snippetStore = useSnippetStore();
const tagStore = useTagStore();
const toast = useToast();

const isModalOpen = ref(false);
const isLoading = ref(false);

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

const form = reactive({
  title: '',
  content: '',
});
const selectedType = ref<SelectMenuItem>();
const tagsValue = ref<string[]>([]);

onMounted(async () => {
  if (tagStore.tags.length === 0) {
    await tagStore.fetchTags();
  }
});

const availableTags = computed(() => tagStore.tags.map(t => t.name));

function onTagCreate(label: string) {
  tagsValue.value.push(label)
}

function openModal() {
  form.title = props.snippet.title;
  form.content = props.snippet.content;

  selectedType.value = snippetTypes.find(t => t.value === props.snippet.snippet_type);

  if (props.snippet.tags && Array.isArray(props.snippet.tags)) {
    tagsValue.value = props.snippet.tags.map((t) => t.name);
  } else {
    tagsValue.value = [];
  }

  isModalOpen.value = true;
}

async function handleUpdate() {
  if (!form.title || !form.content || !selectedType.value) {
    toast.add({
      title: 'Ошибка',
      description: 'Заполните обязательные поля',
      color: 'red'
    });
    return;
  }

  isLoading.value = true;
  try {
    const formattedTags = tagsValue.value.map(tagName => ({ name: tagName }));

    await snippetStore.updateSnippet(props.snippet.id, {
      title: form.title,
      content: form.content,
      snippet_type: selectedType.value.value,
      technology_id: props.snippet.technology_id,
      tags: formattedTags
    });

    toast.add({
      title: 'Успешно',
      description: 'Сниппет обновлен',
      color: 'green'
    });
    isModalOpen.value = false;

    tagStore.fetchTags();

  } catch (e: any) {
    console.error(e)
    toast.add({
      title: 'Ошибка',
      description: e.message || 'Не удалось обновить сниппет',
      color: 'red'
    });
  } finally {
    isLoading.value = false;
  }
}

async function handleDelete() {
  if (!confirm('Вы уверены, что хотите удалить этот сниппет?')) return;

  isLoading.value = true;
  try {
    await snippetStore.deleteSnippet(props.snippet.id);
    toast.add({
      title: 'Удалено',
      description: 'Сниппет был удален',
      color: 'gray'
    });
    isModalOpen.value = false;
  } catch (e: any) {
    toast.add({
      title: 'Ошибка',
      description: e.message || 'Не удалось удалить сниппет',
      color: 'red'
    });
  } finally {
    isLoading.value = false;
  }
}
</script>
