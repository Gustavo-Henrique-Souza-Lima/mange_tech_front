<template>
  <div v-if="!isAuthRoute" class="flex min-h-screen bg-gray-50">
    <aside class="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col fixed h-full z-10">
      <div class="p-6 border-b border-gray-100 flex items-center justify-center">
        <h1 class="text-xl font-bold text-indigo-600 tracking-wide">MANGE<span class="text-gray-800">TECH</span></h1>
      </div>

      <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
        
        <router-link v-if="temPermissao(['ADMIN', 'TECNICO', 'SUPERVISOR'])" to="/"
          class="flex items-center gap-3 px-4 py-3 text-gray-600 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
          active-class="bg-indigo-50 text-indigo-600 font-medium">
          <LayoutDashboard :size="20" />
          <span>Dashboard</span>
        </router-link>

        <router-link to="/chamados"
          class="flex items-center gap-3 px-4 py-3 text-gray-600 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
          active-class="bg-indigo-50 text-indigo-600 font-medium">
          <Wrench :size="20" />
          <span>Chamados</span>
        </router-link>

        <router-link to="/ativos"
          class="flex items-center gap-3 px-4 py-3 text-gray-600 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
          active-class="bg-indigo-50 text-indigo-600 font-medium">
          <Package :size="20" />
          <span>Ativos</span>
        </router-link>

        <router-link to="/ambientes"
          class="flex items-center gap-3 px-4 py-3 text-gray-600 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
          active-class="bg-indigo-50 text-indigo-600 font-medium">
          <MapPin :size="20" />
          <span>Ambientes</span>
        </router-link>

        <router-link v-if="temPermissao(['ADMIN', 'SUPERVISOR'])" to="/usuarios"
          class="flex items-center gap-3 px-4 py-3 text-gray-600 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
          active-class="bg-indigo-50 text-indigo-600 font-medium">
          <Users :size="20" />
          <span>Usuários</span>
        </router-link>

        <router-link to="/perfil"
          class="flex items-center gap-3 px-4 py-3 text-gray-600 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors relative"
          active-class="bg-indigo-50 text-indigo-600 font-medium"
        >
          <User :size="20" />
          <span class="text-sm font-medium">Meu Perfil</span>
          
          <div :title="cargoDisplay.label" class="absolute right-3 top-1/2 transform -translate-y-1/2 w-3 h-3 rounded-full border border-white" :class="cargoDisplay.color"></div>
        </router-link>

        <router-link to="/configuracoes"
          class="flex items-center gap-3 px-4 py-3 text-gray-600 rounded-lg hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
          active-class="bg-indigo-50 text-indigo-600 font-medium">
          <Settings :size="20" />
          <span>Configurações</span>
        </router-link>
      </nav>

      <div class="p-4 border-t border-gray-100">
        <button @click="logout"
          class="flex items-center gap-3 px-4 py-3 w-full text-red-500 rounded-lg hover:bg-red-50 transition-colors">
          <LogOut :size="20" />
          <span>Sair</span>
        </button>
      </div>
    </aside>

    <main class="flex-1 md:ml-64 p-8 overflow-y-auto">
      <router-view></router-view>
    </main>
  </div>

  <div v-else>
    <router-view></router-view>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LayoutDashboard, Wrench, Package, Users, Settings, LogOut, MapPin, User } from 'lucide-vue-next'
import authService from '@/api/authService'
import usuariosService from '@/api/usuariosService'

const route = useRoute()
const router = useRouter()
const currentUser = ref(null)

const isAuthRoute = computed(() => {
  return ['/login', '/cadastro'].includes(route.path)
})

// REMOVIDA: A função isActive não é mais necessária no link do perfil
// const isActive = (path) => {
//   return route.path === path
// }

// Computado para exibir o cargo e a cor no ícone
const cargoDisplay = computed(() => {
  if (!currentUser.value) {
    return { label: 'Visitante', color: 'bg-gray-400' }
  }
  const user = currentUser.value.user
  const groups = user.groups || []

  if (user.is_superuser || groups.includes('ADMIN')) {
    return { label: 'Administrador', color: 'bg-purple-600' }
  }
  if (groups.includes('SUPERVISOR')) {
    return { label: 'Supervisor', color: 'bg-orange-500' }
  }
  if (groups.includes('TECNICO')) {
    return { label: 'Técnico', color: 'bg-blue-500' }
  }
  return { label: 'Usuário Padrão', color: 'bg-green-500' }
})

// Função auxiliar para checar permissão no template
const temPermissao = (cargosPermitidos) => {
  if (!currentUser.value) return false
  const user = currentUser.value.user
  if (user.is_superuser) return true 

  if (user.groups && Array.isArray(user.groups)) {
    return user.groups.some(g => cargosPermitidos.includes(g))
  }
  return false
}

const logout = () => {
  authService.logout()
  router.push('/login')
}

onMounted(async () => {
  if (authService.isAuthenticated()) {
    try {
      const res = await usuariosService.getMe()
      currentUser.value = res.data
    } catch (e) {
      console.error('Erro ao carregar usuário', e)
    }
  }
})
</script>