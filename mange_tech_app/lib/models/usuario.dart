class Usuario {
  final int id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final String nomeCompleto;
  final String? telefone;
  final String? endereco;
  final String? nif;
  final bool ativo;

  Usuario({
    required this.id,
    required this.username,
    required this.email,
    this.firstName = '',
    this.lastName = '',
    String? nomeCompleto,
    this.telefone,
    this.endereco,
    this.nif,
    this.ativo = true,
  }) : nomeCompleto = nomeCompleto ?? '$firstName $lastName'.trim();

  factory Usuario.fromJson(Map<String, dynamic> json) {
    // Se vier do endpoint de perfil
    if (json.containsKey('user')) {
      final user = json['user'];
      return Usuario(
        id: user['id'],
        username: user['username'],
        email: user['email'] ?? '',
        firstName: user['first_name'] ?? '',
        lastName: user['last_name'] ?? '',
        nomeCompleto: user['nome_completo'],
        telefone: json['telefone'],
        endereco: json['endereco'],
        nif: json['nif'],
        ativo: true,
      );
    }
    
    // Se vier direto do user
    return Usuario(
      id: json['id'],
      username: json['username'],
      email: json['email'] ?? '',
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      nomeCompleto: json['nome_completo'],
      telefone: json['telefone'],
      endereco: json['endereco'],
      nif: json['nif'],
      ativo: true,
    );
  }

  // Para compatibilidade com código antigo
  String get nome => nomeCompleto.isNotEmpty ? nomeCompleto : username;
  String get nivel => 'Usuário';
  String get setor => 'TI';
}