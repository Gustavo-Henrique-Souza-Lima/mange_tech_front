import api from './axios'

export default {
  // Login
  async login(username, password) {
    try {
      const response = await api.post('/token/', {
        username,
        password
      })
      
      // Salvar token
      localStorage.setItem('token', response.data.access)
      localStorage.setItem('refreshToken', response.data.refresh)
      
      // Configurar header para próximas requisições
      api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
      
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Cadastro
  async register(userData) {
    try {
      const response = await api.post('/register/', userData)
      return response.data
    } catch (error) {
      throw error
    }
  },

  // Logout
  logout() {
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
  }
}