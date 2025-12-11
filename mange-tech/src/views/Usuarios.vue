<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    
    <div class="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
          👥 Gestão de Usuários
        </h2>
        <p class="text-sm text-gray-500 mt-1">Administre acessos e permissões do sistema</p>
      </div>
      <button 
        @click="abrirModalNovo"
        class="bg-indigo-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-indigo-700 shadow-sm flex items-center gap-2 transition-all transform hover:scale-105 w-full sm:w-auto justify-center"
      >
        <Plus :size="18" />
        Novo Usuário
      </button>
    </div>

    <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 mb-6">
      <div class="relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Buscar por nome, email ou username..."
          class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-gray-50 focus:bg-white transition-colors"
        />
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
              <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Usuário</th>
              <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Contato</th>
              <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">NIF/CPF</th>
              <th class="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">Cadastro</th>
              <th class="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr 
              v-for="perfil in usuariosFiltrados" 
              :key="perfil.user?.id || perfil.id" 
              @click="irParaDetalhes(perfil.id)"
              class="hover:bg-indigo-50 transition-colors group cursor-pointer"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold border border-indigo-200 text-sm">
                      {{ getIniciais(perfil) }}
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ getNomeCompleto(perfil) }}</div>
                    <div class="text-xs text-gray-500">@{{ perfil.user?.username || 'N/A' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ perfil.user?.email || 'Sem email' }}</div>
                <div class="text-xs text-gray-500">{{ perfil.telefone || 'Sem telefone' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">{{ perfil.nif || '-' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatarData(perfil.created_at) }}</td>
              
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button @click.stop="abrirModalEditar(perfil)" class="text-blue-400 hover:text-blue-600 mr-3 p-1 rounded hover:bg-blue-50 transition" title="Editar">
                  <Edit2 :size="18" />
                </button>
                <button @click.stop="confirmarRemocao(perfil)" class="text-red-400 hover:text-red-600 p-1 rounded hover:bg-red-50 transition" title="Remover">
                  <Trash2 :size="18" />
                </button>
              </td>
            </tr>
            <tr v-if="usuariosFiltrados.length === 0">
              <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                Nenhum usuário encontrado com esse termo.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="lg:hidden space-y-4">
        <div 
          v-for="perfil in usuariosFiltrados" 
          :key="perfil.user?.id || perfil.id" 
          @click="irParaDetalhes(perfil.id)"
          class="bg-white rounded-xl border border-gray-200 p-5 shadow-sm active:bg-gray-50 cursor-pointer transition-colors"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="h-12 w-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold border border-indigo-200">
                {{ getIniciais(perfil) }}
              </div>
              <div>
                <h3 class="text-sm font-bold text-gray-900">{{ getNomeCompleto(perfil) }}</h3>
                <p class="text-xs text-gray-500">@{{ perfil.user?.username }}</p>
              </div>
            </div>
            <div class="text-gray-400">
              <ChevronRight :size="20" />
            </div>
          </div>
          
          <div class="space-y-2 text-sm text-gray-600 mb-4 border-t border-gray-100 pt-3">
            <div class="flex justify-between"><span class="text-gray-400">Email:</span> <span class="font-medium text-gray-800">{{ perfil.user?.email || '-' }}</span></div>
            <div class="flex justify-between"><span class="text-gray-400">Telefone:</span> <span class="font-medium text-gray-800">{{ perfil.telefone || '-' }}</span></div>
          </div>

          <div class="flex gap-2">
            <button @click.stop="abrirModalEditar(perfil)" class="flex-1 py-2 bg-blue-50 text-blue-600 rounded-lg text-xs font-bold uppercase tracking-wide hover:bg-blue-100 transition">Editar</button>
            <button @click.stop="confirmarRemocao(perfil)" class="flex-1 py-2 bg-red-50 text-red-600 rounded-lg text-xs font-bold uppercase tracking-wide hover:bg-red-100 transition">Remover</button>
          </div>
        </div>
        
        <div v-if="usuariosFiltrados.length === 0" class="text-center py-12 bg-white rounded-lg border border-gray-200">
          <p class="text-gray-500">Nenhum usuário encontrado</p>
        </div>
      </div>

    </div>

    <div v-if="mostrarModal" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4 backdrop-blur-sm" @click.self="fecharModal">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl animate-scale-in">
        
        <div class="flex items-center justify-between p-6 border-b border-gray-100 sticky top-0 bg-white z-10">
          <div>
            <h3 class="text-xl font-bold text-gray-800">{{ editando ? 'Editar Perfil' : 'Novo Usuário' }}</h3>
            <p class="text-xs text-gray-500 mt-0.5">{{ editando ? 'Atualize os dados cadastrais' : 'Preencha os dados para criar a conta' }}</p>
          </div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600 bg-gray-50 p-2 rounded-full transition"><X :size="20" /></button>
        </div>

        <form @submit.prevent="salvarUsuario" class="p-6 space-y-5">
          <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 space-y-4">
            <h4 class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Credenciais de Acesso</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">Username <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.username" type="text" required :disabled="editando" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white disabled:bg-gray-100 disabled:text-gray-500" placeholder="joaosilva" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">Email <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.email" type="email" required :disabled="editando" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white disabled:bg-gray-100 disabled:text-gray-500" placeholder="joao@empresa.com" />
              </div>
            </div>

            <div v-if="!editando" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">Senha <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.password" type="password" required minlength="6" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white" placeholder="******" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">Confirmar Senha <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.password_confirm" type="password" required class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white" placeholder="******" />
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <h4 class="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Informações Pessoais</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">Nome <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.first_name" type="text" required class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="João" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">Sobrenome <span class="text-red-500">*</span></label>
                <input v-model="formUsuario.last_name" type="text" required class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Silva" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">Telefone</label>
                <input v-model="formUsuario.telefone" type="tel" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="(11) 99999-9999" />
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">NIF / CPF</label>
                <input v-model="formUsuario.nif" type="text" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="000.000.000-00" />
              </div>
              <div class="sm:col-span-2">
                <label class="block text-xs font-semibold text-gray-700 mb-1.5">Endereço Completo</label>
                <input v-model="formUsuario.endereco" type="text" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Rua, Número, Bairro, Cidade" />
              </div>
            </div>
          </div>

          <div v-if="erroForm" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex items-center gap-2">
            ⚠️ {{ erroForm }}
          </div>
          <div v-if="sucessoForm" class="p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm flex items-center gap-2">
            ✅ {{ sucessoForm }}
          </div>

          <div class="flex flex-col sm:flex-row gap-3 justify-end pt-4 border-t border-gray-100">
            <button type="button" @click="fecharModal" class="px-5 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition order-2 sm:order-1" :disabled="salvando">Cancelar</button>
            <button type="submit" class="px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium shadow-md transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 order-1 sm:order-2" :disabled="salvando">
              <span v-if="salvando" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ salvando ? 'Salvando...' : (editando ? 'Salvar Alterações' : 'Criar Conta') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="mostrarModalRemocao" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4 backdrop-blur-sm" @click.self="fecharModalRemocao">
      <div class="bg-white rounded-xl w-full max-w-sm p-6 shadow-2xl animate-scale-in">
        <div class="text-center mb-6">
          <div class="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 text-red-600">
            <Trash2 :size="32" />
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Tem certeza?</h3>
          <p class="text-sm text-gray-500">
            Você está prestes a remover o usuário <strong>{{ usuarioParaRemover?.user?.username }}</strong>. Esta ação não pode ser desfeita.
          </p>
        </div>
        <div class="flex gap-3 justify-center">
          <button @click="fecharModalRemocao" class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition flex-1" :disabled="removendo">Cancelar</button>
          <button @click="removerUsuario" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium shadow-md transition flex-1 flex items-center justify-center gap-2" :disabled="removendo">
            <span v-if="removendo" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ removendo ? 'Apagando...' : 'Sim, Remover' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router' 
import { Plus, Search, X, Edit2, Trash2, Eye, ChevronRight } from 'lucide-vue-next'
import usuariosService from '@/api/usuariosService'
import authService from '@/api/authService'

const router = useRouter() 

const usuarios = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const mostrarModal = ref(false)
const editando = ref(false)
const salvando = ref(false)
const erroForm = ref('')
const sucessoForm = ref('')
const mostrarModalRemocao = ref(false)
const usuarioParaRemover = ref(null)
const removendo = ref(false)

const formUsuario = ref({
  username: '', email: '', first_name: '', last_name: '',
  password: '', password_confirm: '', telefone: '', endereco: '', nif: ''
})

const usuariosFiltrados = computed(() => {
  if (!searchTerm.value) return usuarios.value
  const termo = searchTerm.value.toLowerCase()
  return usuarios.value.filter(perfil => {
    const nome = getNomeCompleto(perfil).toLowerCase()
    const email = (perfil.user?.email || '').toLowerCase()
    const username = (perfil.user?.username || '').toLowerCase()
    return nome.includes(termo) || email.includes(termo) || username.includes(termo)
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
    console.error(err)
    error.value = err.message || 'Erro ao carregar usuários'
  } finally {
    loading.value = false
  }
}

const irParaDetalhes = (id) => {
  if (id) {
    router.push({ name: 'usuario-detalhes', params: { id } })
  }
}

const abrirModalNovo = () => {
  editando.value = false
  mostrarModal.value = true
  limparFormulario()
}

const abrirModalEditar = (perfil) => {
  if (!perfil?.id || !perfil.user) return
  editando.value = true
  mostrarModal.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  formUsuario.value = {
    id: perfil.id,
    user_id: perfil.user.id,
    username: perfil.user.username || '',
    email: perfil.user.email || '',
    first_name: perfil.user.first_name || '',
    last_name: perfil.user.last_name || '',
    telefone: perfil.telefone || '',
    endereco: perfil.endereco || '',
    nif: perfil.nif || '',
    password: '',
    password_confirm: ''
  }
}

const fecharModal = () => {
  if (!salvando.value) {
    mostrarModal.value = false
    limparFormulario()
  }
}

const limparFormulario = () => {
  formUsuario.value = {
    username: '', email: '', first_name: '', last_name: '',
    password: '', password_confirm: '', telefone: '', endereco: '', nif: ''
  }
  erroForm.value = ''
  sucessoForm.value = ''
}

const salvarUsuario = async () => {
  salvando.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  
  if (!editando.value) {
    if (formUsuario.value.password !== formUsuario.value.password_confirm) {
      erroForm.value = 'As senhas não coincidem'
      salvando.value = false
      return
    }
    if (formUsuario.value.password.length < 6) {
      erroForm.value = 'A senha deve ter no mínimo 6 caracteres'
      salvando.value = false
      return
    }
  }
  
  try {
    if (editando.value) {
      try {
        await usuariosService.updateUser(formUsuario.value.id, {
          first_name: formUsuario.value.first_name,
          last_name: formUsuario.value.last_name,
          email: formUsuario.value.email
        })
      } catch (err) { console.warn(err) }

      await usuariosService.updateProfile(formUsuario.value.id, {
        telefone: formUsuario.value.telefone || '',
        endereco: formUsuario.value.endereco || '',
        nif: formUsuario.value.nif || ''
      })
      sucessoForm.value = 'Usuário atualizado com sucesso!'
    } else {
      await authService.register({
        username: formUsuario.value.username,
        email: formUsuario.value.email,
        password: formUsuario.value.password,
        first_name: formUsuario.value.first_name,
        last_name: formUsuario.value.last_name
      })
      
      await new Promise(resolve => setTimeout(resolve, 800))
      
      const todosResponse = await usuariosService.getAll()
      const todos = todosResponse.data.results || todosResponse.data
      const criado = todos.find(u => u.user?.username === formUsuario.value.username)
      
      if (criado?.id) {
        await usuariosService.updateProfile(criado.id, {
          telefone: formUsuario.value.telefone || '',
          endereco: formUsuario.value.endereco || '',
          nif: formUsuario.value.nif || ''
        })
      }
      sucessoForm.value = 'Usuário criado com sucesso!'
    }
    
    setTimeout(() => {
      fecharModal()
      buscarUsuarios()
    }, 1500)
  } catch (err) {
    console.error(err)
    if (err.response?.data) {
      const errors = err.response.data
      erroForm.value = errors.username?.[0] || errors.email?.[0] || errors.password?.[0] || errors.detail || 'Erro ao salvar'
    } else {
      erroForm.value = err.message || 'Erro ao salvar'
    }
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
  if (!usuarioParaRemover.value?.id) return
  removendo.value = true
  try {
    await usuariosService.delete(usuarioParaRemover.value.id)
    fecharModalRemocao()
    buscarUsuarios()
  } catch (err) {
    alert('Erro ao remover: ' + (err.response?.status === 403 ? 'Sem permissão' : 'Erro desconhecido'))
  } finally {
    removendo.value = false
  }
}

const getNomeCompleto = (perfil) => {
  if (!perfil?.user) return 'N/A'
  const { first_name, last_name, username } = perfil.user
  if (first_name || last_name) return `${first_name || ''} ${last_name || ''}`.trim()
  return username || 'Sem nome'
}

const getIniciais = (perfil) => {
  if (!perfil?.user) return '??'
  const { first_name, last_name, username } = perfil.user
  if (first_name && last_name) return `${first_name[0]}${last_name[0]}`.toUpperCase()
  if (username && username.length >= 2) return username.substring(0, 2).toUpperCase()
  return username ? username[0].toUpperCase() : '?'
}

const formatarData = (data) => {
  if (!data) return 'N/A'
  return new Date(data).toLocaleDateString('pt-BR')
}

onMounted(() => {
  buscarUsuarios()
})
</script>

<style scoped>
@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.animate-scale-in {
  animation: scaleIn 0.2s ease-out forwards;
}
</style>