<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Ativos</h2>
        <p class="text-sm text-gray-500">Gerencie todos os ativos da empresa</p>
      </div>
      <button 
        @click="abrirModal"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2"
      >
        <Plus :size="16" />
        Novo Ativo
      </button>
    </div>

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
      <select v-model="filtroStatus" @change="buscarAtivos" class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 bg-white">
        <option value="">Todos os Status</option>
        <option value="ativo">Ativo</option>
        <option value="manutencao">Em Manutenção</option>
        <option value="inativo">Inativo</option>
        <option value="descartado">Descartado</option>
      </select>
    </div>

    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
      <p class="text-gray-500">Carregando ativos...</p>
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
      Erro ao carregar ativos: {{ error }}
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="ativo in ativos" 
        :key="ativo.id" 
        @click="irParaDetalhes(ativo.id)"
        class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer group"
      >
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-semibold text-gray-800 mb-1 group-hover:text-blue-600 transition-colors">{{ ativo.nome }}</h3>
            <p class="text-xs text-gray-500 font-mono bg-gray-100 px-1 rounded inline-block">{{ ativo.codigo_patrimonio || 'N/A' }}</p>
          </div>
          <span :class="`px-2 py-1 rounded text-xs font-medium ${getStatusColor(ativo.status)}`">
            {{ ativo.status_display || ativo.status }}
          </span>
        </div>
        <div class="space-y-2 text-sm">
          <p v-if="ativo.categoria" class="text-gray-600">
            <span class="text-gray-400 text-xs uppercase font-bold mr-1">Categoria:</span> 
            {{ ativo.categoria.nome }}
          </p>
          <p v-if="ativo.ambiente" class="text-gray-600">
            <span class="text-gray-400 text-xs uppercase font-bold mr-1">Local:</span> 
            {{ ativo.ambiente.nome }}
          </p>
        </div>
        
        <div class="mt-4 pt-3 border-t border-gray-100 flex justify-end">
           <span class="text-xs text-blue-600 font-medium hover:underline">Ver Detalhes →</span>
        </div>
      </div>
    </div>

    <div v-if="!loading && !error && ativos.length === 0" class="text-center py-12">
      <p class="text-gray-500">Nenhum ativo encontrado</p>
    </div>

    <div 
      v-if="mostrarModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="fecharModal"
    >
      <div class="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 class="text-xl font-bold text-gray-800">Novo Ativo</h3>
            <p class="text-sm text-gray-500 mt-1">Cadastre um novo ativo</p>
          </div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600"><X :size="24" /></button>
        </div>

        <form @submit.prevent="salvarAtivo" class="p-6">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Nome *</label>
            <input v-model="formAtivo.nome" type="text" required class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" placeholder="Ex: Notebook Dell" />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
            <textarea v-model="formAtivo.descricao" rows="3" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Código Patrimônio</label>
              <input v-model="formAtivo.codigo_patrimonio" type="text" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">QR Code</label>
              <input v-model="formAtivo.qr_code" type="text" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Categoria</label>
              <select v-model="formAtivo.categoria" class="w-full px-3 py-2 border rounded-lg bg-white">
                <option value="">Selecione...</option>
                <option v-for="cat in categorias" :key="cat.id" :value="cat.id">{{ cat.nome }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Ambiente</label>
              <select v-model="formAtivo.ambiente" class="w-full px-3 py-2 border rounded-lg bg-white">
                <option value="">Selecione...</option>
                <option v-for="amb in ambientes" :key="amb.id" :value="amb.id">{{ amb.nome }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Status *</label>
              <select v-model="formAtivo.status" required class="w-full px-3 py-2 border rounded-lg bg-white">
                <option value="ativo">Ativo</option>
                <option value="manutencao">Em Manutenção</option>
                <option value="inativo">Inativo</option>
                <option value="descartado">Descartado</option>
              </select>
            </div>
          </div>

          <div class="flex gap-3 justify-end mt-6">
            <button type="button" @click="fecharModal" class="px-4 py-2 border rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600" :disabled="salvando">
              {{ salvando ? 'Salvando...' : 'Criar Ativo' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router' // Import Router
import { Plus, Search, X } from 'lucide-vue-next'
import ativosService from '@/api/ativosService'
import api from '@/api/axios'

const router = useRouter() // Router instance

// Estados
const ativos = ref([])
const loading = ref(false)
const error = ref(null)
const searchTerm = ref('')
const filtroStatus = ref('')

// Modal
const mostrarModal = ref(false)
const salvando = ref(false)
const categorias = ref([])
const ambientes = ref([])
const formAtivo = ref({
  nome: '', descricao: '', codigo_patrimonio: '', qr_code: '', 
  categoria: '', ambiente: '', status: 'ativo'
})

// Navegação
const irParaDetalhes = (id) => {
  router.push({ name: 'ativo-detalhes', params: { id } })
}

// Funções de Dados
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
  } finally {
    loading.value = false
  }
}

const buscarDadosAuxiliares = async () => {
  try {
    const [catRes, ambRes] = await Promise.all([
      api.get('/categorias/'),
      api.get('/ambientes/')
    ])
    categorias.value = catRes.data.results || catRes.data
    ambientes.value = ambRes.data.results || ambRes.data
  } catch (err) { console.error(err) }
}

const abrirModal = () => {
  mostrarModal.value = true
  buscarDadosAuxiliares()
}

const fecharModal = () => {
  mostrarModal.value = false
  formAtivo.value = { nome: '', descricao: '', codigo_patrimonio: '', qr_code: '', categoria: '', ambiente: '', status: 'ativo' }
}

const salvarAtivo = async () => {
  salvando.value = true
  try {
    await ativosService.create(formAtivo.value)
    fecharModal()
    buscarAtivos()
    alert('Ativo criado!')
  } catch (err) {
    alert('Erro ao criar ativo.')
  } finally {
    salvando.value = false
  }
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