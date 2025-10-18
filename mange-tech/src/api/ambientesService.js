import api from './axios'

export default {
  getAll(params = {}) {
    return api.get('/ambientes/', { params })
  },

  getById(id) {
    return api.get(`/ambientes/${id}/`)
  },

  create(dados) {
    return api.post('/ambientes/', dados)
  },

  update(id, dados) {
    return api.put(`/ambientes/${id}/`, dados)
  },

  delete(id) {
    return api.delete(`/ambientes/${id}/`)
  },

  // Buscar ativos de um ambiente específico
  getAtivos(id) {
    return api.get(`/ambientes/${id}/ativos/`)
  }
}