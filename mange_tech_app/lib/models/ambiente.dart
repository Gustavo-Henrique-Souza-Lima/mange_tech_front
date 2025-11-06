class Ambiente {
  final int id;
  final String nome;
  final String? descricao;
  final String? localizacaoAmbiente;
  final int? responsavelId;
  final String? responsavelNome;
  final int totalAtivos;
  final DateTime createdAt;
  final DateTime updatedAt;

  Ambiente({
    required this.id,
    required this.nome,
    this.descricao,
    this.localizacaoAmbiente,
    this.responsavelId,
    this.responsavelNome,
    this.totalAtivos = 0,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Ambiente.fromJson(Map<String, dynamic> json) {
    return Ambiente(
      id: json['id'],
      nome: json['nome'],
      descricao: json['descricao'],
      localizacaoAmbiente: json['localizacao_ambiente'],
      responsavelId: json['responsavel'] != null 
          ? (json['responsavel'] is Map ? json['responsavel']['id'] : json['responsavel'])
          : null,
      responsavelNome: json['responsavel'] != null && json['responsavel'] is Map
          ? json['responsavel']['nome_completo'] ?? json['responsavel']['username']
          : null,
      totalAtivos: json['total_ativos'] ?? 0,
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nome': nome,
      'descricao': descricao,
      'localizacao_ambiente': localizacaoAmbiente,
      'responsavel': responsavelId,
      'total_ativos': totalAtivos,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }
}