<template>
  <div class="p-6">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else-if="chamado" class="max-w-5xl mx-auto space-y-6">
      
      <div class="flex items-center gap-4 mb-4">
        <router-link to="/chamados" class="text-gray-500 hover:text-gray-700 flex items-center gap-1">
          <span>←</span> Voltar
        </router-link>
        <h1 class="text-2xl font-bold text-gray-800">Chamado #{{ chamado.id }}</h1>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
        <div class="flex justify-between items-start mb-4">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ chamado.titulo }}</h2>
            <p class="text-sm text-gray-500">
              Aberto em {{ formatDateTime(chamado.data_abertura) }} por <span class="font-medium">{{ chamado.solicitante?.nome_completo || chamado.solicitante?.username }}</span>
            </p>
          </div>
          <div class="flex gap-2">
             <span :class="getStatusClass(chamado.status)" class="px-3 py-1 rounded-full text-sm font-semibold border">
               {{ chamado.status_display }}
             </span>
             <span :class="getUrgenciaClass(chamado.urgencia)" class="px-3 py-1 rounded-full text-sm font-semibold border">
               {{ chamado.urgencia_display }}
             </span>
          </div>
        </div>

        <div class="prose max-w-none text-gray-700 bg-gray-50 p-4 rounded-md mb-6 border border-gray-200">
          <p class="whitespace-pre-wrap">{{ chamado.descricao }}</p>
        </div>

        <div v-if="chamado.ativos && chamado.ativos.length" class="mb-6">
          <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wide mb-3">Ativos Relacionados</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="ativo in chamado.ativos" :key="ativo.id" class="flex items-start bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition">
              <div class="mr-4 flex-shrink-0">
                <img v-if="ativo.qrUrl" :src="ativo.qrUrl" alt="QR Code" class="w-20 h-20 border p-1 rounded bg-white" />
                <div v-else class="w-20 h-20 bg-gray-100 flex items-center justify-center rounded border text-xs text-gray-400 text-center p-1">
                  Sem QR
                </div>
              </div>
              <div>
                <p class="font-bold text-gray-900">{{ ativo.nome }}</p>
                <p class="text-xs text-gray-500 uppercase tracking-wider font-semibold mt-1">Patrimônio</p>
                <p class="text-sm font-mono bg-gray-100 px-1 rounded inline-block">{{ ativo.codigo_patrimonio }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div class="lg:col-span-1 space-y-6">
           
           <div class="bg-white p-5 rounded-lg shadow-sm border">
             <h3 class="font-bold text-gray-800 mb-3">Atualizar Status</h3>
             <select v-model="novoStatus" class="w-full border-gray-300 rounded-md shadow-sm p-2 text-sm mb-3 border focus:ring-blue-500 focus:border-blue-500">
               <option value="aberto">Aberto</option>
               <option value="aguardando_responsaveis">Aguardando Resp.</option>
               <option value="em_andamento">Em Andamento</option>
               <option value="realizado">Realizado</option>
               <option value="concluido">Concluído</option>
               <option value="cancelado">Cancelado</option>
             </select>
             <textarea 
                v-model="comentarioStatus" 
                placeholder="Motivo da alteração..." 
                class="w-full border-gray-300 rounded-md shadow-sm p-2 text-sm mb-3 border h-20 focus:ring-blue-500 focus:border-blue-500"
             ></textarea>
             
             <label class="block text-xs font-medium text-gray-700 mb-1">Evidência (opcional)</label>
             <input type="file" @change="(e) => arquivoStatus = e.target.files[0]" class="block w-full text-xs text-gray-500 mb-4 cursor-pointer"/>

             <button 
                @click="atualizarStatus" 
                class="w-full bg-blue-600 text-white py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="loadingAction || !novoStatus || novoStatus === chamado.status"
             >
               {{ loadingAction ? 'Salvando...' : 'Salvar Alteração' }}
             </button>
           </div>

           <div class="bg-white p-5 rounded-lg shadow-sm border">
             <h3 class="font-bold text-gray-800 mb-3 flex justify-between items-center">
                Anexos Gerais
                <span class="text-xs font-normal text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">{{ chamado.anexos?.length || 0 }}</span>
             </h3>
             <ul v-if="chamado.anexos && chamado.anexos.length" class="space-y-2 mb-4 max-h-60 overflow-y-auto">
               <li v-for="anexo in chamado.anexos" :key="anexo.id" class="flex items-center justify-between text-sm bg-gray-50 p-2 rounded hover:bg-gray-100 transition">
                 <div class="flex items-center overflow-hidden">
                   <span class="mr-2 text-gray-400">📎</span>
                   <a :href="anexo.url" target="_blank" class="text-blue-600 hover:underline truncate max-w-[140px]" :title="anexo.nome_arquivo">
                     {{ anexo.nome_arquivo }}
                   </a>
                 </div>
                 <span class="text-xs text-gray-400 ml-2 whitespace-nowrap">{{ anexo.tamanho_formatado }}</span>
               </li>
             </ul>
             <p v-else class="text-sm text-gray-400 italic mb-4 text-center">Nenhum anexo geral.</p>
             
             <div class="border-t pt-3">
               <label class="block text-xs font-medium text-gray-700 mb-2">Upload rápido</label>
               <input type="file" ref="fileInput" @change="handleFileSelect" class="block w-full text-xs text-gray-500 mb-2"/>
               <button 
                  v-if="arquivoSelecionado"
                  @click="enviarArquivo" 
                  class="w-full bg-green-600 text-white py-1.5 rounded text-sm hover:bg-green-700 transition shadow-sm"
                  :disabled="loadingAction"
               >
                  {{ loadingAction ? 'Enviando...' : 'Enviar Arquivo' }}
               </button>
             </div>
           </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          
          <div class="bg-white p-5 rounded-lg shadow-sm border">
            <h3 class="font-bold text-gray-800 mb-2">Adicionar Comentário / Observação</h3>
            <textarea 
              v-model="novoComentario" 
              placeholder="Escreva uma atualização sobre o chamado..." 
              class="w-full border-gray-300 rounded-md shadow-sm p-3 text-sm border focus:ring-blue-500 focus:border-blue-500 min-h-[80px]"
            ></textarea>
            
            <div class="flex justify-between items-center mt-3 pt-2 border-t border-gray-100">
               <div class="flex items-center gap-2">
                 <label class="text-xs font-medium text-gray-600">Anexar:</label>
                 <input type="file" @change="(e) => arquivoComentario = e.target.files[0]" class="text-xs text-gray-500 w-48"/>
               </div>
               
               <button 
                 @click="enviarComentario" 
                 class="bg-gray-800 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-900 transition disabled:opacity-50"
                 :disabled="(!novoComentario && !arquivoComentario) || loadingAction"
               >
                 {{ loadingAction ? 'Enviando...' : 'Comentar' }}
               </button>
            </div>
          </div>

          <div class="bg-white p-6 rounded-lg shadow-sm border">
            <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2">
              <span>📅</span> Histórico de Atividades
            </h3>
            
            <div class="relative border-l-2 border-gray-200 ml-3 space-y-8 pl-8 pb-4">
              <div v-for="log in chamado.historico" :key="log.id" class="relative group">
                <span class="absolute -left-[41px] top-1 flex h-6 w-6 items-center justify-center rounded-full bg-white ring-4 ring-white border-2 border-blue-500 z-10">
                  <div class="h-2 w-2 rounded-full bg-blue-500"></div>
                </span>
                
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-baseline mb-1">
                   <p class="text-sm font-medium text-gray-900">
                      <span class="font-bold text-gray-800">{{ log.user?.nome_completo || log.user?.username }}</span> 
                      
                      <span v-if="log.comentario && log.comentario.includes('Status alterado')" class="text-gray-500 mx-1">alterou o status para</span>
                      <span v-else class="text-gray-500 mx-1">registrou:</span>

                      <span :class="getStatusClass(log.status)" class="px-2 py-0.5 rounded text-xs border inline-block transform translate-y-[-1px]">{{ log.status_display }}</span>
                   </p>
                   <span class="text-xs text-gray-400 group-hover:text-gray-600 transition">{{ formatDateTime(log.created_at) }}</span>
                </div>
                
                <div v-if="log.comentario" class="text-sm text-gray-600 bg-gray-50 p-3 rounded-md italic border-l-4 border-gray-300 mt-1">
                  "{{ log.comentario }}"
                </div>

                <div v-if="log.anexos && log.anexos.length" class="mt-2 flex flex-wrap gap-2">
                   <a v-for="anexoH in log.anexos" :key="anexoH.id" :href="anexoH.url" target="_blank" class="text-xs bg-white border border-blue-100 px-2 py-1 rounded hover:bg-blue-50 text-blue-600 flex items-center gap-1 shadow-sm transition hover:shadow-md">
                      <span>📎</span> {{ anexoH.nome_arquivo }}
                   </a>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
    
    <div v-else class="flex flex-col items-center justify-center h-64 text-gray-500">
       <div class="text-4xl mb-2">😕</div>
       <p>Chamado não encontrado ou erro ao carregar.</p>
       <button @click="fetchChamado" class="mt-4 text-blue-600 hover:underline">Tentar novamente</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import chamadosService from '@/api/chamadosService'
import QRCode from 'qrcode'

const route = useRoute()
const chamado = ref(null)
const loading = ref(true)
const loadingAction = ref(false)

// Estados
const novoStatus = ref('')
const comentarioStatus = ref('')
const novoComentario = ref('')
const arquivoStatus = ref(null)
const arquivoComentario = ref(null)
const arquivoSelecionado = ref(null)
const fileInput = ref(null)

const fetchChamado = async () => {
  loading.value = true
  try {
    const res = await chamadosService.getById(route.params.id)
    const dados = res.data
    
    if (dados.ativos && dados.ativos.length) {
      for (const ativo of dados.ativos) {
        if (ativo.qr_code) {
          try {
            ativo.qrUrl = await QRCode.toDataURL(ativo.qr_code)
          } catch (err) { console.error(err) }
        }
      }
    }
    chamado.value = dados
    novoStatus.value = dados.status
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

// Mudar Status (com anexo opcional)
const atualizarStatus = async () => {
  if (!novoStatus.value) return
  
  if (novoStatus.value !== chamado.value.status && !comentarioStatus.value) {
    alert('Por favor, adicione um comentário explicando a mudança de status.')
    return
  }

  loadingAction.value = true
  try {
    await chamadosService.alterarStatus(
      chamado.value.id, 
      novoStatus.value, 
      comentarioStatus.value,
      arquivoStatus.value
    )
    comentarioStatus.value = ''
    arquivoStatus.value = null
    await fetchChamado() 
    alert('Status atualizado com sucesso!')
  } catch (error) {
    console.error(error)
    alert('Erro ao atualizar status.')
  } finally {
    loadingAction.value = false
  }
}

// Adicionar Comentário (com anexo opcional)
const enviarComentario = async () => {
  if (!novoComentario.value && !arquivoComentario.value) return
  
  loadingAction.value = true
  try {
    await chamadosService.adicionarComentario(
      chamado.value.id, 
      novoComentario.value,
      arquivoComentario.value
    )
    novoComentario.value = ''
    arquivoComentario.value = null
    await fetchChamado()
  } catch (error) {
    alert('Erro ao enviar comentário')
  } finally {
    loadingAction.value = false
  }
}

// Upload Rápido (Anexos Gerais)
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) arquivoSelecionado.value = file
}

const enviarArquivo = async () => {
  if (!arquivoSelecionado.value) return
  loadingAction.value = true
  try {
    await chamadosService.uploadAnexo(chamado.value.id, arquivoSelecionado.value)
    arquivoSelecionado.value = null
    if(fileInput.value) fileInput.value.value = ''
    await fetchChamado()
    alert('Arquivo anexado com sucesso!')
  } catch (error) {
    alert('Erro ao enviar arquivo.')
  } finally {
    loadingAction.value = false
  }
}

const formatDateTime = (dataIso) => {
  if (!dataIso) return '-'
  return new Date(dataIso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const getStatusClass = (status) => {
  const map = {
    'aberto': 'bg-red-50 text-red-700 border-red-200',
    'aguardando_responsaveis': 'bg-yellow-50 text-yellow-700 border-yellow-200',
    'em_andamento': 'bg-blue-50 text-blue-700 border-blue-200',
    'realizado': 'bg-purple-50 text-purple-700 border-purple-200',
    'concluido': 'bg-green-50 text-green-700 border-green-200',
    'cancelado': 'bg-gray-50 text-gray-700 border-gray-200'
  }
  return map[status] || 'bg-gray-50 text-gray-700 border-gray-200'
}

const getUrgenciaClass = (urgencia) => {
  const map = {
    'critica': 'bg-red-100 text-red-800 border-red-300',
    'alta': 'bg-orange-100 text-orange-800 border-orange-300',
    'media': 'bg-yellow-100 text-yellow-800 border-yellow-300',
    'baixa': 'bg-green-100 text-green-800 border-green-300'
  }
  return map[urgencia] || 'bg-gray-100 text-gray-800 border-gray-300'
}

onMounted(() => {
  fetchChamado()
})
</script>