<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Chamados</h2>
        <p class="text-sm text-gray-500">Gerencie todos os chamados de suporte técnico</p>
      </div>
      <button 
        @click="abrirModalNovo"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2"
      >
        <Plus :size="16" />
        Novo Chamado
      </button>
    </div>

    <div class="flex gap-2 mb-6 flex-col sm:flex-row">
      <div class="flex-1 relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          @input="buscarChamados"
          type="text"
          placeholder="Buscar por título, ID ou descrição..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <select v-model="filtroStatus" @change="buscarChamados" class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 bg-white">
        <option value="">Todos os Status</option>
        <option value="aberto">Aberto</option>
        <option value="aguardando_responsaveis">Aguardando Responsáveis</option>
        <option value="em_andamento">Em Andamento</option>
        <option value="realizado">Realizado</option>
        <option value="concluido">Concluído</option>
        <option value="cancelado">Cancelado</option>
      </select>
      <select v-model="filtroUrgencia" @change="buscarChamados" class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 bg-white">
        <option value="">Todas as Prioridades</option>
        <option value="baixa">Baixa</option>
        <option value="media">Média</option>
        <option value="alta">Alta</option>
        <option value="critica">Crítica</option>
      </select>
    </div>

    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <p class="text-gray-500">Carregando...</p>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Erro ao carregar chamados: {{ error }}
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="chamado in chamados" 
        :key="chamado.id" 
        @click="irParaDetalhes(chamado.id)"
        class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer relative group"
      >
        <div class="flex items-start justify-between mb-3">
          <h3 class="font-semibold text-gray-800 flex-1 truncate pr-2">#{{ chamado.id }} - {{ chamado.titulo }}</h3>
          <span :class="`px-2 py-1 rounded-xs text-xs font-medium ml-2 whitespace-nowrap ${getStatusColor(chamado.status)}`">
            {{ chamado.status_display || chamado.status }}
          </span>
        </div>
        
        <p class="text-sm text-gray-600 mb-4 line-clamp-2 h-10">{{ chamado.descricao }}</p>
        
        <div class="space-y-2 text-sm">
          <p class="flex justify-between">
            <span class="text-gray-500">Prioridade:</span>
            <span :class="`font-medium ${getUrgenciaColor(chamado.urgencia)}`">
              {{ chamado.urgencia_display || chamado.urgencia }}
            </span>
          </p>
          <p v-if="chamado.solicitante" class="flex justify-between">
            <span class="text-gray-500">Solicitante:</span> 
            <span class="text-gray-800 truncate max-w-[150px]">{{ chamado.solicitante.nome_completo || chamado.solicitante.username }}</span>
          </p>
          <p class="pt-2 border-t border-gray-100 flex justify-between">
            <span class="text-gray-500">Aberto em:</span>
            <span class="text-gray-800">{{ formatDate(chamado.data_abertura) }}</span>
          </p>
        </div>

        <div class="mt-4 pt-2">
            <span class="text-blue-600 text-sm font-medium hover:underline flex items-center justify-end">
                Ver Detalhes →
            </span>
        </div>
      </div>
    </div>

    <div v-if="!loading && !error && chamados.length === 0" class="text-center py-12">
      <p class="text-gray-500 mb-2">Nenhum chamado encontrado</p>
      <p class="text-xs text-gray-400">Tente mudar os filtros ou criar um novo.</p>
    </div>

    <div 
      v-if="mostrarModalNovo" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="fecharModalNovo"
    >
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-xl">
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-xl font-bold text-gray-800">Novo Chamado</h3>
            <p class="text-sm text-gray-500 mt-1">Preencha os dados para abrir uma solicitação</p>
          </div>
          <button 
            @click="fecharModalNovo"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X :size="24" />
          </button>
        </div>

        <form @submit.prevent="salvarChamado" class="p-6">
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

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
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

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Ativos Relacionados (opcional)
            </label>
            <select
              v-model="formChamado.ativos_ids"
              multiple
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              size="4"
            >
              <option v-for="ativo in ativosDisponiveis" :key="ativo.id" :value="ativo.id">
                {{ ativo.nome }} - {{ ativo.codigo_patrimonio }}
              </option>
            </select>
            <p class="text-xs text-gray-500 mt-1">Segure Ctrl (ou Cmd) para selecionar mais de um.</p>
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
              @click="fecharModalNovo"
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
import { useRouter, useRoute } from 'vue-router' // Importação do Router
import { Plus, Search, X } from 'lucide-vue-next'
import chamadosService from '@/api/chamadosService'
import ativosService from '@/api/ativosService'

// ========================================
// CONFIGURAÇÃO
// ========================================
const router = useRouter()
const route = useRoute()

// ========================================
// ESTADOS PRINCIPAIS
// ========================================
const chamados = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const filtroStatus = ref('')
const filtroUrgencia = ref('')

// ========================================
// ESTADOS MODAL NOVO
// ========================================
const mostrarModalNovo = ref(false)
const salvando = ref(false)
const erroForm = ref('')
const sucessoForm = ref('')
const ativosDisponiveis = ref([])

const formChamado = ref({
  titulo: '',
  descricao: '',
  urgencia: '',
  data_sugerida: '',
  ativos_ids: []
})

// ========================================
// NAVEGAÇÃO (Alteração Principal)
// ========================================
const irParaDetalhes = (id) => {
  // Redireciona para a rota configurada no router/index.js
  router.push({ name: 'chamado-detalhes', params: { id } })
}

// ========================================
// FUNÇÕES - LISTAGEM
// ========================================
const buscarChamados = async () => {
  loading.value = true
  error.value = null
  
  try {
    const filtros = {}
    if (searchTerm.value) filtros.search = searchTerm.value
    if (filtroStatus.value) filtros.status = filtroStatus.value
    if (filtroUrgencia.value) filtros.urgencia = filtroUrgencia.value
    
    // Se vier filtro de ativo/qrcode da URL
    if (route.query.ativo) filtros.ativo = route.query.ativo
    if (route.query.qrcode) filtros.search = route.query.qrcode

    const response = await chamadosService.getAll(filtros)
    chamados.value = response.data.results || response.data
    
  } catch (err) {
    error.value = err.message || 'Erro ao carregar chamados'
    console.error('Erro ao buscar chamados:', err)
  } finally {
    loading.value = false
  }
}

// ========================================
// FUNÇÕES - MODAL NOVO CHAMADO
// ========================================
const buscarAtivos = async () => {
  try {
    const response = await ativosService.getAll({ status: 'ativo' })
    ativosDisponiveis.value = response.data.results || response.data
  } catch (err) {
    console.error('Erro ao buscar ativos:', err)
  }
}

const abrirModalNovo = () => {
  mostrarModalNovo.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  buscarAtivos()
}

const fecharModalNovo = () => {
  if (!salvando.value) {
    mostrarModalNovo.value = false
    limparFormulario()
  }
}

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

const salvarChamado = async () => {
  salvando.value = true
  erroForm.value = ''
  sucessoForm.value = ''
  
  try {
    const dados = {
      titulo: formChamado.value.titulo,
      descricao: formChamado.value.descricao,
      urgencia: formChamado.value.urgencia,
    }

    if (formChamado.value.data_sugerida) {
      dados.data_sugerida = formChamado.value.data_sugerida
    }

    if (formChamado.value.ativos_ids.length > 0) {
      dados.ativos_ids = [...formChamado.value.ativos_ids] // Clone array
    }

    await chamadosService.create(dados)
    
    sucessoForm.value = 'Chamado criado com sucesso!'
    
    setTimeout(() => {
      fecharModalNovo()
      buscarChamados()
    }, 1500)
    
  } catch (err) {
    console.error('Erro ao criar chamado:', err)
    erroForm.value = err.response?.data?.detail || 
                     err.response?.data?.message || 
                     'Erro ao criar chamado. Verifique os campos.'
  } finally {
    salvando.value = false
  }
}

// ========================================
// HELPERS
// ========================================
const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const getStatusColor = (status) => {
  const colors = {
    'aberto': 'bg-blue-100 text-blue-800',
    'aguardando_responsaveis': 'bg-yellow-100 text-yellow-800',
    'em_andamento': 'bg-purple-100 text-purple-800',
    'realizado': 'bg-indigo-100 text-indigo-800',
    'concluido': 'bg-green-100 text-green-800',
    'cancelado': 'bg-red-100 text-red-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getUrgenciaColor = (urgencia) => {
  const colors = {
    'critica': 'text-red-600 font-bold',
    'alta': 'text-orange-600 font-bold',
    'media': 'text-yellow-600',
    'baixa': 'text-green-600'
  }
  return colors[urgencia] || 'text-gray-600'
}

// ========================================
// LIFECYCLE
// ========================================
onMounted(() => {
  // Se vier filtro de QR code, já aplica na busca
  if (route.query.qrcode) {
    searchTerm.value = route.query.qrcode
  }
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