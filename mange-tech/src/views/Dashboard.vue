<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-1">Dashboard</h2>
      <p class="text-sm text-gray-500">Visão geral do sistema de gestão de chamados e ativos</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p class="text-gray-500">Carregando dados...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <p class="text-red-700 font-medium">Erro ao carregar dados</p>
      <p class="text-red-600 text-sm mt-1">{{ error }}</p>
      <button 
        @click="carregarDados" 
        class="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
      >
        Tentar novamente
      </button>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
          <p class="text-xs text-gray-500 mb-1">Total de Chamados</p>
          <p class="text-3xl font-bold text-blue-600 mb-1">{{ estatisticas.total || 0 }}</p>
          <p class="text-xs text-gray-400">Todos os chamados</p>
        </div>

        <div class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
          <p class="text-xs text-gray-500 mb-1">Chamados Abertos</p>
          <p class="text-3xl font-bold text-yellow-600 mb-1">{{ chamadosAbertos }}</p>
          <p class="text-xs text-gray-400">Aguardando atendimento</p>
        </div>

        <div class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
          <p class="text-xs text-gray-500 mb-1">Ativos Operacionais</p>
          <p class="text-3xl font-bold text-green-600 mb-1">{{ ativosStats.ativo || 0 }}</p>
          <p class="text-xs text-gray-400">De {{ ativosStats.total || 0 }} totais</p>
        </div>

        <div class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
          <p class="text-xs text-gray-500 mb-1">Concluídos (Mês)</p>
          <p class="text-3xl font-bold text-purple-600 mb-1">{{ estatisticas.concluidos_mes_atual || 0 }}</p>
          <p class="text-xs text-gray-400">Este mês</p>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Status dos Chamados -->
        <div class="bg-white p-5 rounded-lg border border-gray-200">
          <p class="text-sm font-semibold text-gray-700 mb-4">Status dos Chamados</p>
          <div v-if="statusList.length > 0" class="space-y-3">
            <div 
              v-for="status in statusList" 
              :key="status.key" 
              class="flex items-center justify-between p-3 bg-gray-50 rounded hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-center gap-3">
                <div :class="`w-3 h-3 rounded-full ${status.color}`"></div>
                <span class="text-sm font-medium text-gray-700">{{ status.label }}</span>
              </div>
              <span class="text-lg font-bold text-gray-800">{{ status.value }}</span>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-400">
            <p class="text-sm">Nenhum dado disponível</p>
          </div>
        </div>

        <!-- Chamados Recentes -->
        <div class="bg-white p-5 rounded-lg border border-gray-200">
          <p class="text-sm font-semibold text-gray-700 mb-4">Chamados Recentes</p>
          <div v-if="chamadosRecentes.length > 0" class="space-y-2">
            <div 
              v-for="chamado in chamadosRecentes" 
              :key="chamado.id" 
              class="p-3 bg-gray-50 rounded hover:bg-gray-100 transition-colors cursor-pointer"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <p class="font-medium text-gray-800 text-sm">{{ chamado.titulo }}</p>
                  <p class="text-xs text-gray-500 mt-1">
                    <span :class="getStatusColor(chamado.status)">
                      {{ chamado.status_display || chamado.status }}
                    </span>
                    <span class="mx-1">•</span>
                    <span :class="getUrgenciaColor(chamado.urgencia)">
                      {{ chamado.urgencia_display || chamado.urgencia }}
                    </span>
                  </p>
                </div>
                <span v-if="chamado.esta_em_atraso" class="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                  Atrasado
                </span>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-400">
            <p class="text-sm">Nenhum chamado recente</p>
          </div>
        </div>
      </div>

      <!-- Alertas e Estatísticas -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <!-- Ativos em Manutenção -->
        <div class="p-4 rounded-lg border bg-yellow-50 border-yellow-200">
          <p class="text-sm font-semibold text-gray-800 mb-1">Ativos em Manutenção</p>
          <p class="text-2xl font-bold text-yellow-700 mb-1">{{ ativosStats.manutencao || 0 }}</p>
          <p class="text-xs text-gray-600">Precisam de atenção</p>
        </div>

        <!-- Chamados em Atraso -->
        <div class="p-4 rounded-lg border bg-red-50 border-red-200">
          <p class="text-sm font-semibold text-gray-800 mb-1">Chamados em Atraso</p>
          <p class="text-2xl font-bold text-red-700 mb-1">{{ estatisticas.em_atraso || 0 }}</p>
          <p class="text-xs text-gray-600">Requerem urgência</p>
        </div>

        <!-- Em Andamento -->
        <div class="p-4 rounded-lg border bg-blue-50 border-blue-200">
          <p class="text-sm font-semibold text-gray-800 mb-1">Em Andamento</p>
          <p class="text-2xl font-bold text-blue-700 mb-1">{{ chamadosEmAndamento }}</p>
          <p class="text-xs text-gray-600">Sendo tratados agora</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import dashboardService from '@/api/dashboardService'

// Estados
const loading = ref(true)
const error = ref(null)
const estatisticas = ref({})
const chamadosRecentes = ref([])
const ativosStats = ref({})

// Computed Properties
const chamadosAbertos = computed(() => {
  const statusAbertos = estatisticas.value.por_status || []
  const aberto = statusAbertos.find(s => s.status === 'aberto')
  const aguardando = statusAbertos.find(s => s.status === 'aguardando_responsaveis')
  return (aberto?.total || 0) + (aguardando?.total || 0)
})

const chamadosEmAndamento = computed(() => {
  const statusAbertos = estatisticas.value.por_status || []
  const emAndamento = statusAbertos.find(s => s.status === 'em_andamento')
  return emAndamento?.total || 0
})

const statusList = computed(() => {
  const porStatus = estatisticas.value.por_status || []
  
  const statusMap = {
    'aberto': { label: 'Aberto', color: 'bg-blue-500' },
    'aguardando_responsaveis': { label: 'Aguardando Responsáveis', color: 'bg-yellow-500' },
    'em_andamento': { label: 'Em Andamento', color: 'bg-purple-500' },
    'realizado': { label: 'Realizado', color: 'bg-gray-500' },
    'concluido': { label: 'Concluído', color: 'bg-green-500' },
    'cancelado': { label: 'Cancelado', color: 'bg-red-500' }
  }
  
  return porStatus.map(s => ({
    key: s.status,
    label: statusMap[s.status]?.label || s.status,
    color: statusMap[s.status]?.color || 'bg-gray-500',
    value: s.total
  }))
})

// Helper Functions
const getStatusColor = (status) => {
  const colors = {
    'aberto': 'text-blue-600 font-medium',
    'aguardando_responsaveis': 'text-yellow-600 font-medium',
    'em_andamento': 'text-purple-600 font-medium',
    'realizado': 'text-gray-600 font-medium',
    'concluido': 'text-green-600 font-medium',
    'cancelado': 'text-red-600 font-medium'
  }
  return colors[status] || 'text-gray-600'
}

const getUrgenciaColor = (urgencia) => {
  const colors = {
    'baixa': 'text-green-600',
    'media': 'text-yellow-600',
    'alta': 'text-orange-600',
    'critica': 'text-red-600 font-bold'
  }
  return colors[urgencia] || 'text-gray-600'
}

// Carregar dados
const carregarDados = async () => {
  loading.value = true
  error.value = null
  
  try {
    const data = await dashboardService.getDashboardCompleto()
    estatisticas.value = data.estatisticas
    chamadosRecentes.value = data.chamadosRecentes
    ativosStats.value = data.ativosStats
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Erro ao carregar dados do dashboard'
    console.error('Erro ao carregar dashboard:', err)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  carregarDados()
})
</script>