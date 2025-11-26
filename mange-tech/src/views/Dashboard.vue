<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-1">Dashboard Gerencial</h2>
      <p class="text-sm text-gray-500">Visão completa do sistema de chamados e ativos</p>
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
      <!-- ==================== CARDS DE ESTATÍSTICAS ==================== -->
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

      <!-- ==================== GRÁFICOS ==================== -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Gráfico de Barras - Status dos Chamados -->
        <ChartCard
          title="Chamados por Status"
          type="bar"
          :data="graficoStatusData"
          :options="graficoStatusOptions"
        />

        <!-- Gráfico de Pizza - Urgência dos Chamados -->
        <ChartCard
          title="Chamados por Urgência"
          type="doughnut"
          :data="graficoUrgenciaData"
          :options="graficoUrgenciaOptions"
        />

        <!-- Gráfico de Linhas - Chamados ao Longo do Tempo -->
        <ChartCard
          title="Tendência de Chamados (Últimos 7 dias)"
          type="line"
          :data="graficoTendenciaData"
          :options="graficoTendenciaOptions"
        />

        <!-- Lista de Chamados Recentes -->
        <div class="bg-white p-5 rounded-lg border border-gray-200">
          <p class="text-sm font-semibold text-gray-700 mb-4">Chamados Recentes</p>
          <div v-if="chamadosRecentes.length > 0" class="space-y-2">
            <div 
              v-for="chamado in chamadosRecentes" 
              :key="chamado.id" 
              class="p-3 bg-gray-50 rounded hover:bg-gray-100 transition-colors cursor-pointer"
              @click="$router.push('/chamados')"
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

      <!-- ==================== ALERTAS E ESTATÍSTICAS ==================== -->
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
import ChartCard from '@/components/ChartCard.vue'

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

// ==================== DADOS DOS GRÁFICOS ====================

// Gráfico de Status (Barras)
const graficoStatusData = computed(() => {
  const porStatus = estatisticas.value.por_status || []
  
  const statusMap = {
    'aberto': { label: 'Aberto', color: 'rgba(59, 130, 246, 0.8)' },
    'aguardando_responsaveis': { label: 'Aguardando', color: 'rgba(251, 191, 36, 0.8)' },
    'em_andamento': { label: 'Em Andamento', color: 'rgba(139, 92, 246, 0.8)' },
    'realizado': { label: 'Realizado', color: 'rgba(107, 114, 128, 0.8)' },
    'concluido': { label: 'Concluído', color: 'rgba(34, 197, 94, 0.8)' },
    'cancelado': { label: 'Cancelado', color: 'rgba(239, 68, 68, 0.8)' }
  }
  
  return {
    labels: porStatus.map(s => statusMap[s.status]?.label || s.status),
    datasets: [{
      label: 'Quantidade',
      data: porStatus.map(s => s.total),
      backgroundColor: porStatus.map(s => statusMap[s.status]?.color || 'rgba(107, 114, 128, 0.8)')
    }]
  }
})

const graficoStatusOptions = {
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1
      }
    }
  }
}

// Gráfico de Urgência (Pizza)
const graficoUrgenciaData = computed(() => {
  const porUrgencia = estatisticas.value.por_urgencia || []
  
  const urgenciaMap = {
    'baixa': { label: 'Baixa', color: 'rgba(34, 197, 94, 0.8)' },
    'media': { label: 'Média', color: 'rgba(251, 191, 36, 0.8)' },
    'alta': { label: 'Alta', color: 'rgba(249, 115, 22, 0.8)' },
    'critica': { label: 'Crítica', color: 'rgba(239, 68, 68, 0.8)' }
  }
  
  return {
    labels: porUrgencia.map(u => urgenciaMap[u.urgencia]?.label || u.urgencia),
    datasets: [{
      data: porUrgencia.map(u => u.total),
      backgroundColor: porUrgencia.map(u => urgenciaMap[u.urgencia]?.color || 'rgba(107, 114, 128, 0.8)')
    }]
  }
})

const graficoUrgenciaOptions = {
  plugins: {
    legend: {
      position: 'bottom'
    }
  }
}

// Gráfico de Tendência (Linha) - SIMULADO (você pode implementar no backend)
const graficoTendenciaData = computed(() => {
  // Aqui você pode adicionar uma API no backend para retornar dados dos últimos 7 dias
  return {
    labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
    datasets: [
      {
        label: 'Abertos',
        data: [5, 8, 12, 7, 10, 6, 9],
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4
      },
      {
        label: 'Concluídos',
        data: [3, 6, 8, 5, 7, 4, 6],
        borderColor: 'rgba(34, 197, 94, 1)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4
      }
    ]
  }
})

const graficoTendenciaOptions = {
  plugins: {
    legend: {
      display: true,
      position: 'top'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 2
      }
    }
  }
}

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