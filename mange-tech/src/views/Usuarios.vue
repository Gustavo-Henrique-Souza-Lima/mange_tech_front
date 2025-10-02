<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 mb-1">Usuários</h2>
        <p class="text-sm text-gray-500">Gerencie os usuários do sistema</p>
      </div>
      <button class="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600 flex items-center gap-2">
        <Plus :size="16" />
        Novo Usuário
      </button>
    </div>

    <!-- Filters -->
    <div class="flex gap-2 mb-6">
      <div class="flex-1 relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" :size="18" />
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Buscar por nome ou email..."
          class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Todos os Níveis
      </button>
      <button class="px-4 py-2 border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50">
        Status
      </button>
    </div>

    <!-- Usuarios Table -->
    <div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nível</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Setor</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="usuario in filteredUsuarios" :key="usuario.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                  <span class="text-blue-600 font-medium">{{ usuario.iniciais }}</span>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">{{ usuario.nome }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ usuario.email }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="`px-2 py-1 rounded text-xs font-medium ${getNivelColor(usuario.nivel)}`">
                {{ usuario.nivel }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ usuario.setor }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="`px-2 py-1 rounded text-xs font-medium ${usuario.ativo ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`">
                {{ usuario.ativo ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              <button class="text-blue-600 hover:text-blue-800 mr-3">Editar</button>
              <button class="text-red-600 hover:text-red-800">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, Search } from 'lucide-vue-next'

const searchTerm = ref('')

const usuarios = [
  {
    id: 1,
    nome: 'Carlos Tech',
    email: 'carlos.tech@mangetech.com',
    nivel: 'Técnico',
    setor: 'TI',
    ativo: true,
    iniciais: 'CT'
  },
  {
    id: 2,
    nome: 'Ana Tech',
    email: 'ana.tech@mangetech.com',
    nivel: 'Técnico',
    setor: 'TI',
    ativo: true,
    iniciais: 'AT'
  },
  {
    id: 3,
    nome: 'João Admin',
    email: 'joao.admin@mangetech.com',
    nivel: 'Administrador',
    setor: 'TI',
    ativo: true,
    iniciais: 'JA'
  },
  {
    id: 4,
    nome: 'Maria Tech',
    email: 'maria.tech@mangetech.com',
    nivel: 'Técnico',
    setor: 'TI',
    ativo: true,
    iniciais: 'MT'
  },
  {
    id: 5,
    nome: 'Pedro Costa',
    email: 'pedro.costa@mangetech.com',
    nivel: 'Usuário',
    setor: 'Vendas',
    ativo: true,
    iniciais: 'PC'
  },
  {
    id: 6,
    nome: 'João Silva',
    email: 'joao.silva@mangetech.com',
    nivel: 'Usuário',
    setor: 'Administrativo',
    ativo: true,
    iniciais: 'JS'
  },
  {
    id: 7,
    nome: 'Maria Santos',
    email: 'maria.santos@mangetech.com',
    nivel: 'Usuário',
    setor: 'Produção',
    ativo: true,
    iniciais: 'MS'
  },
  {
    id: 8,
    nome: 'Roberto Alves',
    email: 'roberto.alves@mangetech.com',
    nivel: 'Usuário',
    setor: 'Financeiro',
    ativo: false,
    iniciais: 'RA'
  }
]

const filteredUsuarios = computed(() => {
  return usuarios.filter(usuario =>
    usuario.nome.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    usuario.email.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const getNivelColor = (nivel) => {
  const colors = {
    'Administrador': 'bg-purple-100 text-purple-800',
    'Técnico': 'bg-blue-100 text-blue-800',
    'Usuário': 'bg-gray-100 text-gray-800'
  }
  return colors[nivel] || 'bg-gray-100 text-gray-800'
}
</script>