<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <div v-if="loading" class="flex flex-col justify-center items-center h-64 text-blue-600">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
      <p class="mt-4 font-medium animate-pulse">Carregando detalhes...</p>
    </div>

    <div v-else-if="chamado" class="max-w-6xl mx-auto space-y-6">
      
      <div class="flex items-center justify-between mb-2">
        <router-link to="/chamados" class="text-gray-500 hover:text-gray-800 flex items-center gap-2 transition-colors font-medium">
          <span>&larr;</span> Voltar para lista
        </router-link>
        <span class="text-xs text-gray-400">ID: #{{ chamado.id }}</span>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div class="p-6 border-b border-gray-100">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h1 class="text-2xl font-bold text-gray-900 tracking-tight">{{ chamado.titulo }}</h1>
              <p class="text-sm text-gray-500 mt-1">
                Aberto por <span class="font-semibold text-gray-700">{{ chamado.solicitante?.nome_completo || chamado.solicitante?.username }}</span> 
                em {{ formatDateTime(chamado.data_abertura) }}
              </p>
            </div>
            <div class="flex items-center gap-3">
               <span :class="getStatusClass(chamado.status)" class="px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border shadow-sm">
                 {{ chamado.status_display }}
               </span>
               <span :class="getUrgenciaClass(chamado.urgencia)" class="px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border shadow-sm flex items-center gap-1">
                 <span v-if="chamado.urgencia === 'critica' || chamado.urgencia === 'alta'">🔥</span>
                 {{ chamado.urgencia_display }}
               </span>
            </div>
          </div>
        </div>

        <div class="p-6 bg-gray-50/50">
          <h3 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Descrição do Problema</h3>
          <div class="prose max-w-none text-gray-700 bg-white p-5 rounded-lg border border-gray-200 shadow-sm">
            <p class="whitespace-pre-wrap leading-relaxed">{{ chamado.descricao }}</p>
          </div>
        </div>

        <div v-if="chamado.ativos && chamado.ativos.length" class="p-6 border-t border-gray-100">
          <h3 class="text-sm font-bold text-gray-800 uppercase tracking-wide mb-4 flex items-center gap-2">
            <span>📦</span> Ativos Vinculados
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="ativo in chamado.ativos" :key="ativo.id" class="group flex items-start bg-white border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md hover:border-blue-300 transition-all duration-200">
              
              <div class="mr-4 flex-shrink-0 flex flex-col items-center">
                <div 
                  class="relative w-24 h-24 bg-white border rounded-lg p-1 cursor-pointer overflow-hidden shadow-sm group-hover:scale-105 transition-transform"
                  @click="abrirModalQr(ativo.qrUrl, ativo.nome)"
                  title="Clique para ampliar"
                >
                  <img v-if="ativo.qrUrl" :src="ativo.qrUrl" alt="QR Code" class="w-full h-full object-contain" />
                  <div v-else class="w-full h-full bg-gray-100 flex items-center justify-center text-[10px] text-gray-400 text-center">
                    Sem QR
                  </div>
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 flex items-center justify-center transition-all">
                    <span class="opacity-0 group-hover:opacity-100 text-xl">🔍</span>
                  </div>
                </div>
                <span class="text-[10px] text-blue-600 mt-1 font-medium cursor-pointer hover:underline" @click="abrirModalQr(ativo.qrUrl, ativo.nome)">Ampliar</span>
              </div>

              <div class="flex-1 min-w-0">
                <p class="font-bold text-gray-900 truncate" :title="ativo.nome">{{ ativo.nome }}</p>
                
                <div class="mt-2 space-y-1">
                  <div>
                    <p class="text-[10px] text-gray-400 uppercase font-bold">Patrimônio</p>
                    <p class="text-xs font-mono bg-gray-100 px-1.5 py-0.5 rounded text-gray-600 inline-block border">{{ ativo.codigo_patrimonio }}</p>
                  </div>
                  <div v-if="ativo.qr_code">
                    <p class="text-[10px] text-gray-400 uppercase font-bold">Código QR</p>
                    <p class="text-xs text-blue-600 font-mono truncate">{{ ativo.qr_code }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div class="lg:col-span-1 space-y-6">
           
           <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
             <h3 class="font-bold text-gray-800 mb-4 border-b pb-2">Gerenciar Chamado</h3>
             
             <label class="text-xs font-semibold text-gray-500 uppercase">Novo Status</label>
             <div class="relative mb-3">
               <select v-model="novoStatus" class="w-full appearance-none bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5">
                 <option value="aberto">⭕ Aberto</option>
                 <option value="aguardando_responsaveis">⏳ Aguardando Resp.</option>
                 <option value="em_andamento">⚙️ Em Andamento</option>
                 <option value="realizado">✅ Realizado</option>
                 <option value="concluido">🏁 Concluído</option>
                 <option value="cancelado">🚫 Cancelado</option>
               </select>
               <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                 <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
               </div>
             </div>

             <label class="text-xs font-semibold text-gray-500 uppercase">Motivo (Obrigatório)</label>
             <textarea 
                v-model="comentarioStatus" 
                placeholder="Explique o motivo da alteração..." 
                class="w-full bg-gray-50 border border-gray-300 rounded-lg p-2.5 text-sm mb-3 focus:ring-blue-500 focus:border-blue-500 min-h-[80px]"
             ></textarea>
             
             <div class="mb-4">
                <label class="text-xs font-semibold text-gray-500 uppercase block mb-1">Evidência (Opcional)</label>
                <input type="file" @change="(e) => arquivoStatus = e.target.files[0]" class="block w-full text-xs text-gray-500 file:mr-2 file:py-1 file:px-2 file:rounded-md file:border-0 file:text-xs file:bg-gray-200 file:text-gray-700 hover:file:bg-gray-300"/>
             </div>

             <button 
                @click="atualizarStatus" 
                class="w-full bg-blue-600 text-white py-2.5 rounded-lg text-sm font-bold hover:bg-blue-700 transition shadow-md disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
                :disabled="loadingAction || !novoStatus || novoStatus === chamado.status"
             >
               <span v-if="loadingAction" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
               {{ loadingAction ? 'Salvando...' : 'Salvar Alteração' }}
             </button>
           </div>

           <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
             <div class="flex justify-between items-center mb-4 border-b pb-2">
                <h3 class="font-bold text-gray-800">Anexos Gerais</h3>
                <span class="bg-blue-100 text-blue-800 text-xs font-bold px-2.5 py-0.5 rounded-full">{{ chamado.anexos?.length || 0 }}</span>
             </div>
             
             <div v-if="chamado.anexos && chamado.anexos.length" class="space-y-3 mb-5 max-h-80 overflow-y-auto pr-1">
               <div v-for="anexo in chamado.anexos" :key="anexo.id" class="flex items-center justify-between p-3 bg-white border border-gray-200 rounded-lg hover:border-blue-400 hover:shadow-sm transition group">
                 <div class="flex items-center gap-3 overflow-hidden">
                   <div class="w-8 h-8 rounded bg-blue-50 flex items-center justify-center text-blue-500 shrink-0">
                     📎
                   </div>
                   <div class="flex flex-col min-w-0">
                     <a :href="anexo.url" target="_blank" class="text-sm font-medium text-gray-700 hover:text-blue-600 truncate block" :title="anexo.nome_arquivo">
                       {{ anexo.nome_arquivo }}
                     </a>
                     <span class="text-[10px] text-gray-400">{{ anexo.tamanho_formatado }} • {{ formatDataCurta(anexo.data_upload) }}</span>
                   </div>
                 </div>
                 <a :href="anexo.url" target="_blank" class="text-gray-400 hover:text-blue-600 p-1" title="Baixar">⬇️</a>
               </div>
             </div>
             
             <div v-else class="flex flex-col items-center justify-center py-6 border-2 border-dashed border-gray-200 rounded-lg bg-gray-50 mb-4">
               <span class="text-2xl mb-1">📂</span>
               <p class="text-sm text-gray-400">Nenhum arquivo anexado.</p>
             </div>
             
             <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
               <label class="block text-xs font-bold text-gray-500 mb-2 uppercase">Novo Upload</label>
               <div class="flex gap-2">
                 <input type="file" ref="fileInput" @change="handleFileSelect" class="block w-full text-xs text-gray-500 file:mr-2 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200"/>
               </div>
               <button 
                  v-if="arquivoSelecionado"
                  @click="enviarArquivo" 
                  class="mt-3 w-full bg-green-600 text-white py-1.5 rounded-md text-xs font-bold hover:bg-green-700 transition shadow-sm uppercase tracking-wide"
                  :disabled="loadingAction"
               >
                  {{ loadingAction ? 'Enviando 0%' : 'Enviar Arquivo Agora' }}
               </button>
             </div>
           </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          
          <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-200">
            <h3 class="font-bold text-gray-800 mb-2 flex items-center gap-2">💬 Adicionar Comentário</h3>
            <div class="flex gap-3 items-start">
              <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center font-bold text-gray-500 text-xs">EU</div>
              <div class="flex-1">
                <textarea 
                  v-model="novoComentario" 
                  placeholder="Escreva uma observação técnica..." 
                  class="w-full border-gray-300 rounded-lg shadow-sm p-3 text-sm border focus:ring-blue-500 focus:border-blue-500 min-h-[60px]"
                ></textarea>
                <div class="flex justify-between items-center mt-2">
                   <div class="flex items-center gap-2">
                     <label class="cursor-pointer flex items-center gap-1 text-xs font-medium text-gray-500 hover:text-blue-600 bg-gray-100 px-2 py-1 rounded transition">
                        📎 Anexar
                        <input type="file" @change="(e) => arquivoComentario = e.target.files[0]" class="hidden"/>
                     </label>
                     <span v-if="arquivoComentario" class="text-xs text-blue-600 truncate max-w-[150px]">{{ arquivoComentario.name }}</span>
                   </div>
                   <button 
                     @click="enviarComentario" 
                     class="bg-gray-800 text-white px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-gray-900 transition shadow-sm disabled:opacity-50"
                     :disabled="(!novoComentario && !arquivoComentario) || loadingAction"
                   >
                     Enviar
                   </button>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2 border-b pb-3">
              <span>📅</span> Linha do Tempo
            </h3>
            
            <div class="relative border-l-2 border-gray-200 ml-4 space-y-8 pl-8 pb-2">
              <div v-for="log in chamado.historico" :key="log.id" class="relative group">
                <span class="absolute -left-[41px] top-1 flex h-6 w-6 items-center justify-center rounded-full bg-white ring-4 ring-white border-2 border-blue-500 z-10 shadow-sm">
                  <div class="h-2 w-2 rounded-full bg-blue-500"></div>
                </span>
                
                <div class="bg-gray-50 rounded-lg p-4 border border-gray-100 hover:border-gray-300 transition-colors">
                  <div class="flex flex-col sm:flex-row sm:justify-between sm:items-baseline mb-2">
                     <div class="text-sm">
                        <span class="font-bold text-gray-900">{{ log.user?.nome_completo || log.user?.username }}</span> 
                        
                        <span v-if="log.comentario && log.comentario.includes('Status alterado')" class="text-gray-500 mx-1">mudou para</span>
                        <span v-else class="text-gray-500 mx-1">comentou:</span>

                        <span :class="getStatusClass(log.status)" class="px-2 py-0.5 rounded text-[10px] font-bold border inline-block uppercase">{{ log.status_display }}</span>
                     </div>
                     <span class="text-xs text-gray-400 font-mono mt-1 sm:mt-0">{{ formatDateTime(log.created_at) }}</span>
                  </div>
                  
                  <div v-if="log.comentario" class="text-sm text-gray-700 whitespace-pre-wrap pl-1">
                    {{ log.comentario }}
                  </div>

                  <div v-if="log.anexos && log.anexos.length" class="mt-3 pt-3 border-t border-gray-200 flex flex-wrap gap-2">
                     <a v-for="anexoH in log.anexos" :key="anexoH.id" :href="anexoH.url" target="_blank" class="text-xs bg-white border border-blue-200 px-3 py-1.5 rounded-md hover:bg-blue-50 text-blue-700 flex items-center gap-2 shadow-sm transition">
                        <span>📎</span> {{ anexoH.nome_arquivo }}
                     </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
    
    <div v-else class="flex flex-col items-center justify-center h-64 text-gray-500">
       <div class="text-6xl mb-4">😕</div>
       <p class="text-lg">Chamado não encontrado.</p>
       <button @click="fetchChamado" class="mt-4 text-blue-600 hover:underline font-medium">Tentar novamente</button>
    </div>

    <div v-if="modalQrAberto" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-90 p-4 transition-opacity" @click.self="fecharModalQr">
      <div class="bg-white p-4 rounded-2xl max-w-sm w-full relative shadow-2xl animate-scaleIn">
        <button @click="fecharModalQr" class="absolute top-2 right-3 text-gray-400 hover:text-gray-700 text-2xl font-bold">&times;</button>
        
        <div class="text-center">
          <h3 class="text-lg font-bold text-gray-800 mb-1">{{ qrTitulo }}</h3>
          <p class="text-xs text-gray-500 mb-4">Aponte a câmera para ler</p>
          
          <div class="bg-white p-2 border-2 border-gray-100 rounded-xl inline-block shadow-inner">
            <img :src="qrImagemAmpliada" class="w-64 h-64 object-contain" />
          </div>
          
          <div class="mt-4">
            <button @click="fecharModalQr" class="w-full bg-gray-100 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-200 transition">Fechar</button>
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

// Estados do Modal QR
const modalQrAberto = ref(false)
const qrImagemAmpliada = ref('')
const qrTitulo = ref('')

const fetchChamado = async () => {
  loading.value = true
  try {
    const res = await chamadosService.getById(route.params.id)
    const dados = res.data
    
    if (dados.ativos && dados.ativos.length) {
      for (const ativo of dados.ativos) {
        if (ativo.qr_code) {
          try {
            ativo.qrUrl = await QRCode.toDataURL(ativo.qr_code, { width: 300, margin: 2 })
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

// Modal Logic
const abrirModalQr = (url, titulo) => {
  if (!url) return
  qrImagemAmpliada.value = url
  qrTitulo.value = titulo
  modalQrAberto.value = true
}

const fecharModalQr = () => {
  modalQrAberto.value = false
}

// Actions
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

const formatDataCurta = (dataIso) => {
  if (!dataIso) return '-'
  return new Date(dataIso).toLocaleDateString('pt-BR')
}

const getStatusClass = (status) => {
  const map = {
    'aberto': 'bg-red-50 text-red-700 border-red-200',
    'aguardando_responsaveis': 'bg-yellow-50 text-yellow-700 border-yellow-200',
    'em_andamento': 'bg-blue-50 text-blue-700 border-blue-200',
    'realizado': 'bg-purple-50 text-purple-700 border-purple-200',
    'concluido': 'bg-green-50 text-green-700 border-green-200',
    'cancelado': 'bg-gray-50 text-gray-600 border-gray-200'
  }
  return map[status] || 'bg-gray-50 text-gray-700 border-gray-200'
}

const getUrgenciaClass = (urgencia) => {
  const map = {
    'critica': 'bg-red-50 text-red-700 border-red-200',
    'alta': 'bg-orange-50 text-orange-700 border-orange-200',
    'media': 'bg-yellow-50 text-yellow-700 border-yellow-200',
    'baixa': 'bg-green-50 text-green-700 border-green-200'
  }
  return map[urgencia] || 'bg-gray-50 text-gray-700 border-gray-200'
}

onMounted(() => {
  fetchChamado()
})
</script>

<style scoped>
@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.animate-scaleIn {
  animation: scaleIn 0.2s ease-out forwards;
}
</style>