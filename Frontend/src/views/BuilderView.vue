<template>
  <IconSelector v-model="techForm.icon"></IconSelector>
</template>

<script setup lang="ts">
import IconSelector from '@/components/builder/IconSelector.vue'
import { useTechnologyStore } from '@/stores/technology';
import { onMounted, reactive } from 'vue';

const techStore = useTechnologyStore()

const techForm = reactive({
  name: '',
  description: '',
  icon: ''
})

onMounted(() => {
  techStore.fetchTechnologies()
})
</script>
