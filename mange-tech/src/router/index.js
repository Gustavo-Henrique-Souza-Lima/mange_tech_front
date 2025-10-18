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

// Guard de navegação MELHORADO
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = authService.isAuthenticated()

  console.log('Navegação:', {
    to: to.path,
    requiresAuth,
    isAuthenticated,
    token: localStorage.getItem('token')
  })

  if (requiresAuth && !isAuthenticated) {
    // Precisa de autenticação mas não está autenticado
    console.log('Redirecionando para login - não autenticado')
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    // Já está autenticado e tentando acessar login
    console.log('Redirecionando para dashboard - já autenticado')
    next('/')
  } else {
    // Tudo certo, pode navegar
    console.log('Navegação permitida')
    next()
  }
})

export default router