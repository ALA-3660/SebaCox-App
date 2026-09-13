/// Provider API Service for SebaCox.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

import '../../../core/network/api_client.dart';
import '../../../shared/models/api_response.dart';
import '../models/provider_model.dart';
import '../models/provider_service_model.dart';
import '../models/provider_service_area_model.dart';

class ProviderApiService {
  final ApiClient _apiClient;

  ProviderApiService({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  /// Discover providers with optional filters
  Future<ApiResponse<List<ProviderProfile>>> getProviders({
    String? query,
    int? serviceId,
    int? categoryId,
    int? upazilaId,
    int? districtId,
    String? providerType,
    bool? isVerified,
    String? availability,
  }) async {
    final queryParams = <String, String>{};
    if (query != null && query.isNotEmpty) queryParams['q'] = query;
    if (serviceId != null) queryParams['service_id'] = serviceId.toString();
    if (categoryId != null) queryParams['category_id'] = categoryId.toString();
    if (upazilaId != null) queryParams['upazila_id'] = upazilaId.toString();
    if (districtId != null) queryParams['district_id'] = districtId.toString();
    if (providerType != null) queryParams['provider_type'] = providerType;
    if (isVerified != null) queryParams['is_verified'] = isVerified.toString();
    if (availability != null) queryParams['availability'] = availability;

    final uri = Uri(path: '/api/v1/providers/', queryParameters: queryParams.isNotEmpty ? queryParams : null);

    return await _apiClient.get<List<ProviderProfile>>(
      uri.toString(),
      fromJson: (json) {
        if (json is List) {
          return json.map((e) => ProviderProfile.fromJson(e as Map<String, dynamic>)).toList();
        }
        return [];
      },
    );
  }

  /// Get provider detail by ID or Slug
  Future<ApiResponse<ProviderProfile>> getProviderDetail(dynamic idOrSlug) async {
    return await _apiClient.get<ProviderProfile>(
      '/api/v1/providers/$idOrSlug/',
      fromJson: (json) => ProviderProfile.fromJson(json as Map<String, dynamic>),
    );
  }

  /// Get authenticated user's provider profile
  Future<ApiResponse<ProviderProfile>> getMyProviderProfile() async {
    return await _apiClient.get<ProviderProfile>(
      '/api/v1/providers/me/',
      fromJson: (json) => ProviderProfile.fromJson(json as Map<String, dynamic>),
    );
  }

  /// Create new provider profile (Phase 5 Profile Creation Flow)
  Future<ApiResponse<ProviderProfile>> createProviderProfile(Map<String, dynamic> data) async {
    return await _apiClient.post<ProviderProfile>(
      '/api/v1/providers/',
      data: data,
      fromJson: (json) => ProviderProfile.fromJson(json as Map<String, dynamic>),
    );
  }

  /// Update existing provider profile
  Future<ApiResponse<ProviderProfile>> updateProviderProfile(int providerId, Map<String, dynamic> data) async {
    return await _apiClient.patch<ProviderProfile>(
      '/api/v1/providers/$providerId/',
      data: data,
      fromJson: (json) => ProviderProfile.fromJson(json as Map<String, dynamic>),
    );
  }

  /// Add service offering
  Future<ApiResponse<ProviderServiceItem>> addProviderService(int providerId, Map<String, dynamic> data) async {
    return await _apiClient.post<ProviderServiceItem>(
      '/api/v1/providers/$providerId/services/',
      data: data,
      fromJson: (json) => ProviderServiceItem.fromJson(json as Map<String, dynamic>),
    );
  }

  /// Remove service offering
  Future<ApiResponse<void>> removeProviderService(int providerId, int serviceId) async {
    return await _apiClient.delete<void>(
      '/api/v1/providers/$providerId/services/$serviceId/',
    );
  }

  /// Add service area coverage
  Future<ApiResponse<ProviderServiceAreaItem>> addProviderServiceArea(int providerId, Map<String, dynamic> data) async {
    return await _apiClient.post<ProviderServiceAreaItem>(
      '/api/v1/providers/$providerId/service-areas/',
      data: data,
      fromJson: (json) => ProviderServiceAreaItem.fromJson(json as Map<String, dynamic>),
    );
  }

  /// Remove service area coverage
  Future<ApiResponse<void>> removeProviderServiceArea(int providerId, int areaId) async {
    return await _apiClient.delete<void>(
      '/api/v1/providers/$providerId/service-areas/$areaId/',
    );
  }

  /// Update availability status
  Future<ApiResponse<Map<String, dynamic>>> updateAvailability(
    int providerId,
    String availability, {
    String? note,
  }) async {
    return await _apiClient.patch<Map<String, dynamic>>(
      '/api/v1/providers/$providerId/availability/',
      data: {
        'availability_status': availability,
        if (note != null && note.isNotEmpty) 'note': note,
      },
      fromJson: (json) => json as Map<String, dynamic>,
    );
  }
}
