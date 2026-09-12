/// Category Repository for Flutter with in-memory caching hooks.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import '../models/category_model.dart';
import '../models/service_model.dart';
import '../services/category_api_service.dart';

class CategoryRepository {
  final CategoryApiService apiService;

  List<CategoryItem>? _cachedCategoryTree;
  List<CategoryItem>? _cachedFeaturedCategories;
  List<ServiceItem>? _cachedFeaturedServices;

  CategoryRepository(this.apiService);

  Future<List<CategoryItem>> getCategoryTree({bool forceRefresh = false}) async {
    if (!forceRefresh && _cachedCategoryTree != null) {
      return _cachedCategoryTree!;
    }
    final tree = await apiService.fetchCategoryTree();
    _cachedCategoryTree = tree;
    return tree;
  }

  Future<List<CategoryItem>> getFeaturedCategories({bool forceRefresh = false}) async {
    if (!forceRefresh && _cachedFeaturedCategories != null) {
      return _cachedFeaturedCategories!;
    }
    final featured = await apiService.fetchFeaturedCategories();
    _cachedFeaturedCategories = featured;
    return featured;
  }

  Future<List<ServiceItem>> getFeaturedServices({bool forceRefresh = false}) async {
    if (!forceRefresh && _cachedFeaturedServices != null) {
      return _cachedFeaturedServices!;
    }
    final services = await apiService.fetchFeaturedServices();
    _cachedFeaturedServices = services;
    return services;
  }

  Future<List<ServiceItem>> getServicesByCategory(int categoryId) async {
    return await apiService.fetchServicesByCategory(categoryId);
  }

  Future<List<ServiceItem>> searchServices(String query, {int? categoryId}) async {
    return await apiService.searchServices(query, categoryId: categoryId);
  }

  void clearCache() {
    _cachedCategoryTree = null;
    _cachedFeaturedCategories = null;
    _cachedFeaturedServices = null;
  }
}
