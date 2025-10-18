import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/api/authService'

import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Ativos from '../views/Ativos.vue'
import Chamados from '../views/Chamados.vue'
import Usuarios from '../views/Usuarios.vue'
import Configuracoes from '../views/Configuracoes.vue'

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
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
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
      meta: { requiresAuth: true }
    },
    {
      path: '/configuracoes',
      name: 'configuracoes',
      component: Configuracoes,
      meta: { requiresAuth: true }
    }
  ]
})

// Guard de navegação
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = authService.isAuthenticated()

  if (requiresAuth && !isAuthenticated) {
    // Redireciona para login se não estiver autenticado
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    // Redireciona para dashboard se já estiver autenticado
    next('/')
  } else {
    next()
  }
})

export default router