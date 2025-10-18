<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Ativos</h2>
        <p class="text-sm text-gray-500">Gerencie todos os ativos da empresa</p>
      </div>
      <button class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2">
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
      <p class="text-gray-500">Carregando ativos...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Erro ao carregar ativos: {{ error }}
    </div>

    <!-- Ativos Grid -->
    <div v-else class="grid grid-cols-3 gap-4">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Search } from 'lucide-vue-next'
import ativosService from '@/api/ativosService'

const ativos = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const filtroStatus = ref('')

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

onMounted(() => {
  buscarAtivos()
})
</script>