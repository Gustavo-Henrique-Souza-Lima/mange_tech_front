import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../widgets/app_drawer.dart';
import '../models/ativo.dart';
import '../models/categoria.dart';
import '../models/ambiente.dart';
import '../services/api_services.dart';
import 'package:csv/csv.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

class AtivosScreen extends StatefulWidget {
  @override
  _AtivosScreenState createState() => _AtivosScreenState();
}

class _AtivosScreenState extends State<AtivosScreen> {
  List<Ativo> list = [];
  List<Ativo> filteredList = [];
  bool loading = true;
  final _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    load();
    _searchController.addListener(_filterAtivos);
  }

  void load() async {
    setState(() => loading = true);
    final srv = Provider.of<ApiService>(context, listen: false);
    final d = await srv.getAtivos();
    setState(() {
      list = d;
      filteredList = d;
      loading = false;
    });
  }

  void _filterAtivos() {
    final query = _searchController.text.toLowerCase();
    setState(() {
      if (query.isEmpty) {
        filteredList = list;
      } else {
        filteredList = list.where((ativo) {
          return ativo.nome.toLowerCase().contains(query) ||
              ativo.codigoPatrimonio?.toLowerCase().contains(query) == true ||
              ativo.id.toString().contains(query);
        }).toList();
      }
    });
  }

  void _showCreateDialog() {
    showDialog(
      context: context,
      builder: (context) => CreateAtivoDialog(onCreated: load),
    );
  }

  Future<void> _exportToCSV() async {
    try {
      // Preparar dados para CSV
      List<List<dynamic>> rows = [];
      
      // Cabeçalho
      rows.add([
        'ID',
        'Nome',
        'Código Patrimônio',
        'QR Code',
        'Status',
        'Categoria',
        'Ambiente',
        'Descrição',
        'Data Criação',
      ]);

      // Dados
      for (var ativo in list) {
        rows.add([
          ativo.id,
          ativo.nome,
          ativo.codigoPatrimonio ?? '',
          ativo.qrCode ?? '',
          ativo.statusDisplay,
          ativo.categoria?.nome ?? '',
          ativo.ambiente?.nome ?? '',
          ativo.descricao ?? '',
          ativo.createdAt.toIso8601String(),
        ]);
      }

      // Converter para CSV
      String csv = const ListToCsvConverter().convert(rows);

      // Salvar arquivo
      final directory = await getApplicationDocumentsDirectory();
      final path = '${directory.path}/ativos_${DateTime.now().millisecondsSinceEpoch}.csv';
      final file = File(path);
      await file.writeAsString(csv);

      // Compartilhar arquivo
      await Share.shareXFiles([XFile(path)], text: 'Exportação de Ativos');

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Ativos exportados com sucesso!'),
          backgroundColor: Colors.green,
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Erro ao exportar: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: AppDrawer(),
      appBar: AppBar(title: Text('Ativos')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: loading
            ? Center(child: CircularProgressIndicator())
            : Column(
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _searchController,
                          decoration: InputDecoration(
                            prefixIcon: Icon(Icons.search),
                            hintText: 'Buscar por ID ou nome...',
                            suffixIcon: _searchController.text.isNotEmpty
                                ? IconButton(
                                    icon: Icon(Icons.clear),
                                    onPressed: () {
                                      _searchController.clear();
                                    },
                                  )
                                : null,
                          ),
                        ),
                      ),
                      SizedBox(width: 12),
                      ElevatedButton.icon(
                        onPressed: _exportToCSV,
                        icon: Icon(Icons.download),
                        label: Text('Exportar'),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        ),
                      ),
                      SizedBox(width: 8),
                      ElevatedButton.icon(
                        onPressed: _showCreateDialog,
                        icon: Icon(Icons.add),
                        label: Text('Novo Ativo'),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 12),
                  if (filteredList.isEmpty)
                    Expanded(
                      child: Center(
                        child: Text(
                          'Nenhum ativo encontrado',
                          style: TextStyle(fontSize: 16, color: Colors.grey),
                        ),
                      ),
                    )
                  else
                    Expanded(
                      child: ListView.separated(
                        itemCount: filteredList.length,
                        separatorBuilder: (_, __) => Divider(),
                        itemBuilder: (ctx, i) {
                          final a = filteredList[i];
                          return ListTile(
                            leading: CircleAvatar(
                              backgroundColor: a.status == 'ativo'
                                  ? Colors.green
                                  : a.status == 'manutencao'
                                      ? Colors.orange
                                      : Colors.grey,
                              child: Icon(Icons.devices, color: Colors.white),
                            ),
                            title: Text(a.nome),
                            subtitle: Text(
                              '${a.local}${a.codigoPatrimonio != null ? " • ${a.codigoPatrimonio}" : ""}',
                            ),
                            trailing: Container(
                              padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                              decoration: BoxDecoration(
                                color: a.status == 'ativo'
                                    ? Colors.green[50]
                                    : a.status == 'manutencao'
                                        ? Colors.orange[50]
                                        : Colors.grey[200],
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(
                                a.statusDisplay,
                                style: TextStyle(
                                  color: a.status == 'ativo'
                                      ? Colors.green[700]
                                      : a.status == 'manutencao'
                                          ? Colors.orange[700]
                                          : Colors.grey[700],
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            onTap: () {
                              // TODO: Navegar para detalhes do ativo
                            },
                          );
                        },
                      ),
                    ),
                ],
              ),
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}

// ============================================
// DIALOG PARA CRIAR ATIVO
// ============================================

class CreateAtivoDialog extends StatefulWidget {
  final VoidCallback onCreated;

  const CreateAtivoDialog({required this.onCreated});

  @override
  _CreateAtivoDialogState createState() => _CreateAtivoDialogState();
}

class _CreateAtivoDialogState extends State<CreateAtivoDialog> {
  final _formKey = GlobalKey<FormState>();
  final _nomeController = TextEditingController();
  final _descricaoController = TextEditingController();
  final _codigoPatrimonioController = TextEditingController();
  final _qrCodeController = TextEditingController();

  String _status = 'ativo';
  int? _categoriaId;
  int? _ambienteId;
  
  List<Categoria> _categorias = [];
  List<Ambiente> _ambientes = [];
  bool _loadingData = true;
  bool _submitting = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final api = Provider.of<ApiService>(context, listen: false);
      
      // Carregar categorias e ambientes
      final categoriasResponse = await api.getCategorias();
      final ambientesResponse = await api.getAmbientes();
      
      setState(() {
        _categorias = categoriasResponse;
        _ambientes = ambientesResponse;
        _loadingData = false;
      });
    } catch (e) {
      setState(() {
        _loadingData = false;
        _error = 'Erro ao carregar dados: $e';
      });
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _submitting = true;
      _error = null;
    });

    try {
      final api = Provider.of<ApiService>(context, listen: false);
      final result = await api.createAtivo(
        nome: _nomeController.text,
        descricao: _descricaoController.text,
        codigoPatrimonio: _codigoPatrimonioController.text.isNotEmpty 
            ? _codigoPatrimonioController.text 
            : null,
        qrCode: _qrCodeController.text.isNotEmpty 
            ? _qrCodeController.text 
            : null,
        status: _status,
        categoriaId: _categoriaId,
        ambienteId: _ambienteId,
      );

      if (result['success']) {
        Navigator.of(context).pop();
        widget.onCreated();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Ativo criado com sucesso!'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        setState(() {
          _error = result['error'] ?? 'Erro ao criar ativo';
          _submitting = false;
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Erro de conexão: $e';
        _submitting = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        width: 600,
        constraints: BoxConstraints(maxHeight: 700),
        padding: EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Cabeçalho
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Novo Ativo',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  IconButton(
                    icon: Icon(Icons.close),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ],
              ),
              SizedBox(height: 24),

              // Erro
              if (_error != null) ...[
                Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red[50],
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.red[300]!),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.error_outline, color: Colors.red),
                      SizedBox(width: 8),
                      Expanded(
                        child: Text(_error!, style: TextStyle(color: Colors.red[900])),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 16),
              ],

              // Formulário
              Expanded(
                child: _loadingData
                    ? Center(child: CircularProgressIndicator())
                    : SingleChildScrollView(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // Nome
                            TextFormField(
                              controller: _nomeController,
                              decoration: InputDecoration(
                                labelText: 'Nome *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.devices),
                              ),
                              validator: (value) {
                                if (value == null || value.isEmpty) {
                                  return 'O nome é obrigatório';
                                }
                                return null;
                              },
                            ),
                            SizedBox(height: 16),

                            // Descrição
                            TextFormField(
                              controller: _descricaoController,
                              decoration: InputDecoration(
                                labelText: 'Descrição *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.description),
                                alignLabelWithHint: true,
                              ),
                              maxLines: 3,
                              validator: (value) {
                                if (value == null || value.isEmpty) {
                                  return 'A descrição é obrigatória';
                                }
                                return null;
                              },
                            ),
                            SizedBox(height: 16),

                            // Código Patrimônio
                            TextFormField(
                              controller: _codigoPatrimonioController,
                              decoration: InputDecoration(
                                labelText: 'Código de Patrimônio',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.qr_code_2),
                              ),
                            ),
                            SizedBox(height: 16),

                            // QR Code
                            TextFormField(
                              controller: _qrCodeController,
                              decoration: InputDecoration(
                                labelText: 'QR Code',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.qr_code_scanner),
                              ),
                            ),
                            SizedBox(height: 16),

                            // Status
                            DropdownButtonFormField<String>(
                              value: _status,
                              decoration: InputDecoration(
                                labelText: 'Status *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.info_outline),
                              ),
                              items: [
                                DropdownMenuItem(value: 'ativo', child: Text('Ativo')),
                                DropdownMenuItem(value: 'manutencao', child: Text('Manutenção')),
                                DropdownMenuItem(value: 'inativo', child: Text('Inativo')),
                                DropdownMenuItem(value: 'descartado', child: Text('Descartado')),
                              ],
                              onChanged: (value) {
                                setState(() => _status = value!);
                              },
                            ),
                            SizedBox(height: 16),

                            // Categoria
                            DropdownButtonFormField<int>(
                              value: _categoriaId,
                              decoration: InputDecoration(
                                labelText: 'Categoria',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.category),
                              ),
                              hint: Text('Selecione uma categoria'),
                              items: _categorias.map((cat) {
                                return DropdownMenuItem(
                                  value: cat.id,
                                  child: Text(cat.nome),
                                );
                              }).toList(),
                              onChanged: (value) {
                                setState(() => _categoriaId = value);
                              },
                            ),
                            SizedBox(height: 16),

                            // Ambiente
                            DropdownButtonFormField<int>(
                              value: _ambienteId,
                              decoration: InputDecoration(
                                labelText: 'Ambiente',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.location_on),
                              ),
                              hint: Text('Selecione um ambiente'),
                              items: _ambientes.map((amb) {
                                return DropdownMenuItem(
                                  value: amb.id,
                                  child: Text(amb.nome),
                                );
                              }).toList(),
                              onChanged: (value) {
                                setState(() => _ambienteId = value);
                              },
                            ),
                          ],
                        ),
                      ),
              ),

              SizedBox(height: 24),

              // Botões
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: _submitting ? null : () => Navigator.of(context).pop(),
                    child: Text('Cancelar'),
                  ),
                  SizedBox(width: 12),
                  ElevatedButton(
                    onPressed: _submitting ? null : _submit,
                    style: ElevatedButton.styleFrom(
                      padding: EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                    ),
                    child: _submitting
                        ? SizedBox(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                            ),
                          )
                        : Text('Criar Ativo'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _nomeController.dispose();
    _descricaoController.dispose();
    _codigoPatrimonioController.dispose();
    _qrCodeController.dispose();
    super.dispose();
  }
}