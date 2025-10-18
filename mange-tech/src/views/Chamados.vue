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
      <p class="text-gray-500">Carregando...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Erro ao carregar chamados: {{ error }}
    </div>

    <!-- Chamados Grid -->
    <div v-else class="grid grid-cols-3 gap-4">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Search } from 'lucide-vue-next'
import chamadosService from '@/api/chamadosService'

const chamados = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const filtroStatus = ref('')
const filtroUrgencia = ref('')

const buscarChamados = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Montar filtros
    const filtros = {}
    if (searchTerm.value) filtros.search = searchTerm.value
    if (filtroStatus.value) filtros.status = filtroStatus.value
    if (filtroUrgencia.value) filtros.urgencia = filtroUrgencia.value
    
    // Fazer requisição
    const response = await chamadosService.getAll(filtros)
    chamados.value = response.data.results || response.data
    
  } catch (err) {
    error.value = err.message
    console.error('Erro ao buscar chamados:', err)
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

onMounted(() => {
  buscarChamados()
})
</script>