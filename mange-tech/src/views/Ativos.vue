<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Ativos</h2>
        <p class="text-sm text-gray-500">Gerencie todos os ativos da empresa</p>
      </div>
      <button 
        @click="abrirModal"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2"
      >
        <Plus :size="16" />
        Novo Ativo
      </button>
    </div>

    <!-- Filtros -->
    <div class="flex gap-2 mb-6">
      <div class="flex-1 relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          @input="buscarAtivos"
          type="text"
          placeholder="Buscar por código ou nome..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <select v-model="filtroStatus" @change="buscarAtivos" class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700">
        <option value="">Todos os Status</option>
        <option value="ativo">Ativo</option>
        <option value="manutencao">Em Manutenção</option>
        <option value="inativo">Inativo</option>
        <option value="descartado">Descartado</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <p class="text-gray-500">Carregando ativos...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Erro ao carregar ativos: {{ error }}
    </div>

    <!-- Ativos Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="ativo in ativos" 
        :key="ativo.id" 
        class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-semibold text-gray-800 mb-1">{{ ativo.nome }}</h3>
            <p class="text-xs text-gray-500">Código: {{ ativo.codigo_patrimonio || 'N/A' }}</p>
          </div>
          <span :class="`px-2 py-1 rounded text-xs font-medium ${getStatusColor(ativo.status)}`">
            {{ ativo.status_display || ativo.status }}
          </span>
        </div>
        <div class="space-y-2 text-sm">
          <p v-if="ativo.categoria">
            <span class="text-gray-500">Categoria:</span> 
            <span class="text-gray-800">{{ ativo.categoria.nome }}</span>
          </p>
          <p v-if="ativo.ambiente">
            <span class="text-gray-500">Ambiente:</span> 
            <span class="text-gray-800">{{ ativo.ambiente.nome }}</span>
          </p>
          <p class="pt-2 border-t border-gray-100">
            <span class="text-gray-500">Cadastrado:</span>
            <span class="text-gray-800">{{ formatDate(ativo.created_at) }}</span>
          </p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && !error && ativos.length === 0" class="text-center py-12">
      <p class="text-gray-500">Nenhum ativo encontrado</p>
    </div>

    <!-- Modal Novo Ativo -->
    <div 
      v-if="mostrarModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="fecharModal"
    >
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-xl font-bold text-gray-800">Novo Ativo</h3>
            <p class="text-sm text-gray-500 mt-1">Cadastre um novo ativo</p>
          </div>
          <button 
            @click="fecharModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X :size="24" />
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="salvarAtivo" class="p-6">
          <!-- Nome -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Nome <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formAtivo.nome"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: Notebook Dell Latitude"
            />
          </div>

          <!-- Descrição -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Descrição
            </label>
            <textarea
              v-model="formAtivo.descricao"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Informações adicionais sobre o ativo..."
            ></textarea>
          </div>

          <!-- Código Patrimônio e QR Code -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Código de Patrimônio
              </label>
              <input
                v-model="formAtivo.codigo_patrimonio"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Ex: PAT-001"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                QR Code
              </label>
              <input
                v-model="formAtivo.qr_code"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Código QR"
              />
            </div>
          </div>

          <!-- Categoria, Ambiente e Status -->
          <div class="grid grid-cols-3 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Categoria
              </label>
              <select
                v-model="formAtivo.categoria"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecione...</option>
                <option v-for="cat in categorias" :key="cat.id" :value="cat.id">
                  {{ cat.nome }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Ambiente
              </label>
              <select
                v-model="formAtivo.ambiente"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecione...</option>
                <option v-for="amb in ambientes" :key="amb.id" :value="amb.id">
                  {{ amb.nome }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Status <span class="text-red-500">*</span>
              </label>
              <select
                v-model="formAtivo.status"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecione...</option>
                <option value="ativo">Ativo</option>
                <option value="manutencao">Em Manutenção</option>
                <option value="inativo">Inativo</option>
                <option value="descartado">Descartado</option>
              </select>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="erroForm" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ erroForm }}
          </div>

          <!-- Success Message -->
          <div v-if="sucessoForm" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
            {{ sucessoForm }}
          </div>

          <!-- Buttons -->
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
              {{ salvando ? 'Salvando...' : 'Criar Ativo' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Search, X } from 'lucide-vue-next'
import ativosService from '@/api/ativosService'
import api from '@/api/axios'

// Estados principais
const ativos = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const filtroStatus = ref('')

// Estados do modal
const mostrarModal = ref(false)
const salvando = ref(false)
const erroForm = ref('')
const sucessoForm = ref('')
const categorias = ref([])
const ambientes = ref([])

// Formulário
const formAtivo = ref({
  nome: '',
  descricao: '',
  codigo_patrimonio: '',
  qr_code: '',
  categoria: '',
  ambiente: '',
  status: ''
})

// Buscar ativos
const buscarAtivos = async () => {
  loading.value = true
  error.value = null
  
  try {
    const filtros = {}
    if (searchTerm.value) filtros.search = searchTerm.value
    if (filtroStatus.value) filtros.status = filtroStatus.value
    
    const response = await ativosService.getAll(filtros)
    ativos.value = response.data.results || response.data
    
  } catch (err) {
    error.value = err.message
    console.error('Erro ao buscar ativos:', err)
  } finally {
    loading.value = false
  }
}

// Buscar categorias e ambientes
const buscarDadosAuxiliares = async () => {
  try {
    const [categoriasRes, ambientesRes] = await Promise.all([
      api.get('/categorias/'),
      api.get('/ambientes/')
    ])
    
    categorias.value = categoriasRes.data.results || categoriasRes.data
    ambientes.value = ambientesRes.data.results || ambientesRes.data
  } catch (err) {
    console.error('Erro ao buscar dados auxiliares:', err)
  }
}

// Abrir modal
const abrirModal = () => {
  mostrarModal.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  buscarDadosAuxiliares()
}

// Fechar modal
const fecharModal = () => {
  if (!salvando.value) {
    mostrarModal.value = false
    limparFormulario()
  }
}

// Limpar formulário
const limparFormulario = () => {
  formAtivo.value = {
    nome: '',
    descricao: '',
    codigo_patrimonio: '',
    qr_code: '',
    categoria: '',
    ambiente: '',
    status: ''
  }
  erroForm.value = ''
  sucessoForm.value = ''
}

// Salvar ativo
const salvarAtivo = async () => {
  salvando.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  
  try {
    const dados = {
      nome: formAtivo.value.nome,
      status: formAtivo.value.status
    }

    // Campos opcionais
    if (formAtivo.value.descricao) dados.descricao = formAtivo.value.descricao
    if (formAtivo.value.codigo_patrimonio) dados.codigo_patrimonio = formAtivo.value.codigo_patrimonio
    if (formAtivo.value.qr_code) dados.qr_code = formAtivo.value.qr_code
    if (formAtivo.value.categoria) dados.categoria = formAtivo.value.categoria
    if (formAtivo.value.ambiente) dados.ambiente = formAtivo.value.ambiente

    await ativosService.create(dados)
    
    sucessoForm.value = 'Ativo criado com sucesso!'
    
    setTimeout(() => {
      fecharModal()
      buscarAtivos()
    }, 1500)
    
  } catch (err) {
    console.error('Erro ao criar ativo:', err)
    erroForm.value = err.response?.data?.detail || 
                     err.response?.data?.message || 
                     'Erro ao criar ativo. Tente novamente.'
  } finally {
    salvando.value = false
  }
}

// Helpers
const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('pt-BR')
}

const getStatusColor = (status) => {
  const colors = {
    'ativo': 'bg-green-100 text-green-800',
    'manutencao': 'bg-yellow-100 text-yellow-800',
    'inativo': 'bg-gray-100 text-gray-800',
    'descartado': 'bg-red-100 text-red-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

// Lifecycle
onMounted(() => {
  buscarAtivos()
})
</script>