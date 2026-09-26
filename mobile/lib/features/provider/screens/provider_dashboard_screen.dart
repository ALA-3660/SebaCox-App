/// Provider Personal Dashboard for SebaCox.
/// Manages Provider's own profile, services, areas, and availability state.
/// Global Bangla Typography Standard compliant.
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/provider_model.dart';
import '../models/provider_enums.dart';
import '../models/provider_service_model.dart';
import '../models/provider_service_area_model.dart';
import '../repositories/provider_repository.dart';
import '../widgets/availability_badge.dart';
import '../widgets/verification_badge.dart';
import '../widgets/service_configuration_dialog.dart';
import 'provider_profile_screen.dart';

class ProviderDashboardScreen extends StatefulWidget {
  const ProviderDashboardScreen({super.key});

  @override
  State<ProviderDashboardScreen> createState() => _ProviderDashboardScreenState();
}

class _ProviderDashboardScreenState extends State<ProviderDashboardScreen> with SingleTickerProviderStateMixin {
  final _repository = ProviderRepository();
  late TabController _tabController;
  ProviderProfile? _profile;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadProfile();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadProfile() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final res = await _repository.getMyProviderProfile();
    setState(() {
      _isLoading = false;
      if (res.isSuccess && res.data != null) {
        _profile = res.data;
      } else {
        _errorMessage = res.message ?? 'প্রোফাইল লোড করা যায়নি';
      }
    });
  }

  Future<void> _changeAvailability(AvailabilityStatus newStatus) async {
    if (_profile == null) return;
    final res = await _repository.updateAvailability(_profile!.id, newStatus.value);
    if (res.isSuccess) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('উপলব্ধতা পরিবর্তিত হয়ে "${newStatus.labelBn}" হয়েছে')),
      );
      _loadProfile();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(
          'সেবাদাতা ড্যাশবোর্ড',
          style: AppTypography.mediumHeading2.copyWith(
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        backgroundColor: AppColors.primary,
        elevation: 0,
        actions: [
          if (_profile != null)
            IconButton(
              icon: const Icon(Icons.visibility_outlined, color: Colors.white),
              tooltip: 'পাবলিক ভিউ দেখুন',
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => ProviderProfileScreen(provider: _profile!),
                  ),
                );
              },
            ),
        ],
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.white,
          labelStyle: AppTypography.mediumHeading3.copyWith(fontWeight: FontWeight.bold),
          unselectedLabelStyle: AppTypography.mediumHeading3,
          tabs: const [
            Tab(text: 'সারসংক্ষেপ'),
            Tab(text: 'আমার সেবা'),
            Tab(text: 'সেবা এলাকা'),
          ],
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _errorMessage != null
              ? _buildErrorView()
              : TabBarView(
                  controller: _tabController,
                  children: [
                    _buildOverviewTab(),
                    _buildServicesTab(),
                    _buildAreasTab(),
                  ],
                ),
    );
  }

  Widget _buildErrorView() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.info_outline, size: 48, color: AppColors.textSecondary),
            const SizedBox(height: 16),
            Text(
              _errorMessage ?? 'কোনো সেবাদাতা প্রোফাইল পাওয়া যায়নি',
              style: AppTypography.bodyRegular,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loadProfile,
              style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary),
              child: const Text('পুনরায় চেষ্টা করুন'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOverviewTab() {
    if (_profile == null) return const SizedBox.shrink();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header Card
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.Border.all(color: AppColors.border),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        _profile!.displayNameBn,
                        style: AppTypography.largeHeading2.copyWith(
                          fontWeight: FontWeight.bold,
                          color: AppColors.textPrimary,
                        ),
                      ),
                    ),
                    VerificationBadge(
                      status: _profile!.verificationStatus,
                      isVerified: _profile!.isVerified,
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  _profile!.providerType.labelBn,
                  style: AppTypography.bodySmall.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Text(
                      'বর্তমান স্ট্যাটাস: ',
                      style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
                    ),
                    Text(
                      _profile!.status.labelBn,
                      style: AppTypography.mediumHeading3.copyWith(
                        fontWeight: FontWeight.bold,
                        color: _profile!.status == ProviderStatus.active
                            ? const Color(0xFF10B981)
                            : const Color(0xFFF59E0B),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // Availability Controller
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.Border.all(color: AppColors.border),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'কাজের উপলব্ধতা (Availability)',
                      style: AppTypography.mediumHeading2.copyWith(
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    AvailabilityBadge(status: _profile!.availabilityStatus),
                  ],
                ),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: AvailabilityStatus.values.map((status) {
                    final isCurrent = _profile!.availabilityStatus == status;
                    return ChoiceChip(
                      label: Text(
                        status.labelBn,
                        style: AppTypography.mediumHeading3.copyWith(
                          fontSize: 12,
                          color: isCurrent ? Colors.white : AppColors.textPrimary,
                        ),
                      ),
                      selected: isCurrent,
                      selectedColor: AppColors.primary,
                      backgroundColor: AppColors.background,
                      onSelected: (selected) {
                        if (selected) _changeAvailability(status);
                      },
                    );
                  }).toList(),
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // Metrics row
          Row(
            children: [
              Expanded(
                child: _buildMetricTile(
                  'মোট সেবা',
                  '${_profile!.services.length}',
                  Icons.miscellaneous_services_outlined,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildMetricTile(
                  'সেবা এলাকা',
                  '${_profile!.serviceAreas.length}',
                  Icons.location_city_outlined,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMetricTile(String label, String value, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: AppColors.primary, size: 24),
          const SizedBox(height: 8),
          Text(
            value,
            style: AppTypography.largeHeading1.copyWith(
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
              fontSize: 24,
            ),
          ),
          Text(
            label,
            style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
          ),
        ],
      ),
    );
  }

  Widget _buildServicesTab() {
    if (_profile == null) return const SizedBox.shrink();

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Add Service Action Header
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: AppColors.border),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'প্রদত্ত সেবাসমূহ (${_profile!.services.length})',
                    style: AppTypography.mediumHeading2.copyWith(
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  Text(
                    'মাস্টার ট্যাক্সোনমি অনুযায়ী আপনার সেবা ও রেট কনফিগার করুন',
                    style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
                  ),
                ],
              ),
              ElevatedButton.icon(
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (ctx) => ServiceConfigurationDialog(
                      providerId: _profile!.id,
                      onSave: (payload) async {
                        final res = await _repository.addProviderService(_profile!.id, payload);
                        if (res.isSuccess) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('সেবা সফলভাবে যুক্ত হয়েছে')),
                          );
                          _loadProfile();
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text(res.message ?? 'সেবা যোগ করা সম্ভব হয়নি')),
                          );
                        }
                      },
                    ),
                  );
                },
                icon: const Icon(Icons.add, size: 18),
                label: const Text('নতুন সেবা'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 14),

        if (_profile!.services.isEmpty)
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(vertical: 48),
              child: Column(
                children: [
                  const Icon(Icons.miscellaneous_services_outlined, size: 48, color: AppColors.textSecondary),
                  const SizedBox(height: 12),
                  Text(
                    'এখনো কোনো সেবা যুক্ত করেননি।\n"নতুন সেবা" বাটনে চাপ দিয়ে আপনার দক্ষতা ও সেবা কনফিগার করুন।',
                    style: AppTypography.bodyRegular.copyWith(color: AppColors.textSecondary),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          )
        else
          ..._profile!.services.map(
            (s) => Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: AppColors.border),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.03),
                    blurRadius: 6,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Title & Action Icons
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: AppColors.primary.withValues(alpha: 0.08),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: const Icon(Icons.build_circle_outlined, color: AppColors.primary, size: 24),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              s.effectiveTitleBn,
                              style: AppTypography.mediumHeading2.copyWith(
                                fontWeight: FontWeight.bold,
                                color: AppColors.textPrimary,
                                fontSize: 16,
                              ),
                            ),
                            if (s.categoryNameBn != null)
                              Text(
                                s.categoryNameBn!,
                                style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
                              ),
                          ],
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.delete_outline, color: Colors.redAccent, size: 20),
                        tooltip: 'সেবা বাতিল করুন',
                        onPressed: () async {
                          final confirm = await showDialog<bool>(
                            context: context,
                            builder: (ctx) => AlertDialog(
                              title: Text('সেবা অপসারণ', style: AppTypography.mediumHeading2),
                              content: Text(
                                'আপনি কি নিশ্চিতভাবে "${s.effectiveTitleBn}" সেবাটি তালিকা থেকে মুছে ফেলতে চান?',
                                style: AppTypography.bodyRegular,
                              ),
                              actions: [
                                TextButton(
                                  onPressed: () => Navigator.of(ctx).pop(false),
                                  child: const Text('না'),
                                ),
                                ElevatedButton(
                                  onPressed: () => Navigator.of(ctx).pop(true),
                                  style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                                  child: const Text('হ্যাঁ, মুছে ফেলুন'),
                                ),
                              ],
                            ),
                          );

                          if (confirm == true) {
                            await _repository.removeProviderService(_profile!.id, s.id);
                            _loadProfile();
                          }
                        },
                      ),
                    ],
                  ),

                  // Description if provided
                  if (s.descriptionBn.isNotEmpty) ...[
                    const SizedBox(height: 10),
                    Text(
                      s.descriptionBn,
                      style: AppTypography.bodySmall.copyWith(color: AppColors.textPrimary),
                    ),
                  ],

                  const SizedBox(height: 12),

                  // Badges (Pricing, Emergency, Warranty)
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      // Price Badge
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: AppColors.primary.withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.payments_outlined, size: 14, color: AppColors.primary),
                            const SizedBox(width: 4),
                            Text(
                              s.formattedPriceString,
                              style: AppTypography.bodySmall.copyWith(
                                fontWeight: FontWeight.bold,
                                color: AppColors.primary,
                              ),
                            ),
                          ],
                        ),
                      ),

                      // Emergency Badge
                      if (s.isEmergencyAvailable)
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFEF2F2),
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: const Color(0xFFFCA5A5)),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const Icon(Icons.flash_on, size: 14, color: Color(0xFFDC2626)),
                              const SizedBox(width: 4),
                              Text(
                                s.emergencyFee != null
                                    ? 'জরুরি সেবা (+৳${s.emergencyFee!.toStringAsFixed(0)})'
                                    : 'জরুরি সেবা উপলব্ধ',
                                style: AppTypography.bodySmall.copyWith(
                                  fontWeight: FontWeight.bold,
                                  color: const Color(0xFFDC2626),
                                ),
                              ),
                            ],
                          ),
                        ),

                      // Warranty Badge
                      if (s.warrantyTextBn.isNotEmpty)
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: const Color(0xFFECFDF5),
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: const Color(0xFFA7F3D0)),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const Icon(Icons.verified_user_outlined, size: 14, color: Color(0xFF059669)),
                              const SizedBox(width: 4),
                              Text(
                                s.warrantyTextBn,
                                style: AppTypography.bodySmall.copyWith(
                                  fontWeight: FontWeight.bold,
                                  color: const Color(0xFF059669),
                                ),
                              ),
                            ],
                          ),
                        ),
                    ],
                  ),

                  // Skills tag chips
                  if (s.skills.isNotEmpty) ...[
                    const SizedBox(height: 10),
                    Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: s.skills.map((skill) {
                        return Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.background,
                            borderRadius: BorderRadius.circular(6),
                            border: Border.Border.all(color: AppColors.border),
                          ),
                          child: Text(
                            skill,
                            style: AppTypography.bodySmall.copyWith(
                              fontSize: 11,
                              color: AppColors.textSecondary,
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ],
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildAreasTab() {
    if (_profile == null) return const SizedBox.shrink();

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        if (_profile!.serviceAreas.isEmpty)
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(vertical: 32),
              child: Text(
                'কোনো নির্দিষ্ট এলাকা নির্ধারিত নেই।\nডিফল্ট হিসেবে সমগ্র জেলা গণ্য হবে।',
                style: AppTypography.bodyRegular.copyWith(color: AppColors.textSecondary),
                textAlign: TextAlign.center,
              ),
            ),
          )
        else
          ..._profile!.serviceAreas.map(
            (a) => Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.Border.all(color: AppColors.border),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.location_pin, color: AppColors.primary, size: 18),
                      const SizedBox(width: 8),
                      Text(
                        a.displayNameBn,
                        style: AppTypography.mediumHeading2.copyWith(
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                    ],
                  ),
                  IconButton(
                    icon: const Icon(Icons.delete_outline, color: Colors.redAccent, size: 20),
                    onPressed: () async {
                      await _repository.removeProviderServiceArea(_profile!.id, a.id);
                      _loadProfile();
                    },
                  ),
                ],
              ),
            ),
          ),
      ],
    );
  }
}
