import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../widgets/app_drawer.dart';
import '../models/ativo.dart';
import '../services/api_services.dart';

class AtivosScreen extends StatefulWidget {
  @override
  _AtivosScreenState createState() => _AtivosScreenState();
}

class _AtivosScreenState extends State<AtivosScreen> {
  List<Ativo> list = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    load();
  }

  void load() async {
    final srv = Provider.of<ApiService>(context, listen: false);
    final d = await srv.getAtivos();
    setState(() {
      list = d;
      loading = false;
    });
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
                          decoration: InputDecoration(
                            prefixIcon: Icon(Icons.search),
                            hintText: 'Buscar por ID ou nome...',
                          ),
                        ),
                      ),
                      SizedBox(width: 12),
                      ElevatedButton(
                        onPressed: () {},
                        child: Text('Exportar'),
                      ),
                      SizedBox(width: 8),
                      ElevatedButton(
                        onPressed: () {},
                        child: Text('+ Novo Ativo'),
                      ),
                    ],
                  ),
                  SizedBox(height: 12),
                  Expanded(
                    child: ListView.separated(
                      itemCount: list.length,
                      separatorBuilder: (_, __) => Divider(),
                      itemBuilder: (ctx, i) {
                        final a = list[i];
                        return ListTile(
                          title: Text(a.nome),
                          subtitle: Text(a.local),
                          trailing: Text(
                            a.status,
                            style: TextStyle(
                              color: a.status.contains('manutenção')
                                  ? Colors.orange
                                  : Colors.green,
                            ),
                          ),
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
