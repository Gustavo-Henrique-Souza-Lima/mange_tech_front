import 'usuario.dart';
import 'ativo.dart';

class Chamado {
  final int id;
  final String titulo;
  final String? descricao;
  final String status;
  final String statusDisplay;
  final String urgencia;
  final String urgenciaDisplay;
  final DateTime? dataSugerida;
  final DateTime dataAbertura;
  final DateTime? dataConclusao;
  final Usuario solicitante;
  final List<Ativo>? ativos;
  final List<ChamadoResponsavel>? responsaveis;
  final bool estaEmAtraso;

  Chamado({
    required this.id,
    required this.titulo,
    this.descricao,
    required this.status,
    required this.statusDisplay,
    required this.urgencia,
    required this.urgenciaDisplay,
    this.dataSugerida,
    required this.dataAbertura,
    this.dataConclusao,
    required this.solicitante,
    this.ativos,
    this.responsaveis,
    this.estaEmAtraso = false,
  });

  factory Chamado.fromJson(Map<String, dynamic> json) {
    return Chamado(
      id: json['id'],
      titulo: json['titulo'],
      descricao: json['descricao'],
      status: json['status'],
      statusDisplay: json['status_display'] ?? json['status'],
      urgencia: json['urgencia'] ?? 'media',
      urgenciaDisplay: json['urgencia_display'] ?? 'Média',
      dataSugerida: json['data_sugerida'] != null 
          ? DateTime.parse(json['data_sugerida']) 
          : null,
      dataAbertura: DateTime.parse(json['data_abertura']),
      dataConclusao: json['data_conclusao'] != null 
          ? DateTime.parse(json['data_conclusao']) 
          : null,
      solicitante: Usuario.fromJson(json['solicitante']),
      ativos: json['ativos'] != null
          ? (json['ativos'] as List).map((a) => Ativo.fromJson(a)).toList()
          : null,
      responsaveis: json['responsaveis'] != null
          ? (json['responsaveis'] as List).map((r) => ChamadoResponsavel.fromJson(r)).toList()
          : null,
      estaEmAtraso: json['esta_em_atraso'] ?? false,
    );
  }

  // Para compatibilidade com código antigo
  String get prioridade => urgenciaDisplay;
}

class ChamadoResponsavel {
  final int id;
  final Usuario responsavel;
  final String role;
  final String roleDisplay;
  final DateTime dataAtribuicao;

  ChamadoResponsavel({
    required this.id,
    required this.responsavel,
    required this.role,
    required this.roleDisplay,
    required this.dataAtribuicao,
  });

  factory ChamadoResponsavel.fromJson(Map<String, dynamic> json) {
    return ChamadoResponsavel(
      id: json['id'],
      responsavel: Usuario.fromJson(json['responsavel']),
      role: json['role'],
      roleDisplay: json['role_display'],
      dataAtribuicao: DateTime.parse(json['data_atribuicao']),
    );
  }
}