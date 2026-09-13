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
        if (_profile!.services.isEmpty)
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(vertical: 32),
              child: Text(
                'এখনো কোনো সেবা যুক্ত করেননি।\nনতুন সেবা যোগ করে কাজ শুরু করুন।',
                style: AppTypography.bodyRegular.copyWith(color: AppColors.textSecondary),
                textAlign: TextAlign.center,
              ),
            ),
          )
        else
          ..._profile!.services.map(
            (s) => Container(
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
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          s.effectiveTitleBn,
                          style: AppTypography.mediumHeading2.copyWith(
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                          ),
                        ),
                        if (s.startingPrice != null)
                          Text(
                            'মূল্য: ৳${s.startingPrice!.toStringAsFixed(0)} (${s.priceType.labelBn})',
                            style: AppTypography.bodySmall.copyWith(color: AppColors.primary),
                          ),
                      ],
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.delete_outline, color: Colors.redAccent, size: 20),
                    onPressed: () async {
                      await _repository.removeProviderService(_profile!.id, s.id);
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
