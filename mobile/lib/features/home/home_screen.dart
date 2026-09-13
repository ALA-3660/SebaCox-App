import 'package:flutter/material.dart';
import '../../core/config/env_config.dart';
import '../../core/constants/api_constants.dart';
import '../../core/constants/app_brand.dart';
import '../../core/constants/app_colors.dart';
import '../../core/network/api_client.dart';
import '../../core/theme/app_typography.dart';
import '../../shared/helpers/error_mapper.dart';
import '../../shared/models/health_status.dart';
import '../../shared/widgets/app_button.dart';
import '../../shared/widgets/status_card.dart';
import '../provider/screens/provider_list_screen.dart';
import '../provider/screens/provider_registration_flow_screen.dart';
import '../provider/screens/provider_dashboard_screen.dart';

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

  void _showPostBottomSheet() {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'আমার পোস্ট করুন',
                style: AppTypography.largeHeading2.copyWith(
                  fontWeight: FontWeight.bold,
                  color: AppColors.textPrimary,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                'আপনি কীভাবে সেবাকক্স ব্যবহার করতে চান?',
                style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
              ),
              const SizedBox(height: 16),
              ListTile(
                leading: Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: AppColors.primary.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(Icons.search, color: AppColors.primary),
                ),
                title: Text(
                  'আমি সেবা নিব',
                  style: AppTypography.mediumHeading2.copyWith(fontWeight: FontWeight.bold),
                ),
                subtitle: const Text('আপনার প্রয়োজনীয় সেবার চাহিদা বা অনুরোধ পোস্ট করুন (Phase 6)'),
                onTap: () {
                  Navigator.pop(ctx);
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('চাহিদা পোস্ট ইঞ্জিন পরবর্তী ধাপে উন্মুক্ত হবে।')),
                  );
                },
              ),
              const Divider(),
              ListTile(
                leading: Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xFF10B981).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(Icons.handyman_outlined, color: Color(0xFF10B981)),
                ),
                title: Text(
                  'আমি সেবা দিব',
                  style: AppTypography.mediumHeading2.copyWith(fontWeight: FontWeight.bold),
                ),
                subtitle: const Text('সেবাদাতা হিসেবে নতুন প্রোফাইল নিবন্ধন করুন'),
                onTap: () {
                  Navigator.pop(ctx);
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const ProviderRegistrationFlowScreen()),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
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
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppColors.primary.withOpacity(0.15)),
                ),
                child: Column(
                  children: [
                    Text(
                      AppBrand.sloganWithQuotes,
                      textAlign: TextAlign.center,
                      style: AppTypography.mediumHeading2.copyWith(
                        color: AppColors.primary,
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
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
                  ],
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

              const SizedBox(height: 24),

              // Provider Foundation Quick Action Panel
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppColors.border),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'সেবাদাতা ও সেবা নেটওয়ার্ক',
                      style: AppTypography.mediumHeading2.copyWith(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: OutlinedButton.icon(
                            icon: const Icon(Icons.people_outline, size: 16),
                            label: const Text('সেবাদাতাগণ'),
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (_) => const ProviderListScreen()),
                              );
                            },
                          ),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: ElevatedButton.icon(
                            style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary),
                            icon: const Icon(Icons.dashboard_customize_outlined, size: 16, color: Colors.white),
                            label: const Text('ড্যাশবোর্ড', style: TextStyle(color: Colors.white)),
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (_) => const ProviderDashboardScreen()),
                              );
                            },
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _showPostBottomSheet,
        backgroundColor: AppColors.primary,
        icon: const Icon(Icons.add, color: Colors.white),
        label: Text(
          'আমার পোস্ট',
          style: AppTypography.mediumHeading3.copyWith(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
