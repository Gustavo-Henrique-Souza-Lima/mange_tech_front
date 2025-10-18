import api from './axios'

export default {
  // Listar todos os usuários
  getAll(params = {}) {
    return api.get('/usuarios/', { params })
  },

  // Buscar usuário por ID
  getById(id) {
    return api.get(`/usuarios/${id}/`)
  },

  // Buscar usuário logado
  getMe() {
    return api.get('/usuarios/me/')
  },

  // Criar novo usuário (admin)
  create(dados) {
    return api.post('/usuarios/', dados)
  },

  // Atualizar usuário
  update(id, dados) {
    return api.put(`/usuarios/${id}/`, dados)
  },

  // Atualizar parcial
  patch(id, dados) {
    return api.patch(`/usuarios/${id}/`, dados)
  },

  // Deletar usuário
  delete(id) {
    return api.delete(`/usuarios/${id}/`)
  },

  // Buscar perfil do usuário
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