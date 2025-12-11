import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/api/authService'
import usuariosService from '@/api/usuariosService' 

import Login from '../views/Login.vue'
import Cadastro from '../views/Cadastro.vue'
import Dashboard from '../views/Dashboard.vue'
import Ativos from '../views/Ativos.vue'
import Chamados from '../views/Chamados.vue'
import Usuarios from '../views/Usuarios.vue'
import Configuracoes from '../views/Configuracoes.vue'
import ChamadoDetalhes from '../views/ChamadoDetalhes.vue'
import Ambientes from '../views/Ambientes.vue'
import AtivoDetalhes from '../views/AtivosDetalhes.vue'
import UsuarioDetalhes from '@/views/UsuarioDetalhes.vue'
import MeuPerfil from '@/views/MeuPerfil.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresAuth: false }
    },
    {
      path: '/cadastro',
      name: 'cadastro',
      component: Cadastro,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true, roles: ['ADMIN', 'TECNICO', 'SUPERVISOR'] }
    },
    {
      path: '/ativos',
      name: 'ativos',
      component: Ativos,
      meta: { requiresAuth: true }
    },
    {
      path: '/chamados',
      name: 'chamados',
      component: Chamados,
      meta: { requiresAuth: true }
    },
    {
      path: '/usuarios',
      name: 'usuarios',
      component: Usuarios,
      meta: { requiresAuth: true, roles: ['ADMIN', 'SUPERVISOR'] }
    },
    {
      path: '/usuarios/:id',
      name: 'usuario-detalhes',
      component: UsuarioDetalhes,
      meta: { requiresAuth: true, roles: ['ADMIN', 'SUPERVISOR'] }
    },
    {
      path: '/configuracoes',
      name: 'configuracoes',
      component: Configuracoes,
      meta: { requiresAuth: true }
    },
    {
      path: '/chamados/:id',
      name: 'chamado-detalhes',
      component: ChamadoDetalhes,
      meta: { requiresAuth: true }
    },
    {
      path: '/ambientes',
      name: 'ambientes',
      component: Ambientes,
      meta: { requiresAuth: true }
    },
    {
      path: '/ativos/:id',
      name: 'ativo-detalhes',
      component: AtivoDetalhes,
      meta: { requiresAuth: true }
    },
    {
      path: '/perfil',
      name: 'meu-perfil',
      component: MeuPerfil,
      meta: { requiresAuth: true } // Todos logados podem ver
    },
  ]
})

// --- GUARD DE PROTEÇÃO ---
router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = authService.isAuthenticated()

  if (requiresAuth && !isAuthenticated) {
    return next('/login')
  }
  else if ((to.path === '/login' || to.path === '/cadastro') && isAuthenticated) {
    return next('/')
  }

  if (isAuthenticated && to.meta.roles) {
    try {
      const res = await usuariosService.getMe()
      const user = res.data.user

      const isSuperUser = user.is_superuser

      const userGroups = user.groups || []

      const temPermissao = isSuperUser || to.meta.roles.some(role => userGroups.includes(role))

      if (!temPermissao) {
        console.warn(`⛔ Acesso negado a ${to.path}. Redirecionando para Chamados.`)
        return next('/chamados') // Joga usuário comum para tela segura
      }
    } catch (error) {
      console.error('Erro ao verificar permissão:', error)

      return next('/chamados')
    }
  }

  next()
})

export default router