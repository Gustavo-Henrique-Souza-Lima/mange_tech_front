<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <div v-if="loading" class="flex justify-center h-64 items-center">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
    </div>

    <div v-else-if="ativo" class="max-w-5xl mx-auto space-y-6">
      
      <div class="flex items-center gap-4 mb-2">
        <router-link to="/ativos" class="text-gray-500 hover:text-gray-800 flex items-center gap-1 font-medium">
          <span>&larr;</span> Voltar
        </router-link>
        <h1 class="text-2xl font-bold text-gray-800">{{ ativo.nome }}</h1>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <div class="space-y-6">
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 text-center">
            <div class="mb-4 flex justify-center">
              <img v-if="qrUrl" :src="qrUrl" class="w-48 h-48 border p-2 rounded-lg" />
              <div v-else class="w-48 h-48 bg-gray-100 flex items-center justify-center rounded text-gray-400">Sem QR</div>
            </div>
            <p class="text-sm font-mono bg-gray-100 py-1 rounded inline-block px-3 border mb-2">
              {{ ativo.codigo_patrimonio || 'Sem Código' }}
            </p>
            <div class="mt-2">
              <span :class="`px-3 py-1 rounded-full text-xs font-bold uppercase ${getStatusColor(ativo.status)}`">
                {{ ativo.status_display }}
              </span>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h3 class="font-bold text-gray-800 mb-4 border-b pb-2">Detalhes</h3>
            <div class="space-y-3 text-sm">
              <div>
                <p class="text-gray-500 text-xs uppercase font-bold">Categoria</p>
                <p class="font-medium">{{ ativo.categoria?.nome || '-' }}</p>
              </div>
              <div>
                <p class="text-gray-500 text-xs uppercase font-bold">Localização</p>
                <p class="font-medium">{{ ativo.ambiente?.nome || '-' }}</p>
              </div>
              <div>
                <p class="text-gray-500 text-xs uppercase font-bold">Descrição</p>
                <p class="text-gray-600">{{ ativo.descricao || 'Sem descrição.' }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="md:col-span-2">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-6 border-b border-gray-100 flex justify-between items-center">
              <h3 class="font-bold text-gray-800 flex items-center gap-2">
                <span>🔧</span> Histórico de Manutenção
              </h3>
              <router-link to="/chamados" class="text-xs text-blue-600 hover:underline">Ver todos</router-link>
            </div>

            <div v-if="chamadosRelacionados.length" class="divide-y divide-gray-100">
              <div v-for="chamado in chamadosRelacionados" :key="chamado.id" class="p-4 hover:bg-gray-50 transition flex justify-between items-start">
                <div>
                  <div class="flex items-center gap-2 mb-1">
                    <span class="text-xs font-mono text-gray-400">#{{ chamado.id }}</span>
                    <h4 class="font-bold text-gray-800 text-sm">{{ chamado.titulo }}</h4>
                  </div>
                  <p class="text-xs text-gray-500 mb-2">{{ formatDate(chamado.created_at) }}</p>
                  <span :class="`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${getChamadoStatusColor(chamado.status)}`">
                    {{ chamado.status_display }}
                  </span>
                </div>
                <router-link :to="`/chamados/${chamado.id}`" class="text-gray-400 hover:text-blue-600">
                  ➔
                </router-link>
              </div>
            </div>
            
            <div v-else class="p-8 text-center text-gray-400 text-sm">
              Nenhum chamado registrado para este ativo.
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ativosService from '@/api/ativosService'
import chamadosService from '@/api/chamadosService' // Precisamos buscar chamados
import QRCode from 'qrcode'

const route = useRoute()
const ativo = ref(null)
const chamadosRelacionados = ref([])
const loading = ref(true)
const qrUrl = ref('')

const carregarDados = async () => {
  loading.value = true
  try {
    const id = route.params.id
    
    // 1. Busca o Ativo
    const resAtivo = await ativosService.getById(id)
    ativo.value = resAtivo.data
    
    // 2. Gera QR Code
    if (ativo.value.qr_code) {
      qrUrl.value = await QRCode.toDataURL(ativo.value.qr_code, { width: 300 })
    }

    // 3. Busca Chamados filtrados por este ativo
    // Nota: O backend precisa suportar filtro ?ativo=ID
    const resChamados = await chamadosService.getAll({ ativo: id })
    chamadosRelacionados.value = resChamados.data.results || resChamados.data

  } catch (error) {
    console.error(error)
    alert('Erro ao carregar detalhes do ativo')
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => new Date(date).toLocaleDateString('pt-BR')

const getStatusColor = (status) => {
  const map = { 'ativo': 'bg-green-100 text-green-800', 'manutencao': 'bg-yellow-100 text-yellow-800', 'inativo': 'bg-gray-100 text-gray-800', 'descartado': 'bg-red-100 text-red-800' }
  return map[status] || 'bg-gray-100'
}

const getChamadoStatusColor = (status) => {
  const map = { 'aberto': 'bg-red-50 text-red-700', 'concluido': 'bg-green-50 text-green-700', 'em_andamento': 'bg-blue-50 text-blue-700' }
  return map[status] || 'bg-gray-50 text-gray-600'
}

onMounted(() => {
  carregarDados()
})
</script>