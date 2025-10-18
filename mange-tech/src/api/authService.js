// src/api/authService.js
import api from './axios'

export default {
  // Login
  async login(username, password) {
    try {
      console.log('🔄 Tentando fazer login...')
      
      const response = await api.post('/token/', {
        username,
        password
      })
      
      console.log('✅ Login bem-sucedido:', response.data)
      
      // Salvar token
      localStorage.setItem('token', response.data.access)
      localStorage.setItem('refreshToken', response.data.refresh)
      
      // Configurar header para próximas requisições
      api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
      
      return response.data
      
    } catch (error) {
      console.error('❌ Erro no login:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        message: error.message
      })
      
      // Melhorar mensagens de erro
      if (!error.response) {
        const networkError = new Error('Não foi possível conectar ao servidor. Verifique se o backend está rodando.')
        networkError.isNetworkError = true
        throw networkError
      }
      
      if (error.response.status === 404) {
        const notFoundError = new Error('Rota da API não encontrada. Verifique as URLs do backend.')
        notFoundError.isNotFound = true
        notFoundError.response = error.response
        throw notFoundError
      }
      
      throw error
    }
  },

  // Cadastro
  async register(userData) {
    try {
      console.log('🔄 Tentando registrar usuário...')
      
      const response = await api.post('/register/', userData)
      
      console.log('✅ Cadastro bem-sucedido:', response.data)
      return response.data
      
    } catch (error) {
      console.error('❌ Erro no cadastro:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      })
      
      if (!error.response) {
        const networkError = new Error('Não foi possível conectar ao servidor. Verifique se o backend está rodando.')
        networkError.isNetworkError = true
        throw networkError
      }
      
      if (error.response.status === 404) {
        const notFoundError = new Error('Rota da API não encontrada. Verifique as URLs do backend.')
        notFoundError.isNotFound = true
        notFoundError.response = error.response
        throw notFoundError
      }
      
      throw error
    }
  },

  // Logout
  logout() {
    console.log('🚪 Fazendo logout...')
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    delete api.defaults.headers.common['Authorization']
  },

  // Verificar se está autenticado
  isAuthenticated() {
    return !!localStorage.getItem('token')
  },

  // Obter token
  getToken() {
    return localStorage.getItem('token')
  },

  // Refresh token
  async refreshToken() {
    try {
      const refreshToken = localStorage.getItem('refreshToken')
      
      if (!refreshToken) {
        throw new Error('Refresh token não encontrado')
      }
      
      const response = await api.post('/token/refresh/', {
        refresh: refreshToken
      })
      
      localStorage.setItem('token', response.data.access)
      api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
      
      console.log('✅ Token renovado com sucesso')
      return response.data
      
    } catch (error) {
      console.error('❌ Erro ao renovar token:', error)
      this.logout()
      throw error
    }
  }
}