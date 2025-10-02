<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-1">Dashboard</h2>
      <p class="text-sm text-gray-500">Visão geral do sistema de gestão de chamados e ativos</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-4 gap-4 mb-6">
      <div v-for="(stat, index) in stats" :key="index" class="bg-white p-5 rounded-lg border border-gray-200">
        <p class="text-xs text-gray-500 mb-1">{{ stat.title }}</p>
        <p :class="`text-3xl font-bold ${stat.color} mb-1`">{{ stat.value }}</p>
        <p class="text-xs text-gray-400">{{ stat.subtitle }}</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-2 gap-6 mb-6">
      <div class="bg-white p-5 rounded-lg border border-gray-200">
        <p class="text-sm font-semibold text-gray-700 mb-4">[ Gráfico de Status dos Chamados ]</p>
        <div class="h-48 bg-gray-50 rounded flex items-center justify-center text-gray-400">
          Gráfico de pizza/barras aqui
        </div>
      </div>
      <div class="bg-white p-5 rounded-lg border border-gray-200">
        <p class="text-sm font-semibold text-gray-700 mb-4">[ Chamados Recentes ]</p>
        <div class="space-y-2">
          <div v-for="chamado in recentChamados" :key="chamado.id" class="p-3 bg-gray-50 rounded text-sm">
            <p class="font-medium text-gray-800">{{ chamado.titulo }}</p>
            <p class="text-xs text-gray-500 mt-1">
              {{ chamado.status }} • {{ chamado.prioridade }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Alerts -->
    <div class="grid grid-cols-3 gap-4">
      <div v-for="(alert, index) in alerts" :key="index" :class="`p-4 rounded-lg border ${alert.color}`">
        <p class="text-sm font-semibold text-gray-800 mb-1">{{ alert.title }}</p>
        <p class="text-xs text-gray-600">{{ alert.value }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useMockDataStore } from '../stores/mockData'

const store = useMockDataStore()

const stats = computed(() => [
  {
    title: 'Chamados Abertos',
    value: store.dashboard.chamadosAbertos,
    subtitle: '+12% vs mês anterior',
    color: 'text-blue-600'
  },
  {
    title: 'Tempo Médio Resolução',
    value: store.dashboard.tempoMedioResolucao,
    subtitle: '-8% melhora contínua',
    color: 'text-green-600'
  },
  {
    title: 'Ativos Ativos',
    value: store.dashboard.ativosAtivos,
    subtitle: '+3% vs mês anterior',
    color: 'text-purple-600'
  },
  {
    title: 'Taxa de Satisfação',
    value: `${store.dashboard.taxaSatisfacao}%`,
    subtitle: '+2% avaliações positivas',
    color: 'text-emerald-600'
  }
])

const recentChamados = computed(() => store.chamados.slice(0, 4))

const alerts = computed(() => [
  {
    title: 'Manutenções Atrasadas',
    value: `${store.dashboard.manutencoes} ativos precisam de atenção`,
    color: 'bg-yellow-50 border-yellow-200'
  },
  {
    title: 'Técnicos Disponíveis',
    value: `${store.dashboard.tecnicosDisponiveis} de 15 técnicos online`,
    color: 'bg-blue-50 border-blue-200'
  },
  {
    title: 'Performance',
    value: `Acima da meta em ${store.dashboard.performanceMedia}%`,
    color: 'bg-green-50 border-green-200'
  }
])
</script>