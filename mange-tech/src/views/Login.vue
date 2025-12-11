<template>
  <div class="min-h-screen flex bg-white">
    
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-indigo-900 to-blue-800 text-white flex-col justify-center items-center p-12 relative overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
         <div class="absolute top-10 left-10 w-64 h-64 bg-white rounded-full mix-blend-overlay filter blur-3xl animate-blob"></div>
         <div class="absolute bottom-10 right-10 w-64 h-64 bg-purple-500 rounded-full mix-blend-overlay filter blur-3xl animate-blob animation-delay-2000"></div>
      </div>

      <div class="relative z-10 text-center">
        <div class="mb-6 inline-flex p-4 bg-white/10 rounded-2xl backdrop-blur-sm border border-white/20 shadow-xl">
           <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
        </div>
        <h2 class="text-4xl font-extrabold mb-4 tracking-tight">MANGE_TECH</h2>
        <p class="text-lg text-blue-100 max-w-md mx-auto leading-relaxed">
          Gerencie chamados, ativos e usuários com eficiência e agilidade. A solução completa para o seu suporte técnico.
        </p>
      </div>
      
      <div class="absolute bottom-8 text-xs text-blue-300">
        © 2025 Mange Tech System v1.0
      </div>
    </div>

    <div class="flex-1 flex flex-col justify-center items-center p-8 lg:p-16 bg-white">
      <div class="w-full max-w-md">
        
        <div class="lg:hidden text-center mb-8">
          <h1 class="text-3xl font-bold text-indigo-900">MANGE_TECH</h1>
          <p class="text-sm text-gray-500">Gestão de Chamados</p>
        </div>

        <div class="mb-10">
          <h2 class="text-2xl font-bold text-gray-900">Bem-vindo de volta! 👋</h2>
          <p class="text-gray-500 mt-2">Insira suas credenciais para acessar o painel.</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Usuário</label>
            <div class="relative">
              <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              </span>
              <input
                v-model="loginForm.username"
                type="text"
                required
                autocomplete="username"
                class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all text-sm"
                placeholder="Ex: joaosilva"
                @input="error = ''"
              />
            </div>
          </div>

          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-sm font-semibold text-gray-700">Senha</label>
              <a href="#" class="text-xs text-indigo-600 hover:text-indigo-800 font-medium">Esqueceu a senha?</a>
            </div>
            <div class="relative">
              <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-gray-400">
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
              </span>
              <input
                v-model="loginForm.password"
                type="password"
                required
                autocomplete="current-password"
                class="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all text-sm"
                placeholder="••••••••"
                @input="error = ''"
              />
            </div>
          </div>

          <div v-if="error" class="p-4 bg-red-50 border-l-4 border-red-500 text-red-700 text-sm rounded animate-shake">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-indigo-600 text-white py-3.5 rounded-xl font-bold hover:bg-indigo-700 active:bg-indigo-800 disabled:bg-indigo-300 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-indigo-500/30 flex justify-center items-center gap-2"
          >
            <span v-if="loading" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
            {{ loading ? 'Acessando...' : 'Entrar na Conta' }}
          </button>
        </form>

        <div class="mt-8 text-center border-t border-gray-100 pt-6">
          <p class="text-sm text-gray-600">
            Ainda não tem acesso?
            <router-link to="/cadastro" class="text-indigo-600 hover:text-indigo-800 font-bold ml-1 hover:underline">
              Criar conta gratuita
            </router-link>
          </p>
        </div>
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

const loginForm = reactive({ username: '', password: '' })

const handleLogin = async () => {
  if (loading.value) return 
  loading.value = true
  error.value = ''
  
  try {
    await authService.login(loginForm.username, loginForm.password)
    await new Promise(resolve => setTimeout(resolve, 100))
    router.push('/')
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Usuário ou senha incorretos.'
    } else {
      error.value = 'Erro de conexão. Tente novamente mais tarde.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animate-shake {
  animation: shake 0.3s cubic-bezier(.36,.07,.19,.97) both;
}
@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}
</style>