import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../widgets/app_drawer.dart';
import '../widgets/info_card.dart';
import '../services/mock_service.dart';
import 'package:fl_chart/fl_chart.dart';
class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Map<String, dynamic>? data;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    load();
  }

  void load() async {
    final srv = Provider.of<MockService>(context, listen: false);
    final d = await srv.getDashboardData();
    setState(() {
      data = d;
      loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: AppDrawer(),
      appBar: AppBar(title: Text('Dashboard'), centerTitle: false),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: loading ? Center(child: CircularProgressIndicator()) :
        SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: [
                  InfoCard(title: 'Chamados Abertos', value: '${data!['chamadosAbertos']}', subtitle: '+12% vs mês anterior'),
                  InfoCard(title: 'Tempo Médio Resolução', value: data!['tempoMedio'], subtitle: '-8% melhora contínua'),
                  InfoCard(title: 'Ativos Ativos', value: '${data!['ativosAtivos']}', subtitle: '+3% vs mês anterior'),
                  InfoCard(title: 'Taxa de Satisfação', value: '${data!['satisfacao']}%', subtitle: '+2% avaliações positivas'),
                ],
              ),
              SizedBox(height: 20),
              // simple pie chart using fl_chart
              Card(
                child: Container(
                  padding: EdgeInsets.all(16),
                  width: double.infinity,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Gráfico de Status dos Chamados', style: TextStyle(color: Colors.grey[700])),
                      SizedBox(height: 12),
                      Container(
                        height: 200,
                        child: PieChart(
                          PieChartData(sections: [
                            PieChartSectionData(value: data!['grafico']['abertos'].toDouble(), title: 'Abertos', radius: 60),
                            PieChartSectionData(value: data!['grafico']['fechados'].toDouble(), title: 'Fechados', radius: 60),
                          ]),
                        ),
                      )
                    ],
                  ),
                ),
              ),
              SizedBox(height: 20),
              Row(
                children: [
                  Expanded(child: Card(child: Container(padding: EdgeInsets.all(16), height: 80, child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text('Manutenções Atrasadas', style: TextStyle(color: Colors.grey[700])), SizedBox(height:8), Text('8 ativos precisam de atenção')])))),
                  SizedBox(width: 12),
                  Expanded(child: Card(child: Container(padding: EdgeInsets.all(16), height: 80, child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text('Técnicos Disponíveis', style: TextStyle(color: Colors.grey[700])), SizedBox(height:8), Text('12 de 15 técnicos online')])))),
                  SizedBox(width: 12),
                  Expanded(child: Card(child: Container(padding: EdgeInsets.all(16), height: 80, child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text('Performance', style: TextStyle(color: Colors.grey[700])), SizedBox(height:8), Text('Acima da meta em 15%')])))),
                ],
              )
            ],
          ),
        ),
      )
    );
  }
}
