import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart'; // Adicione intl
import '../widgets/app_drawer.dart';
import '../models/chamado.dart';
import '../models/ativo.dart';
import '../services/api_services.dart';
import 'chamado_detalhes_screen.dart'; // Importe a nova tela

class ChamadosScreen extends StatefulWidget {
  @override
  _ChamadosScreenState createState() => _ChamadosScreenState();
}

class _ChamadosScreenState extends State<ChamadosScreen> {
  List<Chamado> list = [];
  List<Chamado> filteredList = [];
  bool loading = true;
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    load();
  }

  void load() async {
    setState(() => loading = true);
    final srv = Provider.of<ApiService>(context, listen: false);
    final d = await srv.getChamados();
    setState(() {
      list = d;
      filteredList = d;
      loading = false;
    });
  }

  void _filter(String query) {
    setState(() {
      if (query.isEmpty) {
        filteredList = list;
      } else {
        filteredList = list.where((c) =>
            c.titulo.toLowerCase().contains(query.toLowerCase()) ||
            c.id.toString().contains(query)).toList();
      }
    });
  }

  void _openDetails(Chamado chamado) async {
    // Navega e espera voltar para atualizar a lista (caso o status mude)
    await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => ChamadoDetalhesScreen(chamado: chamado)),
    );
    load();
  }

  void _showCreateDialog() {
    showDialog(
      context: context,
      builder: (context) => CreateChamadoDialog(onCreated: load),
    );
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'aberto': return Colors.orange.shade100;
      case 'em_andamento': return Colors.blue.shade100;
      case 'aguardando_responsaveis': return Colors.purple.shade100;
      case 'concluido': return Colors.green.shade100;
      case 'cancelado': return Colors.red.shade100;
      default: return Colors.grey.shade200;
    }
  }

  Color _getStatusTextColor(String status) {
    switch (status.toLowerCase()) {
      case 'aberto': return Colors.orange.shade900;
      case 'em_andamento': return Colors.blue.shade900;
      case 'aguardando_responsaveis': return Colors.purple.shade900;
      case 'concluido': return Colors.green.shade900;
      case 'cancelado': return Colors.red.shade900;
      default: return Colors.black87;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFF5F7FA),
      drawer: AppDrawer(),
      appBar: AppBar(
        title: Text('Chamados', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: IconThemeData(color: Colors.black87),
      ),
      body: Column(
        children: [
          // Barra de Pesquisa Estilizada
          Container(
            padding: EdgeInsets.all(16),
            color: Colors.white,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    onChanged: _filter,
                    decoration: InputDecoration(
                      hintText: 'Buscar chamados...',
                      prefixIcon: Icon(Icons.search, color: Colors.grey),
                      filled: true,
                      fillColor: Colors.grey[100],
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(30),
                        borderSide: BorderSide.none,
                      ),
                      contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                    ),
                  ),
                ),
                SizedBox(width: 12),
                FloatingActionButton(
                  mini: true,
                  elevation: 0,
                  backgroundColor: Colors.blue[700],
                  child: Icon(Icons.add),
                  onPressed: _showCreateDialog,
                ),
              ],
            ),
          ),
          
          // Lista de Chamados
          Expanded(
            child: loading
                ? Center(child: CircularProgressIndicator())
                : filteredList.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.inbox_outlined, size: 64, color: Colors.grey[300]),
                            SizedBox(height: 16),
                            Text('Nenhum chamado encontrado', style: TextStyle(color: Colors.grey)),
                          ],
                        ),
                      )
                    : ListView.builder(
                        padding: EdgeInsets.all(16),
                        itemCount: filteredList.length,
                        itemBuilder: (ctx, i) {
                          final c = filteredList[i];
                          return Card(
                            margin: EdgeInsets.only(bottom: 12),
                            elevation: 0,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                              side: BorderSide(color: Colors.grey.shade200),
                            ),
                            child: InkWell(
                              borderRadius: BorderRadius.circular(12),
                              onTap: () => _openDetails(c),
                              child: Padding(
                                padding: EdgeInsets.all(16),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                      children: [
                                        Container(
                                          padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                          decoration: BoxDecoration(
                                            color: _getStatusColor(c.status),
                                            borderRadius: BorderRadius.circular(8),
                                          ),
                                          child: Text(
                                            c.statusDisplay,
                                            style: TextStyle(
                                              fontSize: 11,
                                              fontWeight: FontWeight.bold,
                                              color: _getStatusTextColor(c.status),
                                            ),
                                          ),
                                        ),
                                        Text(
                                          DateFormat('dd/MM/yyyy').format(c.dataAbertura),
                                          style: TextStyle(fontSize: 12, color: Colors.grey[500]),
                                        ),
                                      ],
                                    ),
                                    SizedBox(height: 12),
                                    Text(
                                      c.titulo,
                                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                                    ),
                                    SizedBox(height: 4),
                                    Text(
                                      'ID: #${c.id} • Prioridade: ${c.prioridade}',
                                      style: TextStyle(fontSize: 13, color: Colors.grey[600]),
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
}

// ... (Mantenha o CreateChamadoDialog igual, não precisa alterar)
// ============================================
// DIALOG PARA CRIAR CHAMADO
// ============================================

class CreateChamadoDialog extends StatefulWidget {
  final VoidCallback onCreated;

  const CreateChamadoDialog({required this.onCreated});

  @override
  _CreateChamadoDialogState createState() => _CreateChamadoDialogState();
}

class _CreateChamadoDialogState extends State<CreateChamadoDialog> {
  final _formKey = GlobalKey<FormState>();
  final _tituloController = TextEditingController();
  final _descricaoController = TextEditingController();
  
  String _urgencia = 'media';
  DateTime? _dataSugerida;
  List<Ativo> _ativosDisponiveis = [];
  List<int> _ativosSelecionados = [];
  bool _loadingAtivos = true;
  bool _submitting = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadAtivos();
  }

  Future<void> _loadAtivos() async {
    try {
      final api = Provider.of<ApiService>(context, listen: false);
      final ativos = await api.getAtivos();
      setState(() {
        _ativosDisponiveis = ativos;
        _loadingAtivos = false;
      });
    } catch (e) {
      setState(() {
        _loadingAtivos = false;
        _error = 'Erro ao carregar ativos';
      });
    }
  }

  Future<void> _selectDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(Duration(days: 365)),
    );

    if (picked != null) {
      final time = await showTimePicker(
        context: context,
        initialTime: TimeOfDay.now(),
      );

      if (time != null) {
        setState(() {
          _dataSugerida = DateTime(
            picked.year,
            picked.month,
            picked.day,
            time.hour,
            time.minute,
          );
        });
      }
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
      final result = await api.createChamado(
        titulo: _tituloController.text,
        descricao: _descricaoController.text,
        urgencia: _urgencia,
        dataSugerida: _dataSugerida,
        ativosIds: _ativosSelecionados.isNotEmpty ? _ativosSelecionados : null,
      );

      if (result['success']) {
        Navigator.of(context).pop();
        widget.onCreated();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Chamado criado com sucesso!'),
            backgroundColor: Colors.green,
          ),
        );
      } else {
        setState(() {
          _error = result['error'] ?? 'Erro ao criar chamado';
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
                    'Novo Chamado',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
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
                        child: Text(
                          _error!,
                          style: TextStyle(color: Colors.red[900]),
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 16),
              ],

              // Formulário
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Título
                      TextFormField(
                        controller: _tituloController,
                        decoration: InputDecoration(
                          labelText: 'Título *',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.title),
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'O título é obrigatório';
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
                        maxLines: 4,
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'A descrição é obrigatória';
                          }
                          return null;
                        },
                      ),
                      SizedBox(height: 16),

                      // Urgência
                      DropdownButtonFormField<String>(
                        value: _urgencia,
                        decoration: InputDecoration(
                          labelText: 'Urgência *',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.priority_high),
                        ),
                        items: [
                          DropdownMenuItem(value: 'baixa', child: Text('Baixa')),
                          DropdownMenuItem(value: 'media', child: Text('Média')),
                          DropdownMenuItem(value: 'alta', child: Text('Alta')),
                          DropdownMenuItem(value: 'critica', child: Text('Crítica')),
                        ],
                        onChanged: (value) {
                          setState(() {
                            _urgencia = value!;
                          });
                        },
                      ),
                      SizedBox(height: 16),

                      // Data Sugerida
                      InkWell(
                        onTap: _selectDate,
                        child: InputDecorator(
                          decoration: InputDecoration(
                            labelText: 'Data Sugerida (opcional)',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.calendar_today),
                          ),
                          child: Text(
                            _dataSugerida != null
                                ? '${_dataSugerida!.day.toString().padLeft(2, '0')}/${_dataSugerida!.month.toString().padLeft(2, '0')}/${_dataSugerida!.year} ${_dataSugerida!.hour.toString().padLeft(2, '0')}:${_dataSugerida!.minute.toString().padLeft(2, '0')}'
                                : 'Selecione a data e hora',
                            style: TextStyle(
                              color: _dataSugerida != null
                                  ? Colors.black
                                  : Colors.grey[600],
                            ),
                          ),
                        ),
                      ),
                      SizedBox(height: 16),

                      // Ativos
                      Text(
                        'Ativos Relacionados (opcional)',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      SizedBox(height: 8),
                      
                      if (_loadingAtivos)
                        Center(child: CircularProgressIndicator())
                      else if (_ativosDisponiveis.isEmpty)
                        Text(
                          'Nenhum ativo disponível',
                          style: TextStyle(color: Colors.grey[600]),
                        )
                      else
                        Container(
                          height: 150,
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey[300]!),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: ListView.builder(
                            itemCount: _ativosDisponiveis.length,
                            itemBuilder: (context, index) {
                              final ativo = _ativosDisponiveis[index];
                              final isSelected = _ativosSelecionados.contains(ativo.id);
                              
                              return CheckboxListTile(
                                title: Text(ativo.nome),
                                subtitle: Text(ativo.local),
                                value: isSelected,
                                onChanged: (selected) {
                                  setState(() {
                                    if (selected == true) {
                                      _ativosSelecionados.add(ativo.id);
                                    } else {
                                      _ativosSelecionados.remove(ativo.id);
                                    }
                                  });
                                },
                              );
                            },
                          ),
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
                        : Text('Criar Chamado'),
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
    _tituloController.dispose();
    _descricaoController.dispose();
    super.dispose();
  }
}