/// Provider Card Widget for SebaCox.
/// Global Bangla Typography Standard compliant:
/// - Hind Siliguri (Main Heading)
/// - Baloo Da 2 (Medium Heading / Badges)
/// - Tiro Bangla (Body / Helper text)
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/provider_model.dart';
import 'availability_badge.dart';
import 'verification_badge.dart';

class ProviderCard extends StatelessWidget {
  final ProviderProfile provider;
  final VoidCallback? onTap;

  const ProviderCard({
    super.key,
    required this.provider,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: provider.isFeatured ? AppColors.primary.withOpacity(0.35) : AppColors.border,
          width: provider.isFeatured ? 1.5 : 1.0,
        ),
      ),
      color: Colors.white,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header: Avatar, Name, Type, and Badges
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Avatar
                  Container(
                    width: 48,
                    height: 48,
                    decoration: BoxDecoration(
                      color: AppColors.primary.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Center(
                      child: Text(
                        provider.displayNameBn.isNotEmpty ? provider.displayNameBn[0] : 'S',
                        style: AppTypography.largeHeading2.copyWith(
                          color: AppColors.primary,
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),

                  // Name & Sub-details
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: Text(
                                provider.displayNameBn,
                                style: AppTypography.mediumHeading1.copyWith(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.textPrimary,
                                ),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            if (provider.isFeatured) ...[
                              const SizedBox(width: 4),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: const Color(0xFFFEF3C7),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Text(
                                  'ফিচার্ড',
                                  style: AppTypography.mediumHeading3.copyWith(
                                    fontSize: 9,
                                    color: const Color(0xFFB45309),
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ],
                          ],
                        ),
                        const SizedBox(height: 2),
                        Text(
                          provider.providerType.labelBn,
                          style: AppTypography.bodySmall.copyWith(
                            color: AppColors.textSecondary,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 12),

              // Badges: Verification & Availability
              Row(
                children: [
                  AvailabilityBadge(status: provider.availabilityStatus),
                  const SizedBox(width: 8),
                  VerificationBadge(
                    status: provider.verificationStatus,
                    isVerified: provider.isVerified,
                  ),
                ],
              ),

              if (provider.shortDescriptionBn.isNotEmpty) ...[
                const SizedBox(height: 10),
                Text(
                  provider.shortDescriptionBn,
                  style: AppTypography.bodyRegular.copyWith(
                    color: AppColors.textSecondary,
                    fontSize: 13,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],

              const SizedBox(height: 12),
              const Divider(height: 1, color: AppColors.border),
              const SizedBox(height: 10),

              // Footer: Service areas & Services summary
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Service area indicator
                  Expanded(
                    child: Row(
                      children: [
                        const Icon(
                          Icons.location_on_outlined,
                          size: 14,
                          color: AppColors.primary,
                        ),
                        const SizedBox(width: 4),
                        Expanded(
                          child: Text(
                            provider.serviceAreas.isNotEmpty
                                ? provider.serviceAreas.first.displayNameBn
                                : 'কক্সবাজার জেলা',
                            style: AppTypography.bodySmall.copyWith(
                              fontSize: 12,
                              color: AppColors.textSecondary,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Services count
                  Text(
                    '${provider.servicesCount}টি সেবা',
                    style: AppTypography.mediumHeading3.copyWith(
                      fontSize: 12,
                      color: AppColors.primary,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
