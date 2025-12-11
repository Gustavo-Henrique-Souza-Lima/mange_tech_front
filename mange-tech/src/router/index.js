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

// ----------------------------------------------------
// 1. DADOS MOCKADOS E CONTROLE
// ----------------------------------------------------
const MOCKED_USER_ADMIN = {
    id: 1,
    username: 'admin_test',
    email: 'adm@adm.com',
    is_superuser: true,           // SIMULA PERMISSÃO DE ADMIN/SUPER
    groups: ['ADMIN', 'TECNICO'], // SIMULA GRUPOS
    first_name: 'Admin',
    last_name: 'test'
};

// Variável de controle (Definida em .env.local como VITE_MOCK_MODE=true)
const IS_MOCK_MODE = import.meta.env.VITE_MOCK_MODE === 'true';

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
            meta: { requiresAuth: true }
        },
    ]
})

// --- GUARD DE PROTEÇÃO (RBAC) ---
router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const isAuthenticated = authService.isAuthenticated() 

    if (requiresAuth && !isAuthenticated) {
        return next('/login')
    } else if ((to.path === '/login' || to.path === '/cadastro') && isAuthenticated) {
        return next('/')
    }

    if (isAuthenticated && to.meta.roles) {
        try {
            let data;

            if (IS_MOCK_MODE) {
                console.warn('⚠️ Modo MOCK ativo: Usando dados de permissão mockados.');
                data = MOCKED_USER_ADMIN; 
            } else {
                const res = await usuariosService.getMe()
                data = res && res.data ? res.data : null; 
            }
            
            if (!data) {
                console.error('API /me/ retornou payload vazio ou inválido. Forçando logout.');
                throw new Error('Erro ao obter dados de permissão.'); 
            }

            const userPayload = data.user || data 
            
            if (!userPayload || typeof userPayload !== 'object' || !('is_superuser' in userPayload)) {
                 // Deve pegar casos onde o JSON é malformado ou incompleto
                console.error('Payload do usuário logado é inválido ou incompleto. Falha na leitura de permissão.');
                throw new Error('Payload inválido.');
            }

            console.log(`✅ Dados lidos pelo Frontend: User: ${userPayload.username}, Super: ${!!userPayload.is_superuser}, Roles: [${userPayload.groups}]`); 

            const isSuperUser = !!userPayload.is_superuser
            const userGroups = userPayload.groups || []

            let temPermissao = false;

            if (isSuperUser) {
                temPermissao = true;
            }
            else {
                const requiredRoles = to.meta.roles;
                temPermissao = requiredRoles.some(role => userGroups.includes(role));
            }

            if (!temPermissao) {
                console.warn(`⛔ Acesso negado a ${to.path}. User: ${userPayload.username}, Roles: [${userGroups}], Super: ${isSuperUser}`)
                return next('/chamados')
            }

        } catch (error) {
            console.error('Erro de verificação de permissão no router:', error)
            if (!IS_MOCK_MODE) {
                authService.logout()
                return next('/login')
            }
        }
    }

    next()
})

export default router