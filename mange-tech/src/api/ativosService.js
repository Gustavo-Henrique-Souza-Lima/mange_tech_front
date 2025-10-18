import api from './axios'

export default {
  getAll(params = {}) {
    return api.get('/ativos/', { params })
  },

  getById(id) {
    return api.get(`/ativos/${id}/`)
  },

  create(dados) {
    return api.post('/ativos/', dados)
  },

  update(id, dados) {
    return api.put(`/ativos/${id}/`, dados)
  },

  delete(id) {
    return api.delete(`/ativos/${id}/`)
  }
}