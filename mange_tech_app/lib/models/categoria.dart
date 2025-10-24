class Categoria {
  final int id;
  final String nome;
  final String? descricao;
  final int totalAtivos;

  Categoria({
    required this.id,
    required this.nome,
    this.descricao,
    required this.totalAtivos,
  });

  factory Categoria.fromJson(Map<String, dynamic> json) {
    return Categoria(
      id: json['id'],
      nome: json['nome'],
      descricao: json['descricao'],
      totalAtivos: json['total_ativos'] ?? 0,
    );
  }
}