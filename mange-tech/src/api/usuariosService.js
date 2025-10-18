// src/api/usuariosService.js
import api from './axios'

export default {
  // Listar todos os usuários
  async getAll(params = {}) {
    try {
      const response = await api.get('/usuarios/', { params })
      return response
    } catch (error) {
      console.error('Erro ao buscar usuários:', error)
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
      throw error
    }
  },

  // Buscar usuário logado
  async getMe() {
    try {
      const response = await api.get('/usuarios/me/')
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

  // Atualizar parcial (PATCH)
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
      throw error
    }
  }
}