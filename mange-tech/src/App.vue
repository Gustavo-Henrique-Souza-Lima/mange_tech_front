<template>
  <div v-if="!isAuthRoute" class="flex min-h-screen bg-gray-50">
    <Sidebar />
    <div class="flex-1 ml-64 p-8"> 
      <RouterView />
    </div>
  </div>
  <div v-else>
    <RouterView />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import { RouterView } from 'vue-router'

const route = useRoute()

// Verifica se a rota atual é de autenticação
const isAuthRoute = computed(() => {
  return ['/login', '/cadastro'].includes(route.path)
})
</script>