// src/api/usuariosService.js - OPÇÃO B (Usando endpoints existentes)
import api from './axios'

export default {
  // Listar todos os usuários
  async getAll(params = {}) {
    try {
      // Tenta primeiro o endpoint personalizado, se não existir usa o /me/ como fallback
      const response = await api.get('/usuarios/', { params })
      return response
    } catch (error) {
      // Se /usuarios/ não existir, você pode listar via outro endpoint
      // ou criar uma lista manual buscando apenas o usuário atual
      console.error('Erro ao buscar usuários:', error)
      
      // Fallback: retorna apenas o usuário atual se o endpoint não existir
      if (error.response?.status === 404) {
        console.warn('⚠️ Endpoint /usuarios/ não encontrado, retornando apenas usuário atual')
        const meResponse = await api.get('/me/')
        return {
          data: {
            results: [meResponse.data],
            count: 1
          }
        }
      }
      
      throw error
    }
  },

  // Buscar usuário por ID
  async getById(id) {
    try {
      const response = await api.get(`/usuarios/${id}/`)
      return response
    } catch (error) {
      console.error('Erro ao buscar usuário:', error)
      
      // Se não existir endpoint de usuários, busca o atual
      if (error.response?.status === 404) {
        const meResponse = await api.get('/me/')
        if (meResponse.data.id === id) {
          return meResponse
        }
      }
      
      throw error
    }
  },

  // Buscar usuário logado (endpoint que SEMPRE existe)
  async getMe() {
    try {
      const response = await api.get('/me/')
      return response
    } catch (error) {
      console.error('Erro ao buscar usuário atual:', error)
      throw error
    }
  },

  // Atualizar usuário (PUT completo)
  async update(id, dados) {
    try {
      const response = await api.put(`/usuarios/${id}/`, dados)
      return response
    } catch (error) {
      console.error('Erro ao atualizar usuário:', error)
      throw error
    }
  },

  // Atualizar parcial (PATCH) - MELHOR PARA EDIÇÃO
  async patch(id, dados) {
    try {
      const response = await api.patch(`/usuarios/${id}/`, dados)
      return response
    } catch (error) {
      console.error('Erro ao atualizar usuário:', error)
      throw error
    }
  },

  // Deletar usuário
  async delete(id) {
    try {
      const response = await api.delete(`/usuarios/${id}/`)
      return response
    } catch (error) {
      console.error('Erro ao deletar usuário:', error)
      throw error
    }
  },

  // Buscar perfil completo do usuário
  async getPerfil(id) {
    try {
      const response = await api.get(`/usuarios/${id}/`)
      return response.data
    } catch (error) {
      console.error('Erro ao buscar perfil:', error)
      
      // Se não existir, tenta buscar o usuário atual
      if (error.response?.status === 404) {
        const meResponse = await api.get('/me/')
        if (meResponse.data.id === id) {
          return meResponse.data
        }
      }
      
      throw error
    }
  },

  // ========================================
  // MÉTODOS AUXILIARES - SEM API
  // ========================================
  
  // Buscar múltiplos usuários por IDs (útil para responsáveis)
  async getBatch(ids) {
    try {
      const promises = ids.map(id => this.getById(id))
      const responses = await Promise.all(promises)
      return responses.map(r => r.data)
    } catch (error) {
      console.error('Erro ao buscar usuários em lote:', error)
      throw error
    }
  },

  // Buscar usuários com filtro de busca (simula search)
  async search(termo) {
    try {
      const response = await this.getAll({ search: termo })
      return response.data.results || response.data
    } catch (error) {
      console.error('Erro ao buscar usuários:', error)
      throw error
    }
  }
}