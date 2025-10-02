import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Ativos from '../views/Ativos.vue'
import Chamados from '../views/Chamados.vue'
import Usuarios from '../views/Usuarios.vue'
import Configuracoes from '../views/Configuracoes.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/ativos',
      name: 'ativos',
      component: Ativos
    },
    {
      path: '/chamados',
      name: 'chamados',
      component: Chamados
    },
    {
      path: '/usuarios',
      name: 'usuarios',
      component: Usuarios
    },
    {
      path: '/configuracoes',
      name: 'configuracoes',
      component: Configuracoes
    }
  ]
})

export default router