<!-- src/views/Usuarios.vue - VERSÃO COMPLETA FUNCIONAL -->
<template>
  <div class="container mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Usuários</h2>
        <p class="text-sm text-gray-500">Gerencie os usuários do sistema</p>
      </div>
      <button 
        @click="abrirModalNovo"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center justify-center gap-2 w-full sm:w-auto"
      >
        <Plus :size="16" />
        Novo Usuário
      </button>
    </div>

    <!-- Filtros -->
    <div class="mb-6">
      <div class="relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Buscar por nome, email ou username..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <p class="text-gray-500">Carregando usuários...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Erro ao carregar usuários: {{ error }}
      <button @click="buscarUsuarios" class="ml-2 underline">Tentar novamente</button>
    </div>

    <!-- CONTEÚDO -->
    <div v-else>
      <!-- DESKTOP - TABELA -->
      <div class="hidden lg:block bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuário</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Telefone</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">NIF/CPF</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cadastro</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="perfil in usuariosFiltrados" :key="perfil.user?.id || perfil.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                    <span class="text-blue-600 font-medium text-sm">{{ getIniciais(perfil) }}</span>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ getNomeCompleto(perfil) }}</div>
                    <div class="text-xs text-gray-500">@{{ perfil.user?.username || 'N/A' }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ perfil.user?.email || 'Sem email' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ perfil.telefone || 'Não informado' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ perfil.nif || 'Não informado' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatarData(perfil.created_at) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <button @click="abrirModalEditar(perfil)" class="text-blue-600 hover:text-blue-800 mr-3">Editar</button>
                <button @click="confirmarRemocao(perfil)" class="text-red-600 hover:text-red-800">Remover</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="usuariosFiltrados.length === 0" class="text-center py-12">
          <p class="text-gray-500">Nenhum usuário encontrado</p>
        </div>
      </div>

      <!-- MOBILE - CARDS -->
      <div class="lg:hidden space-y-4">
        <div v-for="perfil in usuariosFiltrados" :key="perfil.user?.id || perfil.id" class="bg-white rounded-lg border border-gray-200 p-4">
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center flex-1">
              <div class="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <span class="text-blue-600 font-medium">{{ getIniciais(perfil) }}</span>
              </div>
              <div class="ml-3 flex-1 min-w-0">
                <div class="text-sm font-semibold text-gray-900 truncate">{{ getNomeCompleto(perfil) }}</div>
                <div class="text-xs text-gray-500 truncate">@{{ perfil.user?.username || 'N/A' }}</div>
              </div>
            </div>
          </div>
          <div class="space-y-2 text-sm mb-4">
            <div class="flex justify-between">
              <span class="text-gray-500">Email:</span>
              <span class="text-gray-800 truncate ml-2">{{ perfil.user?.email || 'Sem email' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Telefone:</span>
              <span class="text-gray-800">{{ perfil.telefone || 'Não informado' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">NIF/CPF:</span>
              <span class="text-gray-800">{{ perfil.nif || 'Não informado' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Cadastro:</span>
              <span class="text-gray-800">{{ formatarData(perfil.created_at) }}</span>
            </div>
          </div>
          <div class="flex gap-2">
            <button @click="abrirModalEditar(perfil)" class="flex-1 px-3 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 transition-colors">Editar</button>
            <button @click="confirmarRemocao(perfil)" class="flex-1 px-3 py-2 bg-red-500 text-white rounded-lg text-sm font-medium hover:bg-red-600 transition-colors">Remover</button>
          </div>
        </div>
        <div v-if="usuariosFiltrados.length === 0" class="text-center py-12 bg-white rounded-lg border border-gray-200">
          <p class="text-gray-500">Nenhum usuário encontrado</p>
        </div>
      </div>
    </div>

    <!-- MODAL NOVO/EDITAR -->
    <div v-if="mostrarModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="fecharModal">
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between p-4 sm:p-6 border-b border-gray-200">
          <div>
            <h3 class="text-lg sm:text-xl font-bold text-gray-800">{{ editando ? 'Editar Usuário' : 'Novo Usuário' }}</h3>
            <p class="text-xs sm:text-sm text-gray-500 mt-1">{{ editando ? 'Atualize as informações do usuário' : 'Cadastre um novo usuário no sistema' }}</p>
          </div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600 transition-colors"><X :size="24" /></button>
        </div>
        <form @submit.prevent="salvarUsuario" class="p-4 sm:p-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nome <span class="text-red-500">*</span></label>
              <input v-model="formUsuario.first_name" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="João" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Sobrenome <span class="text-red-500">*</span></label>
              <input v-model="formUsuario.last_name" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Silva" />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email <span class="text-red-500">*</span></label>
              <input v-model="formUsuario.email" type="email" required :disabled="editando" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100" placeholder="usuario@exemplo.com" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Username <span class="text-red-500">*</span></label>
              <input v-model="formUsuario.username" type="text" required :disabled="editando" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100" placeholder="joaosilva" />
              <p v-if="editando" class="text-xs text-gray-500 mt-1">Email e Username não podem ser alterados</p>
            </div>
          </div>
          <div v-if="!editando" class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Senha <span class="text-red-500">*</span></label>
              <input v-model="formUsuario.password" type="password" required minlength="6" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Mínimo 6 caracteres" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Confirmar Senha <span class="text-red-500">*</span></label>
              <input v-model="formUsuario.password_confirm" type="password" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Digite novamente" />
            </div>
          </div>
          <div class="border-t border-gray-200 pt-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-3">Informações Adicionais</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Telefone</label>
                <input v-model="formUsuario.telefone" type="tel" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="(11) 99999-9999" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">NIF/CPF</label>
                <input v-model="formUsuario.nif" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="000.000.000-00" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Endereço</label>
              <input v-model="formUsuario.endereco" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Rua, número, bairro, cidade" />
            </div>
          </div>
          <div v-if="erroForm" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">{{ erroForm }}</div>
          <div v-if="sucessoForm" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">{{ sucessoForm }}</div>
          <div class="flex flex-col sm:flex-row gap-3 justify-end">
            <button type="button" @click="fecharModal" class="w-full sm:w-auto px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors order-2 sm:order-1" :disabled="salvando">Cancelar</button>
            <button type="submit" class="w-full sm:w-auto px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors order-1 sm:order-2" :disabled="salvando">{{ salvando ? 'Salvando...' : (editando ? 'Atualizar' : 'Criar Usuário') }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL REMOÇÃO -->
    <div v-if="mostrarModalRemocao" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="fecharModalRemocao">
      <div class="bg-white rounded-lg w-full max-w-md p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-2">Confirmar Remoção</h3>
        <p class="text-sm text-gray-600 mb-6">Tem certeza que deseja remover o usuário <strong>{{ usuarioParaRemover?.user?.username }}</strong>? Esta ação não pode ser desfeita.</p>
        <div class="flex flex-col sm:flex-row gap-3 justify-end">
          <button @click="fecharModalRemocao" class="w-full sm:w-auto px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors order-2 sm:order-1" :disabled="removendo">Cancelar</button>
          <button @click="removerUsuario" class="w-full sm:w-auto px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors order-1 sm:order-2" :disabled="removendo">{{ removendo ? 'Removendo...' : 'Remover' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus, Search, X } from 'lucide-vue-next'
import usuariosService from '@/api/usuariosService'
import authService from '@/api/authService'

// ✅ DECLARAÇÃO DE TODAS AS VARIÁVEIS
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
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  password_confirm: '',
  telefone: '',
  endereco: '',
  nif: ''
})

// ✅ COMPUTED
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

// ✅ FUNÇÕES
const buscarUsuarios = async () => {
  loading.value = true
  error.value = null
  try {
    console.log('🔄 Buscando usuários...')
    const response = await usuariosService.getAll()
    const data = response.data
    usuarios.value = data.results || (Array.isArray(data) ? data : [data])
    console.log('✅ Usuários:', usuarios.value)
  } catch (err) {
    console.error('❌ Erro:', err)
    error.value = err.message || 'Erro ao carregar usuários'
  } finally {
    loading.value = false
  }
}

const abrirModalNovo = () => {
  editando.value = false
  mostrarModal.value = true
  limparFormulario()
}

const abrirModalEditar = (perfil) => {
  console.log('✏️ Editando:', perfil)
  if (!perfil || !perfil.id || !perfil.user) {
    alert('Erro: Dados inválidos')
    return
  }
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
  console.log('📝 Form:', formUsuario.value)
}

const fecharModal = () => {
  if (!salvando.value) {
    mostrarModal.value = false
    limparFormulario()
  }
}

const limparFormulario = () => {
  formUsuario.value = {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: '',
    telefone: '',
    endereco: '',
    nif: ''
  }
  erroForm.value = ''
  sucessoForm.value = ''
}

const salvarUsuario = async () => {
  console.log('💾 Salvando...', editando.value ? 'EDITAR' : 'CRIAR')
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
      if (!formUsuario.value.id) throw new Error('ID não encontrado')
      console.log('🆔 ID:', formUsuario.value.id)
      
      try {
        await usuariosService.updateUser(formUsuario.value.id, {
          first_name: formUsuario.value.first_name,
          last_name: formUsuario.value.last_name,
          email: formUsuario.value.email
        })
      } catch (err) {
        console.warn('⚠️ Erro updateUser:', err)
      }

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
      
      const temDados = formUsuario.value.telefone || formUsuario.value.endereco || formUsuario.value.nif
      if (temDados) {
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
      }
      sucessoForm.value = 'Usuário criado com sucesso!'
    }
    
    setTimeout(() => {
      fecharModal()
      buscarUsuarios()
    }, 1500)
  } catch (err) {
    console.error('❌ Erro:', err)
    if (err.response?.data) {
      const errors = err.response.data
      erroForm.value = errors.username?.[0] || errors.email?.[0] || errors.password?.[0] || errors.detail || errors.error || errors.message || 'Erro ao salvar'
    } else {
      erroForm.value = err.message || 'Erro ao salvar'
    }
  } finally {
    salvando.value = false
  }
}

const confirmarRemocao = (perfil) => {
  console.log('🗑️ Remover:', perfil)
  if (!perfil?.id) {
    alert('Erro: ID inválido')
    return
  }
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
  if (!usuarioParaRemover.value?.id) {
    alert('Erro: ID não encontrado')
    fecharModalRemocao()
    return
  }
  removendo.value = true
  try {
    console.log('🗑️ Removendo ID:', usuarioParaRemover.value.id)
    await usuariosService.delete(usuarioParaRemover.value.id)
    console.log('✅ Removido')
    fecharModalRemocao()
    buscarUsuarios()
  } catch (err) {
    console.error('❌ Erro:', err)
    if (err.response?.status === 404) alert('Usuário não encontrado')
    else if (err.response?.status === 403) alert('Sem permissão')
    else alert('Erro ao remover')
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