import 'package:easy_pass/utils/bottom_bar.dart';
import 'package:flutter/material.dart';

class SettingsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Center(
            child: Text("This is settings page."),
          ),
          BottomBar(
            selectedPage: 'settings',
          ),
        ],
      ),
    );
  }
}