import 'package:flutter/material.dart';

class AppDrawer extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Widget link(String title, String route, IconData icon) {
      return ListTile(
        leading: Icon(icon, color: Colors.blueGrey),
        title: Text(title),
        onTap: () {
          Navigator.of(context).pushReplacementNamed(route);
        },
      );
    }

    return Drawer(
      child: SafeArea(
        child: Column(
          children: [
            Container(
              height: 70,
              alignment: Alignment.centerLeft,
              padding: EdgeInsets.symmetric(horizontal: 16),
              child: Text('MANGE_TECH', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            ),
            Divider(),
            link('Dashboard', '/', Icons.dashboard),
            link('Chamados', '/chamados', Icons.build),
            link('Ativos', '/ativos', Icons.inventory_2),
            link('Usuários', '/usuarios', Icons.person),
            Spacer(),
            ListTile(
              leading: Icon(Icons.settings),
              title: Text('Configurações'),
              onTap: () => Navigator.of(context).pushReplacementNamed('/config'),
            ),
          ],
        ),
      ),
    );
  }
}
