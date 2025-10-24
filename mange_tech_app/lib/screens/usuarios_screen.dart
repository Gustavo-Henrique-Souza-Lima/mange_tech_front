import 'package:flutter/material.dart';
import '../widgets/app_drawer.dart';
import '../models/usuario.dart';
import '../services/api_services.dart'; // ✅ Import da API

class UsuariosScreen extends StatefulWidget {
  @override
  _UsuariosScreenState createState() => _UsuariosScreenState();
}

class _UsuariosScreenState extends State<UsuariosScreen> {
  final ApiService _api = ApiService(); // ✅ Instância da API
  List<Usuario> usuarios = [];
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    setState(() {
      loading = true;
      error = null;
    });

    try {
      final d = await _api.getUsuarios();
      setState(() {
        usuarios = d;
        loading = false;
      });
    } catch (e) {
      setState(() {
        error = 'Erro ao carregar usuários: $e';
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: AppDrawer(),
      appBar: AppBar(title: Text('Usuários')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: loading
            ? Center(child: CircularProgressIndicator())
            : error != null
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.error_outline, size: 48, color: Colors.red),
                        SizedBox(height: 16),
                        Text(error!, textAlign: TextAlign.center),
                        SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: load,
                          child: Text('Tentar Novamente'),
                        ),
                      ],
                    ),
                  )
                : Column(
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: TextField(
                              decoration: InputDecoration(
                                prefixIcon: Icon(Icons.search),
                                hintText: 'Buscar por nome ou email...',
                              ),
                            ),
                          ),
                          SizedBox(width: 12),
                          ElevatedButton(
                            onPressed: () {},
                            child: Text('+ Novo Usuário'),
                          ),
                        ],
                      ),
                      SizedBox(height: 12),
                      Expanded(
                        child: Card(
                          child: SingleChildScrollView(
                            scrollDirection: Axis.horizontal,
                            child: DataTable(
                              columns: [
                                DataColumn(label: Text('NOME')),
                                DataColumn(label: Text('EMAIL')),
                                DataColumn(label: Text('NÍVEL')),
                                DataColumn(label: Text('SETOR')),
                                DataColumn(label: Text('STATUS')),
                                DataColumn(label: Text('AÇÕES')),
                              ],
                              rows: usuarios.map((u) {
                                return DataRow(
                                  cells: [
                                    DataCell(Text(u.nome)),
                                    DataCell(Text(u.email)),
                                    DataCell(Text(u.nivel)),
                                    DataCell(Text(u.setor)),
                                    DataCell(
                                      Container(
                                        padding: EdgeInsets.symmetric(
                                            horizontal: 8, vertical: 4),
                                        decoration: BoxDecoration(
                                          color: u.ativo
                                              ? Colors.green[50]
                                              : Colors.grey[200],
                                          borderRadius:
                                              BorderRadius.circular(8),
                                        ),
                                        child: Text(u.ativo ? 'Ativo' : 'Inativo'),
                                      ),
                                    ),
                                    DataCell(
                                      Row(
                                        children: [
                                          TextButton(
                                              onPressed: () {},
                                              child: Text('Editar')),
                                          TextButton(
                                            onPressed: () {},
                                            child: Text(
                                              'Remover',
                                              style: TextStyle(
                                                  color: Colors.red),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                );
                              }).toList(),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
      ),
    );
  }
}
