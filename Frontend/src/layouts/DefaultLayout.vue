<script setup lang="ts">
import Header from '@/components/ui/Header.vue'
import Sidebar from '@/components/ui/Sidebar.vue'
import Footer from '@/components/ui/Footer.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
    <Header />
    <div class="flex flex-1 overflow-hidden">
      <Sidebar />
      <main class="flex-1 overflow-y-auto p-8">
        <UContainer>
          <slot />
        </UContainer>
      </main>
    </div>
    <Footer />
  </div>
</template>


<!-- <script setup lang="ts">

</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
    <Header></Header>

    <main class="flex-1 py-6">
      <UContainer>
        <slot />
      </UContainer>
    </main>

    <Footer></Footer>
  </div>
</template> -->
