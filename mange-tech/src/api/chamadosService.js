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
  },

  // Upload de Anexo Avulso (Correção: Removido Header Manual)
  async uploadAnexo(chamadoId, arquivo) {
    try {
      const formData = new FormData()
      formData.append('arquivo', arquivo)
      formData.append('chamado', chamadoId) 

      const response = await api.post('/anexos/', formData)
      return response.data
    } catch (error) {
      console.error('Erro ao enviar anexo:', error)
      throw error
    }
  },

  // Alterar Status com Anexo (Correção: Removido Header Manual)
  async alterarStatus(id, status, comentario = '', arquivo = null) {
    try {
      const formData = new FormData()
      formData.append('status', status)
      if(comentario) formData.append('comentario', comentario)
      if(arquivo) formData.append('arquivo', arquivo)

      const response = await api.post(`/chamados/${id}/alterar_status/`, formData)
      return response.data
    } catch (error) {
      console.error('Erro ao alterar status:', error)
      throw error
    }
  },

  // Adicionar Comentário com Anexo (Correção: Removido Header Manual)
  async adicionarComentario(id, comentario, arquivo = null) {
    const formData = new FormData()
    if(comentario) formData.append('comentario', comentario)
    if(arquivo) formData.append('arquivo', arquivo)

    return api.post(`/chamados/${id}/comentar/`, formData)
  },
}