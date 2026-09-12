/// Expandable Category Tree View widget.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/category_model.dart';

class CategoryTreeView extends StatelessWidget {
  final List<CategoryItem> categories;
  final Function(CategoryItem) onSelectCategory;

  const CategoryTreeView({
    super.key,
    required this.categories,
    required this.onSelectCategory,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      itemCount: categories.length,
      separatorBuilder: (_, __) => const Divider(height: 1, color: AppColors.divider),
      itemBuilder: (context, index) {
        final cat = categories[index];
        return _buildCategoryTile(context, cat);
      },
    );
  }

  Widget _buildCategoryTile(BuildContext context, CategoryItem category) {
    if (category.children.isEmpty) {
      return ListTile(
        title: Text(
          category.nameBn,
          style: AppTypography.mediumHeading4.copyWith(fontSize: 15),
        ),
        subtitle: Text(
          category.nameEn,
          style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
        ),
        trailing: const Icon(Icons.arrow_forward_ios, size: 14, color: AppColors.textTertiary),
        onTap: () => onSelectCategory(category),
      );
    }

    return ExpansionTile(
      leading: Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: AppColors.primarySurface,
          borderRadius: BorderRadius.circular(8),
        ),
        child: const Icon(Icons.folder_outlined, color: AppColors.primary, size: 20),
      ),
      title: Text(
        category.nameBn,
        style: AppTypography.mediumHeading3.copyWith(fontSize: 16),
      ),
      subtitle: Text(
        '${category.nameEn} • ${category.children.length}টি সাব-ক্যাটাগরি',
        style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
      ),
      children: category.children.map((child) {
        return Container(
          color: AppColors.backgroundSecondary.withOpacity(0.5),
          child: ListTile(
            contentPadding: const EdgeInsets.only(left: 48, right: 16),
            title: Text(
              child.nameBn,
              style: AppTypography.mediumHeading4.copyWith(fontSize: 14),
            ),
            subtitle: Text(
              child.nameEn,
              style: AppTypography.bodySmall.copyWith(fontSize: 11),
            ),
            trailing: const Icon(Icons.chevron_right, size: 18, color: AppColors.textTertiary),
            onTap: () => onSelectCategory(child),
          ),
        );
      }).toList(),
    );
  }
}
