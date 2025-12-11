<template>
  <div class="min-h-screen flex bg-white">
    
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-gray-900 to-gray-800 text-white flex-col justify-center items-center p-12 relative overflow-hidden">
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5"></div>
      
      <div class="relative z-10 text-center max-w-lg">
        <h2 class="text-3xl font-bold mb-6">Junte-se à equipe</h2>
        <div class="space-y-4 text-left bg-white/5 p-6 rounded-xl backdrop-blur-sm border border-white/10">
           <div class="flex items-center gap-3">
              <div class="bg-green-500 rounded-full p-1"><svg class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg></div>
              <span>Acompanhe chamados em tempo real</span>
           </div>
           <div class="flex items-center gap-3">
              <div class="bg-green-500 rounded-full p-1"><svg class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg></div>
              <span>Gestão completa de ativos e patrimônio</span>
           </div>
           <div class="flex items-center gap-3">
              <div class="bg-green-500 rounded-full p-1"><svg class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg></div>
              <span>Relatórios e métricas de desempenho</span>
           </div>
        </div>
      </div>
    </div>

    <div class="flex-1 flex flex-col justify-center items-center p-6 lg:p-12 bg-white overflow-y-auto">
      <div class="w-full max-w-lg">
        
        <div class="mb-8">
          <router-link to="/login" class="text-sm text-gray-500 hover:text-gray-900 flex items-center gap-1 mb-4 transition-colors">
            &larr; Voltar para login
          </router-link>
          <h2 class="text-3xl font-bold text-gray-900">Criar Nova Conta</h2>
          <p class="text-gray-500 mt-2">Preencha os dados abaixo para começar.</p>
        </div>

        <form @submit.prevent="handleCadastro" class="space-y-5">
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Nome</label>
              <input v-model="cadastroForm.first_name" type="text" required class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all text-sm" placeholder="Seu nome" @input="clearMessages" />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Sobrenome</label>
              <input v-model="cadastroForm.last_name" type="text" required class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all text-sm" placeholder="Seu sobrenome" @input="clearMessages" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Usuário</label>
            <div class="relative">
               <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400 text-sm">@</span>
               <input v-model="cadastroForm.username" type="text" required class="w-full pl-8 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all text-sm" placeholder="usuario_sistema" @input="clearMessages" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">E-mail</label>
            <input v-model="cadastroForm.email" type="email" required class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all text-sm" placeholder="voce@empresa.com" @input="clearMessages" />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Senha</label>
              <input v-model="cadastroForm.password" type="password" required minlength="6" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all text-sm" placeholder="******" @input="clearMessages" />
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Confirmar</label>
              <input v-model="cadastroForm.password_confirm" type="password" required class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition-all text-sm" placeholder="******" @input="clearMessages" />
            </div>
          </div>

          <div v-if="error" class="p-4 bg-red-50 text-red-600 text-sm rounded-lg flex items-center gap-2 border border-red-100">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            {{ error }}
          </div>

          <div v-if="success" class="p-4 bg-green-50 text-green-700 text-sm rounded-lg flex items-center gap-2 border border-green-100">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            {{ success }}
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gray-900 text-white py-3.5 rounded-lg font-bold hover:bg-black disabled:bg-gray-400 disabled:cursor-not-allowed transition-all shadow-md mt-4 flex justify-center items-center gap-2"
          >
            <span v-if="loading" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ loading ? 'Criando Conta...' : 'Cadastrar-se' }}
          </button>
        </form>

        <p class="text-xs text-gray-400 mt-6 text-center">
          Ao se cadastrar, você concorda com nossos Termos de Serviço e Política de Privacidade.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/api/authService'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const success = ref('')

const cadastroForm = reactive({
  username: '', email: '', password: '', password_confirm: '',
  first_name: '', last_name: ''
})

const handleCadastro = async () => {
  if (loading.value) return
  loading.value = true
  error.value = ''
  success.value = ''
  
  if (cadastroForm.password !== cadastroForm.password_confirm) {
    error.value = 'As senhas não coincidem.'
    loading.value = false
    return
  }
  if (cadastroForm.password.length < 6) {
    error.value = 'A senha deve ter no mínimo 6 caracteres.'
    loading.value = false
    return
  }
  
  try {
    await authService.register({
      username: cadastroForm.username,
      email: cadastroForm.email,
      password: cadastroForm.password,
      first_name: cadastroForm.first_name,
      last_name: cadastroForm.last_name
    })
    
    success.value = 'Conta criada com sucesso! Redirecionando...'
    
    setTimeout(async () => {
      try {
        await authService.login(cadastroForm.username, cadastroForm.password)
        router.push('/')
      } catch (e) {
        router.push('/login')
      }
    }, 1500)
    
  } catch (err) {
    if (err.response?.data?.username) error.value = 'Este nome de usuário já está em uso.'
    else if (err.response?.data?.email) error.value = 'Este e-mail já está cadastrado.'
    else error.value = 'Erro ao criar conta. Verifique os dados.'
  } finally {
    loading.value = false
  }
}

const clearMessages = () => {
  error.value = ''
  success.value = ''
}
</script>