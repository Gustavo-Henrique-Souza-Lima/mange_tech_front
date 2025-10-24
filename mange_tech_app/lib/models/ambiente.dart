import 'usuario.dart';

class Ambiente {
  final int id;
  final String nome;
  final String? descricao;
  final String? localizacaoAmbiente;
  final Usuario? responsavel;
  final int totalAtivos;

  Ambiente({
    required this.id,
    required this.nome,
    this.descricao,
    this.localizacaoAmbiente,
    this.responsavel,
    required this.totalAtivos,
  });

  factory Ambiente.fromJson(Map<String, dynamic> json) {
    return Ambiente(
      id: json['id'],
      nome: json['nome'],
      descricao: json['descricao'],
      localizacaoAmbiente: json['localizacao_ambiente'],
      responsavel: json['responsavel'] != null 
          ? Usuario.fromJson(json['responsavel']) 
          : null,
      totalAtivos: json['total_ativos'] ?? 0,
    );
  }
}