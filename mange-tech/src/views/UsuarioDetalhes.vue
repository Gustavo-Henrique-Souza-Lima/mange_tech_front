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
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col h-full">
            <div class="h-24 bg-gradient-to-r from-indigo-500 to-purple-600"></div>
            
            <div class="px-6 pb-6 relative flex-1 flex flex-col">
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
                
                <div class="mt-3 flex justify-center gap-2 flex-wrap">
                  <span v-if="usuario.user?.is_superuser" class="px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-200">
                    Administrador
                  </span>
                  <span v-else-if="usuario.user?.groups?.includes('SUPERVISOR')" class="px-3 py-1 rounded-full text-xs font-semibold bg-orange-100 text-orange-800 border border-orange-200">
                    Supervisor
                  </span>
                  <span v-else-if="usuario.user?.groups?.includes('TECNICO')" class="px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-200">
                    Técnico
                  </span>
                  <span v-else class="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-600 border border-gray-200">
                    Padrão
                  </span>
                </div>
              </div>

              <hr class="border-gray-100 mb-4">

              <div class="space-y-3 mb-6">
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

              <div v-if="podeEditar" class="mt-auto pt-4 border-t border-gray-100 grid grid-cols-2 gap-3">
                <button 
                  @click="abrirModalEdicao"
                  class="flex items-center justify-center gap-2 px-4 py-2 bg-indigo-50 text-indigo-700 rounded-lg text-sm font-bold hover:bg-indigo-100 transition"
                >
                  <Edit2 :size="16" /> Editar
                </button>
                <button 
                  @click="abrirModalExclusao"
                  class="flex items-center justify-center gap-2 px-4 py-2 bg-red-50 text-red-600 rounded-lg text-sm font-bold hover:bg-red-100 transition"
                >
                  <Trash2 :size="16" /> Excluir
                </button>
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

    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4 backdrop-blur-sm" @click.self="fecharModais">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl animate-scale-in">
        <div class="flex items-center justify-between p-6 border-b border-gray-100 sticky top-0 bg-white z-10">
          <h3 class="text-xl font-bold text-gray-800">Editar Perfil</h3>
          <button @click="fecharModais" class="text-gray-400 hover:text-gray-600"><X :size="24" /></button>
        </div>

        <form @submit.prevent="salvarEdicao" class="p-6 space-y-5">
          <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-100">
            <h4 class="text-xs font-bold text-indigo-700 uppercase tracking-wide mb-2">Permissões e Cargo</h4>
            <div class="flex flex-wrap gap-4">
              <label class="flex items-center gap-2 cursor-pointer hover:opacity-80">
                <input type="radio" v-model="editForm.cargo" value="admin" class="text-indigo-600 focus:ring-indigo-500">
                <span class="text-sm font-medium text-gray-700">Administrador</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer hover:opacity-80">
                <input type="radio" v-model="editForm.cargo" value="supervisor" class="text-indigo-600 focus:ring-indigo-500">
                <span class="text-sm font-medium text-gray-700">Supervisor</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer hover:opacity-80">
                <input type="radio" v-model="editForm.cargo" value="tecnico" class="text-indigo-600 focus:ring-indigo-500">
                <span class="text-sm font-medium text-gray-700">Técnico</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer hover:opacity-80">
                <input type="radio" v-model="editForm.cargo" value="padrao" class="text-indigo-600 focus:ring-indigo-500">
                <span class="text-sm font-medium text-gray-700">Usuário Padrão</span>
              </label>
            </div>
            <div class="mt-3 flex items-center gap-2 pt-2 border-t border-indigo-200">
               <input type="checkbox" v-model="editForm.is_active" id="statusAtivo" class="rounded text-indigo-600 focus:ring-indigo-500">
               <label for="statusAtivo" class="text-sm text-gray-700 font-medium">Conta Ativa (Login permitido)</label>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1">Nome</label>
              <input v-model="editForm.first_name" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1">Sobrenome</label>
              <input v-model="editForm.last_name" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required />
            </div>
            <div class="sm:col-span-2">
              <label class="block text-xs font-bold text-gray-700 mb-1">Email</label>
              <input v-model="editForm.email" type="email" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1">Telefone</label>
              <input v-model="editForm.telefone" type="tel" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1">NIF/CPF</label>
              <input v-model="editForm.nif" type="text" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" />
            </div>
            <div class="sm:col-span-2">
              <label class="block text-xs font-bold text-gray-700 mb-1">Endereço</label>
              <input v-model="editForm.endereco" type="text" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" />
            </div>
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-100">
            <button type="button" @click="fecharModais" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700" :disabled="salvando">Cancelar</button>
            <button type="submit" class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-bold shadow-md flex items-center gap-2" :disabled="salvando">
              <span v-if="salvando" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ salvando ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4 backdrop-blur-sm" @click.self="fecharModais">
      <div class="bg-white rounded-xl w-full max-w-sm p-6 shadow-2xl animate-scale-in text-center">
        <div class="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-red-600">
          <Trash2 :size="32" />
        </div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Excluir Usuário?</h3>
        <p class="text-sm text-gray-600 mb-6">
          Você está prestes a remover permanentemente <strong>{{ usuario.user?.username }}</strong>.
        </p>
        <div class="flex gap-3 justify-center">
          <button @click="fecharModais" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex-1" :disabled="salvando">Cancelar</button>
          <button @click="confirmarExclusao" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-bold shadow-md flex-1 flex justify-center items-center gap-2" :disabled="salvando">
            <span v-if="salvando" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ salvando ? 'Apagando...' : 'Sim, Excluir' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import usuariosService from '@/api/usuariosService'
import { 
  User, Mail, Phone, Calendar, MapPin, 
  Shield, ArrowLeft, AlertCircle, Edit2, Trash2, X 
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const usuario = ref(null)
const currentUser = ref(null) // Dados do usuário LOGADO
const loading = ref(true)
const error = ref(null)
const salvando = ref(false)

// Estados dos Modais
const showEditModal = ref(false)
const showDeleteModal = ref(false)

// Formulário de Edição
const editForm = reactive({
  first_name: '',
  last_name: '',
  email: '',
  telefone: '',
  nif: '',
  endereco: '',
  cargo: 'padrao', // padrao, admin, tecnico, supervisor
  is_active: true
})

// --- SEGURANÇA NO FRONTEND ---
// Só mostra botões de ação se o usuário logado for ADMIN ou SUPERVISOR
const podeEditar = computed(() => {
  if (!currentUser.value) return false
  const user = currentUser.value.user
  if (user.is_superuser) return true // Admin supremo
  
  const groups = user.groups || []
  return groups.includes('ADMIN') || groups.includes('SUPERVISOR')
})

const carregarUsuario = async () => {
  loading.value = true
  error.value = null
  const id = route.params.id

  if (!id || id === 'undefined') {
    error.value = 'ID inválido.'
    loading.value = false
    return
  }

  try {
    const response = await usuariosService.getById(id)
    usuario.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Usuário não encontrado.'
  } finally {
    loading.value = false
  }
}

// Abrir modal e preencher dados
const abrirModalEdicao = () => {
  if (!usuario.value) return
  
  const u = usuario.value
  const user = u.user || {}

  editForm.first_name = user.first_name || ''
  editForm.last_name = user.last_name || ''
  editForm.email = user.email || ''
  editForm.telefone = u.telefone || ''
  editForm.nif = u.nif || ''
  editForm.endereco = u.endereco || ''
  editForm.is_active = user.is_active

  // Determinar cargo atual para o Radio Button
  if (user.is_superuser) editForm.cargo = 'admin'
  else {
    const groups = user.groups || []
    if (groups.includes('ADMIN')) editForm.cargo = 'admin'
    else if (groups.includes('SUPERVISOR')) editForm.cargo = 'supervisor'
    else if (groups.includes('TECNICO')) editForm.cargo = 'tecnico'
    else editForm.cargo = 'padrao'
  }

  showEditModal.value = true
}

const abrirModalExclusao = () => {
  showDeleteModal.value = true
}

const fecharModais = () => {
  if (salvando.value) return
  showEditModal.value = false
  showDeleteModal.value = false
}

const salvarEdicao = async () => {
  salvando.value = true
  try {
    const id = usuario.value.id
    
    // Mapeamento: Valor do Radio (Frontend) -> Nome do Grupo (Backend)
    const cargoMap = {
        'admin': 'ADMIN',
        'supervisor': 'SUPERVISOR',
        'tecnico': 'TECNICO',
        'padrao': 'USUARIO'
    }

    const payloadUser = {
      first_name: editForm.first_name,
      last_name: editForm.last_name,
      email: editForm.email,
      is_active: editForm.is_active,
      cargo: cargoMap[editForm.cargo] // Envia 'TECNICO', 'ADMIN', etc.
    }

    await usuariosService.updateUser(id, payloadUser)

    await usuariosService.updateProfile(id, {
      telefone: editForm.telefone,
      endereco: editForm.endereco,
      nif: editForm.nif
    })

    alert('Perfil atualizado com sucesso!')
    fecharModais()
    await carregarUsuario() // Recarrega os dados
  } catch (err) {
    console.error(err)
    alert('Erro ao atualizar: ' + (err.response?.data?.error || 'Verifique os dados.'))
  } finally {
    salvando.value = false
  }
}

const confirmarExclusao = async () => {
  salvando.value = true
  try {
    await usuariosService.delete(usuario.value.id)
    alert('Usuário removido com sucesso.')
    router.push('/usuarios')
  } catch (err) {
    console.error(err)
    alert('Erro ao excluir usuário.')
  } finally {
    salvando.value = false
  }
}

// Helpers Visuais
const getNomeCompleto = (u) => u?.user?.first_name ? `${u.user.first_name} ${u.user.last_name}` : u?.user?.username || 'Usuário'
const getIniciais = (u) => (u?.user?.username || 'U').substring(0, 2).toUpperCase()
const formatarData = (d) => d ? new Date(d).toLocaleDateString('pt-BR') : '-'
const formatarDataHora = (d) => d ? new Date(d).toLocaleString('pt-BR') : '-'

onMounted(async () => {
  // 1. Busca quem é o usuário atual para ver se ele pode ver os botões
  try {
    const me = await usuariosService.getMe()
    currentUser.value = me.data
  } catch (e) {
    console.error('Erro ao identificar usuário atual', e)
  }

  // 2. Carrega o perfil que estamos visitando
  carregarUsuario()
})
</script>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.2s ease-out forwards;
}
@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>