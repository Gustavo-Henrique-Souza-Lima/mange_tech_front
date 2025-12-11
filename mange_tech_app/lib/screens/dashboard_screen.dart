import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../widgets/app_drawer.dart';
import '../widgets/info_card.dart';
import '../services/api_services.dart';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _api = ApiService();
  Map<String, dynamic>? data;
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
      final d = await _api.getDashboardData();
      setState(() {
        data = d;
        loading = false;
      });
    } catch (e) {
      setState(() {
        error = 'Erro ao carregar dados: $e';
        loading = false;
      });
    }
  }

  // Helper para definir cores baseadas no status
  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'aberto':
        return Colors.orange;
      case 'em_andamento':
        return Colors.blue;
      case 'aguardando_responsaveis':
        return Colors.purple; // Aguardando
      case 'realizado':
      case 'concluido':
        return Colors.green;
      case 'cancelado':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  // Helper para deixar o nome do status bonito na tela
  String _getStatusTitle(String status) {
    switch (status.toLowerCase()) {
      case 'aberto': return 'Aberto';
      case 'em_andamento': return 'Em Andamento';
      case 'aguardando_responsaveis': return 'Aguardando';
      case 'realizado': return 'Realizado';
      case 'concluido': return 'Concluído';
      case 'cancelado': return 'Cancelado';
      default: return status;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFF5F7FA), // Fundo levemente cinza
      drawer: AppDrawer(),
      appBar: AppBar(
        title: Text('Dashboard', style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: IconThemeData(color: Colors.black87),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: load,
          ),
        ],
      ),
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
                        ElevatedButton(onPressed: load, child: Text('Tentar Novamente')),
                      ],
                    ),
                  )
                : SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // CARDS DO TOPO
                      Wrap(
                          spacing: 16, // Espaçamento horizontal maior
                          runSpacing: 16, // Espaçamento vertical maior
                          children: [
                            InfoCard(
                              title: 'Chamados Abertos',
                              value: '${data!['chamadosAbertos'] ?? 0}',
                              subtitle: 'Fila de atendimento',
                              icon: Icons.assignment_late_rounded, // Ícone de alerta
                              color: Colors.orange, // Cor Laranja
                            ),
                            InfoCard(
                              title: 'Tempo Médio',
                              value: '${data!['tempoMedio'] ?? '-'}',
                              subtitle: 'Horas por chamado',
                              icon: Icons.timer_outlined, // Ícone de tempo
                              color: Colors.blue, // Cor Azul
                            ),
                            InfoCard(
                              title: 'Ativos Operantes',
                              value: '${data!['ativosAtivos'] ?? 0}',
                              subtitle: 'Em funcionamento',
                              icon: Icons.precision_manufacturing_outlined, // Ícone industrial
                              color: Colors.purple, // Cor Roxa
                            ),
                            InfoCard(
                              title: 'Satisfação',
                              value: '${data!['satisfacao'] ?? 0}%',
                              subtitle: 'Avaliação média',
                              icon: Icons.sentiment_very_satisfied_rounded, // Ícone feliz
                              color: Colors.green, // Cor Verde
                            ),
                          ],
                        ),
                        SizedBox(height: 24),

                        // GRÁFICO DE PIZZA MODERNO
                        Card(
                          elevation: 2,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          child: Padding(
                            padding: EdgeInsets.all(20),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Status dos Chamados',
                                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.grey[800]),
                                ),
                                SizedBox(height: 24),
                                Row(
                                  children: [
                                    // O Gráfico
                                    Expanded(
                                      flex: 3,
                                      child: SizedBox(
                                        height: 200,
                                        child: PieChart(
                                          PieChartData(
                                            sectionsSpace: 2,
                                            centerSpaceRadius: 40,
                                            sections: (data!['grafico'] as List).map<PieChartSectionData>((item) {
                                              final double valor = (item['total'] as int).toDouble();
                                              final String status = item['status'];
                                              return PieChartSectionData(
                                                value: valor,
                                                title: '${valor.toInt()}',
                                                titleStyle: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.white),
                                                radius: 50,
                                                color: _getStatusColor(status),
                                              );
                                            }).toList(),
                                          ),
                                        ),
                                      ),
                                    ),
                                    SizedBox(width: 24),
                                    // A Legenda
                                    Expanded(
                                      flex: 2,
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: (data!['grafico'] as List).map<Widget>((item) {
                                          return Padding(
                                            padding: const EdgeInsets.symmetric(vertical: 4.0),
                                            child: Row(
                                              children: [
                                                Container(
                                                  width: 12,
                                                  height: 12,
                                                  decoration: BoxDecoration(
                                                    color: _getStatusColor(item['status']),
                                                    shape: BoxShape.circle,
                                                  ),
                                                ),
                                                SizedBox(width: 8),
                                                Expanded(
                                                  child: Text(
                                                    _getStatusTitle(item['status']),
                                                    style: TextStyle(fontSize: 12, color: Colors.grey[700]),
                                                    overflow: TextOverflow.ellipsis,
                                                  ),
                                                ),
                                                Text(
                                                  '${item['total']}',
                                                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                                                ),
                                              ],
                                            ),
                                          );
                                        }).toList(),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        
                        SizedBox(height: 24),

                        // CARDS INFERIORES (Manutenção e Técnicos)
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Expanded(
                              child: Card(
                                elevation: 2,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                child: Padding(
                                  padding: EdgeInsets.all(16),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Row(
                                        children: [
                                          Icon(Icons.warning_amber_rounded, color: Colors.orange, size: 20),
                                          SizedBox(width: 8),
                                          Text('Atenção', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700])),
                                        ],
                                      ),
                                      SizedBox(height: 12),
                                      Text('Manutenções Atrasadas', style: TextStyle(fontSize: 14, color: Colors.grey[600])),
                                      SizedBox(height: 4),
                                      Text('8 ativos', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                            SizedBox(width: 16),
                            Expanded(
                              child: Card(
                                elevation: 2,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                child: Padding(
                                  padding: EdgeInsets.all(16),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Row(
                                        children: [
                                          Icon(Icons.people_outline, color: Colors.blue, size: 20),
                                          SizedBox(width: 8),
                                          Text('Equipe', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700])),
                                        ],
                                      ),
                                      SizedBox(height: 12),
                                      Text('Técnicos Online', style: TextStyle(fontSize: 14, color: Colors.grey[600])),
                                      SizedBox(height: 4),
                                      Text('12 / 15', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
      ),
    );
  }
}