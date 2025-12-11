<template>
  <aside 
    class="w-64 bg-white border-r border-gray-200 h-screen fixed left-0 top-0 hidden md:flex flex-col z-10"
  >
    <div class="p-6 border-b border-gray-100 flex items-center justify-center">
      <h1 class="text-xl font-bold text-indigo-600 tracking-wide">MANGE<span class="text-gray-800">TECH</span></h1>
    </div>

    <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
      
      <router-link to="/"
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

      <router-link to="/usuarios"
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
</template>

<script setup>
import { useRouter } from 'vue-router'
import { LayoutDashboard, Wrench, Package, Users, Settings, LogOut, MapPin, User } from 'lucide-vue-next'
import authService from '@/api/authService'
// usuariosService não é mais necessário

const router = useRouter()

const logout = () => {
  authService.logout()
  router.push('/login')
}
</script>