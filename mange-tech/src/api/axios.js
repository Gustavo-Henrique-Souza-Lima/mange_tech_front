// src/api/axios.js

import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para adicionar token e fazer log
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Log para debug
    console.log('📤 Requisição:', {
      method: config.method.toUpperCase(),
      url: config.baseURL + config.url
    })
    
    return config
  },
  (error) => {
    console.error('❌ Erro no request interceptor:', error)
    return Promise.reject(error)
  }
)

// Interceptor para tratar erros e tentar refresh
api.interceptors.response.use(
  (response) => {
    console.log('✅ Resposta:', response.status, response.config.url)
    return response
  },
  async (error) => {
    console.error('❌ Erro na resposta:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      fullURL: error.config?.baseURL + error.config?.url,
      data: error.response?.data
    })

    const originalRequest = error.config

    // Se erro 401 e não é retry
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem('refreshToken')
      
      if (refreshToken) {
        try {
          console.log('🔄 Tentando renovar token...')
          
          const response = await axios.post(
            `${api.defaults.baseURL}/token/refresh/`,
            { refresh: refreshToken }
          )

          const { access } = response.data
          localStorage.setItem('token', access)
          
          console.log('✅ Token renovado com sucesso')

          // Retentar requisição original
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
          
        } catch (refreshError) {
          console.error('❌ Falha ao renovar token:', refreshError)
          
          // Se refresh falhar, redirecionar para login
          localStorage.removeItem('token')
          localStorage.removeItem('refreshToken')
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      } else {
        console.log('⚠️ Sem refresh token, redirecionando para login')
        
        // Sem refresh token, fazer logout
        localStorage.removeItem('token')
        localStorage.removeItem('refreshToken')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api