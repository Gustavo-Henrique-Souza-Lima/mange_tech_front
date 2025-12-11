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
    // PROTEÇÃO: Garante datas válidas mesmo se vier nulo ou formato errado
    DateTime parseDate(dynamic dateString) {
      if (dateString == null) return DateTime.now();
      try {
        return DateTime.parse(dateString);
      } catch (_) {
        return DateTime.now();
      }
    }

    return Ativo(
      id: json['id'] ?? 0, // Se vier nulo, usa 0
      nome: json['nome'] ?? 'Sem Nome', // AQUI QUE ESTAVA O ERRO (Null is not subtype of String)
      descricao: json['descricao'],
      codigoPatrimonio: json['codigo_patrimonio'],
      qrCode: json['qr_code'],
      status: json['status'] ?? 'indefinido',
      statusDisplay: json['status_display'] ?? json['status'] ?? 'Indefinido',
      
      // Proteção para Categoria (verifica se é Map)
      categoria: (json['categoria'] != null && json['categoria'] is Map<String, dynamic>) 
          ? Categoria.fromJson(json['categoria']) 
          : null,
      
      // Proteção para Ambiente (verifica se é Map)
      ambiente: (json['ambiente'] != null && json['ambiente'] is Map<String, dynamic>) 
          ? Ambiente.fromJson(json['ambiente']) 
          : null,
      
      createdAt: parseDate(json['created_at']),
      updatedAt: parseDate(json['updated_at']),
    );
  }

  // Mantive sua lógica de compatibilidade
  String get local => ambiente?.nome ?? 'Sem local';
}