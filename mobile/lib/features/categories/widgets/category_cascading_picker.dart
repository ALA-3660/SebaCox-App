/// Searchable Cascading Category & Sub-Category Modal Picker for Flutter.
/// Phase 4E — Intent-Guided Taxonomy Discovery & Search Alias UX.
/// Global Bangla Typography Standard compliant:
/// - Hind Siliguri: Large Headings / Modal Titles
/// - Baloo Da 2: Sub-headings, Tabs, Badges & Interactive Chips
/// - Tiro Bangla: Body Text, Helper Text & Labels
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
/// "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/category_model.dart';
import '../models/user_intent.dart';
import '../repositories/category_repository.dart';

class CategorySelectionResult {
  final CategoryItem category;
  final SubCategoryItem subcategory;
  final UserIntent? intent;
  final String? matchedAlias;

  const CategorySelectionResult({
    required this.category,
    required this.subcategory,
    this.intent,
    this.matchedAlias,
  });
}

class CategoryCascadingPicker extends StatefulWidget {
  final CategoryRepository repository;
  final int? initialCategoryId;
  final int? initialSubcategoryId;
  final String? initialIntentCode;
  final String title;

  const CategoryCascadingPicker({
    super.key,
    required this.repository,
    this.initialCategoryId,
    this.initialSubcategoryId,
    this.initialIntentCode,
    this.title = 'ক্যাটাগরি ও সেবা নির্বাচন করুন',
  });

  /// Helper static method to show the picker as a mobile-friendly bottom sheet
  static Future<CategorySelectionResult?> show(
    BuildContext context, {
    required CategoryRepository repository,
    int? initialCategoryId,
    int? initialSubcategoryId,
    String? initialIntentCode,
    String title = 'ক্যাটাগরি ও সেবা নির্বাচন করুন',
  }) {
    return showModalBottomSheet<CategorySelectionResult>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => FractionallySizedBox(
        heightFactor: 0.92,
        child: CategoryCascadingPicker(
          repository: repository,
          initialCategoryId: initialCategoryId,
          initialSubcategoryId: initialSubcategoryId,
          initialIntentCode: initialIntentCode,
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

  // Intent Selection
  UserIntent? _selectedIntent;

  // Data lists
  List<CategoryItem> _allCategories = [];
  List<CategoryItem> _filteredCategories = [];
  List<SubCategoryItem> _subcategories = [];
  List<SubCategoryItem> _filteredSubcategories = [];
  TaxonomySearchResult? _taxonomySearchResult;
  bool _isSearchingTaxonomy = false;

  // Selected State
  CategoryItem? _selectedCategory;
  SubCategoryItem? _selectedSubcategory;
  String? _lastMatchedAlias;

  // Search Controllers
  final TextEditingController _categorySearchController = TextEditingController();
  final TextEditingController _subcategorySearchController = TextEditingController();

  // Status flags
  bool _isLoadingCategories = false;
  bool _isLoadingSubcategories = false;
  String? _categoryError;
  String? _subcategoryError;

  // Quick Prompt Recommendations for Cox's Bazar
  static const List<String> _popularCoxKeywords = [
    'রাজমিস্ত্রি',
    'ইলেকট্রিশিয়ান',
    'ফ্রিজ নষ্ট',
    'বাসা বদল পিকআপ',
    'সিসিটিভি লাগাব',
    'পুরাতন ফ্রিজ বিক্রি',
    'জরুরি অ্যাম্বুলেন্স',
    'হোটেল বুকিং',
    'চাঁন্দের গাড়ি',
    'নাজিরারটেক শুঁটকি',
  ];

  @override
  void initState() {
    super.initState();
    if (widget.initialIntentCode != null) {
      _selectedIntent = UserIntent.findByCode(widget.initialIntentCode);
    }
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
      cats.sort((a, b) => a.sortOrder.compareTo(b.sortOrder));

      if (mounted) {
        setState(() {
          _allCategories = cats;
          _applyIntentAndQueryFilter();
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
          _categoryError = 'বিভাগগুলো লোড করা যাচ্ছে না। দয়া করে আবার চেষ্টা করুন।';
        });
      }
    }
  }

  void _applyIntentAndQueryFilter() {
    final query = _categorySearchController.text.trim().toLowerCase();
    List<CategoryItem> baseList = _allCategories;

    // Filter by Intent if selected and not searching text
    if (_selectedIntent != null && query.isEmpty) {
      final suggestedIds = _selectedIntent!.suggestedCategoryIds;
      baseList = _allCategories.where((c) => suggestedIds.contains(c.id)).toList();
      if (baseList.isEmpty) {
        baseList = _allCategories;
      }
    }

    if (query.isEmpty) {
      _filteredCategories = baseList;
      _taxonomySearchResult = null;
      _isSearchingTaxonomy = false;
    } else {
      _filteredCategories = _allCategories.where((cat) {
        final matchBn = cat.nameBn.toLowerCase().contains(query);
        final matchEn = cat.nameEn.toLowerCase().contains(query);
        final matchDesc = cat.descriptionBn.toLowerCase().contains(query);
        final matchSlug = cat.slug.toLowerCase().contains(query);
        return matchBn || matchEn || matchDesc || matchSlug;
      }).toList();
    }
  }

  Future<void> _filterCategories(String query) async {
    final q = query.trim().toLowerCase();
    setState(() {
      _applyIntentAndQueryFilter();
    });

    if (q.length >= 2) {
      setState(() {
        _isSearchingTaxonomy = true;
      });
      try {
        final res = await widget.repository.searchTaxonomy(q);
        if (mounted && _categorySearchController.text.trim().toLowerCase() == q) {
          setState(() {
            _taxonomySearchResult = res;
            _isSearchingTaxonomy = false;
          });
        }
      } catch (_) {
        if (mounted) {
          setState(() {
            _isSearchingTaxonomy = false;
          });
        }
      }
    } else {
      setState(() {
        _taxonomySearchResult = null;
        _isSearchingTaxonomy = false;
      });
    }
  }

  void _onIntentSelected(UserIntent? intent) {
    setState(() {
      _selectedIntent = intent;
      _categorySearchController.clear();
      _applyIntentAndQueryFilter();
    });
  }

  void _onQuickChipTapped(String keyword) {
    _categorySearchController.text = keyword;
    _filterCategories(keyword);
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

  Future<void> _selectRankedItem(RankedSearchItem item) async {
    _lastMatchedAlias = item.matchedAlias;
    try {
      CategoryItem targetCat;
      if (_allCategories.any((c) => c.id == item.categoryId)) {
        targetCat = _allCategories.firstWhere((c) => c.id == item.categoryId);
      } else {
        final fetched = await widget.repository.getMainCategories();
        targetCat = fetched.firstWhere((c) => c.id == item.categoryId);
      }

      if (item.isSubCategory && item.id > 0) {
        final subs = await widget.repository.getSubcategories(item.categoryId);
        SubCategoryItem targetSub;
        if (subs.any((s) => s.id == item.id)) {
          targetSub = subs.firstWhere((s) => s.id == item.id);
        } else {
          targetSub = SubCategoryItem(
            id: item.id,
            categoryId: item.categoryId,
            categoryNameBn: item.categoryNameBn,
            categoryNameEn: item.categoryNameEn,
            nameBn: item.nameBn,
            nameEn: item.nameEn,
            slug: item.slug,
            icon: item.icon,
          );
        }

        if (mounted) {
          Navigator.of(context).pop(
            CategorySelectionResult(
              category: targetCat,
              subcategory: targetSub,
              intent: _selectedIntent,
              matchedAlias: item.matchedAlias,
            ),
          );
        }
      } else {
        _selectCategory(targetCat);
      }
    } catch (_) {
      if (_allCategories.any((c) => c.id == item.categoryId)) {
        _selectCategory(_allCategories.firstWhere((c) => c.id == item.categoryId));
      }
    }
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
          intent: _selectedIntent,
          matchedAlias: _lastMatchedAlias,
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
                    fontWeight: FontWeight.bold,
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
  // STEP 1: Main Category & Intent Selection
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
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Category Search Field
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 6),
          child: TextField(
            controller: _categorySearchController,
            onChanged: _filterCategories,
            style: AppTypography.bodyRegular,
            decoration: InputDecoration(
              hintText: '🔍 সেবা বা প্রয়োজন খুঁজুন (যেমন: রাজমিস্ত্রি, ফ্রিজ, সিসিটিভি)...',
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

        // Quick Suggestion Chips
        SizedBox(
          height: 38,
          child: ListView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            children: [
              ..._popularCoxKeywords.map((kw) {
                final isSelected = _categorySearchController.text.trim() == kw;
                return Padding(
                  padding: const EdgeInsets.only(right: 6),
                  child: ActionChip(
                    label: Text(kw),
                    labelStyle: AppTypography.labelSmall.copyWith(
                      fontSize: 11,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                      color: isSelected ? Colors.white : const Color(0xFF334155),
                    ),
                    backgroundColor: isSelected ? AppColors.primary : const Color(0xFFF1F5F9),
                    side: BorderSide(color: isSelected ? AppColors.primary : const Color(0xFFE2E8F0)),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 0),
                    onPressed: () => _onQuickChipTapped(kw),
                  ),
                );
              }),
            ],
          ),
        ),

        // User Intent Filter Strip
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 4, 16, 6),
          child: Row(
            children: [
              Text(
                'উদ্দেশ্য অনুসারে ফিল্টার:',
                style: AppTypography.bodySmall.copyWith(
                  color: const Color(0xFF64748B),
                  fontWeight: FontWeight.bold,
                  fontSize: 11,
                ),
              ),
              const SizedBox(width: 8),
              if (_selectedIntent != null)
                GestureDetector(
                  onTap: () => _onIntentSelected(null),
                  child: Text(
                    'সব দেখুন (রিসেট)',
                    style: AppTypography.labelSmall.copyWith(
                      color: AppColors.primary,
                      fontWeight: FontWeight.bold,
                      fontSize: 11,
                    ),
                  ),
                ),
            ],
          ),
        ),

        // Intent Chips Row
        SizedBox(
          height: 36,
          child: ListView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 2),
            children: [
              // All Filter
              Padding(
                padding: const EdgeInsets.only(right: 6),
                child: FilterChip(
                  label: const Text('সব ক্যাটাগরি'),
                  selected: _selectedIntent == null,
                  onSelected: (selected) {
                    if (selected) _onIntentSelected(null);
                  },
                  labelStyle: AppTypography.labelSmall.copyWith(
                    fontSize: 11,
                    color: _selectedIntent == null ? Colors.white : const Color(0xFF334155),
                    fontWeight: _selectedIntent == null ? FontWeight.bold : FontWeight.w500,
                  ),
                  selectedColor: AppColors.primary,
                  backgroundColor: Colors.white,
                  checkmarkColor: Colors.white,
                  side: BorderSide(color: _selectedIntent == null ? AppColors.primary : const Color(0xFFCBD5E1)),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 0),
                ),
              ),
              ...UserIntent.standardIntents.map((intent) {
                final isSelected = _selectedIntent?.code == intent.code;
                return Padding(
                  padding: const EdgeInsets.only(right: 6),
                  child: FilterChip(
                    label: Text(intent.nameBn),
                    selected: isSelected,
                    onSelected: (selected) {
                      _onIntentSelected(selected ? intent : null);
                    },
                    labelStyle: AppTypography.labelSmall.copyWith(
                      fontSize: 11,
                      color: isSelected ? Colors.white : const Color(0xFF334155),
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                    ),
                    selectedColor: AppColors.primary,
                    backgroundColor: Colors.white,
                    checkmarkColor: Colors.white,
                    side: BorderSide(color: isSelected ? AppColors.primary : const Color(0xFFCBD5E1)),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 0),
                  ),
                );
              }),
            ],
          ),
        ),

        const SizedBox(height: 4),

        // Categories List
        Expanded(
          child: _filteredCategories.isEmpty && (_taxonomySearchResult == null || _taxonomySearchResult!.rankedResults.isEmpty)
              ? _buildEmptyView('কোনো বিভাগ বা সেবা পাওয়া যায়নি', 'বানান সঠিক আছে কিনা যাচাই করুন অথবা অন্য শব্দে খুঁজুন।')
              : ListView(
                  padding: const EdgeInsets.fromLTRB(16, 6, 16, 24),
                  children: [
                    // Direct Taxonomy / Alias Matches Section
                    if (_categorySearchController.text.trim().isNotEmpty &&
                        _taxonomySearchResult != null &&
                        _taxonomySearchResult!.rankedResults.isNotEmpty) ...[
                      Padding(
                        padding: const EdgeInsets.only(bottom: 8, top: 4),
                        child: Row(
                          children: [
                            const Icon(Icons.bolt, size: 18, color: AppColors.primary),
                            const SizedBox(width: 6),
                            Text(
                              'সরাসরি মিল পাওয়া গেছে (Direct Match)',
                              style: AppTypography.mediumHeading2.copyWith(
                                fontSize: 13,
                                fontWeight: FontWeight.bold,
                                color: AppColors.primary,
                              ),
                            ),
                          ],
                        ),
                      ),
                      ..._taxonomySearchResult!.rankedResults.take(5).map((item) => _buildDirectMatchTile(item)),
                      const SizedBox(height: 14),
                    ],

                    // Intent Banner (if Intent selected)
                    if (_selectedIntent != null && _categorySearchController.text.isEmpty) ...[
                      Container(
                        margin: const EdgeInsets.only(bottom: 12),
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: const Color(0xFFF0FDFA),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: const Color(0xFFCCFBF1)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.lightbulb_outline, size: 18, color: AppColors.primary),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                '${_selectedIntent!.nameBn}: ${_selectedIntent!.shortHintBn}',
                                style: AppTypography.bodySmall.copyWith(
                                  color: const Color(0xFF115E59),
                                  fontSize: 11,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],

                    // Popular Categories Section (if not searching text)
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
                          'অন্যান্য বিভাগ (${_filteredCategories.length}টি)',
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

  Widget _buildDirectMatchTile(RankedSearchItem item) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      decoration: BoxDecoration(
        color: const Color(0xFFF0FDF4),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: const Color(0xFF86EFAC),
          width: 1.2,
        ),
      ),
      child: ListTile(
        onTap: () => _selectRankedItem(item),
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
        leading: Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: const Color(0xFFDCFCE7),
            borderRadius: BorderRadius.circular(10),
          ),
          child: const Icon(
            Icons.check_circle_outline,
            color: Color(0xFF16A34A),
            size: 22,
          ),
        ),
        title: Row(
          children: [
            Expanded(
              child: Text(
                item.nameBn,
                style: AppTypography.mediumHeading2.copyWith(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: const Color(0xFF14532D),
                ),
              ),
            ),
            if (item.matchedAlias.isNotEmpty)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: const Color(0xFFDCFCE7),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  '“${item.matchedAlias}” এলিয়াস মিল',
                  style: AppTypography.bodySmall.copyWith(
                    fontSize: 9,
                    color: const Color(0xFF15803D),
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
          ],
        ),
        subtitle: Text(
          item.isSubCategory
              ? 'ক্যাটাগরি: ${item.categoryNameBn.isNotEmpty ? item.categoryNameBn : ""}'
              : (item.nameEn.isNotEmpty ? item.nameEn : 'প্রধান ক্যাটাগরি'),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: AppTypography.bodySmall.copyWith(
            color: const Color(0xFF166534),
            fontSize: 11,
          ),
        ),
        trailing: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
          decoration: BoxDecoration(
            color: AppColors.primary,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Text(
            'নির্বাচন',
            style: AppTypography.labelSmall.copyWith(
              color: Colors.white,
              fontSize: 11,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
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
