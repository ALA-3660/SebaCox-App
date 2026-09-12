/// Category Card Widget with Global Bangla Typography Standard.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/category_model.dart';

class CategoryCard extends StatelessWidget {
  final CategoryItem category;
  final VoidCallback onTap;
  final bool isCompact;

  const CategoryCard({
    super.key,
    required this.category,
    required this.onTap,
    this.isCompact = false,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: EdgeInsets.all(isCompact ? 10 : 14),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.divider, width: 1),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.03),
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Category Icon with Circle
            Container(
              width: isCompact ? 36 : 46,
              height: isCompact ? 36 : 46,
              decoration: BoxDecoration(
                color: AppColors.primarySurface,
                shape: BoxShape.circle,
              ),
              child: Icon(
                _getCategoryIcon(category.icon),
                color: AppColors.primary,
                size: isCompact ? 18 : 22,
              ),
            ),
            const SizedBox(height: 8),

            // Category Name (Medium Heading -> Baloo Da 2)
            Text(
              category.nameBn,
              textAlign: TextAlign.center,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: isCompact
                  ? AppTypography.mediumHeading4.copyWith(fontSize: 13)
                  : AppTypography.mediumHeading3.copyWith(fontSize: 15),
            ),

            if (!isCompact && category.activeServicesCount > 0) ...[
              const SizedBox(height: 4),
              // Service count label (Body text -> Tiro Bangla)
              Text(
                '${category.activeServicesCount}টি সেবা',
                style: AppTypography.bodySmall.copyWith(
                  color: AppColors.textSecondary,
                  fontSize: 11,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  IconData _getCategoryIcon(String icon) {
    switch (icon) {
      case 'activity':
      case 'heart':
        return Icons.local_hospital_outlined;
      case 'home':
        return Icons.hotel_outlined;
      case 'coffee':
        return Icons.restaurant_outlined;
      case 'compass':
        return Icons.travel_explore_outlined;
      case 'ticket':
        return Icons.confirmation_number_outlined;
      case 'truck':
        return Icons.local_shipping_outlined;
      case 'tool':
        return Icons.build_outlined;
      case 'wrench':
        return Icons.handyman_outlined;
      case 'book':
        return Icons.school_outlined;
      case 'user-check':
        return Icons.work_outline;
      case 'sun':
        return Icons.agriculture_outlined;
      case 'anchor':
        return Icons.phishing_outlined;
      case 'shopping-cart':
      case 'shopping-bag':
        return Icons.storefront_outlined;
      case 'map':
        return Icons.landscape_outlined;
      case 'award':
        return Icons.gavel_outlined;
      case 'dollar-sign':
      case 'credit-card':
        return Icons.account_balance_outlined;
      case 'monitor':
        return Icons.computer_outlined;
      case 'alert-triangle':
        return Icons.warning_amber_rounded;
      default:
        return Icons.grid_view_rounded;
    }
  }
}
