import 'package:flutter/material.dart';
import 'core/config/env_config.dart';
import 'core/theme/app_theme.dart';
import 'features/home/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize environment (defaults to development with configurable URL)
  EnvConfig.setEnvironment(AppEnvironment.development);

  runApp(const SebaCoxApp());
}

class SebaCoxApp extends StatelessWidget {
  const SebaCoxApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SebaCox',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const HomeScreen(),
    );
  }
}
