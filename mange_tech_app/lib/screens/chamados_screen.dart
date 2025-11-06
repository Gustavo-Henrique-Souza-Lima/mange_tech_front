import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../widgets/app_drawer.dart';
import '../models/chamado.dart';
import '../models/ativo.dart';
import '../services/api_services.dart';

class ChamadosScreen extends StatefulWidget {
  @override
  _ChamadosScreenState createState() => _ChamadosScreenState();
}

class _ChamadosScreenState extends State<ChamadosScreen> {
  List<Chamado> list = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    load();
  }

  void load() async {
    final srv = Provider.of<ApiService>(context, listen: false);
    final d = await srv.getChamados();
    setState(() {
      list = d;
      loading = false;
    });
  }

  void _showCreateDialog() {
    showDialog(
      context: context,
      builder: (context) => CreateChamadoDialog(onCreated: load),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: AppDrawer(),
      appBar: AppBar(title: Text('Chamados')),
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
                          decoration: InputDecoration(
                            prefixIcon: Icon(Icons.search),
                            hintText: 'Buscar por ID ou título...',
                          ),
                        ),
                      ),
                      SizedBox(width: 12),
                      ElevatedButton.icon(
                        onPressed: _showCreateDialog,
                        icon: Icon(Icons.add),
                        label: Text('Novo Chamado'),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 12),
                  Expanded(
                    child: ListView.separated(
                      itemCount: list.length,
                      separatorBuilder: (_, __) => Divider(),
                      itemBuilder: (ctx, i) {
                        final c = list[i];
                        return ListTile(
                          leading: CircleAvatar(child: Text('${c.id}')),
                          title: Text(c.titulo),
                          subtitle: Text('Prioridade: ${c.prioridade}'),
                          trailing: Text(
                            c.statusDisplay,
                            style: TextStyle(
                              color: c.status == 'aberto'
                                  ? Colors.red
                                  : c.status == 'concluido'
                                      ? Colors.green
                                      : Colors.orange,
                            ),
                          ),
                          onTap: () {},
                        );
                      },
                    ),
                  ),
                ],
              ),
      ),
    );
  }
}

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