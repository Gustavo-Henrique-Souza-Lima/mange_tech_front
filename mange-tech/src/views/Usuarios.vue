<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    
    <div class="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 flex items-center gap-2">👥 Gestão de Usuários</h2>
        <p class="text-sm text-gray-500 mt-1">Administre acessos e permissões do sistema</p>
      </div>
      <button 
        @click="abrirModalNovo"
        class="bg-indigo-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 shadow-sm flex items-center gap-2 transition-all transform hover:scale-105 w-full sm:w-auto justify-center"
      >
        <Plus :size="18" /> Novo Usuário
      </button>
    </div>

    <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 mb-6">
      <div class="relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input v-model="searchTerm" type="text" placeholder="Buscar por nome, email ou username..." class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-50 focus:bg-white transition-colors" />
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-10 w-10 border-4 border-indigo-600 border-t-transparent"></div>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex justify-between items-center">
      <span>{{ error }}</span>
      <button @click="buscarUsuarios" class="text-sm font-medium hover:underline">Tentar novamente</button>
    </div>

    <div v-else>
      <div class="hidden lg:block bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Usuário</th>
              <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Cargo</th>
              <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Contato</th>
              <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase">Cadastro</th>
              <th class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="perfil in usuariosFiltrados" :key="perfil.id" @click="irParaDetalhes(perfil.id)" class="hover:bg-indigo-50 transition-colors group cursor-pointer">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold border border-indigo-200 text-sm">
                    {{ getIniciais(perfil) }}
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ getNomeCompleto(perfil) }}</div>
                    <div class="text-xs text-gray-500">@{{ perfil.user?.username }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                 <span v-if="perfil.user?.is_superuser" class="px-2 py-1 rounded text-xs font-bold bg-purple-100 text-purple-700">ADMIN</span>
                 <span v-else-if="perfil.user?.groups?.includes('TECNICO')" class="px-2 py-1 rounded text-xs font-bold bg-blue-100 text-blue-700">TÉCNICO</span>
                 <span v-else-if="perfil.user?.groups?.includes('SUPERVISOR')" class="px-2 py-1 rounded text-xs font-bold bg-orange-100 text-orange-700">SUPERVISOR</span>
                 <span v-else class="px-2 py-1 rounded text-xs font-bold bg-gray-100 text-gray-700">PADRÃO</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ perfil.user?.email }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatarData(perfil.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click.stop="abrirModalEditar(perfil)" class="text-blue-400 hover:text-blue-600 mr-3"><Edit2 :size="18" /></button>
                <button @click.stop="confirmarRemocao(perfil)" class="text-red-400 hover:text-red-600"><Trash2 :size="18" /></button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="lg:hidden space-y-4">
         <div v-for="perfil in usuariosFiltrados" :key="perfil.id" @click="irParaDetalhes(perfil.id)" class="bg-white rounded-xl border border-gray-200 p-5 shadow-sm active:bg-gray-50 cursor-pointer">
            <div class="flex justify-between mb-2">
               <span class="font-bold text-gray-900">{{ getNomeCompleto(perfil) }}</span>
               <ChevronRight :size="20" class="text-gray-400"/>
            </div>
            <p class="text-xs text-gray-500 mb-4">{{ perfil.user?.email }}</p>
            <div class="flex gap-2">
               <button @click.stop="abrirModalEditar(perfil)" class="flex-1 py-2 bg-blue-50 text-blue-600 rounded text-xs font-bold">EDITAR</button>
               <button @click.stop="confirmarRemocao(perfil)" class="flex-1 py-2 bg-red-50 text-red-600 rounded text-xs font-bold">REMOVER</button>
            </div>
         </div>
      </div>
    </div>

    <div v-if="mostrarModal" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4 backdrop-blur-sm" @click.self="fecharModal">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl animate-scale-in">
        
        <div class="flex items-center justify-between p-6 border-b border-gray-100 sticky top-0 bg-white z-10">
          <div>
            <h3 class="text-xl font-bold text-gray-800">{{ editando ? 'Editar Usuário' : 'Novo Usuário' }}</h3>
            <p class="text-xs text-gray-500 mt-0.5">{{ editando ? 'Atualize os dados' : 'Crie um novo acesso ao sistema' }}</p>
          </div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600"><X :size="20" /></button>
        </div>

        <form @submit.prevent="salvarUsuario" class="p-6 space-y-5">
          
          <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-100">
            <h4 class="text-xs font-bold text-indigo-700 uppercase tracking-wide mb-3">Definir Cargo</h4>
            <div class="flex flex-wrap gap-4">
              
              <label class="flex items-center gap-2 cursor-pointer" :class="{ 'opacity-50 cursor-not-allowed': !souAdmin }">
                <input type="radio" v-model="formUsuario.cargo" value="ADMIN" class="text-indigo-600 focus:ring-indigo-500" :disabled="!souAdmin">
                <span class="text-sm font-medium text-gray-700">Administrador</span>
              </label>

              <label class="flex items-center gap-2 cursor-pointer" :class="{ 'opacity-50 cursor-not-allowed': !souAdmin }">
                <input type="radio" v-model="formUsuario.cargo" value="SUPERVISOR" class="text-indigo-600 focus:ring-indigo-500" :disabled="!souAdmin">
                <span class="text-sm font-medium text-gray-700">Supervisor</span>
              </label>

              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="formUsuario.cargo" value="TECNICO" class="text-indigo-600 focus:ring-indigo-500">
                <span class="text-sm font-medium text-gray-700">Técnico</span>
              </label>

              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" v-model="formUsuario.cargo" value="USUARIO" class="text-indigo-600 focus:ring-indigo-500">
                <span class="text-sm font-medium text-gray-700">Usuário Padrão</span>
              </label>
            </div>
            
            <p v-if="!souAdmin" class="text-[10px] text-orange-600 mt-2 font-medium">
              * Você precisa de credenciais de Administrador para criar outros Admins ou Supervisores.
            </p>
          </div>

          <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-4">
            <h4 class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Login</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">Username <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.username" type="text" required :disabled="editando" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 bg-white disabled:bg-gray-100" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">Email <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.email" type="email" required :disabled="editando" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 bg-white disabled:bg-gray-100" />
              </div>
            </div>
            <div v-if="!editando" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">Senha <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.password" type="password" required minlength="6" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 bg-white" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">Confirmar Senha</label>
                <input v-model="formUsuario.password_confirm" type="password" required class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 bg-white" />
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
             <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">Nome</label>
                <input v-model="formUsuario.first_name" type="text" required class="w-full px-3 py-2 border rounded-lg" />
             </div>
             <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">Sobrenome</label>
                <input v-model="formUsuario.last_name" type="text" required class="w-full px-3 py-2 border rounded-lg" />
             </div>
             <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">Telefone</label>
                <input v-model="formUsuario.telefone" type="tel" class="w-full px-3 py-2 border rounded-lg" />
             </div>
             <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1">CPF/NIF</label>
                <input v-model="formUsuario.nif" type="text" class="w-full px-3 py-2 border rounded-lg" />
             </div>
          </div>

          <div v-if="erroForm" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex items-center gap-2">⚠️ {{ erroForm }}</div>

          <div class="flex justify-end pt-4 border-t border-gray-100 gap-3">
            <button type="button" @click="fecharModal" class="px-5 py-2.5 border rounded-lg hover:bg-gray-50 text-gray-700" :disabled="salvando">Cancelar</button>
            <button type="submit" class="px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-bold shadow-md" :disabled="salvando">
              {{ salvando ? 'Salvando...' : (editando ? 'Atualizar' : 'Criar Conta') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="mostrarModalRemocao" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4">
       <div class="bg-white rounded-xl w-full max-w-sm p-6 text-center">
          <h3 class="text-xl font-bold mb-2">Tem certeza?</h3>
          <div class="flex gap-3 justify-center mt-4">
             <button @click="fecharModalRemocao" class="px-4 py-2 border rounded-lg">Cancelar</button>
             <button @click="removerUsuario" class="px-4 py-2 bg-red-600 text-white rounded-lg">Excluir</button>
          </div>
       </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Search, X, Edit2, Trash2, Eye, ChevronRight } from 'lucide-vue-next'
import usuariosService from '@/api/usuariosService'

const router = useRouter()
const usuarios = ref([])
const currentUser = ref(null) // Guardar quem sou eu
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const mostrarModal = ref(false)
const editando = ref(false)
const salvando = ref(false)
const erroForm = ref('')
const mostrarModalRemocao = ref(false)
const usuarioParaRemover = ref(null)
const removendo = ref(false)

const formUsuario = ref({
  username: '', email: '', password: '', password_confirm: '',
  first_name: '', last_name: '', telefone: '', endereco: '', nif: '',
  cargo: 'USUARIO' // Default 'padrao'
})

// Verificar se sou Admin Supremo para habilitar radio buttons
const souAdmin = computed(() => {
  if (!currentUser.value) return false
  const user = currentUser.value.user
  return user.is_superuser || (user.groups && user.groups.includes('ADMIN'))
})

const usuariosFiltrados = computed(() => {
  if (!searchTerm.value) return usuarios.value
  const termo = searchTerm.value.toLowerCase()
  return usuarios.value.filter(perfil => {
    const nome = getNomeCompleto(perfil).toLowerCase()
    const email = (perfil.user?.email || '').toLowerCase()
    return nome.includes(termo) || email.includes(termo)
  })
})

const buscarUsuarios = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await usuariosService.getAll()
    const data = response.data
    usuarios.value = data.results || (Array.isArray(data) ? data : [data])
  } catch (err) {
    error.value = 'Erro ao carregar usuários'
  } finally {
    loading.value = false
  }
}

const irParaDetalhes = (id) => {
  if (id) router.push({ name: 'usuario-detalhes', params: { id } })
}

const abrirModalNovo = () => {
  editando.value = false
  mostrarModal.value = true
  limparFormulario()
  formUsuario.value.cargo = 'USUARIO' // Reset para padrão
}

const abrirModalEditar = (perfil) => {
  const idPerfil = perfil.id || perfil.user?.id
  if (!idPerfil) return

  editando.value = true
  mostrarModal.value = true
  erroForm.value = ''
  
  // Preencher formulário
  formUsuario.value = {
    id: idPerfil,
    user_id: perfil.user?.id,
    username: perfil.user?.username || '',
    email: perfil.user?.email || '',
    first_name: perfil.user?.first_name || '',
    last_name: perfil.user?.last_name || '',
    telefone: perfil.telefone || '',
    endereco: perfil.endereco || '',
    nif: perfil.nif || '',
    password: '', 
    password_confirm: ''
  }

  // Detectar cargo atual
  const u = perfil.user || {}
  if (u.is_superuser) formUsuario.value.cargo = 'ADMIN'
  else if (u.groups && u.groups.includes('SUPERVISOR')) formUsuario.value.cargo = 'SUPERVISOR'
  else if (u.groups && u.groups.includes('TECNICO')) formUsuario.value.cargo = 'TECNICO'
  else formUsuario.value.cargo = 'USUARIO'
}

const fecharModal = () => {
  if (!salvando.value) mostrarModal.value = false
}

const limparFormulario = () => {
  formUsuario.value = {
    username: '', email: '', password: '', password_confirm: '',
    first_name: '', last_name: '', telefone: '', endereco: '', nif: '',
    cargo: 'USUARIO'
  }
  erroForm.value = ''
}

const salvarUsuario = async () => {
  salvando.value = true
  erroForm.value = ''
  
  if (!editando.value) {
    if (formUsuario.value.password !== formUsuario.value.password_confirm) {
      erroForm.value = 'As senhas não coincidem'
      salvando.value = false
      return
    }
    if (formUsuario.value.password.length < 6) {
      erroForm.value = 'Senha mínima 6 caracteres'
      salvando.value = false
      return
    }
  }
  
  try {
    const payload = {
        // Dados User
        username: formUsuario.value.username,
        email: formUsuario.value.email,
        first_name: formUsuario.value.first_name,
        last_name: formUsuario.value.last_name,
        // Dados Profile
        telefone: formUsuario.value.telefone,
        endereco: formUsuario.value.endereco,
        nif: formUsuario.value.nif,
        // Cargo (Agora o backend entende isso no CREATE!)
        cargo: formUsuario.value.cargo 
    }

    if (!editando.value) {
        payload.password = formUsuario.value.password
        // CRIAÇÃO: Usamos usuariosService (rota interna) que aceita cargo
        await usuariosService.create(payload) 
        alert('Usuário criado com sucesso!')
    } else {
        // EDIÇÃO: Lógica de atualização
        await usuariosService.updateUser(formUsuario.value.id, {
            first_name: payload.first_name,
            last_name: payload.last_name,
            email: payload.email,
            cargo: payload.cargo
        })
        await usuariosService.updateProfile(formUsuario.value.id, {
            telefone: payload.telefone,
            endereco: payload.endereco,
            nif: payload.nif
        })
        alert('Usuário atualizado!')
    }
    
    fecharModal()
    buscarUsuarios()
  } catch (err) {
    console.error(err)
    erroForm.value = err.response?.data?.error || 'Erro ao salvar. Verifique permissões.'
  } finally {
    salvando.value = false
  }
}

const confirmarRemocao = (perfil) => {
  usuarioParaRemover.value = perfil
  mostrarModalRemocao.value = true
}

const fecharModalRemocao = () => {
  if (!removendo.value) {
    mostrarModalRemocao.value = false
    usuarioParaRemover.value = null
  }
}

const removerUsuario = async () => {
  const idRemover = usuarioParaRemover.value?.id || usuarioParaRemover.value?.user?.id
  if (!idRemover) return
  removendo.value = true
  try {
    await usuariosService.delete(idRemover)
    fecharModalRemocao()
    buscarUsuarios()
  } catch (err) {
    alert('Erro ao remover: Sem permissão.')
  } finally {
    removendo.value = false
  }
}

const getNomeCompleto = (u) => u?.user?.first_name ? `${u.user.first_name} ${u.user.last_name}` : u?.user?.username || 'Usuário'
const getIniciais = (u) => (u?.user?.username || 'U').substring(0, 2).toUpperCase()
const formatarData = (d) => d ? new Date(d).toLocaleDateString('pt-BR') : '-'

onMounted(async () => {
  try {
    const me = await usuariosService.getMe()
    currentUser.value = me.data
  } catch (e) { console.error(e) }
  
  buscarUsuarios()
})
</script>

<style scoped>
.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }
@keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>