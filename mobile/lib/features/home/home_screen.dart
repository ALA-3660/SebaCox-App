import 'package:flutter/material.dart';
import '../../core/config/env_config.dart';
import '../../core/constants/api_constants.dart';
import '../../core/constants/app_colors.dart';
import '../../core/network/api_client.dart';
import '../../shared/helpers/error_mapper.dart';
import '../../shared/models/health_status.dart';
import '../../shared/widgets/app_button.dart';
import '../../shared/widgets/status_card.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiClient _apiClient = ApiClient();

  ConnectionStateStatus _status = ConnectionStateStatus.loading;
  String _statusMessage = 'সংযোগ পরীক্ষা হচ্ছে...';
  String? _details;
  int? _latencyMs;
  final TextEditingController _urlController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _urlController.text = EnvConfig.apiBaseUrl;
    _checkBackendHealth();
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  Future<void> _checkBackendHealth() async {
    setState(() {
      _status = ConnectionStateStatus.loading;
      _statusMessage = 'সংযোগ পরীক্ষা হচ্ছে...';
      _details = null;
      _latencyMs = null;
    });

    final stopwatch = Stopwatch()..start();

    try {
      final response = await _apiClient.get<HealthStatus>(
        ApiConstants.healthEndpoint,
        fromJson: (json) => HealthStatus.fromJson(json as Map<String, dynamic>),
      );

      stopwatch.stop();

      if (mounted) {
        if (response.success && (response.data?.isHealthy ?? false)) {
          setState(() {
            _status = ConnectionStateStatus.success;
            _statusMessage = 'সার্ভারের সাথে সংযোগ সফল';
            _latencyMs = stopwatch.elapsedMilliseconds;
            _details = 'API: ${response.message}\nল্যাটেন্সি: ${_latencyMs}ms';
          });
        } else {
          setState(() {
            _status = ConnectionStateStatus.failure;
            _statusMessage = 'সার্ভারের সাথে সংযোগ ব্যর্থ';
            _details = response.message;
          });
        }
      }
    } catch (e) {
      stopwatch.stop();
      if (mounted) {
        setState(() {
          _status = ConnectionStateStatus.failure;
          _statusMessage = 'সার্ভারের সাথে সংযোগ ব্যর্থ';
          _details = ErrorMapper.map(e);
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SebaCox'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Product Tagline
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Text(
                  '“মানুষের প্রয়োজন থেকে সেবার সমাধান।”',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: AppColors.primary,
                  ),
                ),
              ),
              const SizedBox(height: 12),
              const Text(
                'Phase 1: Project Foundation',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w500,
                  color: AppColors.textSecondary,
                ),
              ),

              const SizedBox(height: 32),

              // Backend Connection Status Card
              Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Backend Connection Status',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w700,
                    color: AppColors.textSecondary.withOpacity(0.9),
                    letterSpacing: 0.5,
                  ),
                ),
              ),
              const SizedBox(height: 12),

              StatusCard(
                status: _status,
                message: _statusMessage,
                details: _details,
              ),

              const SizedBox(height: 24),

              // Re-check action
              AppButton(
                text: 'পুনরায় সংযোগ পরীক্ষা করুন',
                icon: Icons.refresh_rounded,
                isLoading: _status == ConnectionStateStatus.loading,
                onPressed: _checkBackendHealth,
              ),

              const SizedBox(height: 32),

              // Configuration Box (Base URL)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.border),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'API Base URL Configuration',
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 8),
                    TextField(
                      controller: _urlController,
                      decoration: const InputDecoration(
                        isDense: true,
                        hintText: 'http://127.0.0.1:8000',
                        border: OutlineInputBorder(),
                        contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                      ),
                      style: const TextStyle(fontSize: 13, fontFamily: 'monospace'),
                    ),
                    const SizedBox(height: 10),
                    Align(
                      alignment: Alignment.centerRight,
                      child: TextButton(
                        onPressed: () {
                          EnvConfig.setEnvironment(
                            EnvConfig.environment,
                            customBaseUrl: _urlController.text.trim(),
                          );
                          _checkBackendHealth();
                        },
                        child: const Text('URL সংরক্ষণ ও পরীক্ষা করুন'),
                      ),
                    )
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
