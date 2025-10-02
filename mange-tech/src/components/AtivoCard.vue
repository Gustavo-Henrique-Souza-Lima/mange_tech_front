<template>
  <div class="bg-white p-5 rounded-lg border border-gray-200 hover:shadow-md transition-shadow cursor-pointer">
    <div class="flex items-start justify-between mb-3">
      <div>
        <h3 class="font-semibold text-gray-800 mb-1">{{ ativo.nome }}</h3>
        <p class="text-xs text-gray-500">ID: {{ ativo.id }}</p>
      </div>
      <span :class="`px-2 py-1 rounded text-xs font-medium ${getStatusColor(ativo.status)}`">
        {{ ativo.status }}
      </span>
    </div>
    <div class="space-y-2 text-sm">
      <p><span class="text-gray-500">Tipo:</span> <span class="text-gray-800">{{ ativo.tipo }}</span></p>
      <p><span class="text-gray-500">Localização:</span> <span class="text-gray-800">{{ ativo.localizacao }}</span></p>
      <p><span class="text-gray-500">Responsável:</span> <span class="text-gray-800">{{ ativo.responsavel }}</span></p>
      <p><span class="text-gray-500">Última Manutenção:</span> <span class="text-gray-800">{{ ativo.ultimaManutencao }}</span></p>
      <p><span class="text-gray-500">Próxima Manutenção:</span> <span class="text-gray-800">{{ ativo.proximaManutencao || 'N/A' }}</span></p>
      <p><span class="text-gray-500">Chamados Ativos:</span> <span class="text-gray-800">{{ ativo.chamadosAtivos }}</span></p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  ativo: {
    type: Object,
    required: true
  }
})

const getStatusColor = (status) => {
  const colors = {
    'Ativo': 'bg-green-100 text-green-800',
    'Em manutenção': 'bg-yellow-100 text-yellow-800',
    'Inativo': 'bg-gray-100 text-gray-800',
    'Em análise': 'bg-blue-100 text-blue-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}
</script>