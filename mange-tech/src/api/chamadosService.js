// src/api/chamadosService.js
import api from './axios'

export default {
  // Buscar todos
  getAll(params = {}) {
    return api.get('/chamados/', { params })
  },

  // Buscar por ID
  getById(id) {
    return api.get(`/chamados/${id}/`)
  },

  // Criar
  create(dados) {
    return api.post('/chamados/', dados)
  },

  // Atualizar
  update(id, dados) {
    return api.put(`/chamados/${id}/`, dados)
  },

  // Atualizar parcial
  patch(id, dados) {
    return api.patch(`/chamados/${id}/`, dados)
  },

  // Deletar
  delete(id) {
    return api.delete(`/chamados/${id}/`)
  },

  // Filtrar
  filtrar(filtros) {
    return api.get('/chamados/', { params: filtros })
  },

  // Alterar status
  async alterarStatus(id, status, comentario = '') {
    try {
      const response = await api.post(`/chamados/${id}/alterar_status/`, {
        status,
        comentario
      })
      return response.data
    } catch (error) {
      console.error('Erro ao alterar status:', error)
      throw error
    }
  },

  // Atribuir responsável
  async atribuirResponsavel(id, responsavelId, role = 'responsavel_tecnico') {
    try {
      const response = await api.post(`/chamados/${id}/atribuir_responsavel/`, {
        responsavel_id: responsavelId,
        role
      })
      return response.data
    } catch (error) {
      console.error('Erro ao atribuir responsável:', error)
      throw error
    }
  },

  // Meus chamados
  async getMeusChamados() {
    try {
      const response = await api.get('/chamados/meus_chamados/')
      return response.data
    } catch (error) {
      console.error('Erro ao buscar meus chamados:', error)
      throw error
    }
  },

  // Estatísticas
  async getEstatisticas() {
    try {
      const response = await api.get('/chamados/estatisticas/')
      return response.data
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error)
      throw error
    }
  }
}