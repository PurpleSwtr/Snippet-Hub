<template>
  <div v-if="type === SnippetType.CODE">
    <pre class="font-mono text-xs bg-gray-100 dark:bg-gray-900 p-2 rounded border border-gray-100 dark:border-gray-800 whitespace-pre-wrap break-all overflow-hidden"><code v-html="highlightedCode" class="bg-transparent p-0"></code></pre>
  </div>

  <div
    v-else-if="type === SnippetType.MARKDOWN"
    class="markdown-preview prose dark:prose-invert max-w-none text-xs leading-snug wrap-break-word"
    v-html="renderedMarkdown"
  ></div>

  <div v-else class="whitespace-pre-wrap wrap-break-word font-mono text-xs text-gray-700 dark:text-gray-300">
    {{ content }}
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { SnippetType } from '@/types/snippet';
import { marked } from 'marked';
import hljs from 'highlight.js';
import 'highlight.js/styles/monokai.min.css';

const props = defineProps<{
  type: SnippetType;
  content: string;
}>();

const highlightedCode = computed(() => {
  if (!props.content) return '';
  try {
    return hljs.highlightAuto(props.content).value;
  } catch (e) {
    return props.content;
  }
});

const renderedMarkdown = computed(() => {
  if (!props.content) return '';
  return marked.parse(props.content, { async: false });
});
</script>

<style>
.markdown-preview h1, .markdown-preview h2, .markdown-preview h3 {
  font-weight: bold;
  font-size: 1.1em;
  margin-bottom: 0.5rem;
  margin-top: 0.5rem;
}
.markdown-preview ul { list-style-type: disc; padding-left: 1rem; }
.markdown-preview ol { list-style-type: decimal; padding-left: 1rem; }
.markdown-preview pre {
  background: #282c34;
  padding: 0.5rem;
  border-radius: 4px;
  color: #fff;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>
