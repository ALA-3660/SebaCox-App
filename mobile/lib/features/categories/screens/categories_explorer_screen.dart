/// Categories & Services Explorer Screen for SebaCox.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
import 'package:flutter/material.dart';
import '../../../core/constants/app_brand.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../repositories/category_repository.dart';
import '../models/category_model.dart';
import '../models/service_model.dart';
import '../state/category_state.dart';
import '../widgets/category_card.dart';
import '../widgets/service_card.dart';
import '../widgets/category_tree_view.dart';

class CategoriesExplorerScreen extends StatefulWidget {
  final CategoryRepository repository;

  const CategoriesExplorerScreen({
    super.key,
    required this.repository,
  });

  @override
  State<CategoriesExplorerScreen> createState() => _CategoriesExplorerScreenState();
}

class _CategoriesExplorerScreenState extends State<CategoriesExplorerScreen> with SingleTickerProviderStateMixin {
  final TextEditingController _searchController = TextEditingController();
  late TabController _tabController;

  CategoryState _state = const CategoryInitial();
  CategoryItem? _selectedCategory;
  List<ServiceItem> _categoryServices = [];
  bool _isLoadingCategoryServices = false;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _loadInitialData();
  }

  @override
  void dispose() {
    _searchController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadInitialData() async {
    setState(() {
      _state = const CategoryLoading();
    });

    try {
      final tree = await widget.repository.getCategoryTree();
      final featuredCats = await widget.repository.getFeaturedCategories();
      final featuredServices = await widget.repository.getFeaturedServices();

      setState(() {
        _state = CategoryLoaded(
          categoryTree: tree,
          featuredCategories: featuredCats,
          featuredServices: featuredServices,
        );
      });
    } catch (e) {
      setState(() {
        _state = CategoryError('ক্যাটাগরি ও সেবা লোড করতে সমস্যা হয়েছে: ${e.toString()}');
      });
    }
  }

  Future<void> _onSearchChanged(String query) async {
    if (query.trim().isEmpty) {
      if (_state is CategoryLoaded) {
        final current = _state as CategoryLoaded;
        setState(() {
          _state = current.copyWith(searchResults: [], activeSearchQuery: null);
        });
      }
      return;
    }

    try {
      final results = await widget.repository.searchServices(query.trim());
      if (_state is CategoryLoaded) {
        final current = _state as CategoryLoaded;
        setState(() {
          _state = current.copyWith(
            searchResults: results,
            activeSearchQuery: query.trim(),
          );
        });
      }
    } catch (_) {
      // Keep UI stable during quick search failures
    }
  }

  Future<void> _onSelectCategory(CategoryItem category) async {
    setState(() {
      _selectedCategory = category;
      _isLoadingCategoryServices = true;
    });

    try {
      final services = await widget.repository.getServicesByCategory(category.id);
      setState(() {
        _categoryServices = services;
        _isLoadingCategoryServices = false;
      });
    } catch (e) {
      setState(() {
        _isLoadingCategoryServices = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: Text(
          _selectedCategory != null ? _selectedCategory!.nameBn : 'সেবাসমূহ ও ক্যাটাগরি',
          style: AppTypography.largeHeading3.copyWith(
            color: AppColors.primary,
          ),
        ),
        leading: _selectedCategory != null
            ? IconButton(
                icon: const Icon(Icons.arrow_back, color: AppColors.primary),
                onPressed: () {
                  setState(() {
                    _selectedCategory = null;
                    _categoryServices = [];
                  });
                },
              )
            : null,
        bottom: _selectedCategory == null && !(_state is CategoryLoaded && (_state as CategoryLoaded).isSearching)
            ? TabBar(
                controller: _tabController,
                indicatorColor: AppColors.primary,
                indicatorWeight: 3,
                labelColor: AppColors.primary,
                unselectedLabelColor: AppColors.textSecondary,
                labelStyle: AppTypography.mediumHeading4,
                unselectedLabelStyle: AppTypography.bodyMedium,
                tabs: const [
                  Tab(text: 'প্রধান ও জনপ্রিয় সেবা'),
                  Tab(text: 'সব ক্যাটাগরি এক্সপ্লোরার'),
                ],
              )
            : null,
      ),
      body: Column(
        children: [
          // Search Header with Global Typography
          _buildSearchBox(),

          // Main View
          Expanded(
            child: _buildBody(),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBox() {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
      child: TextField(
        controller: _searchController,
        onChanged: _onSearchChanged,
        style: AppTypography.bodyMedium,
        decoration: InputDecoration(
          hintText: 'সেবা বা ক্যাটাগরি খুঁজুন (যেমন: ডাক্তার, ইট, হোটেল)...',
          hintStyle: AppTypography.bodyMedium.copyWith(color: AppColors.textTertiary),
          prefixIcon: const Icon(Icons.search, color: AppColors.primary),
          suffixIcon: _searchController.text.isNotEmpty
              ? IconButton(
                  icon: const Icon(Icons.clear, size: 18),
                  onPressed: () {
                    _searchController.clear();
                    _onSearchChanged('');
                  },
                )
              : null,
          filled: true,
          fillColor: AppColors.backgroundSecondary,
          contentPadding: const EdgeInsets.symmetric(vertical: 10, horizontal: 16),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(10),
            borderSide: BorderSide.none,
          ),
        ),
      ),
    );
  }

  Widget _buildBody() {
    if (_state is CategoryLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(color: AppColors.primary),
            const SizedBox(height: 16),
            Text(
              'ক্যাটাগরি ও সেবা লোড হচ্ছে...',
              style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
            ),
          ],
        ),
      );
    }

    if (_state is CategoryError) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 48, color: AppColors.error),
              const SizedBox(height: 12),
              Text(
                (_state as CategoryError).errorMessage,
                textAlign: TextAlign.center,
                style: AppTypography.bodyMedium.copyWith(color: AppColors.error),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: _loadInitialData,
                style: ElevatedButton.styleFrom(backgroundColor: AppColors.primary),
                child: Text('পুনরায় চেষ্টা করুন', style: AppTypography.labelMedium.copyWith(color: Colors.white)),
              ),
            ],
          ),
        ),
      );
    }

    final loadedState = _state as CategoryLoaded;

    // 1. Search Results View
    if (loadedState.isSearching) {
      return _buildSearchResultsView(loadedState);
    }

    // 2. Category Drilldown Services View
    if (_selectedCategory != null) {
      return _buildCategoryServicesView();
    }

    // 3. Tabbed Home Explorer View
    return TabBarView(
      controller: _tabController,
      children: [
        _buildCuratedHomeTab(loadedState),
        _buildCategoryTreeTab(loadedState),
      ],
    );
  }

  Widget _buildSearchResultsView(CategoryLoaded state) {
    if (state.searchResults.isEmpty) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.search_off, size: 48, color: AppColors.textTertiary),
              const SizedBox(height: 12),
              Text(
                '“${state.activeSearchQuery}” দিয়ে কোনো সেবা পাওয়া যায়নি।',
                textAlign: TextAlign.center,
                style: AppTypography.mediumHeading3.copyWith(color: AppColors.textSecondary),
              ),
              const SizedBox(height: 6),
              Text(
                'বানান পরীক্ষা করুন অথবা ভিন্ন নামে অনুসন্ধান করুন।',
                style: AppTypography.bodySmall.copyWith(color: AppColors.textTertiary),
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.06),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: AppColors.primary.withOpacity(0.12)),
                ),
                child: Text(
                  AppBrand.shortDescriptionWithQuotes,
                  style: AppTypography.bodySmall.copyWith(
                    color: AppColors.primaryDark,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            ],
          ),
        ),
      );
    }

    return ListView.builder(
      itemCount: state.searchResults.length,
      padding: const EdgeInsets.symmetric(vertical: 8),
      itemBuilder: (context, index) {
        final service = state.searchResults[index];
        return ServiceCard(
          service: service,
          onTap: () => _showServiceDetailModal(service),
        );
      },
    );
  }

  Widget _buildCategoryServicesView() {
    if (_isLoadingCategoryServices) {
      return const Center(child: CircularProgressIndicator(color: AppColors.primary));
    }

    if (_categoryServices.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.category_outlined, size: 48, color: AppColors.textTertiary),
            const SizedBox(height: 12),
            Text(
              'এই ক্যাটাগরিতে এখনও কোনো সক্রিয় সেবা তালিকাভুক্ত হয়নি।',
              style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      itemCount: _categoryServices.length,
      padding: const EdgeInsets.symmetric(vertical: 8),
      itemBuilder: (context, index) {
        final service = _categoryServices[index];
        return ServiceCard(
          service: service,
          onTap: () => _showServiceDetailModal(service),
        );
      },
    );
  }

  Widget _buildCuratedHomeTab(CategoryLoaded state) {
    return SingleChildScrollView(
      padding: const EdgeInsets.only(bottom: 24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Brand Slogan & Short Description Card
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
            child: Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppColors.primary.withOpacity(0.06),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: AppColors.primary.withOpacity(0.12)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    AppBrand.sloganWithQuotes,
                    style: AppTypography.mediumHeading2.copyWith(
                      color: AppColors.primary,
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 3),
                  Text(
                    AppBrand.shortDescriptionWithQuotes,
                    style: AppTypography.bodySmall.copyWith(
                      color: AppColors.textSecondary,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Curated Popular Categories
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'জনপ্রিয় সেবা ক্যাটাগরি',
                  style: AppTypography.mediumHeading2.copyWith(fontSize: 18),
                ),
                TextButton(
                  onPressed: () => _tabController.animateTo(1),
                  child: Text('সব দেখুন', style: AppTypography.labelMedium.copyWith(color: AppColors.primary)),
                ),
              ],
            ),
          ),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            padding: const EdgeInsets.symmetric(horizontal: 16),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 3,
              crossAxisSpacing: 10,
              mainAxisSpacing: 10,
              childAspectRatio: 0.92,
            ),
            itemCount: state.featuredCategories.length,
            itemBuilder: (context, index) {
              final cat = state.featuredCategories[index];
              return CategoryCard(
                category: cat,
                isCompact: true,
                onTap: () => _onSelectCategory(cat),
              );
            },
          ),

          const SizedBox(height: 20),

          // Featured Services
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
            child: Text(
              'গুরুত্বপূর্ণ ও নির্বাচিত সেবা',
              style: AppTypography.mediumHeading2.copyWith(fontSize: 18),
            ),
          ),
          ...state.featuredServices.map((service) {
            return ServiceCard(
              service: service,
              onTap: () => _showServiceDetailModal(service),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildCategoryTreeTab(CategoryLoaded state) {
    return CategoryTreeView(
      categories: state.categoryTree,
      onSelectCategory: _onSelectCategory,
    );
  }

  void _showServiceDetailModal(ServiceItem service) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return Padding(
          padding: EdgeInsets.fromLTRB(20, 16, 20, MediaQuery.of(context).viewInsets.bottom + 24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: AppColors.divider,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 16),

              // Title (Large Heading -> Hind Siliguri)
              Text(
                service.nameBn,
                style: AppTypography.largeHeading2.copyWith(fontSize: 22),
              ),
              Text(
                '${service.nameEn} • ${service.categoryNameBn}',
                style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary),
              ),
              const SizedBox(height: 12),

              // Description (Tiro Bangla)
              Text(
                service.shortDescriptionBn.isNotEmpty
                    ? service.shortDescriptionBn
                    : 'সেবা সংক্রান্ত তথ্য ও বিস্তারিত বিবরণ।',
                style: AppTypography.bodyMedium.copyWith(height: 1.5),
              ),

              const SizedBox(height: 16),
              Text(
                'সেবার বৈশিষ্ট্য ও সুবিধাসমূহ:',
                style: AppTypography.mediumHeading3.copyWith(fontSize: 15),
              ),
              const SizedBox(height: 8),

              Wrap(
                spacing: 8,
                runSpacing: 6,
                children: service.capabilityBadges.map((b) {
                  return Chip(
                    label: Text(b, style: AppTypography.labelSmall),
                    backgroundColor: AppColors.primarySurface,
                    side: BorderSide.none,
                  );
                }).toList(),
              ),

              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => Navigator.pop(context),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  child: Text(
                    'ঠিক আছে',
                    style: AppTypography.labelMedium.copyWith(color: Colors.white),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
