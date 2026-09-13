/// Provider Repository for SebaCox.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

import '../../../shared/models/api_response.dart';
import '../models/provider_model.dart';
import '../models/provider_service_model.dart';
import '../models/provider_service_area_model.dart';
import '../services/provider_api_service.dart';

class ProviderRepository {
  final ProviderApiService _apiService;

  ProviderRepository({ProviderApiService? apiService})
      : _apiService = apiService ?? ProviderApiService();

  Future<ApiResponse<List<ProviderProfile>>> getProviders({
    String? query,
    int? serviceId,
    int? categoryId,
    int? upazilaId,
    int? districtId,
    String? providerType,
    bool? isVerified,
    String? availability,
  }) =>
      _apiService.getProviders(
        query: query,
        serviceId: serviceId,
        categoryId: categoryId,
        upazilaId: upazilaId,
        districtId: districtId,
        providerType: providerType,
        isVerified: isVerified,
        availability: availability,
      );

  Future<ApiResponse<ProviderProfile>> getProviderDetail(dynamic idOrSlug) =>
      _apiService.getProviderDetail(idOrSlug);

  Future<ApiResponse<ProviderProfile>> getMyProviderProfile() =>
      _apiService.getMyProviderProfile();

  Future<ApiResponse<ProviderProfile>> createProviderProfile(Map<String, dynamic> data) =>
      _apiService.createProviderProfile(data);

  Future<ApiResponse<ProviderProfile>> updateProviderProfile(int id, Map<String, dynamic> data) =>
      _apiService.updateProviderProfile(id, data);

  Future<ApiResponse<ProviderServiceItem>> addProviderService(int providerId, Map<String, dynamic> data) =>
      _apiService.addProviderService(providerId, data);

  Future<ApiResponse<void>> removeProviderService(int providerId, int serviceId) =>
      _apiService.removeProviderService(providerId, serviceId);

  Future<ApiResponse<ProviderServiceAreaItem>> addProviderServiceArea(int providerId, Map<String, dynamic> data) =>
      _apiService.addProviderServiceArea(providerId, data);

  Future<ApiResponse<void>> removeProviderServiceArea(int providerId, int areaId) =>
      _apiService.removeProviderServiceArea(providerId, areaId);

  Future<ApiResponse<Map<String, dynamic>>> updateAvailability(
    int providerId,
    String availability, {
    String? note,
  }) =>
      _apiService.updateAvailability(providerId, availability, note: note);
}
