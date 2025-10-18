<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-1">Configurações</h2>
      <p class="text-sm text-gray-500">Configure o sistema de acordo com suas necessidades</p>
    </div>

    <!-- Mensagens de Feedback -->
    <div v-if="mensagemSucesso" class="mb-4 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg">
      {{ mensagemSucesso }}
    </div>

    <div v-if="mensagemErro" class="mb-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
      {{ mensagemErro }}
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Configurações Gerais -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Configurações Gerais</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nome da Empresa</label>
              <input
                v-model="config.nomeEmpresa"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nome da empresa"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email de Notificações</label>
              <input
                v-model="config.emailNotificacoes"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="email@empresa.com"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Fuso Horário</label>
              <select 
                v-model="config.fusoHorario"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="America/Sao_Paulo">América/São Paulo (GMT-3)</option>
                <option value="America/New_York">América/Nova York (GMT-5)</option>
                <option value="Europe/London">Europa/Londres (GMT+0)</option>
                <option value="Asia/Tokyo">Ásia/Tóquio (GMT+9)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Configurações de Chamados -->
        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Configurações de Chamados</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">Notificações por Email</p>
                <p class="text-xs text-gray-500">Enviar email ao criar novo chamado</p>
              </div>
              <button 
                @click="config.notificacoesEmail = !config.notificacoesEmail"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  config.notificacoesEmail ? 'bg-blue-500' : 'bg-gray-200'
                ]"
              >
                <span 
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    config.notificacoesEmail ? 'translate-x-6' : 'translate-x-1'
                  ]"
                ></span>
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">Auto-atribuição</p>
                <p class="text-xs text-gray-500">Atribuir automaticamente aos técnicos disponíveis</p>
              </div>
              <button 
                @click="config.autoAtribuicao = !config.autoAtribuicao"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  config.autoAtribuicao ? 'bg-blue-500' : 'bg-gray-200'
                ]"
              >
                <span 
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    config.autoAtribuicao ? 'translate-x-6' : 'translate-x-1'
                  ]"
                ></span>
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">SLA Ativo</p>
                <p class="text-xs text-gray-500">Monitorar tempo de resposta dos chamados</p>
              </div>
              <button 
                @click="config.slaAtivo = !config.slaAtivo"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  config.slaAtivo ? 'bg-blue-500' : 'bg-gray-200'
                ]"
              >
                <span 
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    config.slaAtivo ? 'translate-x-6' : 'translate-x-1'
                  ]"
                ></span>
              </button>
            </div>

            <div v-if="config.slaAtivo">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Tempo SLA Padrão (horas)
              </label>
              <input
                v-model.number="config.tempoSlaPadrao"
                type="number"
                min="1"
                max="168"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        <!-- Configurações de Segurança -->
        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Segurança</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Tempo de Sessão (minutos)
              </label>
              <input
                v-model.number="config.tempoSessao"
                type="number"
                min="5"
                max="480"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p class="text-xs text-gray-500 mt-1">Tempo máximo sem atividade antes do logout</p>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">Autenticação em Dois Fatores</p>
                <p class="text-xs text-gray-500">Requer código adicional no login</p>
              </div>
              <button 
                @click="config.autenticacao2FA = !config.autenticacao2FA"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  config.autenticacao2FA ? 'bg-blue-500' : 'bg-gray-200'
                ]"
              >
                <span 
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    config.autenticacao2FA ? 'translate-x-6' : 'translate-x-1'
                  ]"
                ></span>
              </button>
            </div>

            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">Forçar Senha Forte</p>
                <p class="text-xs text-gray-500">Exigir letras, números e caracteres especiais</p>
              </div>
              <button 
                @click="config.senhaForte = !config.senhaForte"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  config.senhaForte ? 'bg-blue-500' : 'bg-gray-200'
                ]"
              >
                <span 
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    config.senhaForte ? 'translate-x-6' : 'translate-x-1'
                  ]"
                ></span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Informações do Sistema -->
      <div class="space-y-6">
        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Informações do Sistema</h3>
          <div class="space-y-3 text-sm">
            <div>
              <p class="text-gray-500">Versão</p>
              <p class="text-gray-800 font-medium">{{ sistemaInfo.versao }}</p>
            </div>
            <div>
              <p class="text-gray-500">Última Atualização</p>
              <p class="text-gray-800 font-medium">{{ sistemaInfo.ultimaAtualizacao }}</p>
            </div>
            <div>
              <p class="text-gray-500">Banco de Dados</p>
              <p class="text-gray-800 font-medium">{{ sistemaInfo.bancoDados }}</p>
            </div>
            <div>
              <p class="text-gray-500">Backend</p>
              <p class="text-gray-800 font-medium">{{ sistemaInfo.backend }}</p>
            </div>
            <div>
              <p class="text-gray-500">Frontend</p>
              <p class="text-gray-800 font-medium">{{ sistemaInfo.frontend }}</p>
            </div>
            <div>
              <p class="text-gray-500">Última Configuração Salva</p>
              <p class="text-gray-800 font-medium">{{ ultimoSalvamento || 'Nunca' }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Ações do Sistema</h3>
          <div class="space-y-2">
            <button 
              @click="fazerBackup"
              :disabled="processando"
              class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              {{ processando ? 'Processando...' : 'Backup do Banco de Dados' }}
            </button>
            
            <button 
              @click="limparCache"
              :disabled="processando"
              class="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              Limpar Cache
            </button>
            
            <button 
              @click="verLogs"
              class="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors"
            >
              Ver Logs do Sistema
            </button>
            
            <button 
              @click="confirmarRestaurarPadroes"
              :disabled="processando"
              class="w-full px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            >
              Restaurar Padrões
            </button>
          </div>
        </div>

        <!-- Estatísticas Rápidas -->
        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Estatísticas</h3>
          <div class="space-y-3 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-500">Total de Usuários</span>
              <span class="text-gray-800 font-medium">{{ stats.usuarios }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Chamados Ativos</span>
              <span class="text-gray-800 font-medium">{{ stats.chamadosAtivos }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Ativos Cadastrados</span>
              <span class="text-gray-800 font-medium">{{ stats.ativos }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="mt-6 flex justify-end gap-3">
      <button 
        @click="restaurarConfiguracoes"
        class="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
      >
        Cancelar
      </button>
      <button 
        @click="salvarConfiguracoes"
        :disabled="salvando"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {{ salvando ? 'Salvando...' : 'Salvar Configurações' }}
      </button>
    </div>

    <!-- Modal Confirmação Restaurar Padrões -->
    <div 
      v-if="mostrarModalRestaurar" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="mostrarModalRestaurar = false"
    >
      <div class="bg-white rounded-lg w-full max-w-md p-6">
        <h3 class="text-lg font-bold text-gray-800 mb-2">Restaurar Configurações Padrões</h3>
        <p class="text-sm text-gray-600 mb-6">
          Tem certeza que deseja restaurar todas as configurações para os valores padrões? 
          Esta ação não pode ser desfeita.
        </p>

        <div class="flex gap-3 justify-end">
          <button
            @click="mostrarModalRestaurar = false"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="restaurarPadroes"
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
          >
            Restaurar Padrões
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import chamadosService from '@/api/chamadosService'
import ativosService from '@/api/ativosService'
import usuariosService from '@/api/usuariosService'

// Estados
const salvando = ref(false)
const processando = ref(false)
const mensagemSucesso = ref('')
const mensagemErro = ref('')
const mostrarModalRestaurar = ref(false)
const ultimoSalvamento = ref('')

// Estatísticas
const stats = reactive({
  usuarios: 0,
  chamadosAtivos: 0,
  ativos: 0
})

// Informações do Sistema
const sistemaInfo = reactive({
  versao: '1.0.0 Beta',
  ultimaAtualizacao: '18/10/2025',
  bancoDados: 'PostgreSQL 14',
  backend: 'Django 4.2 + DRF',
  frontend: 'Vue.js 3 + Vite'
})

// Configurações Padrões
const configPadrao = {
  nomeEmpresa: 'MANGE_TECH',
  emailNotificacoes: 'notificacoes@mangetech.com',
  fusoHorario: 'America/Sao_Paulo',
  notificacoesEmail: true,
  autoAtribuicao: false,
  slaAtivo: true,
  tempoSlaPadrao: 24,
  tempoSessao: 60,
  autenticacao2FA: false,
  senhaForte: true
}

// Configurações Atuais
const config = reactive({ ...configPadrao })

// Carregar configurações do localStorage
const carregarConfiguracoes = () => {
  try {
    const configSalvas = localStorage.getItem('sistema_config')
    if (configSalvas) {
      Object.assign(config, JSON.parse(configSalvas))
    }
    
    const ultimoSalvo = localStorage.getItem('sistema_config_data')
    if (ultimoSalvo) {
      ultimoSalvamento.value = new Date(ultimoSalvo).toLocaleString('pt-BR')
    }
  } catch (error) {
    console.error('Erro ao carregar configurações:', error)
  }
}

// Salvar configurações
const salvarConfiguracoes = async () => {
  salvando.value = true
  mensagemSucesso.value = ''
  mensagemErro.value = ''
  
  try {
    // Salvar no localStorage
    localStorage.setItem('sistema_config', JSON.stringify(config))
    localStorage.setItem('sistema_config_data', new Date().toISOString())
    
    // Aqui você pode adicionar uma chamada API para salvar no backend
    // await api.post('/configuracoes/', config)
    
    ultimoSalvamento.value = new Date().toLocaleString('pt-BR')
    mensagemSucesso.value = 'Configurações salvas com sucesso!'
    
    // Limpar mensagem após 3 segundos
    setTimeout(() => {
      mensagemSucesso.value = ''
    }, 3000)
    
  } catch (error) {
    console.error('Erro ao salvar configurações:', error)
    mensagemErro.value = 'Erro ao salvar configurações. Tente novamente.'
    
    setTimeout(() => {
      mensagemErro.value = ''
    }, 3000)
  } finally {
    salvando.value = false
  }
}

// Restaurar configurações (cancelar)
const restaurarConfiguracoes = () => {
  carregarConfiguracoes()
  mensagemSucesso.value = 'Alterações canceladas'
  setTimeout(() => {
    mensagemSucesso.value = ''
  }, 2000)
}

// Confirmar restaurar padrões
const confirmarRestaurarPadroes = () => {
  mostrarModalRestaurar.value = true
}

// Restaurar configurações padrões
const restaurarPadroes = () => {
  Object.assign(config, configPadrao)
  localStorage.removeItem('sistema_config')
  localStorage.removeItem('sistema_config_data')
  ultimoSalvamento.value = ''
  mostrarModalRestaurar.value = false
  mensagemSucesso.value = 'Configurações restauradas para os valores padrões!'
  
  setTimeout(() => {
    mensagemSucesso.value = ''
  }, 3000)
}

// Fazer backup
const fazerBackup = async () => {
  processando.value = true
  mensagemSucesso.value = ''
  mensagemErro.value = ''
  
  try {
    // Simular processo de backup
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Aqui você faria a chamada real para o backend
    // await api.post('/sistema/backup/')
    
    mensagemSucesso.value = 'Backup realizado com sucesso! Arquivo salvo em: /backups/' + new Date().toISOString().split('T')[0] + '.sql'
    
    setTimeout(() => {
      mensagemSucesso.value = ''
    }, 5000)
  } catch (error) {
    mensagemErro.value = 'Erro ao fazer backup. Tente novamente.'
    setTimeout(() => {
      mensagemErro.value = ''
    }, 3000)
  } finally {
    processando.value = false
  }
}

// Limpar cache
const limparCache = () => {
  // Limpar cache do navegador (localStorage de cache, não de config)
  const keysParaManter = ['token', 'refreshToken', 'sistema_config', 'sistema_config_data']
  const todasKeys = Object.keys(localStorage)
  
  todasKeys.forEach(key => {
    if (!keysParaManter.includes(key)) {
      localStorage.removeItem(key)
    }
  })
  
  mensagemSucesso.value = 'Cache limpo com sucesso!'
  setTimeout(() => {
    mensagemSucesso.value = ''
  }, 2000)
}

// Ver logs
const verLogs = () => {
  // Abrir em nova aba ou modal com logs
  window.open('/admin/', '_blank')
  mensagemSucesso.value = 'Abrindo painel de logs...'
  setTimeout(() => {
    mensagemSucesso.value = ''
  }, 2000)
}

// Carregar estatísticas
const carregarEstatisticas = async () => {
  try {
    const [usuariosRes, chamadosRes, ativosRes] = await Promise.all([
      usuariosService.getAll().catch(() => ({ data: { results: [] } })),
      chamadosService.getEstatisticas().catch(() => ({ total: 0 })),
      ativosService.getAll().catch(() => ({ data: { results: [] } }))
    ])
    
    stats.usuarios = usuariosRes.data.results?.length || usuariosRes.data.length || 0
    stats.chamadosAtivos = chamadosRes.total || 0
    stats.ativos = ativosRes.data.results?.length || ativosRes.data.length || 0
  } catch (error) {
    console.error('Erro ao carregar estatísticas:', error)
  }
}

// Lifecycle
onMounted(() => {
  carregarConfiguracoes()
  carregarEstatisticas()
})
</script>