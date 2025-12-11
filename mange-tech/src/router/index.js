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

const MOCKED_USER_ADMIN = {
    id: 1,
    username: 'admin_test',
    email: 'adm@adm.com',
    is_superuser: true,           
    groups: ['ADMIN', 'TECNICO'], 
    first_name: 'Admin',
    last_name: 'test'
};

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

router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    const isAuthenticated = authService.isAuthenticated() 

    console.log(`🧭 Tentativa de navegação para: ${to.path}. Requer Autenticação: ${requiresAuth}. Está Autenticado: ${isAuthenticated}.`);

    if (requiresAuth && !isAuthenticated) {
        console.log(`🔒 Acesso negado: Rota protegida e não autenticado. Redirecionando para /login.`);
        return next('/login')
    } else if ((to.path === '/login' || to.path === '/cadastro') && isAuthenticated) {
        console.log(`🏠 Já autenticado. Redirecionando de ${to.path} para /.`);
        return next('/')
    }

    if (isAuthenticated && to.meta.roles) {
        console.log(`🔑 Verificando permissões (RBAC) para a rota: ${to.path}.`);
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
                console.error('🛑 API /me/ retornou payload vazio ou inválido. Iniciando fluxo de erro.');
                throw new Error('Erro ao obter dados de permissão.'); 
            }

            const userPayload = data.user || data 
            
            if (!userPayload || typeof userPayload !== 'object' || !('is_superuser' in userPayload)) {
                console.error('🛑 Payload do usuário é inválido ou incompleto. Falha na leitura de permissão.');
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
                console.warn(`⛔ Acesso negado a ${to.path}. User: ${userPayload.username}, Roles: [${userGroups}], Super: ${isSuperUser}. Redirecionando para /chamados.`);
                return next('/chamados')
            }
            
            console.log(`🔓 Permissão concedida para ${to.path}.`);

        } catch (error) {
            console.error('🚨 Erro crítico no fluxo de permissão:', error.message);
            if (!IS_MOCK_MODE) {
                console.log('🚪 Forçando logout devido ao erro de permissão.');
                authService.logout()
                return next('/login')
            } else {
                console.warn('⚠️ Em Modo MOCK, erro ignorado para demonstração.');
            }
        }
    }

    console.log(`⏭️ Navegação liberada para ${to.path}.`);
    next()
})

export default router