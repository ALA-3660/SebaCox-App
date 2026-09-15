/// Category & SubCategory Repository for Flutter with robust in-memory caching.
/// Master Taxonomy v1.0 Universal Hierarchy & Search Integration.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"

import '../models/category_model.dart';
import '../models/service_model.dart';
import '../services/category_api_service.dart';

class CategoryRepository {
  final CategoryApiService apiService;

  List<CategoryItem>? _cachedCategoryTree;
  List<CategoryItem>? _cachedMainCategories;
  List<CategoryItem>? _cachedFeaturedCategories;
  List<ServiceItem>? _cachedFeaturedServices;
  final Map<int, List<SubCategoryItem>> _cachedSubcategoriesByCat = {};
  final Map<int, List<ServiceItem>> _cachedServicesByCat = {};

  CategoryRepository(this.apiService);

  /// Get main categories (flat list of active parent categories)
  Future<List<CategoryItem>> getMainCategories({
    String kind = 'PUBLIC_SERVICE_CATEGORY',
    bool forceRefresh = false,
  }) async {
    if (!forceRefresh && _cachedMainCategories != null && _cachedMainCategories!.isNotEmpty) {
      return _cachedMainCategories!;
    }
    final cats = await apiService.fetchCategories(kind: kind);
    _cachedMainCategories = cats;
    return cats;
  }

  /// Get full structured category tree (including subcategories)
  Future<List<CategoryItem>> getCategoryTree({
    String kind = 'PUBLIC_SERVICE_CATEGORY',
    bool forceRefresh = false,
  }) async {
    if (!forceRefresh && _cachedCategoryTree != null && _cachedCategoryTree!.isNotEmpty) {
      return _cachedCategoryTree!;
    }
    final tree = await apiService.fetchCategoryTree(kind: kind);
    _cachedCategoryTree = tree;
    return tree;
  }

  /// Get subcategories for a given category ID
  Future<List<SubCategoryItem>> getSubcategories(
    int categoryId, {
    bool forceRefresh = false,
  }) async {
    if (!forceRefresh && _cachedSubcategoriesByCat.containsKey(categoryId)) {
      return _cachedSubcategoriesByCat[categoryId]!;
    }
    final subs = await apiService.fetchCategorySubcategories(categoryId);
    _cachedSubcategoriesByCat[categoryId] = subs;
    return subs;
  }

  /// Get featured categories
  Future<List<CategoryItem>> getFeaturedCategories({bool forceRefresh = false}) async {
    if (!forceRefresh && _cachedFeaturedCategories != null) {
      return _cachedFeaturedCategories!;
    }
    final featured = await apiService.fetchFeaturedCategories();
    _cachedFeaturedCategories = featured;
    return featured;
  }

  /// Get featured services
  Future<List<ServiceItem>> getFeaturedServices({bool forceRefresh = false}) async {
    if (!forceRefresh && _cachedFeaturedServices != null) {
      return _cachedFeaturedServices!;
    }
    final services = await apiService.fetchFeaturedServices();
    _cachedFeaturedServices = services;
    return services;
  }

  /// Get services by category ID
  Future<List<ServiceItem>> getServicesByCategory(int categoryId, {bool forceRefresh = false}) async {
    if (!forceRefresh && _cachedServicesByCat.containsKey(categoryId)) {
      return _cachedServicesByCat[categoryId]!;
    }
    final services = await apiService.fetchServicesByCategory(categoryId);
    _cachedServicesByCat[categoryId] = services;
    return services;
  }

  /// Bilingual search services
  Future<List<ServiceItem>> searchServices(
    String query, {
    int? categoryId,
    int? subcategoryId,
  }) async {
    return await apiService.searchServices(
      query,
      categoryId: categoryId,
      subcategoryId: subcategoryId,
    );
  }

  /// Search full taxonomy (categories, subcategories, services, aliases)
  Future<TaxonomySearchResult?> searchTaxonomy(String query) async {
    return await apiService.searchTaxonomy(query);
  }

  /// Clear in-memory caches
  void clearCache() {
    _cachedCategoryTree = null;
    _cachedMainCategories = null;
    _cachedFeaturedCategories = null;
    _cachedFeaturedServices = null;
    _cachedSubcategoriesByCat.clear();
    _cachedServicesByCat.clear();
  }
}
