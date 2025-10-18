<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Chamados</h2>
        <p class="text-sm text-gray-500">Gerencie todos os chamados de suporte técnico</p>
      </div>
      <button 
        @click="abrirModal"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2"
      >
        <Plus :size="16" />
        Novo Chamado
      </button>
    </div>

    <!-- Filtros -->
    <div class="flex gap-2 mb-6">
      <div class="flex-1 relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          @input="buscarChamados"
          type="text"
          placeholder="Buscar por título..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <select v-model="filtroStatus" @change="buscarChamados" class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700">
        <option value="">Todos os Status</option>
        <option value="aberto">Aberto</option>
        <option value="aguardando_responsaveis">Aguardando Responsáveis</option>
        <option value="em_andamento">Em Andamento</option>
        <option value="realizado">Realizado</option>
        <option value="concluido">Concluído</option>
        <option value="cancelado">Cancelado</option>
      </select>
      <select v-model="filtroUrgencia" @change="buscarChamados" class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700">
        <option value="">Todas as Prioridades</option>
        <option value="baixa">Baixa</option>
        <option value="media">Média</option>
        <option value="alta">Alta</option>
        <option value="critica">Crítica</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <p class="text-gray-500">Carregando...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Erro ao carregar chamados: {{ error }}
    </div>

    <!-- Chamados Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="chamado in chamados" 
        :key="chamado.id" 
        class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
      >
        <div class="flex items-start justify-between mb-3">
          <h3 class="font-semibold text-gray-800 flex-1">{{ chamado.titulo }}</h3>
          <span :class="`px-2 py-1 rounded text-xs font-medium ml-2 ${getStatusColor(chamado.status)}`">
            {{ chamado.status_display || chamado.status }}
          </span>
        </div>
        <p class="text-sm text-gray-600 mb-4 line-clamp-2">{{ chamado.descricao }}</p>
        <div class="space-y-2 text-sm">
          <p>
            <span class="text-gray-500">Prioridade:</span>
            <span :class="`font-medium ${getUrgenciaColor(chamado.urgencia)}`">
              {{ chamado.urgencia_display || chamado.urgencia }}
            </span>
          </p>
          <p v-if="chamado.solicitante">
            <span class="text-gray-500">Solicitante:</span> 
            <span class="text-gray-800">{{ chamado.solicitante.username }}</span>
          </p>
          <p class="pt-2 border-t border-gray-100">
            <span class="text-gray-500">Criado:</span>
            <span class="text-gray-800">{{ formatDate(chamado.data_abertura) }}</span>
          </p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && !error && chamados.length === 0" class="text-center py-12">
      <p class="text-gray-500">Nenhum chamado encontrado</p>
    </div>

    <!-- Modal Novo Chamado -->
    <div 
      v-if="mostrarModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="fecharModal"
    >
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-xl font-bold text-gray-800">Novo Chamado</h3>
            <p class="text-sm text-gray-500 mt-1">Preencha os dados do chamado</p>
          </div>
          <button 
            @click="fecharModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X :size="24" />
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="salvarChamado" class="p-6">
          <!-- Título -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Título <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formChamado.titulo"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: Computador não liga"
            />
          </div>

          <!-- Descrição -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Descrição <span class="text-red-500">*</span>
            </label>
            <textarea
              v-model="formChamado.descricao"
              required
              rows="4"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Descreva o problema em detalhes..."
            ></textarea>
          </div>

          <!-- Urgência e Data Sugerida -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Urgência <span class="text-red-500">*</span>
              </label>
              <select
                v-model="formChamado.urgencia"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Selecione...</option>
                <option value="baixa">Baixa</option>
                <option value="media">Média</option>
                <option value="alta">Alta</option>
                <option value="critica">Crítica</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Data Sugerida
              </label>
              <input
                v-model="formChamado.data_sugerida"
                type="datetime-local"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <!-- Ativos (opcional) -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Ativos Relacionados (opcional)
            </label>
            <select
              v-model="formChamado.ativos_ids"
              multiple
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              size="4"
            >
              <option v-for="ativo in ativosDisponiveis" :key="ativo.id" :value="ativo.id">
                {{ ativo.nome }} - {{ ativo.codigo_patrimonio }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Segure Ctrl/Cmd para selecionar múltiplos</p>
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
              {{ salvando ? 'Salvando...' : 'Criar Chamado' }}
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
import chamadosService from '@/api/chamadosService'
import ativosService from '@/api/ativosService'

// Estados principais
const chamados = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const filtroStatus = ref('')
const filtroUrgencia = ref('')

// Estados do modal
const mostrarModal = ref(false)
const salvando = ref(false)
const erroForm = ref('')
const sucessoForm = ref('')
const ativosDisponiveis = ref([])

// Formulário
const formChamado = ref({
  titulo: '',
  descricao: '',
  urgencia: '',
  data_sugerida: '',
  ativos_ids: []
})

// Buscar chamados
const buscarChamados = async () => {
  loading.value = true
  error.value = null
  
  try {
    const filtros = {}
    if (searchTerm.value) filtros.search = searchTerm.value
    if (filtroStatus.value) filtros.status = filtroStatus.value
    if (filtroUrgencia.value) filtros.urgencia = filtroUrgencia.value
    
    const response = await chamadosService.getAll(filtros)
    chamados.value = response.data.results || response.data
    
  } catch (err) {
    error.value = err.message
    console.error('Erro ao buscar chamados:', err)
  } finally {
    loading.value = false
  }
}

// Buscar ativos disponíveis
const buscarAtivos = async () => {
  try {
    const response = await ativosService.getAll({ status: 'ativo' })
    ativosDisponiveis.value = response.data.results || response.data
  } catch (err) {
    console.error('Erro ao buscar ativos:', err)
  }
}

// Abrir modal
const abrirModal = () => {
  mostrarModal.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  buscarAtivos()
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
  formChamado.value = {
    titulo: '',
    descricao: '',
    urgencia: '',
    data_sugerida: '',
    ativos_ids: []
  }
  erroForm.value = ''
  sucessoForm.value = ''
}

// Salvar chamado
const salvarChamado = async () => {
  salvando.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  
  try {
    // Preparar dados
    const dados = {
      titulo: formChamado.value.titulo,
      descricao: formChamado.value.descricao,
      urgencia: formChamado.value.urgencia,
    }

    // Adicionar data sugerida se preenchida
    if (formChamado.value.data_sugerida) {
      dados.data_sugerida = formChamado.value.data_sugerida
    }

    // Adicionar ativos se selecionados
    if (formChamado.value.ativos_ids.length > 0) {
      dados.ativos_ids = formChamado.value.ativos_ids
    }

    // Criar chamado
    await chamadosService.create(dados)
    
    sucessoForm.value = 'Chamado criado com sucesso!'
    
    // Aguardar um pouco e fechar modal
    setTimeout(() => {
      fecharModal()
      buscarChamados() // Recarregar lista
    }, 1500)
    
  } catch (err) {
    console.error('Erro ao criar chamado:', err)
    erroForm.value = err.response?.data?.detail || 
                     err.response?.data?.message || 
                     'Erro ao criar chamado. Tente novamente.'
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
    'aberto': 'bg-red-100 text-red-800',
    'aguardando_responsaveis': 'bg-yellow-100 text-yellow-800',
    'em_andamento': 'bg-blue-100 text-blue-800',
    'realizado': 'bg-purple-100 text-purple-800',
    'concluido': 'bg-green-100 text-green-800',
    'cancelado': 'bg-gray-100 text-gray-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getUrgenciaColor = (urgencia) => {
  const colors = {
    'critica': 'text-red-600',
    'alta': 'text-orange-600',
    'media': 'text-yellow-600',
    'baixa': 'text-blue-600'
  }
  return colors[urgencia] || 'text-gray-600'
}

// Lifecycle
onMounted(() => {
  buscarChamados()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>