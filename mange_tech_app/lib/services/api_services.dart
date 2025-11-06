import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/usuario.dart';
import '../models/chamado.dart';
import '../models/ativo.dart';
import '../models/categoria.dart';
import '../models/ambiente.dart';

class ApiService {
  static const String baseUrl = 'http://192.168.15.18:8000';
  
  String? _token;
  
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  // ============================================
  // AUTENTICAÇÃO
  // ============================================

  Future<void> _loadToken() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('auth_token');
  }

  Future<void> _saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('auth_token', token);
    _token = token;
  }

  Future<void> _removeToken() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
    _token = null;
  }

  Map<String, String> _getHeaders({bool needsAuth = true}) {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    
    if (needsAuth && _token != null) {
      headers['Authorization'] = 'Bearer $_token';
    }
    
    return headers;
  }

  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/token/'),
        headers: _getHeaders(needsAuth: false),
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        await _saveToken(data['access']);
        return {'success': true, 'token': data['access']};
      } else {
        return {'success': false, 'error': 'Credenciais inválidas'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Erro de conexão: $e'};
    }
  }

  Future<Map<String, dynamic>> register({
    required String username,
    required String email,
    required String password,
    String firstName = '',
    String lastName = '',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/register/'),
        headers: _getHeaders(needsAuth: false),
        body: jsonEncode({
          'username': username,
          'email': email,
          'password': password,
          'first_name': firstName,
          'last_name': lastName,
        }),
      );

      if (response.statusCode == 201) {
        return {'success': true, 'message': 'Usuário cadastrado com sucesso!'};
      } else {
        final errors = jsonDecode(response.body);
        return {'success': false, 'error': errors.toString()};
      }
    } catch (e) {
      return {'success': false, 'error': 'Erro de conexão: $e'};
    }
  }

  Future<void> logout() async {
    await _removeToken();
  }

  Future<bool> isAuthenticated() async {
    await _loadToken();
    return _token != null;
  }

  Future<Map<String, dynamic>?> getCurrentUser() async {
    await _loadToken();
    
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/me/'),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      return null;
    } catch (e) {
      print('Erro ao obter usuário: $e');
      return null;
    }
  }

  // ============================================
  // DASHBOARD
  // ============================================

  Future<Map<String, dynamic>> getDashboardData() async {
    await _loadToken();
    
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/chamados/estatisticas/'),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final stats = jsonDecode(response.body);
        
        final ativosResponse = await http.get(
          Uri.parse('$baseUrl/ativos/'),
          headers: _getHeaders(),
        );

        int ativosAtivos = 0;
        if (ativosResponse.statusCode == 200) {
          final ativosData = jsonDecode(ativosResponse.body);
          final results = ativosData['results'] ?? ativosData;
          if (results is List) {
            ativosAtivos = results.where((a) => a['status'] == 'ativo').length;
          }
        }

        int abertos = 0;
        int fechados = 0;
        for (var item in stats['por_status']) {
          if (item['status'] == 'aberto' || item['status'] == 'aguardando_responsaveis' || item['status'] == 'em_andamento') {
            abertos += (item['total'] as int);
          } else {
            fechados += (item['total'] as int);
          }
        }

        return {
          'chamadosAbertos': abertos,
          'tempoMedio': '2.4h',
          'ativosAtivos': ativosAtivos,
          'satisfacao': 94,
          'grafico': {
            'abertos': abertos.toDouble(),
            'fechados': fechados.toDouble(),
          },
        };
      }
      
      throw Exception('Erro ao buscar dados do dashboard');
    } catch (e) {
      print('Erro no dashboard: $e');
      rethrow;
    }
  }

  // ============================================
  // CHAMADOS
  // ============================================

  Future<List<Chamado>> getChamados({
    String? status,
    String? urgencia,
    String? search,
  }) async {
    await _loadToken();
    
    try {
      var url = '$baseUrl/chamados/';
      final params = <String, String>{};
      
      if (status != null) params['status'] = status;
      if (urgencia != null) params['urgencia'] = urgencia;
      if (search != null) params['search'] = search;
      
      if (params.isNotEmpty) {
        url += '?' + params.entries.map((e) => '${e.key}=${e.value}').join('&');
      }

      final response = await http.get(
        Uri.parse(url),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final results = data['results'] ?? data;
        
        if (results is List) {
          return results.map((json) => Chamado.fromJson(json)).toList();
        }
      }
      
      return [];
    } catch (e) {
      print('Erro ao buscar chamados: $e');
      return [];
    }
  }

  Future<Chamado?> getChamadoById(int id) async {
    await _loadToken();
    
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/chamados/$id/'),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        return Chamado.fromJson(jsonDecode(response.body));
      }
      return null;
    } catch (e) {
      print('Erro ao buscar chamado: $e');
      return null;
    }
  }

  Future<Map<String, dynamic>> createChamado({
    required String titulo,
    required String descricao,
    required String urgencia,
    DateTime? dataSugerida,
    List<int>? ativosIds,
  }) async {
    await _loadToken();
    
    try {
      final Map<String, dynamic> body = {
        'titulo': titulo,
        'descricao': descricao,
        'urgencia': urgencia,
      };
      
      if (dataSugerida != null) {
        body['data_sugerida'] = dataSugerida.toIso8601String();
      }
      
      if (ativosIds != null && ativosIds.isNotEmpty) {
        body['ativos_ids'] = ativosIds;
      }

      final response = await http.post(
        Uri.parse('$baseUrl/chamados/'),
        headers: _getHeaders(),
        body: jsonEncode(body),
      );

      if (response.statusCode == 201) {
        return {'success': true, 'data': jsonDecode(response.body)};
      } else {
        return {'success': false, 'error': 'Erro ao criar chamado'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Erro de conexão: $e'};
    }
  }

  Future<Map<String, dynamic>> updateChamadoStatus({
    required int chamadoId,
    required String novoStatus,
    String? comentario,
  }) async {
    await _loadToken();
    
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chamados/$chamadoId/alterar_status/'),
        headers: _getHeaders(),
        body: jsonEncode({
          'status': novoStatus,
          'comentario': comentario ?? '',
        }),
      );

      if (response.statusCode == 200) {
        return {'success': true, 'data': jsonDecode(response.body)};
      } else {
        return {'success': false, 'error': 'Erro ao atualizar status'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Erro de conexão: $e'};
    }
  }

  Future<Map<String, dynamic>> deleteChamado(int id) async {
    await _loadToken();
    
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/chamados/$id/remover/'),
        headers: _getHeaders(),
      );

      if (response.statusCode == 204) {
        return {'success': true};
      } else {
        return {'success': false, 'error': 'Erro ao remover chamado'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Erro de conexão: $e'};
    }
  }

  // ============================================
  // ATIVOS
  // ============================================

  Future<List<Ativo>> getAtivos({
    String? status,
    String? search,
    int? ambienteId,
    int? categoriaId,
  }) async {
    await _loadToken();
    
    try {
      var url = '$baseUrl/ativos/';
      final params = <String, String>{};
      
      if (status != null) params['status'] = status;
      if (search != null) params['search'] = search;
      if (ambienteId != null) params['ambiente'] = ambienteId.toString();
      if (categoriaId != null) params['categoria'] = categoriaId.toString();
      
      if (params.isNotEmpty) {
        url += '?' + params.entries.map((e) => '${e.key}=${e.value}').join('&');
      }

      final response = await http.get(
        Uri.parse(url),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final results = data['results'] ?? data;
        
        if (results is List) {
          return results.map((json) => Ativo.fromJson(json)).toList();
        }
      }
      
      return [];
    } catch (e) {
      print('Erro ao buscar ativos: $e');
      return [];
    }
  }

  Future<Map<String, dynamic>> createAtivo({
    required String nome,
    required String descricao,
    String? codigoPatrimonio,
    String? qrCode,
    int? categoriaId,
    int? ambienteId,
    String status = 'ativo',
  }) async {
    await _loadToken();
    
    try {
      final Map<String, dynamic> body = {
        'nome': nome,
        'descricao': descricao,
        'status': status,
      };
      
      if (codigoPatrimonio != null) body['codigo_patrimonio'] = codigoPatrimonio;
      if (qrCode != null) body['qr_code'] = qrCode;
      if (categoriaId != null) body['categoria'] = categoriaId;
      if (ambienteId != null) body['ambiente'] = ambienteId;

      final response = await http.post(
        Uri.parse('$baseUrl/ativos/'),
        headers: _getHeaders(),
        body: jsonEncode(body),
      );

      if (response.statusCode == 201) {
        return {'success': true, 'data': jsonDecode(response.body)};
      } else {
        return {'success': false, 'error': 'Erro ao criar ativo'};
      }
    } catch (e) {
      return {'success': false, 'error': 'Erro de conexão: $e'};
    }
  }

  // ============================================
  // CATEGORIAS
  // ============================================

  Future<List<Categoria>> getCategorias({String? search}) async {
    await _loadToken();
    
    try {
      var url = '$baseUrl/categorias/';
      if (search != null && search.isNotEmpty) {
        url += '?search=$search';
      }

      final response = await http.get(
        Uri.parse(url),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final results = data['results'] ?? data;
        
        if (results is List) {
          return results.map((json) => Categoria.fromJson(json)).toList();
        }
      }
      
      return [];
    } catch (e) {
      print('Erro ao buscar categorias: $e');
      return [];
    }
  }

  // ============================================
  // AMBIENTES
  // ============================================

  Future<List<Ambiente>> getAmbientes({String? search}) async {
    await _loadToken();
    
    try {
      var url = '$baseUrl/ambientes/';
      if (search != null && search.isNotEmpty) {
        url += '?search=$search';
      }

      final response = await http.get(
        Uri.parse(url),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final results = data['results'] ?? data;
        
        if (results is List) {
          return results.map((json) => Ambiente.fromJson(json)).toList();
        }
      }
      
      return [];
    } catch (e) {
      print('Erro ao buscar ambientes: $e');
      return [];
    }
  }

  // ============================================
  // USUÁRIOS
  // ============================================

  Future<List<Usuario>> getUsuarios({String? search}) async {
    await _loadToken();
    
    try {
      var url = '$baseUrl/usuarios/';
      if (search != null && search.isNotEmpty) {
        url += '?search=$search';
      }

      final response = await http.get(
        Uri.parse(url),
        headers: _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final results = data['results'] ?? data;
        
        if (results is List) {
          return results.map((json) => Usuario.fromJson(json)).toList();
        }
      }
      
      return [];
    } catch (e) {
      print('Erro ao buscar usuários: $e');
      return [];
    }
  }
}