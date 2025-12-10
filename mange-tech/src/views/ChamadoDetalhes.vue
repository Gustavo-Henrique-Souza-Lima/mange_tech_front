<template>
  <div class="p-6">
    <div v-if="loading" class="text-center">Carregando...</div>
    
    <div v-else-if="chamado" class="max-w-4xl mx-auto space-y-6">
      
      <div class="bg-white p-6 rounded-lg shadow flex justify-between items-start">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">{{ chamado.titulo }}</h1>
          <p class="text-sm text-gray-500">Aberto em {{ formatarData(chamado.data_abertura) }} por {{ chamado.solicitante.username }}</p>
        </div>
        <div class="flex gap-2">
           <span :class="getStatusClass(chamado.status)" class="px-3 py-1 rounded-full text-sm font-semibold">
             {{ chamado.status_display }}
           </span>
           <span :class="getUrgenciaClass(chamado.urgencia)" class="px-3 py-1 rounded-full text-sm font-semibold">
             {{ chamado.urgencia_display }}
           </span>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="md:col-span-2 bg-white p-6 rounded-lg shadow">
          <h2 class="text-lg font-semibold mb-4">Descrição</h2>
          <p class="text-gray-700 whitespace-pre-wrap">{{ chamado.descricao }}</p>
          
          <div class="mt-6" v-if="chamado.ativos && chamado.ativos.length">
            <h3 class="font-semibold text-gray-600 mb-2">Ativos Relacionados (QR Code)</h3>
            <div class="flex flex-wrap gap-2">
              <div v-for="ativo in chamado.ativos" :key="ativo.id" class="bg-gray-100 p-2 rounded border text-sm">
                <p class="font-bold">{{ ativo.nome }}</p>
                <p class="text-xs text-gray-500">Patrimônio: {{ ativo.codigo_patrimonio }}</p>
                <p v-if="ativo.qr_code" class="text-xs text-blue-600">QR: {{ ativo.qr_code }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-6">
           <div class="bg-white p-6 rounded-lg shadow">
             <h3 class="font-semibold mb-3">Atualizar Status</h3>
             <select v-model="novoStatus" class="w-full border p-2 rounded mb-3">
               <option value="aberto">Aberto</option>
               <option value="em_andamento">Em Andamento</option>
               <option value="aguardando_responsaveis">Aguardando</option>
               <option value="concluido">Concluído</option>
               <option value="cancelado">Cancelado</option>
             </select>
             <textarea v-model="comentarioStatus" placeholder="Comentário sobre a mudança..." class="w-full border p-2 rounded mb-3 text-sm"></textarea>
             <button @click="atualizarStatus" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
               Salvar Mudança
             </button>
           </div>

           <div class="bg-white p-6 rounded-lg shadow">
             <h3 class="font-semibold mb-3">Anexos</h3>
             <ul v-if="chamado.anexos && chamado.anexos.length" class="space-y-2 mb-4">
               <li v-for="anexo in chamado.anexos" :key="anexo.id" class="text-sm flex justify-between items-center">
                 <a :href="anexo.url" target="_blank" class="text-blue-600 hover:underline truncate w-32">
                   {{ anexo.nome_arquivo }}
                 </a>
                 <span class="text-xs text-gray-400">{{ anexo.tamanho_formatado }}</span>
               </li>
             </ul>
             <p v-else class="text-sm text-gray-500 mb-4">Nenhum anexo.</p>
             
             <div class="border-t pt-3">
               <input type="file" ref="fileInput" @change="handleFileUpload" class="text-sm w-full mb-2" />
               <button @click="enviarArquivo" :disabled="!arquivoSelecionado" class="w-full bg-gray-200 text-gray-800 py-1 rounded text-sm hover:bg-gray-300 disabled:opacity-50">
                 Upload Anexo
               </button>
             </div>
           </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-lg shadow">
        <h2 class="text-lg font-semibold mb-4">Histórico de Alterações</h2>
        <div class="space-y-6 border-l-2 border-gray-200 ml-3 pl-6 relative">
          <div v-for="log in chamado.historico" :key="log.id" class="relative">
            <div class="absolute -left-[31px] bg-blue-500 h-4 w-4 rounded-full border-2 border-white"></div>
            <p class="text-sm text-gray-500 mb-1">
              {{ formatarData(log.created_at) }} - 
              <span class="font-bold text-gray-700">{{ log.user.username }}</span> mudou para 
              <span class="font-semibold">{{ log.status_display }}</span>
            </p>
            <div v-if="log.comentario" class="bg-gray-50 p-3 rounded text-gray-700 text-sm italic">
              "{{ log.comentario }}"
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
import chamadosService from '@/api/chamadosService'

const route = useRoute()
const chamado = ref(null)
const loading = ref(true)
const novoStatus = ref('')
const comentarioStatus = ref('')
const arquivoSelecionado = ref(null)
const fileInput = ref(null)

const fetchChamado = async () => {
  loading.value = true
  try {
    const res = await chamadosService.getById(route.params.id)
    chamado.value = res.data
    novoStatus.value = res.data.status
  } catch (error) {
    alert('Erro ao carregar chamado')
  } finally {
    loading.value = false
  }
}

const atualizarStatus = async () => {
  if(!novoStatus.value) return
  try {
    await chamadosService.alterarStatus(chamado.value.id, novoStatus.value, comentarioStatus.value)
    alert('Status atualizado!')
    comentarioStatus.value = ''
    fetchChamado() // Recarrega para ver histórico
  } catch (error) {
    alert('Erro ao atualizar status')
  }
}

const handleFileUpload = (event) => {
  arquivoSelecionado.value = event.target.files[0]
}

const enviarArquivo = async () => {
  if (!arquivoSelecionado.value) return
  try {
    await chamadosService.uploadAnexo(chamado.value.id, arquivoSelecionado.value)
    alert('Arquivo enviado!')
    arquivoSelecionado.value = null
    fileInput.value.value = '' // Limpa input
    fetchChamado() // Recarrega lista
  } catch (error) {
    alert('Erro ao enviar arquivo')
  }
}

const formatarData = (dataIso) => {
  return new Date(dataIso).toLocaleString('pt-BR')
}

// Classes utilitárias para cores (Tailwind)
const getStatusClass = (status) => {
  const map = {
    'aberto': 'bg-blue-100 text-blue-800',
    'concluido': 'bg-green-100 text-green-800',
    'em_andamento': 'bg-yellow-100 text-yellow-800',
    'cancelado': 'bg-red-100 text-red-800'
  }
  return map[status] || 'bg-gray-100 text-gray-800'
}

const getUrgenciaClass = (urgencia) => {
  const map = {
    'alta': 'bg-orange-100 text-orange-800',
    'critica': 'bg-red-100 text-red-800',
    'baixa': 'bg-green-100 text-green-800'
  }
  return map[urgencia] || 'bg-blue-100 text-blue-800'
}

onMounted(() => {
  fetchChamado()
})
</script>