<template>
  <div class="relative inline-flex items-center justify-center group">
    <div
      v-if="props.icon"
      class="absolute inset-0 rounded-full bg-indigo-500 opacity-0 group-hover:opacity-60 group-hover:scale-150 blur-xl transition-all duration-300 ease-out pointer-events-none"
    ></div>
    <div
      v-if="props.icon"
      class="absolute inset-0 rounded-full bg-yellow-100 opacity-0 group-hover:opacity-40 group-hover:scale-125 transition-all duration-300 ease-out pointer-events-none blur-2xl"
    ></div>
    <img
      v-if="props.icon"
      :src="`/icons/all/${props.icon}`"
      class="w-12 h-12 object-contain relative z-10"
    />
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{
  icon?: string
}>();
</script>
