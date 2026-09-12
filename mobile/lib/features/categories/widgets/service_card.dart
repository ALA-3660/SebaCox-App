/// Service Card Widget with Capability Matrix Badges & Bangla Typography.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/service_model.dart';

class ServiceCard extends StatelessWidget {
  final ServiceItem service;
  final VoidCallback onTap;

  const ServiceCard({
    super.key,
    required this.service,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: const BorderSide(color: AppColors.divider, width: 1),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Service Type Icon badge
                  Container(
                    width: 42,
                    height: 42,
                    decoration: BoxDecoration(
                      color: AppColors.primarySurface,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Icon(
                      _getServiceTypeIcon(service.serviceType),
                      color: AppColors.primary,
                      size: 22,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Service Name (Medium Heading -> Baloo Da 2)
                        Text(
                          service.nameBn,
                          style: AppTypography.mediumHeading3.copyWith(
                            fontSize: 16,
                            color: AppColors.textPrimary,
                          ),
                        ),
                        const SizedBox(height: 2),
                        // Category context (Body Small -> Tiro Bangla)
                        Text(
                          service.categoryNameBn.isNotEmpty
                              ? service.categoryNameBn
                              : service.nameEn,
                          style: AppTypography.bodySmall.copyWith(
                            color: AppColors.primary,
                            fontWeight: FontWeight.w600,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Icon(
                    Icons.chevron_right,
                    color: AppColors.textTertiary,
                    size: 20,
                  ),
                ],
              ),

              if (service.shortDescriptionBn.isNotEmpty) ...[
                const SizedBox(height: 8),
                // Short Description (Body Medium -> Tiro Bangla)
                Text(
                  service.shortDescriptionBn,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: AppTypography.bodyMedium.copyWith(
                    color: AppColors.textSecondary,
                    fontSize: 13,
                    height: 1.4,
                  ),
                ),
              ],

              const SizedBox(height: 10),
              // Capability Badges
              Wrap(
                spacing: 6,
                runSpacing: 4,
                children: service.capabilityBadges.map((badge) {
                  return Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                    decoration: BoxDecoration(
                      color: AppColors.backgroundSecondary,
                      borderRadius: BorderRadius.circular(6),
                      border: Border.all(color: AppColors.divider, width: 0.8),
                    ),
                    child: Text(
                      badge,
                      style: AppTypography.labelSmall.copyWith(
                        color: AppColors.textPrimary,
                        fontSize: 11,
                      ),
                    ),
                  );
                }).toList(),
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getServiceTypeIcon(String type) {
    switch (type) {
      case 'BOOKING':
        return Icons.event_available_outlined;
      case 'PRODUCT':
        return Icons.inventory_2_outlined;
      case 'RENTAL':
        return Icons.key_outlined;
      case 'DIGITAL_SERVICE':
        return Icons.devices_outlined;
      case 'MARKETPLACE':
        return Icons.storefront_outlined;
      case 'INFORMATION':
        return Icons.info_outline;
      default:
        return Icons.handyman_outlined;
    }
  }
}
