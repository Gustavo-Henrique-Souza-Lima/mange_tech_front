import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../widgets/app_drawer.dart';
import '../models/chamado.dart';
import '../services/api_services.dart'; //  importa seu novo serviço

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
    final srv = Provider.of<ApiService>(context, listen: false); // 👈 troca MockService por ApiService
    final d = await srv.getChamados();
    setState(() {
      list = d;
      loading = false;
    });
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
                        onPressed: () {},
                        icon: Icon(Icons.add),
                        label: Text('Novo Chamado'),
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
                            c.status,
                            style: TextStyle(
                              color: c.status == 'Aberto'
                                  ? Colors.red
                                  : Colors.green,
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
