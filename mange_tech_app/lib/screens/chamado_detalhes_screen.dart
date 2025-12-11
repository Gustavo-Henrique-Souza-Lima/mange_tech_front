import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../models/chamado.dart';
import '../services/api_services.dart';

class ChamadoDetalhesScreen extends StatefulWidget {
  final Chamado chamado;

  const ChamadoDetalhesScreen({required this.chamado});

  @override
  _ChamadoDetalhesScreenState createState() => _ChamadoDetalhesScreenState();
}

class _ChamadoDetalhesScreenState extends State<ChamadoDetalhesScreen> {
  late Chamado _chamado;
  bool _loading = true; // Carregando geral
  final TextEditingController _comentarioController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _chamado = widget.chamado;
    _refreshChamadoCompleto();
  }

  // MUDANÇA: Em vez de buscar só histórico, buscamos o chamado inteiro atualizado
  Future<void> _refreshChamadoCompleto() async {
    final api = Provider.of<ApiService>(context, listen: false);
    // getChamadoById deve retornar o objeto completo com histórico
    final atualizado = await api.getChamadoById(_chamado.id);
    
    if (mounted) {
      setState(() {
        if (atualizado != null) {
          _chamado = atualizado;
        }
        _loading = false;
      });
    }
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'aberto': return Colors.orange;
      case 'em_andamento': return Colors.blue;
      case 'aguardando_responsaveis': return Colors.purple;
      case 'realizado':
      case 'concluido': return Colors.green;
      case 'cancelado': return Colors.red;
      default: return Colors.grey;
    }
  }

  void _showStatusDialog() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Alterar Status'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Selecione o novo status para o chamado:'),
            SizedBox(height: 16),
            TextField(
              controller: _comentarioController,
              decoration: InputDecoration(
                labelText: 'Comentário (Obrigatório)',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            SizedBox(height: 16),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                _buildStatusOption('Em andamento', 'em_andamento', Colors.blue),
                _buildStatusOption('Concluir', 'concluido', Colors.green),
                _buildStatusOption('Cancelar', 'cancelado', Colors.red),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusOption(String label, String value, Color color) {
    return ActionChip(
      label: Text(label, style: TextStyle(color: Colors.white)),
      backgroundColor: color,
      onPressed: () => _updateStatus(value),
    );
  }

  Future<void> _updateStatus(String novoStatus) async {
    if (_comentarioController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Por favor, adicione um comentário.')),
      );
      return;
    }

    Navigator.pop(context);
    
    final api = Provider.of<ApiService>(context, listen: false);
    final result = await api.updateChamadoStatus(
      chamadoId: _chamado.id,
      novoStatus: novoStatus,
      comentario: _comentarioController.text,
    );

    if (result['success']) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Status atualizado!'), backgroundColor: Colors.green),
      );
      _comentarioController.clear();
      // Recarrega tudo para mostrar o novo status e o novo item no histórico
      _refreshChamadoCompleto(); 
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(result['error'] ?? 'Erro ao atualizar'), backgroundColor: Colors.red),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    // Usamos a lista de histórico que veio dentro do chamado
    final historicoList = _chamado.historico ?? [];

    return Scaffold(
      backgroundColor: Color(0xFFF5F7FA),
      appBar: AppBar(
        title: Text('Chamado #${_chamado.id}'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () {
              setState(() => _loading = true);
              _refreshChamadoCompleto();
            },
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // CARD STATUS
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Row(
                  children: [
                    Container(
                      padding: EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: _getStatusColor(_chamado.status).withOpacity(0.1),
                        shape: BoxShape.circle,
                      ),
                      child: Icon(Icons.info_outline, color: _getStatusColor(_chamado.status)),
                    ),
                    SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Status Atual', style: TextStyle(color: Colors.grey[600], fontSize: 12)),
                          Text(
                            _chamado.statusDisplay,
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: _getStatusColor(_chamado.status),
                            ),
                          ),
                        ],
                      ),
                    ),
                    ElevatedButton(
                      onPressed: _showStatusDialog,
                      child: Text('Alterar'),
                      style: ElevatedButton.styleFrom(
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 16),

            // DETALHES
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: Padding(
                padding: EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(_chamado.titulo, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    SizedBox(height: 12),
                    // Correção do erro de String? com operador ??
                    Text(_chamado.descricao ?? 'Sem descrição', style: TextStyle(fontSize: 15, color: Colors.grey[800], height: 1.5)),
                    Divider(height: 30),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        _infoBadge(Icons.priority_high, 'Prioridade', _chamado.urgenciaDisplay),
                        _infoBadge(Icons.calendar_today, 'Data', DateFormat('dd/MM/yyyy').format(_chamado.dataAbertura)),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 24),

            // HISTÓRICO (TIMELINE)
            Text('Histórico de Atividades', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.grey[800])),
            SizedBox(height: 16),
            
            _loading
                ? Center(child: CircularProgressIndicator())
                : historicoList.isEmpty
                  ? Center(child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Text('Nenhum histórico registrado.', style: TextStyle(color: Colors.grey)),
                    ))
                  : ListView.builder(
                      shrinkWrap: true,
                      physics: NeverScrollableScrollPhysics(),
                      itemCount: historicoList.length,
                      itemBuilder: (context, index) {
                        final item = historicoList[index];
                        final dataFormatada = DateFormat('dd/MM HH:mm').format(item.createdAt);
                        final nomeUsuario = item.usuario?.nomeCompleto ?? item.usuario?.username ?? 'Sistema';

                        return Padding(
                          padding: const EdgeInsets.only(bottom: 16.0),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Column(
                                children: [
                                  Container(
                                    width: 12,
                                    height: 12,
                                    decoration: BoxDecoration(
                                      color: Colors.blue[200],
                                      shape: BoxShape.circle,
                                    ),
                                  ),
                                  Container(width: 2, height: 60, color: Colors.grey[300]),
                                ],
                              ),
                              SizedBox(width: 16),
                              Expanded(
                                child: Card(
                                  margin: EdgeInsets.zero,
                                  elevation: 0,
                                  color: Colors.white,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                    side: BorderSide(color: Colors.grey.shade200)
                                  ),
                                  child: Padding(
                                    padding: const EdgeInsets.all(12.0),
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                          children: [
                                            Text(item.statusDisplay.toUpperCase(), style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11, color: Colors.blue[800])),
                                            Text(dataFormatada, style: TextStyle(color: Colors.grey, fontSize: 11)),
                                          ],
                                        ),
                                        SizedBox(height: 4),
                                        Text(item.comentario ?? '', style: TextStyle(fontSize: 14)),
                                        SizedBox(height: 6),
                                        Row(
                                          children: [
                                            Icon(Icons.person, size: 12, color: Colors.grey),
                                            SizedBox(width: 4),
                                            Text(nomeUsuario, style: TextStyle(fontSize: 12, color: Colors.grey[600], fontStyle: FontStyle.italic)),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
          ],
        ),
      ),
    );
  }

  Widget _infoBadge(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, size: 16, color: Colors.grey),
        SizedBox(width: 6),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: TextStyle(fontSize: 10, color: Colors.grey)),
            Text(value, style: TextStyle(fontWeight: FontWeight.w600)),
          ],
        ),
      ],
    );
  }
}