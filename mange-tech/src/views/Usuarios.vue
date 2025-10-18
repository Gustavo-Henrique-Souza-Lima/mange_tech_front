<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Usuários</h2>
        <p class="text-sm text-gray-500">Gerencie os usuários do sistema</p>
      </div>
      <button 
        @click="abrirModal"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2"
      >
        <Plus :size="16" />
        Novo Usuário
      </button>
    </div>

    <!-- Filters -->
    <div class="flex gap-2 mb-6">
      <div class="flex-1 relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Buscar por nome ou email..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <select v-model="filtroStatus" class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700">
        <option value="">Todos os Status</option>
        <option value="ativo">Ativo</option>
        <option value="inativo">Inativo</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <p class="text-gray-500">Carregando usuários...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Erro ao carregar usuários: {{ error }}
    </div>

    <!-- Usuarios Table -->
    <div v-else class="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Username</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Telefone</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="usuario in usuarios" :key="usuario.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                  <span class="text-blue-600 font-medium">{{ getIniciais(usuario) }}</span>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">
                    {{ getNomeCompleto(usuario) }}
                  </div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ usuario.email || 'N/A' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ usuario.username }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ usuario.profile?.telefone || 'N/A' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button 
                @click="editarUsuario(usuario)"
                class="text-blue-600 hover:text-blue-800 mr-3"
              >
                Editar
              </button>
              <button 
                @click="confirmarRemocao(usuario)"
                class="text-red-600 hover:text-red-800"
              >
                Remover
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="usuarios.length === 0" class="text-center py-12">
        <p class="text-gray-500">Nenhum usuário encontrado</p>
      </div>
    </div>

    <!-- Modal Novo/Editar Usuário -->
    <div 
      v-if="mostrarModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="fecharModal"
    >
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-xl font-bold text-gray-800">
              {{ editando ? 'Editar Usuário' : 'Novo Usuário' }}
            </h3>
            <p class="text-sm text-gray-500 mt-1">
              {{ editando ? 'Atualize os dados do usuário' : 'Cadastre um novo usuário no sistema' }}
            </p>
          </div>
          <button 
            @click="fecharModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X :size="24" />
          </button>
        </div>

        <form @submit.prevent="salvarUsuario" class="p-6">
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Nome <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formUsuario.first_name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nome"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Sobrenome <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formUsuario.last_name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Sobrenome"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Username <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formUsuario.username"
                type="text"
                required
                :disabled="editando"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                placeholder="usuario123"
              />
              <p v-if="editando" class="text-xs text-gray-500 mt-1">
                Username não pode ser alterado
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Email <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formUsuario.email"
                type="email"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="email@exemplo.com"
              />
            </div>
          </div>

          <div v-if="!editando" class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Senha <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formUsuario.password"
                type="password"
                :required="!editando"
                minlength="6"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Mínimo 6 caracteres"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Confirmar Senha <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formUsuario.password_confirm"
                type="password"
                :required="!editando"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Digite novamente"
              />
            </div>
          </div>

          <div class="border-t border-gray-200 pt-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-3">Informações Adicionais</h4>
            
            <div class="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Telefone
                </label>
                <input
                  v-model="formUsuario.telefone"
                  type="tel"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="(00) 00000-0000"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  NIF/CPF
                </label>
                <input
                  v-model="formUsuario.nif"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="000.000.000-00"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Endereço
              </label>
              <input
                v-model="formUsuario.endereco"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Rua, número, bairro, cidade"
              />
            </div>
          </div>

          <div v-if="erroForm" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ erroForm }}
          </div>

          <div v-if="sucessoForm" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
            {{ sucessoForm }}
          </div>

          <div class="flex gap-3 justify-end">
            <button
              type="button"
              @click="fecharModal"
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              :disabled="salvando"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              :disabled="salvando"
            >
              {{ salvando ? 'Salvando...' : (editando ? 'Atualizar' : 'Criar Usuário') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Confirmação Remoção -->
    <div 
      v-if="mostrarModalRemocao" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="fecharModalRemocao"
    >
      <div class="bg-white rounded-lg w-full max-w-md p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-2">Confirmar Remoção</h3>
        <p class="text-sm text-gray-600 mb-6">
          Tem certeza que deseja remover o usuário <strong>{{ usuarioParaRemover?.username }}</strong>?
          Esta ação não pode ser desfeita.
        </p>

        <div class="flex gap-3 justify-end">
          <button
            @click="fecharModalRemocao"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            :disabled="removendo"
          >
            Cancelar
          </button>
          <button
            @click="removerUsuario"
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            :disabled="removendo"
          >
            {{ removendo ? 'Removendo...' : 'Remover' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Plus, Search, X } from 'lucide-vue-next'
import usuariosService from '@/api/usuariosService'
import authService from '@/api/authService'

const usuarios = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const filtroStatus = ref('')

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

// Buscar usuários - CORRIGIDO: sem chamar no @input
const buscarUsuarios = async () => {
  loading.value = true
  error.value = null
  
  try {
    const filtros = {}
    if (searchTerm.value) filtros.search = searchTerm.value
    
    const response = await usuariosService.getAll(filtros)
    usuarios.value = response.data.results || response.data
    
  } catch (err) {
    error.value = err.message
    console.error('Erro ao buscar usuários:', err)
  } finally {
    loading.value = false
  }
}

// Watch para buscar com debounce ao digitar
let searchTimeout
watch(searchTerm, () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    buscarUsuarios()
  }, 500) // Aguarda 500ms após parar de digitar
})

watch(filtroStatus, () => {
  buscarUsuarios()
})

const abrirModal = () => {
  editando.value = false
  mostrarModal.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  limparFormulario()
}

const editarUsuario = (usuario) => {
  editando.value = true
  mostrarModal.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  
  formUsuario.value = {
    id: usuario.id,
    username: usuario.username,
    email: usuario.email || '',
    first_name: usuario.first_name || '',
    last_name: usuario.last_name || '',
    telefone: usuario.profile?.telefone || '',
    endereco: usuario.profile?.endereco || '',
    nif: usuario.profile?.nif || '',
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
      const dados = {
        email: formUsuario.value.email,
        first_name: formUsuario.value.first_name,
        last_name: formUsuario.value.last_name
      }

      await usuariosService.patch(formUsuario.value.id, dados)
      sucessoForm.value = 'Usuário atualizado com sucesso!'
    } else {
      const dados = {
        username: formUsuario.value.username,
        email: formUsuario.value.email,
        password: formUsuario.value.password,
        first_name: formUsuario.value.first_name,
        last_name: formUsuario.value.last_name
      }

      await authService.register(dados)
      sucessoForm.value = 'Usuário criado com sucesso!'
    }
    
    setTimeout(() => {
      fecharModal()
      buscarUsuarios()
    }, 1500)
    
  } catch (err) {
    console.error('Erro ao salvar usuário:', err)
    
    if (err.response?.data?.username) {
      erroForm.value = 'Este nome de usuário já está em uso'
    } else if (err.response?.data?.email) {
      erroForm.value = 'Este e-mail já está cadastrado'
    } else {
      erroForm.value = err.response?.data?.detail || 
                       err.response?.data?.message || 
                       'Erro ao salvar usuário. Tente novamente.'
    }
  } finally {
    salvando.value = false
  }
}

const confirmarRemocao = (usuario) => {
  usuarioParaRemover.value = usuario
  mostrarModalRemocao.value = true
}

const fecharModalRemocao = () => {
  if (!removendo.value) {
    mostrarModalRemocao.value = false
    usuarioParaRemover.value = null
  }
}

const removerUsuario = async () => {
  removendo.value = true
  
  try {
    await usuariosService.delete(usuarioParaRemover.value.id)
    fecharModalRemocao()
    buscarUsuarios()
  } catch (err) {
    console.error('Erro ao remover usuário:', err)
    alert('Erro ao remover usuário. Tente novamente.')
  } finally {
    removendo.value = false
  }
}

// Helpers - CORRIGIDOS com validação
const getNomeCompleto = (usuario) => {
  if (!usuario) return 'N/A'
  if (usuario.first_name && usuario.last_name) {
    return `${usuario.first_name} ${usuario.last_name}`
  }
  return usuario.username || 'N/A'
}

const getIniciais = (usuario) => {
  if (!usuario) return '??'
  
  if (usuario.first_name && usuario.last_name) {
    return `${usuario.first_name[0]}${usuario.last_name[0]}`.toUpperCase()
  }
  
  if (usuario.username && usuario.username.length >= 2) {
    return usuario.username.substring(0, 2).toUpperCase()
  }
  
  return usuario.username ? usuario.username[0].toUpperCase() : '?'
}

onMounted(() => {
  buscarUsuarios()
})
</script>