import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import '../widgets/app_drawer.dart';
import '../models/ativo.dart';
import '../services/api_services.dart';

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

  // Função unificada para abrir o Dialog (Criação ou Edição)
  void _showAtivoDialog({Ativo? ativo}) {
    showDialog(
      context: context,
      builder: (context) => CreateAtivoDialog(
        onSuccess: load,
        ativoParaEditar: ativo, // Se for null é criação, se tiver objeto é edição
      ),
    );
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'ativo': return Colors.green.shade100;
      case 'manutencao': return Colors.orange.shade100;
      case 'inativo': return Colors.grey.shade200;
      case 'descartado': return Colors.red.shade100;
      default: return Colors.blue.shade50;
    }
  }

  Color _getStatusTextColor(String status) {
    switch (status.toLowerCase()) {
      case 'ativo': return Colors.green.shade800;
      case 'manutencao': return Colors.orange.shade900;
      case 'inativo': return Colors.grey.shade700;
      case 'descartado': return Colors.red.shade900;
      default: return Colors.blue.shade900;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFF5F7FA),
      drawer: AppDrawer(),
      appBar: AppBar(
        title: Text('Gestão de Ativos', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: IconThemeData(color: Colors.black87),
      ),
      
      // BOTÃO FLUTUANTE ESTILIZADO (Branco com ícone Azul)
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showAtivoDialog(), // Abre dialog vazio para criar
        backgroundColor: Colors.white,
        foregroundColor: Colors.blue[700],
        elevation: 4,
        icon: Icon(Icons.add),
        label: Text('Novo Ativo', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      
      body: Column(
        children: [
          // Barra de Busca
          Container(
            padding: EdgeInsets.fromLTRB(16, 16, 16, 8),
            color: Colors.white,
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Buscar por nome, código...',
                prefixIcon: Icon(Icons.search, color: Colors.grey),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(icon: Icon(Icons.clear), onPressed: () => _searchController.clear())
                    : null,
                filled: true,
                fillColor: Colors.grey[100],
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
                contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              ),
            ),
          ),

          // Lista de Ativos
          Expanded(
            child: loading
                ? Center(child: CircularProgressIndicator())
                : filteredList.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.inventory_2_outlined, size: 64, color: Colors.grey[300]),
                            SizedBox(height: 16),
                            Text('Nenhum ativo encontrado', style: TextStyle(color: Colors.grey)),
                          ],
                        ),
                      )
                    : ListView.builder(
                        padding: EdgeInsets.all(16),
                        itemCount: filteredList.length,
                        itemBuilder: (ctx, i) {
                          final a = filteredList[i];
                          return Card(
                            margin: EdgeInsets.only(bottom: 12),
                            elevation: 0,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                              side: BorderSide(color: Colors.grey.shade200),
                            ),
                            child: InkWell(
                              borderRadius: BorderRadius.circular(12),
                              onTap: () => _showAtivoDialog(ativo: a), // CLIQUE AQUI PARA EDITAR
                              child: Padding(
                                padding: EdgeInsets.all(16),
                                child: Row(
                                  children: [
                                    // Ícone do Ativo
                                    Container(
                                      width: 48,
                                      height: 48,
                                      decoration: BoxDecoration(
                                        color: Colors.blue[50],
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      child: Icon(Icons.computer, color: Colors.blue[700]),
                                    ),
                                    SizedBox(width: 16),
                                    // Informações Principais
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            a.nome,
                                            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black87),
                                          ),
                                          SizedBox(height: 4),
                                          Row(
                                            children: [
                                              Icon(Icons.location_on_outlined, size: 14, color: Colors.grey),
                                              SizedBox(width: 4),
                                              Text(a.local, style: TextStyle(fontSize: 13, color: Colors.grey[600])),
                                            ],
                                          ),
                                          if (a.codigoPatrimonio != null) ...[
                                            SizedBox(height: 4),
                                            Text(
                                              'Patrimônio: ${a.codigoPatrimonio}',
                                              style: TextStyle(fontSize: 11, color: Colors.grey[500], fontFamily: 'Monospace'),
                                            ),
                                          ]
                                        ],
                                      ),
                                    ),
                                    // Badge de Status
                                    Container(
                                      padding: EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                                      decoration: BoxDecoration(
                                        color: _getStatusColor(a.status),
                                        borderRadius: BorderRadius.circular(20),
                                      ),
                                      child: Text(
                                        a.statusDisplay,
                                        style: TextStyle(
                                          fontSize: 11,
                                          fontWeight: FontWeight.bold,
                                          color: _getStatusTextColor(a.status),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
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
// DIALOG INTELIGENTE (CRIA E EDITA)
// ============================================

class CreateAtivoDialog extends StatefulWidget {
  final VoidCallback onSuccess;
  final Ativo? ativoParaEditar; // Se vier preenchido, é modo edição

  const CreateAtivoDialog({required this.onSuccess, this.ativoParaEditar});

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
  
  List<dynamic> _categorias = [];
  List<dynamic> _ambientes = [];
  bool _loadingData = true;
  bool _submitting = false;
  String? _error;

  bool get isEditing => widget.ativoParaEditar != null;

  @override
  void initState() {
    super.initState();
    _loadData();
    
    // Se for edição, preenche os campos com os dados do ativo clicado
    if (isEditing) {
      final a = widget.ativoParaEditar!;
      _nomeController.text = a.nome;
      _descricaoController.text = a.descricao ?? '';
      _codigoPatrimonioController.text = a.codigoPatrimonio ?? '';
      // Se seu modelo Ativo tiver qrCode, adicione aqui: _qrCodeController.text = a.qrCode ?? '';
      _status = a.status;
      _categoriaId = a.categoria?.id;
      // _ambienteId = a.ambiente?.id; (Se tiver no modelo)
    }
  }

  // SIMULADOR DE SCANNER
  void _scanQRCode() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => Dialog(
        backgroundColor: Colors.black87,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        child: Container(
          height: 300,
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.qr_code_scanner, color: Colors.blueAccent, size: 80),
              SizedBox(height: 24),
              LinearProgressIndicator(color: Colors.blueAccent, backgroundColor: Colors.grey[800]),
              SizedBox(height: 24),
              Text('Lendo Código...', style: TextStyle(color: Colors.white, fontSize: 18)),
            ],
          ),
        ),
      ),
    );

    // Simula delay de leitura
    Timer(Duration(seconds: 2), () {
      Navigator.pop(context); // Fecha scanner
      setState(() {
        // Gera um código aleatório para parecer real
        _qrCodeController.text = "QR-${DateTime.now().millisecondsSinceEpoch.toString().substring(8)}";
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('QR Code lido com sucesso!'), backgroundColor: Colors.green),
      );
    });
  }

  Future<void> _loadData() async {
    try {
      final api = Provider.of<ApiService>(context, listen: false);
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
      Map<String, dynamic> result;

      if (isEditing) {
        // MODO EDIÇÃO: Chama o updateAtivo
        result = await api.updateAtivo(
          widget.ativoParaEditar!.id,
          nome: _nomeController.text,
          descricao: _descricaoController.text,
          codigoPatrimonio: _codigoPatrimonioController.text.isNotEmpty ? _codigoPatrimonioController.text : null,
          qrCode: _qrCodeController.text.isNotEmpty ? _qrCodeController.text : null,
          status: _status,
          categoriaId: _categoriaId,
          ambienteId: _ambienteId,
        );
      } else {
        // MODO CRIAÇÃO: Chama o createAtivo
        result = await api.createAtivo(
          nome: _nomeController.text,
          descricao: _descricaoController.text,
          codigoPatrimonio: _codigoPatrimonioController.text.isNotEmpty ? _codigoPatrimonioController.text : null,
          qrCode: _qrCodeController.text.isNotEmpty ? _qrCodeController.text : null,
          status: _status,
          categoriaId: _categoriaId,
          ambienteId: _ambienteId,
        );
      }

      if (!result['success']) {
        throw Exception(result['error']);
      }

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(isEditing ? 'Ativo atualizado!' : 'Ativo criado com sucesso!'),
          backgroundColor: Colors.green,
        ),
      );

      Navigator.of(context).pop();
      widget.onSuccess();
      
    } catch (e) {
      setState(() {
        _error = 'Erro ao salvar: $e';
        _submitting = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
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
              // Cabeçalho do Dialog
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    isEditing ? 'Editar Ativo' : 'Novo Ativo', // Título dinâmico
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  IconButton(
                    icon: Icon(Icons.close),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ],
              ),
              SizedBox(height: 24),

              if (_error != null) ...[
                Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(color: Colors.red[50], borderRadius: BorderRadius.circular(8)),
                  child: Text(_error!, style: TextStyle(color: Colors.red[900])),
                ),
                SizedBox(height: 16),
              ],

              Expanded(
                child: _loadingData
                    ? Center(child: CircularProgressIndicator())
                    : SingleChildScrollView(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            TextFormField(
                              controller: _nomeController,
                              decoration: InputDecoration(
                                labelText: 'Nome do Equipamento *',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.computer),
                              ),
                              validator: (v) => v!.isEmpty ? 'Obrigatório' : null,
                            ),
                            SizedBox(height: 16),

                            TextFormField(
                              controller: _descricaoController,
                              decoration: InputDecoration(
                                labelText: 'Descrição Detalhada',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.description),
                              ),
                              maxLines: 2,
                            ),
                            SizedBox(height: 16),

                            // CAMPO QR CODE COM BOTÃO DE SCANNER INTEGRADO
                            Row(
                              children: [
                                Expanded(
                                  child: TextFormField(
                                    controller: _qrCodeController,
                                    decoration: InputDecoration(
                                      labelText: 'QR Code / Etiqueta',
                                      border: OutlineInputBorder(),
                                      prefixIcon: Icon(Icons.qr_code),
                                    ),
                                  ),
                                ),
                                SizedBox(width: 8),
                                Container(
                                  height: 56,
                                  width: 56,
                                  decoration: BoxDecoration(
                                    color: Colors.blue[50],
                                    borderRadius: BorderRadius.circular(4),
                                    border: Border.all(color: Colors.grey.shade300),
                                  ),
                                  child: IconButton(
                                    icon: Icon(Icons.qr_code_scanner, color: Colors.blue[700]),
                                    onPressed: _scanQRCode, // Chama o simulador
                                    tooltip: 'Ler Código',
                                  ),
                                ),
                              ],
                            ),
                            SizedBox(height: 16),

                            TextFormField(
                              controller: _codigoPatrimonioController,
                              decoration: InputDecoration(
                                labelText: 'Código Patrimonial',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.tag),
                              ),
                            ),
                            SizedBox(height: 16),

                            DropdownButtonFormField<String>(
                              value: _status,
                              decoration: InputDecoration(
                                labelText: 'Status Atual',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.info),
                              ),
                              items: [
                                DropdownMenuItem(value: 'ativo', child: Text('✅ Ativo')),
                                DropdownMenuItem(value: 'manutencao', child: Text('⚠️ Em Manutenção')),
                                DropdownMenuItem(value: 'inativo', child: Text('💤 Inativo')),
                                DropdownMenuItem(value: 'descartado', child: Text('🗑️ Descartado')),
                              ],
                              onChanged: (v) => setState(() => _status = v!),
                            ),
                            SizedBox(height: 16),

                            DropdownButtonFormField<int>(
                              value: _categoriaId,
                              decoration: InputDecoration(
                                labelText: 'Categoria',
                                border: OutlineInputBorder(),
                                prefixIcon: Icon(Icons.category),
                              ),
                              hint: Text('Selecione'),
                              items: _categorias.map<DropdownMenuItem<int>>((cat) {
                                return DropdownMenuItem(value: cat.id, child: Text(cat.nome));
                              }).toList(),
                              onChanged: (v) => setState(() => _categoriaId = v),
                            ),
                          ],
                        ),
                      ),
              ),

              SizedBox(height: 24),

              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: _submitting ? null : () => Navigator.of(context).pop(),
                    child: Text('Cancelar', style: TextStyle(color: Colors.grey[700])),
                  ),
                  SizedBox(width: 12),
                  ElevatedButton(
                    onPressed: _submitting ? null : _submit,
                    style: ElevatedButton.styleFrom(
                      padding: EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                      backgroundColor: Colors.blue[700],
                      foregroundColor: Colors.white,
                    ),
                    child: _submitting
                        ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                        : Text(isEditing ? 'Salvar Alterações' : 'Cadastrar Ativo'), // Texto dinâmico
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