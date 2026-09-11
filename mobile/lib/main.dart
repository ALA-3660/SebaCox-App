import 'package:flutter/material.dart';
import 'core/config/env_config.dart';
import 'core/network/api_client.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/models/auth_state.dart';
import 'features/auth/repositories/auth_repository.dart';
import 'features/auth/screens/auth_home_screen.dart';
import 'features/auth/screens/auth_screen.dart';
import 'features/auth/services/auth_service.dart';

import 'features/location/repositories/location_repository.dart';
import 'features/location/services/device_location_service.dart';
import 'features/location/services/location_api_service.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize environment (defaults to development with configurable URL)
  EnvConfig.setEnvironment(AppEnvironment.development);

  final apiClient = ApiClient();
  final authService = AuthService(apiClient);
  final authRepository = AuthRepository(
    authService: authService,
    apiClient: apiClient,
  );

  final locationApiService = LocationApiService(apiClient);
  final deviceLocationService = DeviceLocationService();
  final locationRepository = LocationRepository(
    apiService: locationApiService,
    deviceService: deviceLocationService,
  );

  runApp(SebaCoxApp(
    authRepository: authRepository,
    locationRepository: locationRepository,
  ));
}

class SebaCoxApp extends StatefulWidget {
  final AuthRepository authRepository;
  final LocationRepository locationRepository;

  const SebaCoxApp({
    super.key,
    required this.authRepository,
    required this.locationRepository,
  });

  @override
  State<SebaCoxApp> createState() => _SebaCoxAppState();
}

class _SebaCoxAppState extends State<SebaCoxApp> {
  @override
  void initState() {
    super.initState();
    // Verify whether an existing secure session exists on app launch
    widget.authRepository.checkExistingSession();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SebaCox',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: StreamBuilder<AuthState>(
        stream: widget.authRepository.stateStream,
        initialData: widget.authRepository.currentState,
        builder: (context, snapshot) {
          final authState = snapshot.data ?? AuthState.unknown();

          switch (authState.status) {
            case AuthStatus.unknown:
            case AuthStatus.checkingSession:
              return const Scaffold(
                backgroundColor: Color(0xFFF8FAFC),
                body: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      CircularProgressIndicator(
                        color: Color(0xFF0F766E),
                      ),
                      SizedBox(height: 16),
                      Text(
                        'সেশন পরীক্ষা করা হচ্ছে...',
                        style: TextStyle(
                          fontSize: 14,
                          color: Color(0xFF64748B),
                        ),
                      ),
                    ],
                  ),
                ),
              );

            case AuthStatus.authenticated:
              return AuthHomeScreen(
                authRepository: widget.authRepository,
                locationRepository: widget.locationRepository,
                user: authState.user!,
              );

            case AuthStatus.unauthenticated:
            default:
              return AuthScreen(
                authRepository: widget.authRepository,
              );
          }
        },
      ),
    );
  }
}
