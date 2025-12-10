import { describe, it, expect, vi, beforeEach } from 'vitest'
import chamadosService from '@/api/chamadosService'

// 1. Mock do módulo axios completo
// Precisamos garantir que o mock retorne a estrutura que o service espera
const mockAxios = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
  defaults: { 
    headers: { 
      common: {} 
    },
    baseURL: 'http://fake-api' 
  },
  interceptors: {
    request: { use: vi.fn() },
    response: { use: vi.fn() }
  }
}

// Intercepta o import real do axios e devolve nosso mock
vi.mock('@/api/axios', () => ({
  default: mockAxios
}))

describe('Chamados Service', () => {
  
  // Limpa os mocks antes de cada teste para um não sujar o outro
  beforeEach(() => {
    vi.clearAllMocks()
  })
  
  it('deve buscar chamados corretamente (GET)', async () => {
    // Configura o retorno simulado
    mockAxios.get.mockResolvedValue({ data: [] })
    
    await chamadosService.getAll()
    
    // Verifica se chamou a URL correta
    expect(mockAxios.get).toHaveBeenCalledWith('/chamados/', { params: {} })
  })

  it('deve enviar status e comentário ao alterar status', async () => {
    mockAxios.post.mockResolvedValue({ data: { success: true } })
    
    const id = 10
    const status = 'concluido'
    const msg = 'Finalizado via teste'
    
    await chamadosService.alterarStatus(id, status, msg)
    
    expect(mockAxios.post).toHaveBeenCalledWith(`/chamados/${id}/alterar_status/`, {
      status: status,
      comentario: msg
    })
  })

  it('deve criar FormData corretamente para upload', async () => {
    mockAxios.post.mockResolvedValue({ data: 'ok' })
    
    const id = 5
    // Cria um arquivo falso em memória
    const arquivoFake = new File(['conteudo'], 'teste.txt', { type: 'text/plain' })
    
    await chamadosService.uploadAnexo(id, arquivoFake)
    
    // Verifica a URL
    expect(mockAxios.post.mock.calls[0][0]).toBe('/anexos/')
    
    // Verifica o segundo argumento (o FormData)
    const formDataEnviado = mockAxios.post.mock.calls[0][1]
    
    // No ambiente de teste JSDOM, FormData funciona igual no navegador
    expect(formDataEnviado).toBeInstanceOf(FormData)
    expect(formDataEnviado.get('chamado')).toBe(String(id)) // FormData converte tudo pra string
    expect(formDataEnviado.get('arquivo')).not.toBeNull()
  })
})