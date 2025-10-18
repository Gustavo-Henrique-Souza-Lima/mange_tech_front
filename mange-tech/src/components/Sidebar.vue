<template>
  <div class="w-48 bg-white border-r border-gray-200 h-screen fixed left-0 top-0">
    <div class="p-4 border-b border-gray-200">
      <h1 class="text-lg font-bold text-gray-800">MANGE_TECH</h1>
    </div>
    <nav class="p-2">
      <router-link
        v-for="item in menuItems"
        :key="item.to"
        :to="item.to"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-1 transition-colors"
        :class="isActive(item.to) ? 'bg-blue-500 text-white' : 'text-gray-700 hover:bg-gray-100'"
      >
        <component :is="item.icon" :size="20" />
        <span class="text-sm font-medium">{{ item.label }}</span>
      </router-link>
      
      <!-- Botão de Logout -->
      <button
        @click="handleLogout"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-1 transition-colors text-red-600 hover:bg-red-50 mt-4"
      >
        <LogOut :size="20" />
        <span class="text-sm font-medium">Sair</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LayoutDashboard, Wrench, Package, Users, Settings, LogOut } from 'lucide-vue-next'
import authService from '@/api/authService'

const route = useRoute()
const router = useRouter()

const menuItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/chamados', icon: Wrench, label: 'Chamados' },
  { to: '/ativos', icon: Package, label: 'Ativos' },
  { to: '/usuarios', icon: Users, label: 'Usuários' },
  { to: '/configuracoes', icon: Settings, label: 'Configurações' }
]

const isActive = (path) => {
  return route.path === path
}

const handleLogout = () => {
  if (confirm('Deseja realmente sair?')) {
    authService.logout()
    router.push('/login')
  }
}
</script>