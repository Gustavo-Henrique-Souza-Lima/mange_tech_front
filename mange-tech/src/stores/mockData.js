import { defineStore } from 'pinia'

export const useMockDataStore = defineStore('mockData', {
  state: () => ({
    dashboard: {
      chamadosAbertos: 23,
      tempoMedioResolucao: '2.4h',
      ativosAtivos: 156,
      taxaSatisfacao: 94,
      manutencoes: 8,
      tecnicosDisponiveis: 12,
      performanceMedia: 15
    },
    ativos: [
    ],
    chamados: [

    ]
  }),
  getters: {
    getAtivoById: (state) => (id) => {
      return state.ativos.find(ativo => ativo.id === id)
    },
    getChamadosByStatus: (state) => (status) => {
      return state.chamados.filter(chamado => chamado.status === status)
    }
  }
})