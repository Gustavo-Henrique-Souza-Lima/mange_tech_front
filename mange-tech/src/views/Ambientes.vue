<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Gerenciar Ambientes</h1>
      <button @click="abrirModal" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        + Novo Ambiente
      </button>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="min-w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Localização</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição</th>
            <th class="px-6 py-3 text-right">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="amb in ambientes" :key="amb.id">
            <td class="px-6 py-4">{{ amb.nome }}</td>
            <td class="px-6 py-4 text-gray-500">{{ amb.localizacao_ambiente }}</td>
            <td class="px-6 py-4 text-gray-500 text-sm">{{ amb.descricao }}</td>
            <td class="px-6 py-4 text-right">
              <button @click="remover(amb.id)" class="text-red-600 hover:text-red-900 text-sm">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="mostrarModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Novo Ambiente</h2>
        
        <form @submit.prevent="salvarAmbiente" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Nome</label>
            <input v-model="form.nome" required class="w-full border rounded p-2" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Localização</label>
            <input v-model="form.localizacao_ambiente" class="w-full border rounded p-2" placeholder="Ex: Bloco A, 2º Andar" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Descrição</label>
            <textarea v-model="form.descricao" class="w-full border rounded p-2"></textarea>
          </div>
          
          <div class="flex justify-end gap-2 mt-4">
            <button type="button" @click="mostrarModal = false" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded">Cancelar</button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Salvar</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import ambientesService from '@/api/ambientesService'

const ambientes = ref([])
const mostrarModal = ref(false)
const form = reactive({ nome: '', localizacao_ambiente: '', descricao: '' })

const carregarAmbientes = async () => {
  try {
    const res = await ambientesService.getAll()
    ambientes.value = res.data.results || res.data
  } catch (error) {
    console.error(error)
  }
}

const abrirModal = () => {
  form.nome = ''
  form.localizacao_ambiente = ''
  form.descricao = ''
  mostrarModal.value = true
}

const salvarAmbiente = async () => {
  try {
    await ambientesService.create(form)
    mostrarModal.value = false
    carregarAmbientes()
    alert('Ambiente criado!')
  } catch (error) {
    alert('Erro ao criar ambiente')
  }
}

const remover = async (id) => {
  if(!confirm('Tem certeza?')) return
  try {
    await ambientesService.delete(id)
    carregarAmbientes()
  } catch (error) {
    alert('Erro ao remover')
  }
}

onMounted(() => carregarAmbientes())
</script>