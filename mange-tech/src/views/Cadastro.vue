<!-- src/views/Cadastro.vue - MESMO DESIGN DO LOGIN -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="bg-white p-8 rounded-lg border border-gray-200 shadow-sm w-full max-w-2xl">
      <!-- Logo/Título -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">MANGE_TECH</h1>
        <p class="text-sm text-gray-500">Sistema de Gestão de Chamados</p>
      </div>

      <!-- Título da Seção -->
      <div class="text-center mb-6">
        <h2 class="text-xl font-semibold text-gray-800">Criar Nova Conta</h2>
        <p class="text-sm text-gray-500 mt-1">Preencha os dados para se cadastrar</p>
      </div>

      <!-- Formulário de Cadastro -->
      <form @submit.prevent="handleCadastro" class="space-y-4">
        <!-- Nome e Sobrenome -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Nome
            </label>
            <input
              v-model="cadastroForm.first_name"
              type="text"
              required
              autocomplete="given-name"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Nome"
              @input="clearMessages"
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
              autocomplete="family-name"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Sobrenome"
              @input="clearMessages"
            />
          </div>
        </div>

        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Usuário
          </label>
          <input
            v-model="cadastroForm.username"
            type="text"
            required
            autocomplete="username"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Escolha um nome de usuário"
            @input="clearMessages"
          />
        </div>

        <!-- E-mail -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            E-mail
          </label>
          <input
            v-model="cadastroForm.email"
            type="email"
            required
            autocomplete="email"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="seu@email.com"
            @input="clearMessages"
          />
        </div>

        <!-- Senha e Confirmar -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Senha
            </label>
            <input
              v-model="cadastroForm.password"
              type="password"
              required
              minlength="6"
              autocomplete="new-password"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Mínimo 6 caracteres"
              @input="clearMessages"
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
              autocomplete="new-password"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Digite a senha novamente"
              @input="clearMessages"
            />
          </div>
        </div>

        <!-- Mensagens de Erro/Sucesso -->
        <div v-if="error" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {{ error }}
        </div>

        <div v-if="success" class="p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
          {{ success }}
        </div>

        <!-- Botão -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-500 text-white py-2 rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {{ loading ? 'Cadastrando...' : 'Cadastrar' }}
        </button>
      </form>

      <!-- Link para Login -->
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          Já tem uma conta?
          <router-link to="/login" class="text-blue-600 hover:text-blue-700 font-medium ml-1">
            Faça login
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
const success = ref('')

const cadastroForm = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
  first_name: '',
  last_name: ''
})

const handleCadastro = async () => {
  if (loading.value) return
  
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

const clearMessages = () => {
  error.value = ''
  success.value = ''
}
</script>