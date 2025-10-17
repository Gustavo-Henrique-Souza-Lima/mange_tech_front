import 'dart:async';
import '../models/usuario.dart';
import '../models/chamado.dart';
import '../models/ativo.dart';

class MockService {
  Future<Map<String, dynamic>> getDashboardData() async {
    await Future.delayed(Duration(milliseconds: 400));
    return {
      'chamadosAbertos': 23,
      'tempoMedio': '2.4h',
      'ativosAtivos': 156,
      'satisfacao': 94,
      'grafico': {'abertos': 40, 'fechados': 60},
    };
  }

  Future<List<Chamado>> getChamados() async {
    await Future.delayed(Duration(milliseconds: 400));
    return List.generate(6, (i) => Chamado(id: i+1, titulo: 'Erro $i', status: i%3==0 ? 'Aberto' : 'Fechado', prioridade: i%2==0 ? 'Alta' : 'Média'));
  }

  Future<List<Ativo>> getAtivos() async {
    await Future.delayed(Duration(milliseconds: 300));
    return List.generate(5, (i) => Ativo(id: i+1, nome: 'Impressora ${i+1}', status: i%2==0 ? 'Em manutenção' : 'Ativo', local: 'Setor ${i+1}'));
  }

  Future<List<Usuario>> getUsuarios() async {
    await Future.delayed(Duration(milliseconds: 300));
    return [
      Usuario(nome: 'Carlos Tech', email: 'carlos@company.com', nivel: 'Técnico', setor: 'TI', ativo: true),
      Usuario(nome: 'Ana Tech', email: 'ana@company.com', nivel: 'Técnico', setor: 'TI', ativo: true),
      Usuario(nome: 'João Admin', email: 'joao@company.com', nivel: 'Administrador', setor: 'TI', ativo: true),
      Usuario(nome: 'Roberto Alves', email: 'roberto@company.com', nivel: 'Usuário', setor: 'Financeiro', ativo: false),
    ];
  }
}
