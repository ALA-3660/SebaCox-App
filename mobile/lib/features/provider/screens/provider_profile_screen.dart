/// Provider Profile Screen for SebaCox.
/// Public details view of a service provider.
/// Global Bangla Typography Standard compliant.
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/provider_model.dart';
import '../models/provider_service_model.dart';
import '../widgets/availability_badge.dart';
import '../widgets/verification_badge.dart';

class ProviderProfileScreen extends StatelessWidget {
  final ProviderProfile provider;

  const ProviderProfileScreen({
    super.key,
    required this.provider,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(
          'সেবাদাতার প্রোফাইল',
          style: AppTypography.mediumHeading2.copyWith(
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        backgroundColor: AppColors.primary,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Top Banner & Info
            Container(
              width: double.infinity,
              color: Colors.white,
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  // Avatar
                  Container(
                    width: 72,
                    height: 72,
                    decoration: BoxDecoration(
                      color: AppColors.primary.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Center(
                      child: Text(
                        provider.displayNameBn.isNotEmpty ? provider.displayNameBn[0] : 'S',
                        style: AppTypography.largeHeading1.copyWith(
                          color: AppColors.primary,
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Name
                  Text(
                    provider.displayNameBn,
                    style: AppTypography.largeHeading2.copyWith(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimary,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 4),

                  // Provider Type
                  Text(
                    provider.providerType.labelBn,
                    style: AppTypography.bodySmall.copyWith(
                      color: AppColors.textSecondary,
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Badges
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      AvailabilityBadge(status: provider.availabilityStatus),
                      const SizedBox(width: 8),
                      VerificationBadge(
                        status: provider.verificationStatus,
                        isVerified: provider.isVerified,
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(height: 12),

            // Short bio & description
            if (provider.descriptionBn.isNotEmpty || provider.shortDescriptionBn.isNotEmpty) ...[
              Container(
                width: double.infinity,
                color: Colors.white,
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'পরিচিতি ও বিবরণ',
                      style: AppTypography.mediumHeading2.copyWith(
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      provider.descriptionBn.isNotEmpty
                          ? provider.descriptionBn
                          : provider.shortDescriptionBn,
                      style: AppTypography.bodyRegular.copyWith(
                        color: AppColors.textSecondary,
                        height: 1.5,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 12),
            ],

            // Services Offered
            Container(
              width: double.infinity,
              color: Colors.white,
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'প্রদত্ত সেবাসমূহ',
                        style: AppTypography.mediumHeading2.copyWith(
                          fontWeight: FontWeight.bold,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      Text(
                        '${provider.services.length}টি সেবা',
                        style: AppTypography.mediumHeading3.copyWith(
                          color: AppColors.primary,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  if (provider.services.isEmpty)
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      child: Center(
                        child: Text(
                          'এখনো কোনো সেবা যুক্ত করা হয়নি',
                          style: AppTypography.bodySmall.copyWith(
                            color: AppColors.textSecondary,
                          ),
                        ),
                      ),
                    )
                  else
                    ...provider.services.map((service) => _buildServiceItem(service)),
                ],
              ),
            ),

            const SizedBox(height: 12),

            // Service Area Coverage
            Container(
              width: double.infinity,
              color: Colors.white,
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'সেবা প্রদানের এলাকা',
                    style: AppTypography.mediumHeading2.copyWith(
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 12),
                  if (provider.serviceAreas.isEmpty)
                    Text(
                      'সমগ্র কক্সবাজার জেলা',
                      style: AppTypography.bodyRegular.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    )
                  else
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: provider.serviceAreas.map((area) {
                        return Chip(
                          avatar: const Icon(Icons.location_pin, size: 14, color: AppColors.primary),
                          label: Text(
                            area.displayNameBn,
                            style: AppTypography.mediumHeading3.copyWith(
                              fontSize: 12,
                              color: AppColors.textPrimary,
                            ),
                          ),
                          backgroundColor: AppColors.background,
                          side: const BorderSide(color: AppColors.border),
                        );
                      }).toList(),
                    ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Contact Action Button (Safe Contact Display)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton.icon(
                  onPressed: () {
                    // Contact action
                  },
                  icon: const Icon(Icons.phone, size: 18),
                  label: Text(
                    'যোগাযোগ: ${provider.safeContactPhone ?? "লগইন করে দেখুন"}',
                    style: AppTypography.mediumHeading2.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  Widget _buildServiceItem(ProviderServiceItem service) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.background,
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
                  service.effectiveTitleBn,
                  style: AppTypography.mediumHeading2.copyWith(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textPrimary,
                  ),
                ),
                if (service.descriptionBn.isNotEmpty) ...[
                  const SizedBox(height: 2),
                  Text(
                    service.descriptionBn,
                    style: AppTypography.bodySmall.copyWith(
                      color: AppColors.textSecondary,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ],
            ),
          ),
          if (service.startingPrice != null) ...[
            const SizedBox(width: 8),
            Text(
              '৳${service.startingPrice!.toStringAsFixed(0)}',
              style: AppTypography.mediumHeading2.copyWith(
                fontSize: 14,
                color: AppColors.primary,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ],
      ),
    );
  }
}
