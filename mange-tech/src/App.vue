<template>
  <div class="min-h-screen bg-gray-50">
    <Sidebar />
    <div class="ml-48 p-8">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
import { RouterView } from 'vue-router'
</script>