/// Reusable Category Selector Card Component.
/// Launches the Searchable Cascading Category Picker BottomSheet.
/// Global Bangla Typography Standard compliant.
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/category_model.dart';
import '../repositories/category_repository.dart';
import 'category_cascading_picker.dart';

class CategorySelectorCard extends StatelessWidget {
  final CategoryRepository repository;
  final int? selectedCategoryId;
  final String? selectedCategoryNameBn;
  final int? selectedSubcategoryId;
  final String? selectedSubcategoryNameBn;
  final ValueChanged<CategorySelectionResult> onSelected;
  final VoidCallback? onReset;
  final String label;
  final String hint;

  const CategorySelectorCard({
    super.key,
    required this.repository,
    this.selectedCategoryId,
    this.selectedCategoryNameBn,
    this.selectedSubcategoryId,
    this.selectedSubcategoryNameBn,
    required this.onSelected,
    this.onReset,
    this.label = 'ক্যাটাগরি ও সেবা *',
    this.hint = 'ক্যাটাগরি ও সাব-ক্যাটাগরি নির্বাচন করুন',
  });

  Future<void> _openPicker(BuildContext context) async {
    final result = await CategoryCascadingPicker.show(
      context,
      repository: repository,
      initialCategoryId: selectedCategoryId,
      initialSubcategoryId: selectedSubcategoryId,
      title: label,
    );

    if (result != null) {
      onSelected(result);
    }
  }

  @override
  Widget build(BuildContext context) {
    final bool hasSelection = selectedCategoryId != null && selectedSubcategoryId != null;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: AppTypography.mediumHeading2.copyWith(
                fontWeight: FontWeight.bold,
                fontSize: 13,
                color: const Color(0xFF334155),
              ),
            ),
            if (hasSelection && onReset != null)
              GestureDetector(
                onTap: onReset,
                child: Text(
                  'রিসেট',
                  style: AppTypography.labelSmall.copyWith(
                    color: const Color(0xFFDC2626),
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
          ],
        ),
        const SizedBox(height: 8),

        InkWell(
          onTap: () => _openPicker(context),
          borderRadius: BorderRadius.circular(12),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            decoration: BoxDecoration(
              color: hasSelection ? const Color(0xFFF0FDFA) : Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: hasSelection ? AppColors.primary : const Color(0xFFCBD5E1),
                width: hasSelection ? 1.5 : 1,
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.02),
                  blurRadius: 4,
                  offset: const Offset(0, 1),
                ),
              ],
            ),
            child: Row(
              children: [
                Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    color: hasSelection ? AppColors.primary : const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    hasSelection ? Icons.check_circle_outline : Icons.search,
                    color: hasSelection ? Colors.white : const Color(0xFF64748B),
                    size: 20,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: hasSelection
                      ? Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              selectedCategoryNameBn ?? 'প্রধান ক্যাটাগরি',
                              style: AppTypography.bodySmall.copyWith(
                                color: const Color(0xFF0F766E),
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            Text(
                              selectedSubcategoryNameBn ?? 'সাব-ক্যাটাগরি',
                              style: AppTypography.mediumHeading2.copyWith(
                                fontSize: 14,
                                fontWeight: FontWeight.bold,
                                color: const Color(0xFF0F172A),
                              ),
                            ),
                          ],
                        )
                      : Text(
                          hint,
                          style: AppTypography.bodyRegular.copyWith(
                            color: const Color(0xFF94A3B8),
                            fontSize: 13,
                          ),
                        ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                  decoration: BoxDecoration(
                    color: hasSelection ? Colors.white : const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: hasSelection ? const Color(0xFF99F6E4) : const Color(0xFFE2E8F0),
                    ),
                  ),
                  child: Text(
                    hasSelection ? 'পরিবর্তন' : 'বাছাই করুন',
                    style: AppTypography.labelSmall.copyWith(
                      color: hasSelection ? AppColors.primary : const Color(0xFF64748B),
                      fontWeight: FontWeight.bold,
                      fontSize: 11,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
