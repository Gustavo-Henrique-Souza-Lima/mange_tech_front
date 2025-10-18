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

  // Deletar
  delete(id) {
    return api.delete(`/chamados/${id}/`)
  },

  // Filtrar (como na aula)
  filtrar(filtros) {
    return api.get('/chamados/', { params: filtros })
  }
}