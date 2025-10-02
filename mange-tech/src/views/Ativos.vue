<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Ativos</h2>
        <p class="text-sm text-gray-500">Gerencie todos os ativos da empresa</p>
      </div>
      <div class="flex gap-2">
        <button class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200">
          Exportar
        </button>
        <button class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2">
          <Plus :size="16" />
          Novo Ativo
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="flex gap-2 mb-6">
      <div class="flex-1 relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Buscar por ID ou nome..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Todos os Status
      </button>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Todos os Tipos
      </button>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Todas as Localizações
      </button>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Mais Filtros
      </button>
    </div>

    <!-- Ativos Grid -->
    <div class="grid grid-cols-3 gap-4">
      <div v-for="ativo in filteredAtivos" :key="ativo.id" 
           class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-semibold text-gray-800 mb-1">{{ ativo.nome }}</h3>
            <p class="text-xs text-gray-500">ID: {{ ativo.id }}</p>
          </div>
          <span :class="`px-2 py-1 rounded text-xs font-medium ${getStatusColor(ativo.status)}`">
            {{ ativo.status }}
          </span>
        </div>
        <div class="space-y-2 text-sm">
          <p><span class="text-gray-500">Tipo:</span> <span class="text-gray-800">{{ ativo.tipo }}</span></p>
          <p><span class="text-gray-500">Localização:</span> <span class="text-gray-800">{{ ativo.localizacao }}</span></p>
          <p><span class="text-gray-500">Responsável:</span> <span class="text-gray-800">{{ ativo.responsavel }}</span></p>
          <p><span class="text-gray-500">Última Manutenção:</span> <span class="text-gray-800">{{ ativo.ultimaManutencao }}</span></p>
          <p><span class="text-gray-500">Próxima Manutenção:</span> <span class="text-gray-800">{{ ativo.proximaManutencao || 'N/A' }}</span></p>
          <p><span class="text-gray-500">Chamados Ativos:</span> <span class="text-gray-800">{{ ativo.chamadosAtivos }}</span></p>
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

const filteredAtivos = computed(() => {
  return store.ativos.filter(ativo =>
    ativo.nome.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    ativo.id.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const getStatusColor = (status) => {
  const colors = {
    'Ativo': 'bg-green-100 text-green-800',
    'Em manutenção': 'bg-yellow-100 text-yellow-800',
    'Inativo': 'bg-gray-100 text-gray-800',
    'Em análise': 'bg-blue-100 text-blue-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}
</script>