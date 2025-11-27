// src/api/usuariosService.js - VERSÃO FINAL CORRIGIDA
import api from './axios'

export default {
  // Listar todos os usuários (usando endpoint /usuarios/ do UserProfileViewSet)
  async getAll(params = {}) {
    try {
      const response = await api.get('/usuarios/', { params })
      return response
    } catch (error) {
      console.error('Erro ao buscar usuários:', error)
      
      // Fallback: se não existir, retorna apenas usuário atual
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

  // Buscar usuário por ID (endpoint do UserProfile)
  async getById(id) {
    try {
      const response = await api.get(`/usuarios/${id}/`)
      return response
    } catch (error) {
      console.error('Erro ao buscar usuário:', error)
      throw error
    }
  },

  // Buscar usuário logado
  async getMe() {
    try {
      const response = await api.get('/me/')
      return response
    } catch (error) {
      console.error('Erro ao buscar usuário atual:', error)
      throw error
    }
  },

  // ✅ ATUALIZAR PERFIL (PATCH) - UserProfile (telefone, endereco, nif)
  async updateProfile(userId, dados) {
    try {
      const payload = {
        telefone: dados.telefone || '',
        endereco: dados.endereco || '',
        nif: dados.nif || ''
      }

      console.log('📤 Atualizando perfil:', payload)
      const response = await api.patch(`/usuarios/${userId}/`, payload)
      return response
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error)
      throw error
    }
  },

  // ✅ ATUALIZAR USER (first_name, last_name, email) - NOVO ENDPOINT
  async updateUser(userId, dados) {
    try {
      const payload = {
        first_name: dados.first_name,
        last_name: dados.last_name,
        email: dados.email
      }

      console.log('📤 Atualizando dados do usuário:', payload)
      
      // Chama o novo endpoint customizado
      const response = await api.patch(`/usuarios/${userId}/update_user/`, payload)
      return response
    } catch (error) {
      console.error('Erro ao atualizar usuário:', error)
      
      // Se o endpoint não existir (404), tenta atualizar só o profile
      if (error.response?.status === 404) {
        console.warn('⚠️ Endpoint /update_user/ não encontrado. Atualize o backend.')
        throw new Error('Endpoint de atualização de usuário não implementado no backend')
      }
      
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
  }
}