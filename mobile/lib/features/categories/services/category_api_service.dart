/// Category & Service REST API client service for Flutter.
/// Master Taxonomy v1.0 Universal Hierarchy & Search Integration.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"

import '../../../core/network/api_client.dart';
import '../models/category_model.dart';
import '../models/service_model.dart';

class CategoryApiService {
  final ApiClient apiClient;

  const CategoryApiService(this.apiClient);

  /// Helper to build query parameters
  String _buildQueryString(Map<String, dynamic> params) {
    final query = <String>[];
    params.forEach((key, value) {
      if (value != null && value.toString().isNotEmpty) {
        query.add('${Uri.encodeComponent(key)}=${Uri.encodeComponent(value.toString())}');
      }
    });
    return query.isEmpty ? '' : '?${query.join('&')}';
  }

  /// Fetch active main categories (defaulting to PUBLIC_SERVICE_CATEGORY)
  Future<List<CategoryItem>> fetchCategories({
    int? parentId,
    int? level,
    bool? isFeatured,
    bool? isPopular,
    String? kind,
    String? search,
  }) async {
    final qs = _buildQueryString({
      'parent': parentId,
      'level': level,
      'is_featured': isFeatured,
      'is_popular': isPopular,
      'kind': kind ?? 'PUBLIC_SERVICE_CATEGORY',
      'search': search,
    });

    final response = await apiClient.get<List<CategoryItem>>(
      '/api/v1/categories/$qs',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => CategoryItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );

    return response.data ?? [];
  }

  /// Fetch single category details
  Future<CategoryItem?> fetchCategoryDetail(int categoryId) async {
    final response = await apiClient.get<CategoryItem>(
      '/api/v1/categories/$categoryId/',
      fromJson: (json) => CategoryItem.fromJson(json as Map<String, dynamic>),
    );
    return response.data;
  }

  /// Fetch structured recursive category tree
  Future<List<CategoryItem>> fetchCategoryTree({String kind = 'PUBLIC_SERVICE_CATEGORY'}) async {
    final qs = _buildQueryString({'kind': kind});
    final response = await apiClient.get<List<CategoryItem>>(
      '/api/v1/categories/tree/$qs',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => CategoryItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
    return response.data ?? [];
  }

  /// Fetch featured categories
  Future<List<CategoryItem>> fetchFeaturedCategories() async {
    final response = await apiClient.get<List<CategoryItem>>(
      '/api/v1/categories/featured/',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => CategoryItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
    return response.data ?? [];
  }

  /// Fetch subcategories with optional category filter
  Future<List<SubCategoryItem>> fetchSubcategories({
    int? categoryId,
    bool? isPopular,
    String? search,
  }) async {
    final qs = _buildQueryString({
      'category_id': categoryId,
      'is_popular': isPopular,
      'search': search,
    });

    final response = await apiClient.get<List<SubCategoryItem>>(
      '/api/v1/categories/subcategories/$qs',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => SubCategoryItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
    return response.data ?? [];
  }

  /// Fetch subcategories for a specific parent category ID
  Future<List<SubCategoryItem>> fetchCategorySubcategories(int categoryId) async {
    final response = await apiClient.get<List<SubCategoryItem>>(
      '/api/v1/categories/$categoryId/subcategories/',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => SubCategoryItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
    return response.data ?? [];
  }

  /// Search taxonomy across categories, subcategories, services and aliases
  Future<TaxonomySearchResult?> searchTaxonomy(String query) async {
    final qs = _buildQueryString({'q': query});
    final response = await apiClient.get<TaxonomySearchResult>(
      '/api/v1/categories/search/$qs',
      fromJson: (json) => TaxonomySearchResult.fromJson(json as Map<String, dynamic>),
    );
    return response.data;
  }

  /// Fetch direct child categories of a parent (backward compatibility)
  Future<List<CategoryItem>> fetchCategoryChildren(int categoryId) async {
    final response = await apiClient.get<List<CategoryItem>>(
      '/api/v1/categories/$categoryId/children/',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => CategoryItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
    return response.data ?? [];
  }

  /// Fetch services under a category
  Future<List<ServiceItem>> fetchServicesByCategory(int categoryId) async {
    final response = await apiClient.get<List<ServiceItem>>(
      '/api/v1/services/by-category/$categoryId/',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => ServiceItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
    return response.data ?? [];
  }

  /// Fetch featured services
  Future<List<ServiceItem>> fetchFeaturedServices() async {
    final response = await apiClient.get<List<ServiceItem>>(
      '/api/v1/services/featured/',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => ServiceItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
    return response.data ?? [];
  }

  /// Bilingual search for services
  Future<List<ServiceItem>> searchServices(
    String query, {
    int? categoryId,
    int? subcategoryId,
    String? serviceType,
  }) async {
    final qs = _buildQueryString({
      'q': query,
      'category_id': categoryId,
      'subcategory_id': subcategoryId,
      'service_type': serviceType,
    });

    final response = await apiClient.get<List<ServiceItem>>(
      '/api/v1/services/search/$qs',
      fromJson: (json) {
        if (json is List) {
          return json.map((item) => ServiceItem.fromJson(item as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
    return response.data ?? [];
  }

  /// Fetch single service detail
  Future<ServiceItem?> fetchServiceDetail(int serviceId) async {
    final response = await apiClient.get<ServiceItem>(
      '/api/v1/services/$serviceId/',
      fromJson: (json) => ServiceItem.fromJson(json as Map<String, dynamic>),
    );
    return response.data;
  }
}
