// src/api/dashboardService.js
import api from './axios'

export default {
  // Buscar estatísticas gerais do backend
  async getEstatisticas() {
    try {
      const response = await api.get('/chamados/estatisticas/')
      return response.data
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error)
      throw error
    }
  },

  // Buscar chamados recentes
  async getChamadosRecentes(limit = 4) {
    try {
      const response = await api.get('/chamados/', {
        params: {
          ordering: '-created_at',
          page_size: limit
        }
      })
      return response.data.results || response.data
    } catch (error) {
      console.error('Erro ao buscar chamados recentes:', error)
      throw error
    }
  },

  // Buscar estatísticas de ativos
  async getAtivosEstatisticas() {
    try {
      const response = await api.get('/ativos/')
      const ativos = response.data.results || response.data
      
      return {
        total: ativos.length,
        ativo: ativos.filter(a => a.status === 'ativo').length,
        manutencao: ativos.filter(a => a.status === 'manutencao').length,
        inativo: ativos.filter(a => a.status === 'inativo').length,
        descartado: ativos.filter(a => a.status === 'descartado').length
      }
    } catch (error) {
      console.error('Erro ao buscar estatísticas de ativos:', error)
      throw error
    }
  },

  // Buscar tudo de uma vez
  async getDashboardCompleto() {
    try {
      const [estatisticas, chamadosRecentes, ativosStats] = await Promise.all([
        this.getEstatisticas(),
        this.getChamadosRecentes(4),
        this.getAtivosEstatisticas()
      ])

      return {
        estatisticas,
        chamadosRecentes,
        ativosStats
      }
    } catch (error) {
      console.error('Erro ao buscar dashboard completo:', error)
      throw error
    }
  }
}