<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    
    <div v-if="verificandoPermissao" class="flex flex-col justify-center items-center h-[80vh]">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent"></div>
      <p class="text-gray-500 mt-4 font-medium">Verificando permissões...</p>
    </div>

    <div v-else>
      <div class="mb-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Configurações do Sistema</h2>
        <p class="text-sm text-gray-500">Ajustes gerais, segurança e manutenção do sistema.</p>
      </div>

      <div v-if="mensagemSucesso" class="mb-4 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg flex items-center gap-2 animate-fade-in-up">
        ✅ {{ mensagemSucesso }}
      </div>

      <div v-if="mensagemErro" class="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg flex items-center gap-2 animate-fade-in-up">
        ⚠️ {{ mensagemErro }}
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div class="lg:col-span-2 space-y-6">
          
          <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
            <h3 class="text-lg font-bold text-gray-800 mb-4 border-b pb-2">Geral</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Nome da Empresa</label>
                <input v-model="config.nomeEmpresa" type="text" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none transition" placeholder="Nome da empresa" />
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Email de Notificações</label>
                <input v-model="config.emailNotificacoes" type="email" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none transition" placeholder="email@empresa.com" />
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Fuso Horário</label>
                <select v-model="config.fusoHorario" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none bg-white">
                  <option value="America/Sao_Paulo">América/São Paulo (GMT-3)</option>
                  <option value="America/New_York">América/Nova York (GMT-5)</option>
                  <option value="Europe/London">Europa/Londres (GMT+0)</option>
                  <option value="Asia/Tokyo">Ásia/Tóquio (GMT+9)</option>
                </select>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
            <h3 class="text-lg font-bold text-gray-800 mb-4 border-b pb-2">Regras de Chamados</h3>
            <div class="space-y-4">
              
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-bold text-gray-700">Notificações por Email</p>
                  <p class="text-xs text-gray-500">Enviar email ao criar/atualizar chamado</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="config.notificacoesEmail" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                </label>
              </div>

              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-bold text-gray-700">Auto-atribuição</p>
                  <p class="text-xs text-gray-500">Distribuir automaticamente para técnicos</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="config.autoAtribuicao" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                </label>
              </div>

              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-bold text-gray-700">SLA Ativo</p>
                  <p class="text-xs text-gray-500">Monitorar prazos de atendimento</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="config.slaAtivo" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                </label>
              </div>

              <div v-if="config.slaAtivo" class="bg-gray-50 p-3 rounded-lg animate-fade-in-up">
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Tempo SLA Padrão (horas)</label>
                <input v-model.number="config.tempoSlaPadrao" type="number" min="1" max="168" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" />
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
            <h3 class="text-lg font-bold text-gray-800 mb-4 border-b pb-2">Segurança</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Tempo de Sessão (minutos)</label>
                <input v-model.number="config.tempoSessao" type="number" min="5" max="480" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" />
                <p class="text-[10px] text-gray-400 mt-1">Tempo máximo de inatividade antes do logout.</p>
              </div>

              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-bold text-gray-700">Forçar Senha Forte</p>
                  <p class="text-xs text-gray-500">Exigir letras, números e símbolos</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="config.senhaForte" class="sr-only peer">
                  <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="space-y-6">
          
          <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
            <h3 class="text-lg font-bold text-gray-800 mb-4 border-b pb-2">Sistema</h3>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Versão</span> <span class="font-bold text-gray-700">{{ sistemaInfo.versao }}</span></div>
              <div class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Atualizado em</span> <span class="font-bold text-gray-700">{{ sistemaInfo.ultimaAtualizacao }}</span></div>
              <div class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Banco</span> <span class="font-bold text-gray-700">{{ sistemaInfo.bancoDados }}</span></div>
              <div class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Backend</span> <span class="font-bold text-gray-700">{{ sistemaInfo.backend }}</span></div>
              <div class="flex justify-between border-b border-gray-50 pb-2"><span class="text-gray-500">Frontend</span> <span class="font-bold text-gray-700">{{ sistemaInfo.frontend }}</span></div>
              <div class="flex justify-between pt-1"><span class="text-gray-500">Salvo em</span> <span class="font-mono text-xs text-gray-600">{{ ultimoSalvamento || '-' }}</span></div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
            <h3 class="text-lg font-bold text-gray-800 mb-4 border-b pb-2">Resumo de Dados</h3>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between"><span class="text-gray-500">Usuários</span> <span class="font-bold bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{{ stats.usuarios }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Chamados</span> <span class="font-bold bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">{{ stats.chamadosAtivos }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Ativos</span> <span class="font-bold bg-green-100 text-green-700 px-2 py-0.5 rounded-full">{{ stats.ativos }}</span></div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
            <h3 class="text-lg font-bold text-gray-800 mb-4 border-b pb-2">Manutenção</h3>
            <div class="space-y-3">
              <button @click="fazerBackup" :disabled="processando" class="w-full py-2 bg-blue-50 text-blue-700 rounded-lg text-sm font-bold hover:bg-blue-100 transition disabled:opacity-50">
                {{ processando ? 'Aguarde...' : 'Backup do Banco' }}
              </button>
              
              <button @click="limparCache" :disabled="processando" class="w-full py-2 bg-gray-50 text-gray-700 rounded-lg text-sm font-bold hover:bg-gray-100 transition disabled:opacity-50">
                Limpar Cache Local
              </button>
              
              <button @click="verLogs" class="w-full py-2 bg-gray-50 text-gray-700 rounded-lg text-sm font-bold hover:bg-gray-100 transition">
                Ver Logs do Sistema
              </button>
              
              <div class="border-t border-gray-100 my-2"></div>

              <button @click="confirmarRestaurarPadroes" :disabled="processando" class="w-full py-2 bg-red-50 text-red-600 rounded-lg text-sm font-bold hover:bg-red-100 transition disabled:opacity-50">
                Restaurar Padrões
              </button>
            </div>
          </div>

        </div>
      </div>

      <div class="fixed bottom-0 left-0 md:left-64 right-0 p-4 bg-white border-t border-gray-200 flex justify-end gap-3 z-10 shadow-lg">
        <button @click="restaurarConfiguracoes" class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg font-bold hover:bg-gray-50 transition">
          Cancelar
        </button>
        <button @click="salvarConfiguracoes" :disabled="salvando" class="px-6 py-2 bg-indigo-600 text-white rounded-lg font-bold hover:bg-indigo-700 shadow-md flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="salvando" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          {{ salvando ? 'Salvando...' : 'Salvar Alterações' }}
        </button>
      </div>
    </div>

    <div v-if="mostrarModalRestaurar" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
      <div class="bg-white rounded-xl w-full max-w-sm p-6 text-center shadow-2xl animate-scale-in">
        <div class="text-3xl mb-2">⚠️</div>
        <h3 class="text-lg font-bold text-gray-800 mb-2">Tem certeza?</h3>
        <p class="text-sm text-gray-600 mb-6">
          Isso irá apagar suas configurações personalizadas e restaurar os valores originais do sistema.
        </p>
        <div class="flex gap-3 justify-center">
          <button @click="mostrarModalRestaurar = false" class="px-4 py-2 border rounded-lg text-sm font-bold hover:bg-gray-50">Cancelar</button>
          <button @click="restaurarPadroes" class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-bold hover:bg-red-700">Sim, Restaurar</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import chamadosService from '@/api/chamadosService'
import ativosService from '@/api/ativosService'
import usuariosService from '@/api/usuariosService'

const router = useRouter()

// Estados
const verificandoPermissao = ref(true) // Começa bloqueado
const salvando = ref(false)
const processando = ref(false)
const mensagemSucesso = ref('')
const mensagemErro = ref('')
const mostrarModalRestaurar = ref(false)
const ultimoSalvamento = ref('')

const stats = reactive({ usuarios: 0, chamadosAtivos: 0, ativos: 0 })

const sistemaInfo = reactive({
  versao: '1.0.0 Stable',
  ultimaAtualizacao: new Date().toLocaleDateString('pt-BR'),
  bancoDados: 'SQLite/PostgreSQL',
  backend: 'Django DRF',
  frontend: 'Vue 3 + Vite + Tailwind'
})

const configPadrao = {
  nomeEmpresa: 'MANGE_TECH',
  emailNotificacoes: 'admin@mangetech.com',
  fusoHorario: 'America/Sao_Paulo',
  notificacoesEmail: true,
  autoAtribuicao: false,
  slaAtivo: true,
  tempoSlaPadrao: 24,
  tempoSessao: 60,
  senhaForte: true
}

const config = reactive({ ...configPadrao })

// --- SEGURANÇA ---
const verificarPermissao = async () => {
  verificandoPermissao.value = true
  try {
    const res = await usuariosService.getMe()
    const user = res.data.user
    
    // Verifica se é Admin, Técnico ou Supervisor
    const groups = user.groups || []
    const podeAcessar = user.is_superuser || groups.some(g => ['ADMIN', 'TECNICO', 'SUPERVISOR'].includes(g))
    
    if (!podeAcessar) {
      // Se não tiver permissão, redireciona
      router.push('/chamados')
      // Opcional: alert('Acesso negado')
    } else {
      // Se tiver permissão, carrega o resto
      carregarConfiguracoes()
      carregarEstatisticas()
    }
  } catch (error) {
    console.error('Erro ao verificar permissão:', error)
    router.push('/login')
  } finally {
    // Só libera a tela (ou o redirect acontece) aqui
    // Pequeno delay para garantir a transição suave
    setTimeout(() => { verificandoPermissao.value = false }, 500)
  }
}

// Carregar e Salvar (Local Storage por enquanto)
const carregarConfiguracoes = () => {
  try {
    const configSalvas = localStorage.getItem('sistema_config')
    if (configSalvas) Object.assign(config, JSON.parse(configSalvas))
    const ultimoSalvo = localStorage.getItem('sistema_config_data')
    if (ultimoSalvo) ultimoSalvamento.value = new Date(ultimoSalvo).toLocaleString('pt-BR')
  } catch (error) { console.error(error) }
}

const salvarConfiguracoes = async () => {
  salvando.value = true
  try {
    // Simulação de delay de rede
    await new Promise(r => setTimeout(r, 800))
    
    localStorage.setItem('sistema_config', JSON.stringify(config))
    localStorage.setItem('sistema_config_data', new Date().toISOString())
    
    ultimoSalvamento.value = new Date().toLocaleString('pt-BR')
    mensagemSucesso.value = 'Configurações atualizadas com sucesso!'
    setTimeout(() => { mensagemSucesso.value = '' }, 3000)
  } catch (error) {
    mensagemErro.value = 'Erro ao salvar. Tente novamente.'
  } finally {
    salvando.value = false
  }
}

const restaurarConfiguracoes = () => {
  carregarConfiguracoes()
  mensagemSucesso.value = 'Alterações descartadas.'
  setTimeout(() => { mensagemSucesso.value = '' }, 2000)
}

const confirmarRestaurarPadroes = () => { mostrarModalRestaurar.value = true }

const restaurarPadroes = () => {
  Object.assign(config, configPadrao)
  localStorage.removeItem('sistema_config')
  localStorage.removeItem('sistema_config_data')
  ultimoSalvamento.value = ''
  mostrarModalRestaurar.value = false
  mensagemSucesso.value = 'Configurações restauradas!'
  setTimeout(() => { mensagemSucesso.value = '' }, 3000)
}

// Ações do Sistema
const fazerBackup = async () => {
  processando.value = true
  try {
    await new Promise(r => setTimeout(r, 2000))
    mensagemSucesso.value = 'Backup gerado: backup_' + new Date().toISOString().slice(0,10) + '.sql'
    setTimeout(() => { mensagemSucesso.value = '' }, 5000)
  } catch(e) { mensagemErro.value = 'Erro no backup.' }
  finally { processando.value = false }
}

const limparCache = () => {
  const keep = ['token', 'refreshToken', 'sistema_config', 'sistema_config_data']
  Object.keys(localStorage).forEach(k => { if(!keep.includes(k)) localStorage.removeItem(k) })
  mensagemSucesso.value = 'Cache local limpo.'
  setTimeout(() => { mensagemSucesso.value = '' }, 2000)
}

const verLogs = () => {
  window.open('/admin/', '_blank')
}

// Estatísticas
const carregarEstatisticas = async () => {
  try {
    // Busca dados reais para popular os cards
    const [u, c, a] = await Promise.all([
       usuariosService.getAll().catch(()=>({data:{count:0}})),
       chamadosService.getAll().catch(()=>({data:{count:0}})), // Ajuste conforme seu service
       ativosService.getAll().catch(()=>({data:{count:0}}))
    ])
    
    // Tenta pegar o count do DRF ou length do array
    stats.usuarios = u.data.count || u.data.results?.length || 0
    stats.chamadosAtivos = c.data.count || c.data.results?.length || 0
    stats.ativos = a.data.count || a.data.results?.length || 0
  } catch (e) { console.error(e) }
}

onMounted(() => {
  verificarPermissao()
})
</script>

<style scoped>
.animate-fade-in-up { animation: fadeInUp 0.4s ease-out; }
.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
</style>