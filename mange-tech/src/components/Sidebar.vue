<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { LayoutDashboard, Wrench, Package, Users, Settings, LogOut, MapPin, User } from 'lucide-vue-next'
import authService from '@/api/authService'
import usuariosService from '@/api/usuariosService'

const router = useRouter()
const route = useRoute()
const currentUser = ref(null) 

const cargoDisplay = computed(() => {
  const user = currentUser.value?.user;
  
  if (!user) return { label: 'Visitante', color: 'bg-gray-400' };
  
  const groups = user.groups || [];

  if (user.is_superuser || groups.includes('ADMIN')) {
    return { label: 'Administrador', color: 'bg-purple-600' };
  }
  if (groups.includes('SUPERVISOR')) {
    return { label: 'Supervisor', color: 'bg-orange-500' };
  }
  if (groups.includes('TECNICO')) {
    return { label: 'Técnico', color: 'bg-blue-500' };
  }
  return { label: 'Usuário Padrão', color: 'bg-green-500' };
});

const temPermissao = (cargosPermitidos) => {
  const user = currentUser.value?.user;
  if (!user) return false;
  
  if (user.is_superuser) return true; 

  const groups = user.groups || [];
  if (groups && Array.isArray(groups)) {
    return groups.some(g => cargosPermitidos.includes(g));
  }
  return false;
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
      console.error('Erro ao carregar dados do usuário logado:', e)
      // Se falhar o carregamento (token expirado), desloga e redireciona
      authService.logout()
      router.push('/login')
    }
  }
})
</script>