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
        @click="abrirModalDetalhes(chamado.id)"
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

    <!-- ========================================= -->
    <!-- MODAL DETALHES DO CHAMADO -->
    <!-- ========================================= -->
    <div 
      v-if="mostrarModalDetalhes" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="fecharModalDetalhes"
    >
      <div class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <!-- Loading do Modal -->
        <div v-if="loadingDetalhes" class="p-8 text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p class="text-gray-500">Carregando detalhes...</p>
        </div>

        <!-- Conteúdo do Modal -->
        <div v-else-if="chamadoDetalhes">
          <!-- Header -->
          <div class="flex items-start justify-between p-6 border-b border-gray-200">
            <div class="flex-1">
              <h3 class="text-2xl font-bold text-gray-800 mb-2">{{ chamadoDetalhes.titulo }}</h3>
              <div class="flex items-center gap-3">
                <span :class="`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(chamadoDetalhes.status)}`">
                  {{ chamadoDetalhes.status_display }}
                </span>
                <span :class="`text-sm font-medium ${getUrgenciaColor(chamadoDetalhes.urgencia)}`">
                  Prioridade: {{ chamadoDetalhes.urgencia_display }}
                </span>
              </div>
            </div>
            <button 
              @click="fecharModalDetalhes"
              class="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X :size="24" />
            </button>
          </div>

          <!-- Body -->
          <div class="p-6">
            <!-- Descrição -->
            <div class="mb-6">
              <h4 class="text-lg font-semibold text-gray-800 mb-2">Descrição</h4>
              <div class="bg-gray-50 p-4 rounded-lg">
                <p class="text-gray-700 whitespace-pre-wrap">{{ chamadoDetalhes.descricao }}</p>
              </div>
            </div>

            <!-- Informações -->
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div>
                <p class="text-sm text-gray-500">Solicitante</p>
                <p class="font-medium text-gray-800">
                  {{ chamadoDetalhes.solicitante?.nome_completo || chamadoDetalhes.solicitante?.username }}
                </p>
              </div>
              <div>
                <p class="text-sm text-gray-500">Data de Abertura</p>
                <p class="font-medium text-gray-800">{{ formatDateTime(chamadoDetalhes.data_abertura) }}</p>
              </div>
              <div v-if="chamadoDetalhes.data_sugerida">
                <p class="text-sm text-gray-500">Data Sugerida</p>
                <p class="font-medium text-gray-800">{{ formatDateTime(chamadoDetalhes.data_sugerida) }}</p>
              </div>
              <div v-if="chamadoDetalhes.data_conclusao">
                <p class="text-sm text-gray-500">Data de Conclusão</p>
                <p class="font-medium text-gray-800">{{ formatDateTime(chamadoDetalhes.data_conclusao) }}</p>
              </div>
            </div>

            <!-- Ativos Relacionados -->
            <div v-if="chamadoDetalhes.ativos && chamadoDetalhes.ativos.length > 0" class="mb-6">
              <h4 class="text-lg font-semibold text-gray-800 mb-3">Ativos Relacionados</h4>
              <div class="grid grid-cols-2 gap-3">
                <div 
                  v-for="ativo in chamadoDetalhes.ativos" 
                  :key="ativo.id"
                  class="bg-gray-50 p-3 rounded-lg border border-gray-200"
                >
                  <p class="font-medium text-gray-800">{{ ativo.nome }}</p>
                  <p class="text-sm text-gray-500">{{ ativo.codigo_patrimonio }}</p>
                </div>
              </div>
            </div>

            <!-- Histórico de Status -->
            <div v-if="chamadoDetalhes.historico && chamadoDetalhes.historico.length > 0" class="mb-6">
              <h4 class="text-lg font-semibold text-gray-800 mb-3">Histórico de Mudanças</h4>
              <div class="space-y-3">
                <div 
                  v-for="(hist, index) in chamadoDetalhes.historico" 
                  :key="index"
                  class="bg-gray-50 p-4 rounded-lg border-l-4"
                  :class="getStatusBorderColor(hist.status)"
                >
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-medium text-gray-800">{{ hist.status_display }}</span>
                    <span class="text-xs text-gray-500">{{ formatDateTime(hist.created_at) }}</span>
                  </div>
                  <p class="text-sm text-gray-600 mb-1">Por: {{ hist.user?.nome_completo || hist.user?.username }}</p>
                  <p v-if="hist.comentario" class="text-sm text-gray-700 mt-2 italic">
                    "{{ hist.comentario }}"
                  </p>
                </div>
              </div>
            </div>

            <!-- Ações de Status -->
            <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <h4 class="text-lg font-semibold text-gray-800 mb-3">Alterar Status</h4>
              
              <!-- Mensagem de Erro -->
              <div v-if="erroStatus" class="mb-3 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                {{ erroStatus }}
              </div>

              <!-- Mensagem de Sucesso -->
              <div v-if="sucessoStatus" class="mb-3 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
                {{ sucessoStatus }}
              </div>

              <!-- Botões de Status -->
              <div class="grid grid-cols-2 gap-3 mb-3">
                <button
                  v-for="statusOpcao in statusDisponiveis"
                  :key="statusOpcao.value"
                  @click="statusSelecionado = statusOpcao.value"
                  :class="[
                    'px-4 py-3 rounded-lg font-medium transition-all',
                    statusSelecionado === statusOpcao.value
                      ? statusOpcao.activeClass
                      : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
                  ]"
                  :disabled="!podeAlterarPara(statusOpcao.value)"
                >
                  {{ statusOpcao.label }}
                </button>
              </div>

              <!-- Comentário -->
              <div class="mb-3">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Comentário sobre a mudança
                </label>
                <textarea
                  v-model="comentarioStatus"
                  rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Descreva o motivo da mudança de status..."
                ></textarea>
              </div>

              <!-- Botão Confirmar -->
              <button
                @click="confirmarMudancaStatus"
                :disabled="!statusSelecionado || statusSelecionado === chamadoDetalhes.status || alterandoStatus"
                class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {{ alterandoStatus ? 'Alterando...' : 'Confirmar Mudança de Status' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================= -->
    <!-- MODAL NOVO CHAMADO -->
    <!-- ========================================= -->
    <div 
      v-if="mostrarModalNovo" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="fecharModalNovo"
    >
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-xl font-bold text-gray-800">Novo Chamado</h3>
            <p class="text-sm text-gray-500 mt-1">Preencha os dados do chamado</p>
          </div>
          <button 
            @click="fecharModalNovo"
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
import { ref, onMounted, computed } from 'vue'
import { Plus, Search, X } from 'lucide-vue-next'
import chamadosService from '@/api/chamadosService'
import ativosService from '@/api/ativosService'

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
// ESTADOS MODAL DETALHES
// ========================================
const mostrarModalDetalhes = ref(false)
const loadingDetalhes = ref(false)
const chamadoDetalhes = ref(null)
const statusSelecionado = ref('')
const comentarioStatus = ref('')
const alterandoStatus = ref(false)
const erroStatus = ref('')
const sucessoStatus = ref('')

// ========================================
// OPÇÕES DE STATUS
// ========================================
const statusDisponiveis = [
  { 
    value: 'aberto', 
    label: 'Aberto',
    activeClass: 'bg-red-500 text-white border-red-500'
  },
  { 
    value: 'aguardando_responsaveis', 
    label: 'Aguardando Responsáveis',
    activeClass: 'bg-yellow-500 text-white border-yellow-500'
  },
  { 
    value: 'em_andamento', 
    label: 'Em Andamento',
    activeClass: 'bg-blue-500 text-white border-blue-500'
  },
  { 
    value: 'realizado', 
    label: 'Realizado',
    activeClass: 'bg-purple-500 text-white border-purple-500'
  },
  { 
    value: 'concluido', 
    label: 'Concluído',
    activeClass: 'bg-green-500 text-white border-green-500'
  },
  { 
    value: 'cancelado', 
    label: 'Cancelado',
    activeClass: 'bg-gray-500 text-white border-gray-500'
  }
]

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
    
    const response = await chamadosService.getAll(filtros)
    chamados.value = response.data.results || response.data
    
  } catch (err) {
    error.value = err.message
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
      dados.ativos_ids = formChamado.value.ativos_ids
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
                     'Erro ao criar chamado. Tente novamente.'
  } finally {
    salvando.value = false
  }
}

// ========================================
// FUNÇÕES - MODAL DETALHES
// ========================================
const abrirModalDetalhes = async (id) => {
  mostrarModalDetalhes.value = true
  loadingDetalhes.value = true
  chamadoDetalhes.value = null
  statusSelecionado.value = ''
  comentarioStatus.value = ''
  erroStatus.value = ''
  sucessoStatus.value = ''
  
  try {
    const response = await chamadosService.getById(id)
    chamadoDetalhes.value = response.data
    statusSelecionado.value = response.data.status
  } catch (err) {
    console.error('Erro ao buscar detalhes:', err)
    erroStatus.value = 'Erro ao carregar detalhes do chamado'
  } finally {
    loadingDetalhes.value = false
  }
}

const fecharModalDetalhes = () => {
  if (!alterandoStatus.value) {
    mostrarModalDetalhes.value = false
    chamadoDetalhes.value = null
  }
}

// ========================================
// FUNÇÕES - MUDANÇA DE STATUS
// ========================================
const podeAlterarPara = (novoStatus) => {
  if (!chamadoDetalhes.value) return false
  
  const statusAtual = chamadoDetalhes.value.status
  
  // Regras de transição de status
  const transicoes = {
    'aberto': ['aguardando_responsaveis', 'em_andamento', 'cancelado'],
    'aguardando_responsaveis': ['em_andamento', 'cancelado'],
    'em_andamento': ['realizado', 'cancelado'],
    'realizado': ['concluido', 'em_andamento'],
    'concluido': [],
    'cancelado': []
  }
  
  return transicoes[statusAtual]?.includes(novoStatus) || false
}

const confirmarMudancaStatus = async () => {
  if (!statusSelecionado.value || statusSelecionado.value === chamadoDetalhes.value.status) {
    erroStatus.value = 'Selecione um status diferente do atual'
    return
  }

  if (!podeAlterarPara(statusSelecionado.value)) {
    erroStatus.value = 'Transição de status não permitida'
    return
  }

  alterandoStatus.value = true
  erroStatus.value = ''
  sucessoStatus.value = ''
  
  try {
    await chamadosService.alterarStatus(
      chamadoDetalhes.value.id,
      statusSelecionado.value,
      comentarioStatus.value || `Status alterado para ${statusSelecionado.value}`
    )
    
    sucessoStatus.value = 'Status alterado com sucesso!'
    
    // Recarregar detalhes
    setTimeout(async () => {
      await abrirModalDetalhes(chamadoDetalhes.value.id)
      await buscarChamados() // Atualizar lista
      comentarioStatus.value = ''
    }, 1000)
    
  } catch (err) {
    console.error('Erro ao alterar status:', err)
    erroStatus.value = err.response?.data?.error || 
                       err.response?.data?.detail || 
                       'Erro ao alterar status. Tente novamente.'
  } finally {
    alterandoStatus.value = false
  }
}

// ========================================
// HELPERS
// ========================================
const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('pt-BR')
}

const formatDateTime = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
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

const getStatusBorderColor = (status) => {
  const colors = {
    'aberto': 'border-red-500',
    'aguardando_responsaveis': 'border-yellow-500',
    'em_andamento': 'border-blue-500',
    'realizado': 'border-purple-500',
    'concluido': 'border-green-500',
    'cancelado': 'border-gray-500'
  }
  return colors[status] || 'border-gray-500'
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

// ========================================
// LIFECYCLE
// ========================================
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