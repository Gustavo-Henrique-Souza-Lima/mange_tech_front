<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    
    <div v-if="loading" class="flex flex-col justify-center items-center h-[80vh]">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent"></div>
      <p class="text-gray-500 mt-4 font-medium">Carregando perfil...</p>
    </div>

    <div v-else-if="error" class="flex flex-col justify-center items-center h-[80vh]">
      <div class="text-red-500 mb-2">
        <AlertCircle :size="48" />
      </div>
      <h2 class="text-xl font-bold text-gray-800">Usuário não encontrado</h2>
      <p class="text-gray-500 mb-6">{{ error }}</p>
      <router-link to="/usuarios" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
        Voltar para a lista
      </router-link>
    </div>

    <div v-else-if="usuario" class="max-w-5xl mx-auto animate-fade-in-up">
      
      <div class="mb-6">
        <router-link to="/usuarios" class="inline-flex items-center text-gray-500 hover:text-indigo-600 transition font-medium">
          <ArrowLeft :size="20" class="mr-1" /> Voltar para Usuários
        </router-link>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="h-24 bg-gradient-to-r from-indigo-500 to-purple-600"></div>
            
            <div class="px-6 pb-6 relative">
              <div class="relative -mt-12 mb-4 flex justify-center">
                <div class="h-24 w-24 rounded-full bg-white p-1 shadow-md">
                  <div class="h-full w-full rounded-full bg-indigo-100 flex items-center justify-center text-2xl font-bold text-indigo-700 uppercase border border-indigo-50">
                    {{ getIniciais(usuario) }}
                  </div>
                </div>
                <div 
                  class="absolute bottom-1 right-[30%] h-5 w-5 rounded-full border-2 border-white"
                  :class="usuario.user?.is_active ? 'bg-green-500' : 'bg-red-500'"
                  :title="usuario.user?.is_active ? 'Ativo' : 'Inativo'"
                ></div>
              </div>

              <div class="text-center mb-6">
                <h1 class="text-xl font-bold text-gray-900">{{ getNomeCompleto(usuario) }}</h1>
                <p class="text-sm text-gray-500">@{{ usuario.user?.username }}</p>
                
                <div class="mt-3 flex justify-center gap-2">
                  <span v-if="usuario.user?.is_superuser" class="px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-200">
                    Administrador
                  </span>
                  <span v-else class="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-600 border border-gray-200">
                    Usuário Padrão
                  </span>
                </div>
              </div>

              <hr class="border-gray-100 mb-4">

              <div class="space-y-3">
                <div class="flex items-center text-sm text-gray-600">
                  <Mail :size="16" class="mr-3 text-gray-400" />
                  <span class="truncate">{{ usuario.user?.email || 'Sem e-mail' }}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600">
                  <Phone :size="16" class="mr-3 text-gray-400" />
                  <span>{{ usuario.telefone || 'Sem telefone' }}</span>
                </div>
                <div class="flex items-center text-sm text-gray-600">
                  <Calendar :size="16" class="mr-3 text-gray-400" />
                  <span>Membro desde {{ formatarData(usuario.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
              <User :size="20" class="mr-2 text-indigo-600" />
              Dados Pessoais
            </h3>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Nome Completo</label>
                <p class="text-gray-900 font-medium">{{ usuario.user?.first_name }} {{ usuario.user?.last_name }}</p>
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">NIF / CPF</label>
                <p class="text-gray-900 font-medium font-mono">{{ usuario.nif || 'Não informado' }}</p>
              </div>
              <div class="sm:col-span-2">
                <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Endereço</label>
                <div class="flex items-start">
                  <MapPin :size="16" class="mr-2 text-gray-400 mt-0.5" />
                  <p class="text-gray-900">{{ usuario.endereco || 'Endereço não cadastrado' }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
              <Shield :size="20" class="mr-2 text-indigo-600" />
              Segurança e Acesso
            </h3>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Username</label>
                <p class="text-gray-900 font-mono bg-gray-50 px-2 py-1 rounded inline-block border border-gray-200">
                  {{ usuario.user?.username }}
                </p>
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Último Login</label>
                <p class="text-gray-900">{{ usuario.user?.last_login ? formatarDataHora(usuario.user.last_login) : 'Nunca acessou' }}</p>
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Status da Conta</label>
                <span 
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border"
                  :class="usuario.user?.is_active ? 'bg-green-50 text-green-700 border-green-200' : 'bg-red-50 text-red-700 border-red-200'"
                >
                  {{ usuario.user?.is_active ? 'Ativa' : 'Bloqueada/Inativa' }}
                </span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import usuariosService from '@/api/usuariosService'
import { 
  User, Mail, Phone, Calendar, MapPin, 
  Shield, ArrowLeft, AlertCircle 
} from 'lucide-vue-next'

const route = useRoute()
const usuario = ref(null)
const loading = ref(true)
const error = ref(null)

const carregarUsuario = async () => {
  loading.value = true
  error.value = null
  
  const id = route.params.id

  if (!id || id === 'undefined') {
    error.value = 'ID do usuário inválido ou não fornecido.'
    loading.value = false
    return
  }

  try {
    const response = await usuariosService.getById(id)
    usuario.value = response.data
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.detail || 'Usuário não encontrado.'
  } finally {
    loading.value = false
  }
}

const getNomeCompleto = (perfil) => {
  if (!perfil?.user) return 'Usuário Desconhecido'
  const { first_name, last_name, username } = perfil.user
  if (first_name || last_name) return `${first_name || ''} ${last_name || ''}`.trim()
  return username || 'Sem Nome'
}

const getIniciais = (perfil) => {
  if (!perfil?.user) return '??'
  const { first_name, last_name, username } = perfil.user
  if (first_name && last_name) return `${first_name[0]}${last_name[0]}`.toUpperCase()
  if (username && username.length >= 2) return username.substring(0, 2).toUpperCase()
  return username ? username[0].toUpperCase() : '?'
}

const formatarData = (data) => {
  if (!data) return '-'
  return new Date(data).toLocaleDateString('pt-BR', { 
    day: '2-digit', month: 'long', year: 'numeric' 
  })
}

const formatarDataHora = (data) => {
  if (!data) return '-'
  return new Date(data).toLocaleString('pt-BR', { 
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

onMounted(() => {
  carregarUsuario()
})
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>