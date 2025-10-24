import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../widgets/app_drawer.dart';
import '../widgets/info_card.dart';
import '../services/api_services.dart'; // ✅ Corrigido (era api_services.dart)

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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: AppDrawer(),
      appBar: AppBar(
        title: Text('Dashboard'),
        centerTitle: false,
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
                        ElevatedButton(
                          onPressed: load,
                          child: Text('Tentar Novamente'),
                        ),
                      ],
                    ),
                  )
                : SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Wrap(
                          spacing: 12,
                          runSpacing: 12,
                          children: [
                            InfoCard(
                              title: 'Chamados Abertos',
                              value: '${data!['chamadosAbertos'] ?? 0}',
                              subtitle: '+12% vs mês anterior',
                            ),
                            InfoCard(
                              title: 'Tempo Médio Resolução',
                              value: '${data!['tempoMedio'] ?? '-'}',
                              subtitle: '-8% melhora contínua',
                            ),
                            InfoCard(
                              title: 'Ativos Ativos',
                              value: '${data!['ativosAtivos'] ?? 0}',
                              subtitle: '+3% vs mês anterior',
                            ),
                            InfoCard(
                              title: 'Taxa de Satisfação',
                              value: '${data!['satisfacao'] ?? 0}%',
                              subtitle: '+2% avaliações positivas',
                            ),
                          ],
                        ),
                        SizedBox(height: 20),
                        Card(
                          child: Container(
                            padding: EdgeInsets.all(16),
                            width: double.infinity,
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Gráfico de Status dos Chamados',
                                  style: TextStyle(color: Colors.grey[700]),
                                ),
                                SizedBox(height: 12),
                                Container(
                                  height: 200,
                                  child: PieChart(
                                    PieChartData(
                                      sections: [
                                        PieChartSectionData(
                                          value: (data!['grafico']?['abertos'] ?? 0)
                                              .toDouble(),
                                          title: 'Abertos',
                                          radius: 60,
                                          color: Colors.orange,
                                        ),
                                        PieChartSectionData(
                                          value: (data!['grafico']?['fechados'] ?? 0)
                                              .toDouble(),
                                          title: 'Fechados',
                                          radius: 60,
                                          color: Colors.green,
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        SizedBox(height: 20),
                        Row(
                          children: [
                            Expanded(
                              child: Card(
                                child: Container(
                                  padding: EdgeInsets.all(16),
                                  height: 80,
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Manutenções Atrasadas',
                                        style: TextStyle(
                                            color: Colors.grey[700]),
                                      ),
                                      SizedBox(height: 8),
                                      Text('8 ativos precisam de atenção'),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                            SizedBox(width: 12),
                            Expanded(
                              child: Card(
                                child: Container(
                                  padding: EdgeInsets.all(16),
                                  height: 80,
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Técnicos Disponíveis',
                                        style: TextStyle(
                                            color: Colors.grey[700]),
                                      ),
                                      SizedBox(height: 8),
                                      Text('12 de 15 técnicos online'),
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
