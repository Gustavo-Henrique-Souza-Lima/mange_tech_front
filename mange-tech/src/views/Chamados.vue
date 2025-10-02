<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Chamados</h2>
        <p class="text-sm text-gray-500">Gerencie todos os chamados de suporte técnico</p>
      </div>
      <button class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2">
        <Plus :size="16" />
        Novo Chamado
      </button>
    </div>

    <!-- Filters -->
    <div class="flex gap-2 mb-6">
      <div class="flex-1 relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Buscar por ID ou título..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Todos os Status
      </button>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Todas as Prioridades
      </button>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Mais Filtros
      </button>
    </div>

    <!-- Chamados Grid -->
    <div class="grid grid-cols-3 gap-4">
      <div v-for="chamado in filteredChamados" :key="chamado.id" 
           class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex items-start justify-between mb-3">
          <h3 class="font-semibold text-gray-800 flex-1">{{ chamado.titulo }}</h3>
          <span :class="`px-2 py-1 rounded text-xs font-medium ml-2 ${getStatusColor(chamado.status)}`">
            {{ chamado.status }}
          </span>
        </div>
        <p class="text-sm text-gray-600 mb-4 line-clamp-2">{{ chamado.descricao }}</p>
        <div class="space-y-2 text-sm">
          <p><span class="text-gray-500">Status:</span> <span class="text-gray-800">{{ chamado.status }}</span></p>
          <p>
            <span class="text-gray-500">Prioridade:</span>
            <span :class="`font-medium ${getPrioridadeColor(chamado.prioridade)}`">{{ chamado.prioridade }}</span>
          </p>
          <p><span class="text-gray-500">Solicitante:</span> <span class="text-gray-800">{{ chamado.solicitante }}</span></p>
          <p><span class="text-gray-500">Responsável:</span> <span class="text-gray-800">{{ chamado.responsavel || 'Não atribuído' }}</span></p>
          <p><span class="text-gray-500">Local:</span> <span class="text-gray-800">{{ chamado.local }}</span></p>
          <p v-if="chamado.ativo"><span class="text-gray-500">Ativo:</span> <span class="text-gray-800">{{ chamado.ativo }}</span></p>
          <p class="pt-2 border-t border-gray-100">
            <span class="text-gray-500">Criado:</span> <span class="text-gray-800">{{ chamado.criacao }}</span>
            •
            <span class="text-gray-500">Venc:</span> <span class="text-gray-800">{{ chamado.vencimento }}</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, Search } from 'lucide-vue-next'
import { useMockDataStore } from '../stores/mockData'

const store = useMockDataStore()
const searchTerm = ref('')

const filteredChamados = computed(() => {
  return store.chamados.filter(chamado =>
    chamado.titulo.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const getStatusColor = (status) => {
  const colors = {
    'Aberto': 'bg-red-100 text-red-800',
    'Em andamento': 'bg-blue-100 text-blue-800',
    'Aguardando responsáveis': 'bg-yellow-100 text-yellow-800',
    'Realizado': 'bg-purple-100 text-purple-800',
    'Concluído': 'bg-green-100 text-green-800',
    'Cancelado': 'bg-gray-100 text-gray-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getPrioridadeColor = (prioridade) => {
  const colors = {
    'Alta': 'text-red-600',
    'Média': 'text-yellow-600',
    'Baixa': 'text-blue-600'
  }
  return colors[prioridade] || 'text-gray-600'
}
</script>