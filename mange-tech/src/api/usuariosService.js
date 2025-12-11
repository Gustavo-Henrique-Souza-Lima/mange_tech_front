import api from './axios'

export default {
  // Listar todos os usuários
  async getAll(params = {}) {
    try {
      const response = await api.get('/usuarios/', { params })
      return response
    } catch (error) {
      console.error('Erro ao buscar usuários:', error)
      if (error.response?.status === 404 || error.response?.status === 403) {
        try {
            const meResponse = await api.get('/usuarios/me/')
            return {
                data: {
                    results: [meResponse.data],
                    count: 1
                }
            }
        } catch (e) {
            throw error
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
      throw error
    }
  },

  // Buscar usuário logado (para checar permissões no menu)
  async getMe() {
    try {
      const response = await api.get('/usuarios/me/')
      return response
    } catch (error) {
      console.error('Erro ao buscar usuário atual:', error)
      throw error
    }
  },

  // CRIAR USUÁRIO
  async create(dados) {
    try {
      // POST para /usuarios/ aciona o método 'create' personalizado no ViewSet
      const response = await api.post('/usuarios/', dados)
      return response
    } catch (error) {
      console.error('Erro ao criar usuário:', error)
      throw error
    }
  },

  // ATUALIZAR PERFIL 
  async updateProfile(userId, dados) {
    try {
      const payload = {
        telefone: dados.telefone || '',
        endereco: dados.endereco || '',
        nif: dados.nif || ''
      }
      const response = await api.patch(`/usuarios/${userId}/`, payload)
      return response
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error)
      throw error
    }
  },

  async updateUser(userId, dados) {
    try {
      const payload = {
        first_name: dados.first_name,
        last_name: dados.last_name,
        email: dados.email,
        is_active: dados.is_active,
        cargo: dados.cargo, 
      }

      console.log('📤 Atualizando dados do usuário:', payload)
      const response = await api.patch(`/usuarios/${userId}/update_user/`, payload)
      return response
    } catch (error) {
      console.error('Erro ao atualizar usuário (core):', error)
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