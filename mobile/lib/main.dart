import 'package:flutter/material.dart';
import 'core/config/env_config.dart';
import 'core/constants/app_brand.dart';
import 'core/constants/app_colors.dart';
import 'core/network/api_client.dart';
import 'core/theme/app_theme.dart';
import 'core/theme/app_typography.dart';
import 'features/auth/models/auth_state.dart';
import 'features/auth/repositories/auth_repository.dart';
import 'features/auth/screens/auth_home_screen.dart';
import 'features/auth/screens/auth_screen.dart';
import 'features/auth/services/auth_service.dart';

import 'features/location/repositories/location_repository.dart';
import 'features/location/services/device_location_service.dart';
import 'features/location/services/location_api_service.dart';

import 'features/categories/repositories/category_repository.dart';
import 'features/categories/services/category_api_service.dart';

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

  final categoryApiService = CategoryApiService(apiClient);
  final categoryRepository = CategoryRepository(categoryApiService);

  runApp(SebaCoxApp(
    authRepository: authRepository,
    locationRepository: locationRepository,
    categoryRepository: categoryRepository,
  ));
}

class SebaCoxApp extends StatefulWidget {
  final AuthRepository authRepository;
  final LocationRepository locationRepository;
  final CategoryRepository categoryRepository;

  const SebaCoxApp({
    super.key,
    required this.authRepository,
    required this.locationRepository,
    required this.categoryRepository,
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
              return Scaffold(
                backgroundColor: const Color(0xFFF8FAFC),
                body: Center(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 24),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          width: 64,
                          height: 64,
                          decoration: BoxDecoration(
                            color: AppColors.primary,
                            borderRadius: BorderRadius.circular(16),
                            boxShadow: [
                              BoxShadow(
                                color: AppColors.primary.withOpacity(0.25),
                                blurRadius: 12,
                                offset: const Offset(0, 4),
                              ),
                            ],
                          ),
                          alignment: Alignment.center,
                          child: const Text(
                            'SC',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 24,
                              fontWeight: FontWeight.w900,
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          '${AppBrand.appNameEn} (${AppBrand.appNameBn})',
                          style: AppTypography.largeHeading2.copyWith(
                            color: AppColors.primary,
                            fontSize: 22,
                          ),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          AppBrand.sloganWithQuotes,
                          textAlign: TextAlign.center,
                          style: AppTypography.mediumHeading2.copyWith(
                            color: AppColors.primaryDark,
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          AppBrand.shortDescriptionWithQuotes,
                          textAlign: TextAlign.center,
                          style: AppTypography.bodySmall.copyWith(
                            color: AppColors.textSecondary,
                            fontSize: 12,
                          ),
                        ),
                        const SizedBox(height: 32),
                        const CircularProgressIndicator(
                          color: AppColors.primary,
                          strokeWidth: 2.5,
                        ),
                        const SizedBox(height: 14),
                        Text(
                          'সেশন পরীক্ষা করা হচ্ছে...',
                          style: AppTypography.bodySmall.copyWith(
                            color: AppColors.textSecondary,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );

            case AuthStatus.authenticated:
              return AuthHomeScreen(
                authRepository: widget.authRepository,
                locationRepository: widget.locationRepository,
                categoryRepository: widget.categoryRepository,
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
