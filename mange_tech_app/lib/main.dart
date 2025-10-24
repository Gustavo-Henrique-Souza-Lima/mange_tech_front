import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/login_screen.dart';
import 'screens/dashboard_screen.dart';
import 'screens/chamados_screen.dart';
import 'screens/ativos_screen.dart';
import 'screens/usuarios_screen.dart';
import 'screens/configuracoes_screen.dart';
import 'services/api_services.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        Provider<ApiService>(
          create: (_) => ApiService(),
        ),
      ],
      child: MangeTechApp(),
    ),
  );
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
          titleTextStyle: TextStyle(
            color: Colors.black,
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
          iconTheme: IconThemeData(color: Colors.black),
        ),
      ),
      home: AuthChecker(),
      routes: {
        '/login': (_) => LoginScreen(),
        '/dashboard': (_) => DashboardScreen(),
        '/chamados': (_) => ChamadosScreen(),
        '/ativos': (_) => AtivosScreen(),
        '/usuarios': (_) => UsuariosScreen(),
        '/config': (_) => ConfiguracoesScreen(),
      },
    );
  }
}

class AuthChecker extends StatefulWidget {
  @override
  _AuthCheckerState createState() => _AuthCheckerState();
}

class _AuthCheckerState extends State<AuthChecker> {
  bool _checking = true;

  @override
  void initState() {
    super.initState();
    _checkAuth();
  }

  void _checkAuth() async {
    final _api = Provider.of<ApiService>(context, listen: false);
    final isAuthenticated = await _api.isAuthenticated();
    
    if (mounted) {
      if (isAuthenticated) {
        Navigator.of(context).pushReplacementNamed('/dashboard');
      } else {
        Navigator.of(context).pushReplacementNamed('/login');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(),
            SizedBox(height: 16),
            Text('Carregando...'),
          ],
        ),
      ),
    );
  }
}