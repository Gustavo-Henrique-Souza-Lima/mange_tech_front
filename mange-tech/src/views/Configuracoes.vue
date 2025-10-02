<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-1">Configurações</h2>
      <p class="text-sm text-gray-500">Configure o sistema de acordo com suas necessidades</p>
    </div>

    <div class="grid grid-cols-3 gap-6">
      <!-- Configurações Gerais -->
      <div class="col-span-2 space-y-6">
        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Configurações Gerais</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nome da Empresa</label>
              <input
                type="text"
                value="MANGE_TECH"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email de Notificações</label>
              <input
                type="email"
                value="notificacoes@mangetech.com"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Fuso Horário</label>
              <select class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option>América/São Paulo (GMT-3)</option>
                <option>América/Nova York (GMT-5)</option>
                <option>Europa/Londres (GMT+0)</option>
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
              <button class="relative inline-flex h-6 w-11 items-center rounded-full bg-blue-500">
                <span class="translate-x-6 inline-block h-4 w-4 transform rounded-full bg-white transition"></span>
              </button>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">Auto-atribuição</p>
                <p class="text-xs text-gray-500">Atribuir automaticamente aos técnicos disponíveis</p>
              </div>
              <button class="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200">
                <span class="translate-x-1 inline-block h-4 w-4 transform rounded-full bg-white transition"></span>
              </button>
            </div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">SLA Ativo</p>
                <p class="text-xs text-gray-500">Monitorar tempo de resposta dos chamados</p>
              </div>
              <button class="relative inline-flex h-6 w-11 items-center rounded-full bg-blue-500">
                <span class="translate-x-6 inline-block h-4 w-4 transform rounded-full bg-white transition"></span>
              </button>
            </div>
          </div>
        </div>

        <!-- Configurações de Segurança -->
        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Segurança</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tempo de Sessão (minutos)</label>
              <input
                type="number"
                value="60"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">Autenticação em Dois Fatores</p>
                <p class="text-xs text-gray-500">Requer código adicional no login</p>
              </div>
              <button class="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200">
                <span class="translate-x-1 inline-block h-4 w-4 transform rounded-full bg-white transition"></span>
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
              <p class="text-gray-800 font-medium">1.0.0 Beta</p>
            </div>
            <div>
              <p class="text-gray-500">Última Atualização</p>
              <p class="text-gray-800 font-medium">01/10/2025</p>
            </div>
            <div>
              <p class="text-gray-500">Banco de Dados</p>
              <p class="text-gray-800 font-medium">MySQL 8.0</p>
            </div>
            <div>
              <p class="text-gray-500">Backend</p>
              <p class="text-gray-800 font-medium">Django 4.2</p>
            </div>
            <div>
              <p class="text-gray-500">Frontend</p>
              <p class="text-gray-800 font-medium">Vue.js 3</p>
            </div>
          </div>
        </div>

        <div class="bg-white p-6 rounded-lg border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Ações do Sistema</h3>
          <div class="space-y-2">
            <button class="w-full px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600">
              Backup do Banco de Dados
            </button>
            <button class="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200">
              Limpar Cache
            </button>
            <button class="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200">
              Ver Logs do Sistema
            </button>
            <button class="w-full px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium hover:bg-red-600">
              Restaurar Padrões
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="mt-6 flex justify-end">
      <button class="px-6 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600">
        Salvar Configurações
      </button>
    </div>
  </div>
</template>

<script setup>
// Configurações component
</script>