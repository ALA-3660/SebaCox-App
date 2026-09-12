/// Category & Service REST API client service for Flutter.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import '../../../core/network/api_client.dart';
import '../models/category_model.dart';
import '../models/service_model.dart';

class CategoryApiService {
  final ApiClient apiClient;

  const CategoryApiService(this.apiClient);

  /// Fetch active categories (defaulting to public service categories)
  Future<List<CategoryItem>> fetchCategories({
    int? parentId,
    int? level,
    bool? isFeatured,
    String? kind,
  }) async {
    final query = <String, String>{};
    if (parentId != null) query['parent'] = parentId.toString();
    if (level != null) query['level'] = level.toString();
    if (isFeatured != null) query['is_featured'] = isFeatured.toString();
    if (kind != null) query['kind'] = kind;

    final response = await apiClient.get('/api/v1/categories/', queryParameters: query);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => CategoryItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  /// Fetch structured recursive category tree
  Future<List<CategoryItem>> fetchCategoryTree({String kind = 'PUBLIC_SERVICE_CATEGORY'}) async {
    final response = await apiClient.get('/api/v1/categories/tree/', queryParameters: {'kind': kind});
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => CategoryItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  /// Fetch featured categories
  Future<List<CategoryItem>> fetchFeaturedCategories() async {
    final response = await apiClient.get('/api/v1/categories/featured/');
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => CategoryItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  /// Fetch direct child categories of a parent
  Future<List<CategoryItem>> fetchCategoryChildren(int categoryId) async {
    final response = await apiClient.get('/api/v1/categories/$categoryId/children/');
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => CategoryItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  /// Fetch services under a category
  Future<List<ServiceItem>> fetchServicesByCategory(int categoryId) async {
    final response = await apiClient.get('/api/v1/services/by-category/$categoryId/');
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => ServiceItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  /// Fetch featured services
  Future<List<ServiceItem>> fetchFeaturedServices() async {
    final response = await apiClient.get('/api/v1/services/featured/');
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => ServiceItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  /// Bilingual search for services
  Future<List<ServiceItem>> searchServices(String query, {int? categoryId, String? serviceType}) async {
    final queryParams = <String, String>{'q': query};
    if (categoryId != null) queryParams['category_id'] = categoryId.toString();
    if (serviceType != null) queryParams['service_type'] = serviceType;

    final response = await apiClient.get('/api/v1/services/search/', queryParameters: queryParams);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => ServiceItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  /// Fetch single service detail
  Future<ServiceItem> fetchServiceDetail(int serviceId) async {
    final response = await apiClient.get('/api/v1/services/$serviceId/');
    final Map<String, dynamic> data = (response['data'] as Map<String, dynamic>?) ?? {};
    return ServiceItem.fromJson(data);
  }
}
