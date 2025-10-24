import 'categoria.dart';
import 'ambiente.dart';

class Ativo {
  final int id;
  final String nome;
  final String? descricao;
  final String? codigoPatrimonio;
  final String? qrCode;
  final String status;
  final String statusDisplay;
  final Categoria? categoria;
  final Ambiente? ambiente;
  final DateTime createdAt;
  final DateTime updatedAt;

  Ativo({
    required this.id,
    required this.nome,
    this.descricao,
    this.codigoPatrimonio,
    this.qrCode,
    required this.status,
    required this.statusDisplay,
    this.categoria,
    this.ambiente,
    required this.createdAt,
    required this.updatedAt,
  });

  factory Ativo.fromJson(Map<String, dynamic> json) {
    return Ativo(
      id: json['id'],
      nome: json['nome'],
      descricao: json['descricao'],
      codigoPatrimonio: json['codigo_patrimonio'],
      qrCode: json['qr_code'],
      status: json['status'] ?? 'ativo',
      statusDisplay: json['status_display'] ?? 'Ativo',
      categoria: json['categoria'] != null ? Categoria.fromJson(json['categoria']) : null,
      ambiente: json['ambiente'] != null ? Ambiente.fromJson(json['ambiente']) : null,
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }

  // Para compatibilidade com o código antigo
  String get local => ambiente?.nome ?? 'Sem local';
}
