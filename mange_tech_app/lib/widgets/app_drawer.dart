import 'package:flutter/material.dart';
import '../services/api_services.dart';

class AppDrawer extends StatelessWidget {
  final ApiService _api = ApiService();

  @override
  Widget build(BuildContext context) {
    Widget link(String title, String route, IconData icon) {
      return ListTile(
        leading: Icon(icon, color: Colors.blueGrey),
        title: Text(title),
        onTap: () {
          Navigator.of(context).pop(); // Fecha o drawer
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
              decoration: BoxDecoration(
                border: Border(
                  bottom: BorderSide(color: Colors.grey[300]!),
                ),
              ),
              child: Row(
                children: [
                  Icon(Icons.build, color: Colors.blue, size: 32),
                  SizedBox(width: 12),
                  Text(
                    'MANGE_TECH',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                ],
              ),
            ),
            
            link('Dashboard', '/dashboard', Icons.dashboard),
            link('Chamados', '/chamados', Icons.build),
            link('Ativos', '/ativos', Icons.inventory_2),
            link('Usuários', '/usuarios', Icons.person),
            
            Spacer(),
            
            Divider(),
            
            ListTile(
              leading: Icon(Icons.settings, color: Colors.blueGrey),
              title: Text('Configurações'),
              onTap: () {
                Navigator.of(context).pop();
                Navigator.of(context).pushReplacementNamed('/config');
              },
            ),
            
            ListTile(
              leading: Icon(Icons.exit_to_app, color: Colors.red),
              title: Text('Sair', style: TextStyle(color: Colors.red)),
              onTap: () async {
                final confirm = await showDialog<bool>(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: Text('Confirmar Saída'),
                    content: Text('Deseja realmente sair do aplicativo?'),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.of(ctx).pop(false),
                        child: Text('Cancelar'),
                      ),
                      TextButton(
                        onPressed: () => Navigator.of(ctx).pop(true),
                        style: TextButton.styleFrom(
                          foregroundColor: Colors.red,
                        ),
                        child: Text('Sair'),
                      ),
                    ],
                  ),
                );

                if (confirm == true) {
                  await _api.logout();
                  Navigator.of(context).pushNamedAndRemoveUntil(
                    '/login',
                    (route) => false,
                  );
                }
              },
            ),
            
            SizedBox(height: 16),
          ],
        ),
      ),
    );
  }
}