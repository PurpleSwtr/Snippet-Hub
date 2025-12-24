<template>
  <UCard class="relative hover:scale-105 duration-300 hover:shadow-xl shadow-indigo-100 flex flex-col">
    <template #header>
      <div class="flex justify-between items-center h-6">
        <p class="font-bold truncate pr-4 hover:text-indigo-400 duration-300 cursor-default" :title="snippet.title">
          {{ snippet.title }}
        </p>
        <div class="inline-flex gap-3 shrink-0">
          <ChatModal />
          <EditModal :snippet="snippet" />

          <UIcon
            name="i-heroicons-document-duplicate"
            class="h-5 w-5 hover:scale-110 duration-300 hover:cursor-pointer hover:text-indigo-400"
            @click="onClipboardClick"
          />
        </div>
      </div>
    </template>

    <div v-if="snippet.tags && snippet.tags.length" class="px-0 pb-2 flex flex-wrap gap-1">
      <UBadge
        v-for="tag in snippet.tags"
        :key="tag.id || tag.name"
        color="gray"
        variant="soft"
        size="xs"
      >
        {{ tag.name }}
      </UBadge>
    </div>

    <div class="overflow-hidden relative p-0 cursor-pointer">
       <DynamicContent
          :type="snippet.snippet_type"
          :content="snippet.content"
       />
    </div>

  </UCard>
</template>

<script setup lang="ts">
import EditModal from './EditModal.vue';
import ChatModal from './ChatModal.vue';
import DynamicContent from './DynamicContent.vue';

const props = defineProps<{
  snippet: any
}>()
const toast = useToast();

async function onClipboardClick() {
  try {
    await navigator.clipboard.writeText(props.snippet.content);
      toast.add({
      title: 'Готово!',
      description: 'Сниппет успешно скопирован.',
      color: 'success',
      icon: 'i-heroicons-check-circle'
    });
  } catch (err) {
    console.error('Ошибка при копировании текста: ', err);
  }
}
</script>
