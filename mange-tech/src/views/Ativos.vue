<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <div class="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 flex items-center gap-2">
          📦 Gestão de Ativos
        </h2>
        <p class="text-sm text-gray-500 mt-1">Gerencie equipamentos, máquinas e recursos</p>
      </div>
      <button 
        @click="abrirModal"
        class="bg-blue-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-blue-700 shadow-sm flex items-center gap-2 transition-all transform hover:scale-105"
      >
        <Plus :size="18" />
        Novo Ativo
      </button>
    </div>

    <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 mb-6 flex flex-col md:flex-row gap-3">
      <div class="flex-1 relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          @input="buscarAtivos"
          type="text"
          placeholder="Buscar por nome, código ou descrição..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50 focus:bg-white transition-colors"
        />
      </div>
      <div class="flex gap-3">
        <select v-model="filtroStatus" @change="buscarAtivos" class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none">
          <option value="">Todos os Status</option>
          <option value="ativo">✅ Ativo</option>
          <option value="manutencao">🔧 Manutenção</option>
          <option value="inativo">💤 Inativo</option>
          <option value="descartado">🗑️ Descartado</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center py-20">
      <div class="animate-spin rounded-full h-10 w-10 border-4 border-blue-600 border-t-transparent"></div>
    </div>

    <div v-else-if="!ativos.length" class="text-center py-20 bg-white rounded-xl border border-dashed border-gray-300">
      <div class="text-5xl mb-3">📦</div>
      <p class="text-gray-500 font-medium">Nenhum ativo encontrado</p>
      <p class="text-sm text-gray-400">Tente ajustar os filtros ou cadastre um novo.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      <div 
        v-for="ativo in ativos" 
        :key="ativo.id" 
        @click="irParaDetalhes(ativo.id)"
        class="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-lg hover:border-blue-400 transition-all cursor-pointer group flex flex-col justify-between"
      >
        <div>
          <div class="flex justify-between items-start mb-3">
            <div class="bg-blue-50 p-2 rounded-lg text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
              <Box :size="20" />
            </div>
            <span :class="`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border ${getStatusColor(ativo.status)}`">
              {{ ativo.status_display || ativo.status }}
            </span>
          </div>
          
          <h3 class="font-bold text-gray-800 mb-1 group-hover:text-blue-600 truncate" :title="ativo.nome">{{ ativo.nome }}</h3>
          <p class="text-xs text-gray-500 font-mono bg-gray-100 px-2 py-0.5 rounded inline-block border mb-3">
            {{ ativo.codigo_patrimonio || 'S/ CÓDIGO' }}
          </p>

          <div class="space-y-2">
            <div class="flex items-center text-xs text-gray-600 gap-2">
              <Tag :size="14" class="text-gray-400"/>
              <span class="truncate">{{ ativo.categoria?.nome || 'Sem categoria' }}</span>
            </div>
            <div class="flex items-center text-xs text-gray-600 gap-2">
              <MapPin :size="14" class="text-gray-400"/>
              <span class="truncate">{{ ativo.ambiente?.nome || 'Sem local' }}</span>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-gray-100 flex justify-between items-center">
           <span class="text-[10px] text-gray-400">ID: {{ ativo.id }}</span>
           <span class="text-xs font-medium text-blue-600 group-hover:translate-x-1 transition-transform flex items-center gap-1">
             Detalhes <ChevronRight :size="14"/>
           </span>
        </div>
      </div>
    </div>

    <div v-if="mostrarModal" class="fixed inset-0 bg-black bg-opacity-60 z-40 flex items-center justify-center p-4 backdrop-blur-sm" @click.self="fecharModal">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl animate-fade-in-up">
        
        <div class="flex items-center justify-between p-6 border-b border-gray-100 sticky top-0 bg-white z-10">
          <div>
            <h3 class="text-xl font-bold text-gray-800">Cadastrar Novo Ativo</h3>
            <p class="text-xs text-gray-500 mt-0.5">Preencha os dados do equipamento</p>
          </div>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600 bg-gray-100 p-1.5 rounded-full transition"><X :size="20" /></button>
        </div>

        <form @submit.prevent="salvarAtivo" class="p-6 space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="col-span-2">
              <label class="block text-xs font-bold text-gray-700 mb-1.5 uppercase">Nome do Ativo *</label>
              <input v-model="formAtivo.nome" type="text" required class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ex: Servidor Dell PowerEdge" />
            </div>
            
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5 uppercase">Código Patrimônio</label>
              <input v-model="formAtivo.codigo_patrimonio" type="text" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ex: PAT-2024-001" />
            </div>
            
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5 uppercase">ID / Texto do QR Code</label>
              <input v-model="formAtivo.qr_code" type="text" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Gera QR automaticamente" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5 uppercase">Categoria</label>
              <div class="flex gap-2">
                <select v-model="formAtivo.categoria" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                  <option value="">Selecione...</option>
                  <option v-for="cat in categorias" :key="cat.id" :value="cat.id">{{ cat.nome }}</option>
                </select>
                <button type="button" @click="mostrarModalCategoria = true" class="bg-gray-100 hover:bg-blue-100 text-gray-600 hover:text-blue-600 border border-gray-300 rounded-lg px-3 flex items-center justify-center transition" title="Nova Categoria">
                  <Plus :size="18"/>
                </button>
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5 uppercase">Ambiente / Local</label>
              <div class="flex gap-2">
                <select v-model="formAtivo.ambiente" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white">
                  <option value="">Selecione...</option>
                  <option v-for="amb in ambientes" :key="amb.id" :value="amb.id">{{ amb.nome }}</option>
                </select>
                <button type="button" @click="mostrarModalAmbiente = true" class="bg-gray-100 hover:bg-blue-100 text-gray-600 hover:text-blue-600 border border-gray-300 rounded-lg px-3 flex items-center justify-center transition" title="Novo Ambiente">
                  <Plus :size="18"/>
                </button>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5 uppercase">Status *</label>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <label v-for="st in opcoesStatus" :key="st.valor" 
                class="cursor-pointer border rounded-lg p-2 flex flex-col items-center justify-center text-center transition-all"
                :class="formAtivo.status === st.valor ? 'bg-blue-50 border-blue-500 ring-1 ring-blue-500 text-blue-700' : 'hover:bg-gray-50 border-gray-200'"
              >
                <input type="radio" v-model="formAtivo.status" :value="st.valor" class="hidden">
                <span class="text-xl mb-1">{{ st.icon }}</span>
                <span class="text-xs font-medium">{{ st.label }}</span>
              </label>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5 uppercase">Descrição</label>
            <textarea v-model="formAtivo.descricao" rows="3" class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Detalhes técnicos..."></textarea>
          </div>

          <div class="flex gap-3 justify-end pt-4 border-t border-gray-100">
            <button type="button" @click="fecharModal" class="px-5 py-2.5 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition">Cancelar</button>
            <button type="submit" class="px-5 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium shadow-md transition disabled:opacity-50 flex items-center gap-2" :disabled="salvando">
              <span v-if="salvando" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ salvando ? 'Salvando...' : 'Salvar Ativo' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="mostrarModalCategoria" class="fixed inset-0 bg-black bg-opacity-70 z-[60] flex items-center justify-center p-4">
      <div class="bg-white rounded-xl w-full max-w-sm p-6 shadow-2xl animate-scale-in">
        <h3 class="text-lg font-bold mb-4">Nova Categoria</h3>
        <input v-model="formCategoria.nome" class="w-full border p-2 rounded mb-2" placeholder="Nome (ex: Notebooks)" />
        <textarea v-model="formCategoria.descricao" class="w-full border p-2 rounded mb-4" placeholder="Descrição rápida"></textarea>
        <div class="flex justify-end gap-2">
          <button @click="mostrarModalCategoria = false" class="text-gray-500 hover:text-gray-800 px-3">Cancelar</button>
          <button @click="salvarCategoriaRapida" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Salvar</button>
        </div>
      </div>
    </div>

    <div v-if="mostrarModalAmbiente" class="fixed inset-0 bg-black bg-opacity-70 z-[60] flex items-center justify-center p-4">
      <div class="bg-white rounded-xl w-full max-w-sm p-6 shadow-2xl animate-scale-in">
        <h3 class="text-lg font-bold mb-4">Novo Ambiente</h3>
        <input v-model="formAmbiente.nome" class="w-full border p-2 rounded mb-2" placeholder="Nome (ex: Sala TI)" />
        <input v-model="formAmbiente.localizacao_ambiente" class="w-full border p-2 rounded mb-4" placeholder="Localização (ex: Bloco B)" />
        <div class="flex justify-end gap-2">
          <button @click="mostrarModalAmbiente = false" class="text-gray-500 hover:text-gray-800 px-3">Cancelar</button>
          <button @click="salvarAmbienteRapido" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Salvar</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Search, X, Box, Tag, MapPin, ChevronRight } from 'lucide-vue-next'
import ativosService from '@/api/ativosService'
import api from '@/api/axios' // Import direto para categorias/ambientes

const router = useRouter()

// Estados principais
const ativos = ref([])
const loading = ref(false)
const searchTerm = ref('')
const filtroStatus = ref('')

// Estados Modais
const mostrarModal = ref(false)
const mostrarModalCategoria = ref(false)
const mostrarModalAmbiente = ref(false)
const salvando = ref(false)

const categorias = ref([])
const ambientes = ref([])

const formAtivo = ref({
  nome: '', descricao: '', codigo_patrimonio: '', qr_code: '', 
  categoria: '', ambiente: '', status: 'ativo'
})

// Forms Rápidos
const formCategoria = reactive({ nome: '', descricao: '' })
const formAmbiente = reactive({ nome: '', localizacao_ambiente: '' })

const opcoesStatus = [
  { valor: 'ativo', label: 'Ativo', icon: '✅' },
  { valor: 'manutencao', label: 'Manutenção', icon: '🔧' },
  { valor: 'inativo', label: 'Inativo', icon: '💤' },
  { valor: 'descartado', label: 'Descartado', icon: '🗑️' },
]

// --- Funções Principais ---

const buscarAtivos = async () => {
  loading.value = true
  try {
    const filtros = {}
    if (searchTerm.value) filtros.search = searchTerm.value
    if (filtroStatus.value) filtros.status = filtroStatus.value
    const response = await ativosService.getAll(filtros)
    ativos.value = response.data.results || response.data
  } catch (err) { console.error(err) } 
  finally { loading.value = false }
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

// --- Lógica de Criação Rápida ---

const salvarCategoriaRapida = async () => {
  if(!formCategoria.nome) return alert("Nome obrigatório")
  try {
    const res = await api.post('/categorias/', formCategoria)
    // Adiciona na lista e seleciona automaticamente
    categorias.value.push(res.data)
    formAtivo.value.categoria = res.data.id
    
    // Reseta e fecha
    formCategoria.nome = ''
    formCategoria.descricao = ''
    mostrarModalCategoria.value = false
  } catch (err) { alert('Erro ao criar categoria') }
}

const salvarAmbienteRapido = async () => {
  if(!formAmbiente.nome) return alert("Nome obrigatório")
  try {
    const res = await api.post('/ambientes/', formAmbiente)
    // Adiciona na lista e seleciona automaticamente
    ambientes.value.push(res.data)
    formAtivo.value.ambiente = res.data.id
    
    // Reseta e fecha
    formAmbiente.nome = ''
    formAmbiente.localizacao_ambiente = ''
    mostrarModalAmbiente.value = false
  } catch (err) { alert('Erro ao criar ambiente') }
}

// --- Ações do Ativo ---

const abrirModal = () => {
  mostrarModal.value = true
  buscarDadosAuxiliares()
}

const fecharModal = () => {
  if(!salvando.value) mostrarModal.value = false
}

const salvarAtivo = async () => {
  salvando.value = true
  try {
    await ativosService.create(formAtivo.value)
    fecharModal()
    buscarAtivos()
    formAtivo.value = { nome: '', descricao: '', codigo_patrimonio: '', qr_code: '', categoria: '', ambiente: '', status: 'ativo' }
    alert('Ativo criado com sucesso!')
  } catch (err) {
    alert('Erro ao criar ativo. Verifique os campos.')
  } finally {
    salvando.value = false
  }
}

const irParaDetalhes = (id) => {
  router.push({ name: 'ativo-detalhes', params: { id } })
}

const getStatusColor = (status) => {
  const colors = {
    'ativo': 'bg-green-100 text-green-700 border-green-200',
    'manutencao': 'bg-yellow-100 text-yellow-700 border-yellow-200',
    'inativo': 'bg-gray-100 text-gray-700 border-gray-200',
    'descartado': 'bg-red-100 text-red-700 border-red-200'
  }
  return colors[status] || 'bg-gray-100 text-gray-600'
}

onMounted(() => buscarAtivos())
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out;
}
</style>