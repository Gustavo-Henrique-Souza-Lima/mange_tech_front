import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/dashboard_screen.dart';
import 'screens/chamados_screen.dart';
import 'screens/ativos_screen.dart';
import 'screens/usuarios_screen.dart';
import 'screens/configuracoes_screen.dart';
import 'services/mock_service.dart';

void main() {
  runApp(MultiProvider(
    providers: [
      Provider<MockService>(create: (_) => MockService()),
    ],
    child: MangeTechApp(),
  ));
}

class MangeTechApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final baseTheme = ThemeData(
      primarySwatch: Colors.blue,
      scaffoldBackgroundColor: Color(0xFFF7F9FB),
      textTheme: TextTheme(bodyMedium: TextStyle(color: Colors.grey[900])),
    );

    return MaterialApp(
      title: 'MANGE_TECH',
      theme: baseTheme.copyWith(
        appBarTheme: AppBarTheme(
          elevation: 0,
          backgroundColor: Colors.white,
          titleTextStyle: TextStyle(color: Colors.black, fontSize: 18, fontWeight: FontWeight.w600),
          iconTheme: IconThemeData(color: Colors.black),
        ),
      ),
      initialRoute: '/',
      routes: {
        '/': (_) => DashboardScreen(),
        '/chamados': (_) => ChamadosScreen(),
        '/ativos': (_) => AtivosScreen(),
        '/usuarios': (_) => UsuariosScreen(),
        '/config': (_) => ConfiguracoesScreen(),
      },
    );
  }
}
