import api from './axios'

export default {
  getAll(params = {}) {
    return api.get('/categorias/', { params })
  },

  getById(id) {
    return api.get(`/categorias/${id}/`)
  },

  create(dados) {
    return api.post('/categorias/', dados)
  },

  update(id, dados) {
    return api.put(`/categorias/${id}/`, dados)
  },

  delete(id) {
    return api.delete(`/categorias/${id}/`)
  }
}
