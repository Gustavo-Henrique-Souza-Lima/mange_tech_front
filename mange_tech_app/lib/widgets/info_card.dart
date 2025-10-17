import 'package:flutter/material.dart';

class InfoCard extends StatelessWidget {
  final String title;
  final String value;
  final String subtitle;
  const InfoCard({required this.title, required this.value, this.subtitle = ''});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: Container(
        padding: EdgeInsets.all(16),
        width: MediaQuery.of(context).size.width * 0.42,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: TextStyle(color: Colors.grey[700])),
            SizedBox(height: 8),
            Text(value, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            if (subtitle.isNotEmpty) ...[
              SizedBox(height: 6),
              Text(subtitle, style: TextStyle(color: Colors.grey[500], fontSize: 12)),
            ]
          ],
        ),
      ),
    );
  }
}
