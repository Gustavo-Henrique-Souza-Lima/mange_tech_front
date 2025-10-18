<!-- src/views/Login.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="bg-white p-8 rounded-lg border border-gray-200 shadow-sm w-full max-w-md">
      <!-- Logo/Título -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">MANGE_TECH</h1>
        <p class="text-sm text-gray-500">Sistema de Gestão de Chamados</p>
      </div>

      <!-- Tabs -->
      <div class="flex border-b border-gray-200 mb-6">
        <button
          @click="modo = 'login'"
          :class="[
            'flex-1 py-3 text-sm font-medium transition-colors',
            modo === 'login' 
              ? 'text-blue-600 border-b-2 border-blue-600' 
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          Entrar
        </button>
        <button
          @click="modo = 'cadastro'"
          :class="[
            'flex-1 py-3 text-sm font-medium transition-colors',
            modo === 'cadastro' 
              ? 'text-blue-600 border-b-2 border-blue-600' 
              : 'text-gray-500 hover:text-gray-700'
          ]"
        >
          Cadastrar
        </button>
      </div>

      <!-- Formulário de Login -->
      <form v-if="modo === 'login'" @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Usuário
          </label>
          <input
            v-model="loginForm.username"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Digite seu usuário"
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
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Digite sua senha"
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
          {{ loading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>

      <!-- Formulário de Cadastro -->
      <form v-else @submit.prevent="handleCadastro" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Nome
            </label>
            <input
              v-model="cadastroForm.first_name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Nome"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Sobrenome
            </label>
            <input
              v-model="cadastroForm.last_name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Sobrenome"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Usuário
          </label>
          <input
            v-model="cadastroForm.username"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Escolha um nome de usuário"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            E-mail
          </label>
          <input
            v-model="cadastroForm.email"
            type="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="seu@email.com"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Senha
          </label>
          <input
            v-model="cadastroForm.password"
            type="password"
            required
            minlength="6"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Mínimo 6 caracteres"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Confirmar Senha
          </label>
          <input
            v-model="cadastroForm.password_confirm"
            type="password"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Digite a senha novamente"
          />
        </div>

        <div v-if="error" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {{ error }}
        </div>

        <div v-if="success" class="p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
          {{ success }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-500 text-white py-2 rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {{ loading ? 'Cadastrando...' : 'Cadastrar' }}
        </button>
      </form>

      <!-- Footer -->
      <div class="mt-6 text-center">
        <p class="text-xs text-gray-500">
          {{ modo === 'login' ? 'Não tem uma conta?' : 'Já tem uma conta?' }}
          <button
            @click="toggleModo"
            class="text-blue-600 hover:text-blue-700 font-medium ml-1"
          >
            {{ modo === 'login' ? 'Cadastre-se' : 'Faça login' }}
          </button>
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

const modo = ref('login')
const loading = ref(false)
const error = ref('')
const success = ref('')

const loginForm = reactive({
  username: '',
  password: ''
})

const cadastroForm = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  first_name: '',
  last_name: ''
})

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await authService.login(loginForm.username, loginForm.password)
    router.push('/')
  } catch (err) {
    error.value = 'Usuário ou senha inválidos'
    console.error('Erro no login:', err)
  } finally {
    loading.value = false
  }
}

const handleCadastro = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  
  // Validações
  if (cadastroForm.password !== cadastroForm.password_confirm) {
    error.value = 'As senhas não coincidem'
    loading.value = false
    return
  }

  if (cadastroForm.password.length < 6) {
    error.value = 'A senha deve ter no mínimo 6 caracteres'
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
    
    success.value = 'Cadastro realizado com sucesso! Redirecionando...'
    
    // Fazer login automático
    setTimeout(async () => {
      await authService.login(cadastroForm.username, cadastroForm.password)
      router.push('/')
    }, 1500)
    
  } catch (err) {
    if (err.response?.data?.username) {
      error.value = 'Este nome de usuário já está em uso'
    } else if (err.response?.data?.email) {
      error.value = 'Este e-mail já está cadastrado'
    } else {
      error.value = 'Erro ao realizar cadastro. Tente novamente.'
    }
    console.error('Erro no cadastro:', err)
  } finally {
    loading.value = false
  }
}

const toggleModo = () => {
  modo.value = modo.value === 'login' ? 'cadastro' : 'login'
  error.value = ''
  success.value = ''
}
</script>