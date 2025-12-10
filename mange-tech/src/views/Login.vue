<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="bg-white p-8 rounded-lg border border-gray-200 shadow-sm w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">MANGE_TECH</h1>
        <p class="text-sm text-gray-500">Sistema de Gestão de Chamados</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Usuário
          </label>
          <input
            v-model="loginForm.username"
            type="text"
            required
            autocomplete="username"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Digite seu usuário"
            @input="error = ''"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Senha
          </label>
          <input
            v-model="loginForm.password"
            type="password"
            required
            autocomplete="current-password"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Digite sua senha"
            @input="error = ''"
          />
        </div>

        <div v-if="error" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-500 text-white py-2 rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="loading" class="flex items-center justify-center gap-2">
             <span class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
             Entrando...
          </span>
          <span v-else>Entrar</span>
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          Não tem uma conta?
          <router-link to="/cadastro" class="text-blue-600 hover:text-blue-700 font-medium ml-1">
            Cadastre-se aqui
          </router-link>
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

const loginForm = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  // SOLUÇÃO 2 (LÓGICA): 
  // Se já estiver carregando, cancela qualquer novo clique imediatamente.
  if (loading.value) return 
  
  loading.value = true
  error.value = ''
  
  try {
    const response = await authService.login(loginForm.username, loginForm.password)
    
    console.log('Login bem-sucedido:', response)
    
    // Pequeno delay para garantir que o token foi salvo antes de trocar de rota
    await new Promise(resolve => setTimeout(resolve, 100))
    
    router.push('/')
    
  } catch (err) {
    console.error('Erro completo no login:', err)
    
    if (err.response?.status === 401) {
      error.value = 'Usuário ou senha inválidos'
    } else if (err.response?.status === 400) {
      error.value = 'Dados inválidos. Verifique os campos.'
    } else {
      error.value = err.response?.data?.detail || 
                    err.response?.data?.message || 
                    'Erro ao fazer login. Tente novamente.'
    }
  } finally {
    // Só libera o botão quando tudo terminar (sucesso ou erro)
    loading.value = false
  }
}
</script>