<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    
    <div v-if="loading" class="flex flex-col justify-center items-center h-[80vh]">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent"></div>
      <p class="text-gray-500 mt-4 font-medium">Carregando seus dados...</p>
    </div>

    <div v-else-if="usuario && !loading" class="max-w-4xl mx-auto animate-fade-in-up">
      
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-800">Minha Conta</h1>
        <p class="text-sm text-gray-500">Gerencie suas informações pessoais e de acesso.</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden text-center h-full">
            <div class="h-32 bg-gradient-to-br from-indigo-600 to-purple-700"></div>
            <div class="px-6 pb-8 relative">
              <div class="relative -mt-16 mb-4 inline-block">
                <div class="h-32 w-32 rounded-full bg-white p-1.5 shadow-lg mx-auto">
                  <div class="h-full w-full rounded-full bg-indigo-50 flex items-center justify-center text-4xl font-bold text-indigo-600 border border-indigo-100">
                    {{ getIniciais(usuario) }}
                  </div>
                </div>
                <div 
                    class="absolute bottom-2 right-2 h-6 w-6 border-4 border-white rounded-full" 
                    :class="usuario.user?.is_active ? 'bg-green-500' : 'bg-red-500'" 
                    :title="usuario.user?.is_active ? 'Ativo' : 'Inativo'"
                ></div>
              </div>

              <h2 class="text-xl font-bold text-gray-900">{{ getNomeCompleto(usuario) }}</h2>
              <p class="text-sm text-gray-500 mb-4">@{{ usuario.user?.username }}</p>

              <div class="flex justify-center mb-6">
                <span :class="getCargoClass(usuario.user)" class="px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wide">
                    {{ getCargoLabel(usuario.user) }}
                </span>
              </div>

              <button 
                @click="abrirModalEdicao"
                class="w-full py-2.5 bg-white border border-gray-300 text-gray-700 font-bold rounded-lg hover:bg-gray-50 hover:text-indigo-600 transition shadow-sm flex items-center justify-center gap-2"
              >
                <Edit2 :size="18" /> Editar Perfil
              </button>
            </div>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sm:p-8">
            <h3 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2 pb-2 border-b border-gray-100">
              <User :size="20" class="text-indigo-600" /> Informações Pessoais
            </h3>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-y-6 gap-x-8">
              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase mb-1">Nome Completo</label>
                <p class="text-gray-900 font-medium">{{ usuario.user?.first_name }} {{ usuario.user?.last_name }}</p>
              </div>
              
              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase mb-1">E-mail</label>
                <p class="text-gray-900 font-medium">{{ usuario.user?.email }}</p>
              </div>

              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase mb-1">Telefone</label>
                <p class="text-gray-900 font-medium">{{ usuario.telefone || 'Não informado' }}</p>
              </div>

              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase mb-1">CPF / NIF</label>
                <p class="text-gray-900 font-medium font-mono">{{ usuario.nif || 'Não informado' }}</p>
              </div>

              <div class="sm:col-span-2">
                <label class="block text-xs font-bold text-gray-400 uppercase mb-1">Endereço</label>
                <p class="text-gray-900 font-medium">{{ usuario.endereco || 'Endereço não cadastrado' }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sm:p-8">
            <h3 class="text-lg font-bold text-gray-800 mb-6 flex items-center gap-2 pb-2 border-b border-gray-100">
              <Shield :size="20" class="text-indigo-600" /> Segurança
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase mb-1">Último Acesso</label>
                <p class="text-gray-700">{{ formatarDataHora(usuario.user?.last_login) }}</p>
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase mb-1">Membro Desde</label>
                <p class="text-gray-700">{{ formatarData(usuario.user?.date_joined || usuario.created_at) }}</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-60 z-50 flex items-center justify-center p-4 backdrop-blur-sm" @click.self="fecharModal">
      <div class="bg-white rounded-2xl w-full max-w-lg shadow-2xl animate-scale-in">
        <div class="flex items-center justify-between p-6 border-b border-gray-100">
          <h3 class="text-xl font-bold text-gray-800">Editar Meus Dados</h3>
          <button @click="fecharModal" class="text-gray-400 hover:text-gray-600"><X :size="24" /></button>
        </div>

        <form @submit.prevent="salvar" class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1">Nome</label>
              <input v-model="form.first_name" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1">Sobrenome</label>
              <input v-model="form.last_name" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1">Email</label>
            <input v-model="form.email" type="email" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" required />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1">Telefone</label>
              <input v-model="form.telefone" type="tel" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1">NIF/CPF</label>
              <input v-model="form.nif" type="text" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1">Endereço</label>
            <input v-model="form.endereco" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none" />
          </div>

          <div class="flex justify-end pt-4 gap-3">
            <button type="button" @click="fecharModal" class="px-4 py-2 border rounded-lg hover:bg-gray-50 text-gray-700" :disabled="salvando">Cancelar</button>
            <button type="submit" class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-bold shadow-md flex items-center gap-2" :disabled="salvando">
              <span v-if="salvando" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ salvando ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import usuariosService from '@/api/usuariosService'
import { User, Shield, Edit2, X } from 'lucide-vue-next'

const usuario = ref(null)
const loading = ref(true)
const showModal = ref(false)
const salvando = ref(false)

const form = reactive({
  first_name: '', last_name: '', email: '',
  telefone: '', nif: '', endereco: ''
})

const carregarDados = async () => {
  loading.value = true
  try {
    const response = await usuariosService.getMe()
    usuario.value = response.data
  } catch (err) {
    console.error('Erro ao carregar perfil:', err)
  } finally {
    loading.value = false
  }
}

const abrirModalEdicao = () => {
  if (!usuario.value) return
  const u = usuario.value
  const user = u.user || {}

  form.first_name = user.first_name || ''
  form.last_name = user.last_name || ''
  form.email = user.email || ''
  form.telefone = u.telefone || ''
  form.nif = u.nif || ''
  form.endereco = u.endereco || ''
  
  showModal.value = true
}

const fecharModal = () => {
  if (!salvando.value) showModal.value = false
}

const salvar = async () => {
  salvando.value = true
  try {
    const id = usuario.value.id 
    
    // 1. Atualiza User (Nome, Email)
    await usuariosService.updateUser(id, {
      first_name: form.first_name,
      last_name: form.last_name,
      email: form.email
    })

    // 2. Atualiza Profile (Endereço, Telefone, NIF)
    await usuariosService.updateProfile(id, {
      telefone: form.telefone,
      endereco: form.endereco,
      nif: form.nif
    })

    await carregarDados() // Recarrega para mostrar atualizado
    fecharModal()
    alert('Seus dados foram atualizados com sucesso!')
  } catch (err) {
    console.error(err)
    alert('Erro ao atualizar perfil. Verifique os dados.')
  } finally {
    salvando.value = false
  }
}

// Helpers
const getNomeCompleto = (u) => u?.user?.first_name ? `${u.user.first_name} ${u.user.last_name}` : u?.user?.username || 'Usuário'
const getIniciais = (u) => (u?.user?.username || 'U').substring(0, 2).toUpperCase()
const formatarData = (d) => d ? new Date(d).toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' }) : '-'
const formatarDataHora = (d) => d ? new Date(d).toLocaleString('pt-BR') : '-'

// --- FUNÇÕES DE EXIBIÇÃO DE CARGO PARA O TEMPLATE ---
const getCargoLabel = (user) => {
    if (!user) return 'N/A';
    const groups = user.groups || [];
    
    if (user.is_superuser || groups.includes('ADMIN')) return 'Administrador';
    if (groups.includes('SUPERVISOR')) return 'Supervisor';
    if (groups.includes('TECNICO')) return 'Técnico';
    return 'Usuário Padrão';
}

const getCargoClass = (user) => {
    if (!user) return 'bg-gray-100 text-gray-600';
    const groups = user.groups || [];
    
    if (user.is_superuser || groups.includes('ADMIN')) return 'bg-purple-100 text-purple-700 border border-purple-200';
    if (groups.includes('SUPERVISOR')) return 'bg-orange-100 text-orange-700 border border-orange-200';
    if (groups.includes('TECNICO')) return 'bg-blue-100 text-blue-700 border border-blue-200';
    return 'bg-gray-100 text-gray-600 border border-gray-200';
}

onMounted(() => {
  carregarDados()
})
</script>

<style scoped>
.animate-scale-in { animation: scaleIn 0.2s ease-out forwards; }
@keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.animate-fade-in-up { animation: fadeInUp 0.4s ease-out; }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>