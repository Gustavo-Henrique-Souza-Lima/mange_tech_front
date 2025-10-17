import 'package:flutter/material.dart';
import '../widgets/app_drawer.dart';

class ConfiguracoesScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: AppDrawer(),
      appBar: AppBar(title: Text('Configurações')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: ListView(
          children: [
            Card(
              child: Padding(
                padding: EdgeInsets.all(12),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Configurações Gerais', style: TextStyle(fontWeight: FontWeight.bold)),
                  SizedBox(height:8),
                  TextField(decoration: InputDecoration(labelText: 'Nome da Empresa'),),
                  SizedBox(height:8),
                  TextField(decoration: InputDecoration(labelText: 'Email de Notificações'),),
                ]),
              ),
            ),
            SizedBox(height:12),
            Card(child: Padding(padding: EdgeInsets.all(12), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Configurações de Chamados', style: TextStyle(fontWeight: FontWeight.bold)),
              SwitchListTile(value: true, onChanged: (_){}, title: Text('Notificações por Email')),
              SwitchListTile(value: false, onChanged: (_){}, title: Text('Auto-atribuição')),
              SwitchListTile(value: true, onChanged: (_){}, title: Text('SLA Ativo')),
            ]))),
            SizedBox(height:12),
            Card(child: Padding(padding: EdgeInsets.all(12), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Segurança', style: TextStyle(fontWeight: FontWeight.bold)),
              TextField(decoration: InputDecoration(labelText: 'Tempo de Sessão (minutos)'),),
              SwitchListTile(value: false, onChanged: (_){}, title: Text('Autenticação em Dois Fatores')),
              SizedBox(height:10),
              ElevatedButton(onPressed: (){}, child: Text('Salvar Configurações'))
            ]))),
          ],
        ),
      ),
    );
  }
}
