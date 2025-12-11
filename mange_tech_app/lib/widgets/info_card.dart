import 'package:flutter/material.dart';

class InfoCard extends StatelessWidget {
  final String title;
  final String value;
  final String subtitle;
  final IconData icon; // Novo: Ícone
  final Color color;   // Novo: Cor do tema do card

  const InfoCard({
    required this.title,
    required this.value,
    this.subtitle = '',
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    // LayoutBuilder garante que o card se adapte à largura disponível (evita overflow)
    return LayoutBuilder(
      builder: (context, constraints) {
        return Container(
          // Largura dinâmica: Metade da tela menos espaçamentos
          width: (MediaQuery.of(context).size.width / 2) - 24,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20), // Bordas bem arredondadas
            boxShadow: [
              BoxShadow(
                color: color.withOpacity(0.1), // Sombra da cor do tema
                blurRadius: 10,
                offset: Offset(0, 4),
              ),
            ],
          ),
          child: Padding(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Cabeçalho do Card com Ícone colorido
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Container(
                      padding: EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: color.withOpacity(0.1), // Fundo clarinho
                        shape: BoxShape.circle,
                      ),
                      child: Icon(icon, color: color, size: 20),
                    ),
                    // Se quiser colocar algo na direita, põe aqui (ex: menu dots)
                  ],
                ),
                SizedBox(height: 12),
                
                // Título
                Text(
                  title,
                  style: TextStyle(
                    color: Colors.grey[600],
                    fontSize: 13,
                    fontWeight: FontWeight.w500,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                SizedBox(height: 4),
                
                // Valor Principal (Bem grande e na cor do tema)
                Text(
                  value,
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: Colors.black87, // Ou use 'color' se quiser colorir o texto
                  ),
                ),
                
                // Subtítulo
                if (subtitle.isNotEmpty) ...[
                  SizedBox(height: 8),
                  Container(
                    padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.grey[50],
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      subtitle,
                      style: TextStyle(
                        color: Colors.grey[500], 
                        fontSize: 11,
                        fontWeight: FontWeight.w500
                      ),
                    ),
                  ),
                ]
              ],
            ),
          ),
        );
      },
    );
  }
}