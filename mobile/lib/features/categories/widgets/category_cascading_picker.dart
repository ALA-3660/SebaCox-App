/// Searchable Cascading Category & Sub-Category Modal Picker for Flutter.
/// Phase 4C.8 — Master Taxonomy Version 1.0
/// Global Bangla Typography Standard compliant.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/category_model.dart';
import '../repositories/category_repository.dart';

class CategorySelectionResult {
  final CategoryItem category;
  final SubCategoryItem subcategory;

  const CategorySelectionResult({
    required this.category,
    required this.subcategory,
  });
}

class CategoryCascadingPicker extends StatefulWidget {
  final CategoryRepository repository;
  final int? initialCategoryId;
  final int? initialSubcategoryId;
  final String title;

  const CategoryCascadingPicker({
    super.key,
    required this.repository,
    this.initialCategoryId,
    this.initialSubcategoryId,
    this.title = 'ক্যাটাগরি ও সেবা নির্বাচন করুন',
  });

  /// Helper static method to show the picker as a mobile-friendly bottom sheet
  static Future<CategorySelectionResult?> show(
    BuildContext context, {
    required CategoryRepository repository,
    int? initialCategoryId,
    int? initialSubcategoryId,
    String title = 'ক্যাটাগরি ও সেবা নির্বাচন করুন',
  }) {
    return showModalBottomSheet<CategorySelectionResult>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => FractionallySizedBox(
        heightFactor: 0.90,
        child: CategoryCascadingPicker(
          repository: repository,
          initialCategoryId: initialCategoryId,
          initialSubcategoryId: initialSubcategoryId,
          title: title,
        ),
      ),
    );
  }

  @override
  State<CategoryCascadingPicker> createState() => _CategoryCascadingPickerState();
}

class _CategoryCascadingPickerState extends State<CategoryCascadingPicker> {
  // Navigation / Step: 0 = Categories, 1 = Subcategories
  int _currentStep = 0;

  // Data lists
  List<CategoryItem> _allCategories = [];
  List<CategoryItem> _filteredCategories = [];
  List<SubCategoryItem> _subcategories = [];
  List<SubCategoryItem> _filteredSubcategories = [];

  // Selected State
  CategoryItem? _selectedCategory;
  SubCategoryItem? _selectedSubcategory;

  // Search Controllers
  final TextEditingController _categorySearchController = TextEditingController();
  final TextEditingController _subcategorySearchController = TextEditingController();

  // Status flags
  bool _isLoadingCategories = false;
  bool _isLoadingSubcategories = false;
  String? _categoryError;
  String? _subcategoryError;

  @override
  void initState() {
    super.initState();
    _loadCategories();
  }

  @override
  void dispose() {
    _categorySearchController.dispose();
    _subcategorySearchController.dispose();
    super.dispose();
  }

  Future<void> _loadCategories() async {
    setState(() {
      _isLoadingCategories = true;
      _categoryError = null;
    });

    try {
      final cats = await widget.repository.getMainCategories();
      // Sort by backend sort_order
      cats.sort((a, b) => a.sortOrder.compareTo(b.sortOrder));

      if (mounted) {
        setState(() {
          _allCategories = cats;
          _filteredCategories = cats;
          _isLoadingCategories = false;

          // If initial category passed, pre-select it
          if (widget.initialCategoryId != null) {
            try {
              final initialCat = cats.firstWhere((c) => c.id == widget.initialCategoryId);
              _selectCategory(initialCat, autoAdvance: false);
            } catch (_) {}
          }
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoadingCategories = false;
          _categoryError = 'বিভাগগুলো লোড করা যাচ্ছে না।';
        });
      }
    }
  }

  void _filterCategories(String query) {
    final q = query.trim().toLowerCase();
    if (q.isEmpty) {
      setState(() {
        _filteredCategories = _allCategories;
      });
      return;
    }

    setState(() {
      _filteredCategories = _allCategories.where((cat) {
        final matchBn = cat.nameBn.toLowerCase().contains(q);
        final matchEn = cat.nameEn.toLowerCase().contains(q);
        final matchDesc = cat.descriptionBn.toLowerCase().contains(q);
        final matchSlug = cat.slug.toLowerCase().contains(q);
        return matchBn || matchEn || matchDesc || matchSlug;
      }).toList();
    });
  }

  Future<void> _selectCategory(CategoryItem cat, {bool autoAdvance = true}) async {
    setState(() {
      _selectedCategory = cat;
      // CATEGORY CHANGE RULE: Reset subcategory selection
      _selectedSubcategory = null;
      _subcategories = [];
      _filteredSubcategories = [];
      _subcategorySearchController.clear();
      if (autoAdvance) {
        _currentStep = 1;
      }
      _isLoadingSubcategories = true;
      _subcategoryError = null;
    });

    try {
      final subs = await widget.repository.getSubcategories(cat.id);
      // Sort by backend sort_order
      subs.sort((a, b) => a.sortOrder.compareTo(b.sortOrder));

      if (mounted) {
        setState(() {
          _subcategories = subs;
          _filteredSubcategories = subs;
          _isLoadingSubcategories = false;

          // Check if initial subcategory matches
          if (widget.initialSubcategoryId != null) {
            try {
              _selectedSubcategory = subs.firstWhere((s) => s.id == widget.initialSubcategoryId);
            } catch (_) {}
          }
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoadingSubcategories = false;
          _subcategoryError = 'উপ-বিভাগগুলো লোড করা যাচ্ছে না।';
        });
      }
    }
  }

  void _filterSubcategories(String query) {
    final q = query.trim().toLowerCase();
    if (q.isEmpty) {
      setState(() {
        _filteredSubcategories = _subcategories;
      });
      return;
    }

    setState(() {
      _filteredSubcategories = _subcategories.where((sub) {
        final matchBn = sub.nameBn.toLowerCase().contains(q);
        final matchEn = sub.nameEn.toLowerCase().contains(q);
        final matchDesc = sub.shortDescriptionBn.toLowerCase().contains(q);
        final matchSlug = sub.slug.toLowerCase().contains(q);
        return matchBn || matchEn || matchDesc || matchSlug;
      }).toList();
    });
  }

  void _selectSubcategory(SubCategoryItem sub) {
    setState(() {
      _selectedSubcategory = sub;
    });

    if (_selectedCategory != null) {
      Navigator.of(context).pop(
        CategorySelectionResult(
          category: _selectedCategory!,
          subcategory: sub,
        ),
      );
    }
  }

  void _handleBackNavigation() {
    if (_currentStep == 1) {
      setState(() {
        _currentStep = 0;
      });
    } else {
      Navigator.of(context).pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        children: [
          // Drag handle & Header
          _buildHeader(),

          // Main Step Content
          Expanded(
            child: _currentStep == 0 ? _buildCategoryStep() : _buildSubcategoryStep(),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 12),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        border: Border(bottom: BorderSide(color: Color(0xFFF1F5F9))),
      ),
      child: Column(
        children: [
          Center(
            child: Container(
              width: 36,
              height: 4,
              decoration: BoxDecoration(
                color: const Color(0xFFCBD5E1),
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              if (_currentStep == 1)
                IconButton(
                  icon: const Icon(Icons.arrow_back, color: Color(0xFF0F172A)),
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(),
                  onPressed: _handleBackNavigation,
                ),
              if (_currentStep == 1) const SizedBox(width: 8),
              Expanded(
                child: Text(
                  _currentStep == 0 ? widget.title : (_selectedCategory?.nameBn ?? 'সাব-ক্যাটাগরি নির্বাচন'),
                  style: AppTypography.largeHeading3.copyWith(
                    color: const Color(0xFF0F172A),
                    fontSize: 16,
                  ),
                ),
              ),
              IconButton(
                icon: const Icon(Icons.close, color: Color(0xFF64748B), size: 20),
                padding: EdgeInsets.zero,
                constraints: const BoxConstraints(),
                onPressed: () => Navigator.of(context).pop(),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // ==========================================
  // STEP 1: Main Category Selection
  // ==========================================
  Widget _buildCategoryStep() {
    if (_isLoadingCategories) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(color: AppColors.primary),
            const SizedBox(height: 14),
            Text(
              'বিভাগগুলো লোড হচ্ছে...',
              style: AppTypography.bodyRegular.copyWith(color: AppColors.textSecondary),
            ),
          ],
        ),
      );
    }

    if (_categoryError != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 44, color: AppColors.error),
              const SizedBox(height: 12),
              Text(
                _categoryError!,
                textAlign: TextAlign.center,
                style: AppTypography.bodyRegular.copyWith(color: AppColors.error),
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: _loadCategories,
                icon: const Icon(Icons.refresh, size: 18),
                label: Text('আবার চেষ্টা করুন', style: AppTypography.labelMedium.copyWith(color: Colors.white)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
            ],
          ),
        ),
      );
    }

    final popularCategories = _filteredCategories.where((c) => c.isPopular).toList();
    final allOtherCategories = _categorySearchController.text.isEmpty
        ? _filteredCategories.where((c) => !c.isPopular).toList()
        : _filteredCategories;

    return Column(
      children: [
        // Category Search Field
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
          child: TextField(
            controller: _categorySearchController,
            onChanged: _filterCategories,
            style: AppTypography.bodyRegular,
            decoration: InputDecoration(
              hintText: '🔍 Category খুঁজুন (যেমন: নির্মাণ, চিকিৎসা, গাড়ি)...',
              hintStyle: AppTypography.bodyRegular.copyWith(color: const Color(0xFF94A3B8), fontSize: 13),
              filled: true,
              fillColor: const Color(0xFFF8FAFC),
              contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
              ),
              suffixIcon: _categorySearchController.text.isNotEmpty
                  ? IconButton(
                      icon: const Icon(Icons.clear, size: 18, color: Color(0xFF94A3B8)),
                      onPressed: () {
                        _categorySearchController.clear();
                        _filterCategories('');
                      },
                    )
                  : null,
            ),
          ),
        ),

        // Categories List
        Expanded(
          child: _filteredCategories.isEmpty
              ? _buildEmptyView('কোনো বিভাগ পাওয়া যায়নি', 'বানান সঠিক আছে কিনা যাচাই করুন অথবা অন্য শব্দে খুঁজুন।')
              : ListView(
                  padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
                  children: [
                    // Popular Categories Section (if not searching)
                    if (_categorySearchController.text.isEmpty && popularCategories.isNotEmpty) ...[
                      Padding(
                        padding: const EdgeInsets.only(bottom: 8, top: 4),
                        child: Row(
                          children: [
                            const Icon(Icons.star, size: 16, color: Color(0xFFD97706)),
                            const SizedBox(width: 6),
                            Text(
                              'জনপ্রিয় বিভাগ',
                              style: AppTypography.mediumHeading2.copyWith(
                                fontSize: 13,
                                fontWeight: FontWeight.bold,
                                color: const Color(0xFFD97706),
                              ),
                            ),
                          ],
                        ),
                      ),
                      ...popularCategories.map((cat) => _buildCategoryTile(cat, isPopular: true)),
                      const SizedBox(height: 14),
                      Padding(
                        padding: const EdgeInsets.only(bottom: 8),
                        child: Text(
                          'সব বিভাগ (${_allCategories.length}টি)',
                          style: AppTypography.mediumHeading2.copyWith(
                            fontSize: 13,
                            fontWeight: FontWeight.bold,
                            color: const Color(0xFF475569),
                          ),
                        ),
                      ),
                    ],

                    ...allOtherCategories.map((cat) => _buildCategoryTile(cat)),
                  ],
                ),
        ),
      ],
    );
  }

  Widget _buildCategoryTile(CategoryItem cat, {bool isPopular = false}) {
    final isSelected = _selectedCategory?.id == cat.id;

    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      decoration: BoxDecoration(
        color: isSelected ? const Color(0xFFF0FDFA) : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isSelected ? AppColors.primary : const Color(0xFFE2E8F0),
          width: isSelected ? 1.5 : 1,
        ),
      ),
      child: ListTile(
        onTap: () => _selectCategory(cat),
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
        leading: Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: isSelected ? AppColors.primary : const Color(0xFFF1F5F9),
            borderRadius: BorderRadius.circular(10),
          ),
          child: Icon(
            _getCategoryIcon(cat.icon),
            color: isSelected ? Colors.white : AppColors.primary,
            size: 20,
          ),
        ),
        title: Text(
          cat.nameBn,
          style: AppTypography.mediumHeading2.copyWith(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: isSelected ? AppColors.primary : const Color(0xFF0F172A),
          ),
        ),
        subtitle: Text(
          cat.nameEn.isNotEmpty ? cat.nameEn : (cat.descriptionBn.isNotEmpty ? cat.descriptionBn : ''),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: AppTypography.bodySmall.copyWith(
            color: const Color(0xFF64748B),
            fontSize: 11,
          ),
        ),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (cat.activeSubcategoriesCount > 0)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: const Color(0xFFF8FAFC),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFFE2E8F0)),
                ),
                child: Text(
                  '${cat.activeSubcategoriesCount}টি সেবা',
                  style: AppTypography.bodySmall.copyWith(
                    fontSize: 10,
                    color: const Color(0xFF64748B),
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            const SizedBox(width: 4),
            const Icon(Icons.chevron_right, color: Color(0xFF94A3B8), size: 20),
          ],
        ),
      ),
    );
  }

  // ==========================================
  // STEP 2: Sub-category Selection
  // ==========================================
  Widget _buildSubcategoryStep() {
    if (_isLoadingSubcategories) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(color: AppColors.primary),
            const SizedBox(height: 14),
            Text(
              'উপ-বিভাগগুলো লোড হচ্ছে...',
              style: AppTypography.bodyRegular.copyWith(color: AppColors.textSecondary),
            ),
          ],
        ),
      );
    }

    if (_subcategoryError != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 44, color: AppColors.error),
              const SizedBox(height: 12),
              Text(
                _subcategoryError!,
                textAlign: TextAlign.center,
                style: AppTypography.bodyRegular.copyWith(color: AppColors.error),
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: () {
                  if (_selectedCategory != null) {
                    _selectCategory(_selectedCategory!, autoAdvance: false);
                  }
                },
                icon: const Icon(Icons.refresh, size: 18),
                label: Text('আবার চেষ্টা করুন', style: AppTypography.labelMedium.copyWith(color: Colors.white)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
            ],
          ),
        ),
      );
    }

    return Column(
      children: [
        // Selected Category Context Banner
        Container(
          margin: const EdgeInsets.fromLTRB(16, 8, 16, 8),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
          decoration: BoxDecoration(
            color: const Color(0xFFF0FDFA),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: const Color(0xFF99F6E4)),
          ),
          child: Row(
            children: [
              const Icon(Icons.folder_open, color: AppColors.primary, size: 20),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'নির্বাচিত প্রধান ক্যাটাগরি:',
                      style: AppTypography.bodySmall.copyWith(
                        color: const Color(0xFF0F766E),
                        fontSize: 10,
                      ),
                    ),
                    Text(
                      _selectedCategory?.nameBn ?? '',
                      style: AppTypography.mediumHeading2.copyWith(
                        fontSize: 13,
                        fontWeight: FontWeight.bold,
                        color: const Color(0xFF134E4A),
                      ),
                    ),
                  ],
                ),
              ),
              TextButton(
                onPressed: () => setState(() => _currentStep = 0),
                style: TextButton.styleFrom(
                  padding: EdgeInsets.zero,
                  minimumSize: Size.zero,
                  tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                ),
                child: Text(
                  'পরিবর্তন',
                  style: AppTypography.labelSmall.copyWith(
                    color: AppColors.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ),

        // Subcategory Search Field
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
          child: TextField(
            controller: _subcategorySearchController,
            onChanged: _filterSubcategories,
            style: AppTypography.bodyRegular,
            decoration: InputDecoration(
              hintText: '🔍 উপ-বিভাগ খুঁজুন (যেমন: মিস্ত্রি, টাইলস, পেইন্ট)...',
              hintStyle: AppTypography.bodyRegular.copyWith(color: const Color(0xFF94A3B8), fontSize: 13),
              filled: true,
              fillColor: const Color(0xFFF8FAFC),
              contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
              ),
              suffixIcon: _subcategorySearchController.text.isNotEmpty
                  ? IconButton(
                      icon: const Icon(Icons.clear, size: 18, color: Color(0xFF94A3B8)),
                      onPressed: () {
                        _subcategorySearchController.clear();
                        _filterSubcategories('');
                      },
                    )
                  : null,
            ),
          ),
        ),

        // Subcategories List
        Expanded(
          child: _filteredSubcategories.isEmpty
              ? _buildEmptyView('কোনো উপ-বিভাগ পাওয়া যায়নি', 'বানান সঠিক আছে কিনা যাচাই করুন অথবা অন্য শব্দে অনুসন্ধান করুন।')
              : ListView.builder(
                  padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
                  itemCount: _filteredSubcategories.length,
                  itemBuilder: (context, index) {
                    final sub = _filteredSubcategories[index];
                    final isSelected = _selectedSubcategory?.id == sub.id;

                    return Container(
                      margin: const EdgeInsets.only(bottom: 8),
                      decoration: BoxDecoration(
                        color: isSelected ? const Color(0xFFF0FDFA) : Colors.white,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                          color: isSelected ? AppColors.primary : const Color(0xFFE2E8F0),
                          width: isSelected ? 1.5 : 1,
                        ),
                      ),
                      child: ListTile(
                        onTap: () => _selectSubcategory(sub),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
                        leading: Container(
                          width: 36,
                          height: 36,
                          decoration: BoxDecoration(
                            color: isSelected ? AppColors.primary : const Color(0xFFF1F5F9),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Icon(
                            Icons.check_circle_outline,
                            color: isSelected ? Colors.white : const Color(0xFF94A3B8),
                            size: 18,
                          ),
                        ),
                        title: Text(
                          sub.nameBn,
                          style: AppTypography.mediumHeading2.copyWith(
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: isSelected ? AppColors.primary : const Color(0xFF0F172A),
                          ),
                        ),
                        subtitle: sub.nameEn.isNotEmpty
                            ? Text(
                                sub.nameEn,
                                style: AppTypography.bodySmall.copyWith(
                                  color: const Color(0xFF64748B),
                                  fontSize: 11,
                                ),
                              )
                            : null,
                        trailing: isSelected
                            ? const Icon(Icons.check_circle, color: AppColors.primary, size: 22)
                            : const Icon(Icons.chevron_right, color: Color(0xFFCBD5E1), size: 20),
                      ),
                    );
                  },
                ),
        ),
      ],
    );
  }

  Widget _buildEmptyView(String title, String subtitle) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.search_off, size: 44, color: Color(0xFF94A3B8)),
            const SizedBox(height: 12),
            Text(
              title,
              textAlign: TextAlign.center,
              style: AppTypography.mediumHeading2.copyWith(fontSize: 14, color: const Color(0xFF334155)),
            ),
            const SizedBox(height: 4),
            Text(
              subtitle,
              textAlign: TextAlign.center,
              style: AppTypography.bodySmall.copyWith(fontSize: 12, color: const Color(0xFF64748B)),
            ),
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
