/// Location REST API client service for Flutter.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
import '../../../core/network/api_client.dart';
import '../models/location_models.dart';
import '../models/user_location_model.dart';

class LocationApiService {
  final ApiClient apiClient;

  const LocationApiService(this.apiClient);

  Future<List<GeographicItem>> fetchCountries() async {
    final response = await apiClient.get('/api/v1/locations/countries/');
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => GeographicItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<List<GeographicItem>> fetchDivisions({int? countryId, String? countryCode}) async {
    final query = <String, String>{};
    if (countryId != null) query['country'] = countryId.toString();
    if (countryCode != null) query['country_code'] = countryCode;

    final response = await apiClient.get('/api/v1/locations/divisions/', queryParameters: query);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => GeographicItem.fromJson(item as Map<String, dynamic>, parentKey: 'country')).toList();
  }

  Future<List<GeographicItem>> fetchDistricts({int? divisionId, String? divisionCode}) async {
    final query = <String, String>{};
    if (divisionId != null) query['division'] = divisionId.toString();
    if (divisionCode != null) query['division_code'] = divisionCode;

    final response = await apiClient.get('/api/v1/locations/districts/', queryParameters: query);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => GeographicItem.fromJson(item as Map<String, dynamic>, parentKey: 'division')).toList();
  }

  Future<List<GeographicItem>> fetchUpazilas({int? districtId, String? districtCode}) async {
    final query = <String, String>{};
    if (districtId != null) query['district'] = districtId.toString();
    if (districtCode != null) query['district_code'] = districtCode;

    final response = await apiClient.get('/api/v1/locations/upazilas/', queryParameters: query);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => GeographicItem.fromJson(item as Map<String, dynamic>, parentKey: 'district')).toList();
  }

  Future<List<GeographicItem>> fetchMunicipalities({int? districtId, int? upazilaId}) async {
    final query = <String, String>{};
    if (districtId != null) query['district'] = districtId.toString();
    if (upazilaId != null) query['upazila'] = upazilaId.toString();

    final response = await apiClient.get('/api/v1/locations/municipalities/', queryParameters: query);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => GeographicItem.fromJson(item as Map<String, dynamic>, parentKey: 'district')).toList();
  }

  Future<List<GeographicItem>> fetchUnions({int? upazilaId, String? upazilaCode}) async {
    final query = <String, String>{};
    if (upazilaId != null) query['upazila'] = upazilaId.toString();
    if (upazilaCode != null) query['upazila_code'] = upazilaCode;

    final response = await apiClient.get('/api/v1/locations/unions/', queryParameters: query);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => GeographicItem.fromJson(item as Map<String, dynamic>, parentKey: 'upazila')).toList();
  }

  Future<List<GeographicItem>> fetchWards({int? municipalityId, int? unionId, int? cityCorporationId}) async {
    final query = <String, String>{};
    if (municipalityId != null) query['municipality'] = municipalityId.toString();
    if (unionId != null) query['union'] = unionId.toString();
    if (cityCorporationId != null) query['city_corporation'] = cityCorporationId.toString();

    final response = await apiClient.get('/api/v1/locations/wards/', queryParameters: query);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => GeographicItem.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<List<GeographicItem>> fetchLocalities({int? upazilaId, int? wardId, int? unionId, int? municipalityId}) async {
    final query = <String, String>{};
    if (upazilaId != null) query['upazila'] = upazilaId.toString();
    if (wardId != null) query['ward'] = wardId.toString();
    if (unionId != null) query['union'] = unionId.toString();
    if (municipalityId != null) query['municipality'] = municipalityId.toString();

    final response = await apiClient.get('/api/v1/locations/localities/', queryParameters: query);
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => GeographicItem.fromJson(item as Map<String, dynamic>, parentKey: 'upazila')).toList();
  }

  Future<List<LocationSearchResult>> searchLocations(String query, {int limit = 20}) async {
    final response = await apiClient.get(
      '/api/v1/locations/search/',
      queryParameters: {'q': query, 'limit': limit.toString()},
    );
    final List list = (response['data'] as List?) ?? [];
    return list.map((item) => LocationSearchResult.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<UserLocationModel?> fetchSelectedLocation() async {
    final response = await apiClient.get('/api/v1/locations/user/selected/');
    final data = response['data'];
    if (data == null) return null;
    return UserLocationModel.fromJson(data as Map<String, dynamic>);
  }

  Future<UserLocationModel> saveSelectedLocation(Map<String, dynamic> payload) async {
    final response = await apiClient.post('/api/v1/locations/user/selected/', data: payload);
    return UserLocationModel.fromJson(response['data'] as Map<String, dynamic>);
  }

  Future<UserLocationModel> saveCurrentGpsLocation(double lat, double lon, String addressText) async {
    final response = await apiClient.post('/api/v1/locations/user/current/', data: {
      'latitude': lat,
      'longitude': lon,
      'address_text': addressText,
    });
    return UserLocationModel.fromJson(response['data'] as Map<String, dynamic>);
  }
}
