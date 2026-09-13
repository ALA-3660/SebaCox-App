/// Provider List / Discovery Screen for SebaCox.
/// Enables searching, filtering by service and upazila, and viewing provider profiles.
/// Global Bangla Typography Standard compliant.
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/provider_model.dart';
import '../repositories/provider_repository.dart';
import '../widgets/provider_card.dart';
import 'provider_profile_screen.dart';

class ProviderListScreen extends StatefulWidget {
  final int? initialServiceId;
  final int? initialUpazilaId;
  final String? initialCategoryTitle;

  const ProviderListScreen({
    super.key,
    this.initialServiceId,
    this.initialUpazilaId,
    this.initialCategoryTitle,
  });

  @override
  State<ProviderListScreen> createState() => _ProviderListScreenState();
}

class _ProviderListScreenState extends State<ProviderListScreen> {
  final _repository = ProviderRepository();
  final _searchController = TextEditingController();

  List<ProviderProfile> _providers = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchProviders();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _fetchProviders() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final res = await _repository.getProviders(
      query: _searchController.text.trim().isNotEmpty ? _searchController.text.trim() : null,
      serviceId: widget.initialServiceId,
      upazilaId: widget.initialUpazilaId,
    );

    setState(() {
      _isLoading = false;
      if (res.isSuccess && res.data != null) {
        _providers = res.data!;
      } else {
        _errorMessage = res.message ?? 'সেবাদাতাদের তালিকা লোড করা যায়নি';
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(
          widget.initialCategoryTitle ?? 'সেবাদাতাগণ',
          style: AppTypography.mediumHeading2.copyWith(
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        backgroundColor: AppColors.primary,
        elevation: 0,
      ),
      body: Column(
        children: [
          // Search Header
          Container(
            color: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: TextField(
              controller: _searchController,
              onSubmitted: (_) => _fetchProviders(),
              decoration: InputDecoration(
                hintText: 'সেবাদাতা বা সেবা খুঁজুন...',
                prefixIcon: const Icon(Icons.search, color: AppColors.textSecondary),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _searchController.clear();
                          _fetchProviders();
                        },
                      )
                    : null,
                contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
                filled: true,
                fillColor: AppColors.background,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppColors.border),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: AppColors.border),
                ),
              ),
            ),
          ),

          // Provider List
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _errorMessage != null
                    ? Center(
                        child: Text(
                          _errorMessage!,
                          style: AppTypography.bodyRegular,
                        ),
                      )
                    : _providers.isEmpty
                        ? Center(
                            child: Padding(
                              padding: const EdgeInsets.all(24),
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const Icon(
                                    Icons.person_search_outlined,
                                    size: 56,
                                    color: AppColors.textSecondary,
                                  ),
                                  const SizedBox(height: 12),
                                  Text(
                                    'কোনো সেবাদাতা পাওয়া যায়নি',
                                    style: AppTypography.mediumHeading2.copyWith(
                                      fontWeight: FontWeight.bold,
                                      color: AppColors.textPrimary,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    'অনুগ্রহ করে অন্য শব্দ বা সেবা দিয়ে অনুসন্ধান করুন।',
                                    style: AppTypography.bodySmall.copyWith(
                                      color: AppColors.textSecondary,
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                                ],
                              ),
                            ),
                          )
                        : ListView.builder(
                            padding: const EdgeInsets.all(16),
                            itemCount: _providers.length,
                            itemBuilder: (context, index) {
                              final provider = _providers[index];
                              return ProviderCard(
                                provider: provider,
                                onTap: () {
                                  Navigator.of(context).push(
                                    MaterialPageRoute(
                                      builder: (_) => ProviderProfileScreen(provider: provider),
                                    ),
                                  );
                                },
                              );
                            },
                          ),
          ),
        ],
      ),
    );
  }
}
