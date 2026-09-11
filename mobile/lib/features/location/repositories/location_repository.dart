/// Location Repository for state coordination and persistence.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import 'dart:async';
import '../models/location_enums.dart';
import '../models/geo_point.dart';
import '../models/user_location_model.dart';
import '../models/location_models.dart';
import '../state/location_state.dart';
import '../services/device_location_service.dart';
import '../services/location_api_service.dart';

class LocationRepository {
  final LocationApiService apiService;
  final DeviceLocationService deviceService;

  final _stateController = StreamController<LocationState>.broadcast();
  LocationState _currentState = LocationState.initial();

  LocationRepository({
    required this.apiService,
    required this.deviceService,
  }) {
    _stateController.add(_currentState);
  }

  Stream<LocationState> get stateStream => _stateController.stream;
  LocationState get currentState => _currentState;

  void _emit(LocationState newState) {
    _currentState = newState;
    _stateController.add(_currentState);
  }

  /// Initializes location state without blocking or forcing permissions on startup.
  Future<void> initialize() async {
    try {
      final selected = await apiService.fetchSelectedLocation();
      if (selected != null) {
        _emit(_currentState.copyWith(
          status: LocationLoadingStatus.locationReady,
          selectedLocation: selected,
        ));
      }
    } catch (_) {
      // Offline, unauthenticated, or initial state is acceptable
    }
  }

  /// Requests device GPS location.
  /// IMPORTANT: Updates currentGpsLocation WITHOUT mutating selected service area.
  Future<void> fetchCurrentGpsLocation() async {
    _emit(_currentState.copyWith(
      status: LocationLoadingStatus.requestingPermission,
      permissionStatus: LocationPermissionState.requesting,
    ));

    final permission = await deviceService.requestLocationPermission();

    if (permission != LocationPermissionState.granted) {
      _emit(_currentState.copyWith(
        status: LocationLoadingStatus.permissionDenied,
        permissionStatus: permission,
        errorMessage: 'লোকেশন ব্যবহারের অনুমতি পাওয়া যায়নি',
      ));
      return;
    }

    _emit(_currentState.copyWith(
      status: LocationLoadingStatus.fetchingLocation,
      permissionStatus: LocationPermissionState.granted,
    ));

    final point = await deviceService.getCurrentCoordinates();
    if (point != null) {
      // Save GPS coordinates to backend if logged in
      try {
        await apiService.saveCurrentGpsLocation(point.latitude, point.longitude, point.addressText);
      } catch (_) {}

      _emit(_currentState.copyWith(
        status: LocationLoadingStatus.locationReady,
        currentGpsLocation: point,
        clearError: true,
      ));
    } else {
      _emit(_currentState.copyWith(
        status: LocationLoadingStatus.locationError,
        errorMessage: 'জিপিএস অবস্থান সনাক্ত করা যায়নি',
      ));
    }
  }

  /// Manually selects an administrative location hierarchy as the active service area.
  Future<bool> selectAdministrativeArea({
    required int districtId,
    int? upazilaId,
    int? unionId,
    int? municipalityId,
    int? wardId,
    int? localityId,
    String? label,
  }) async {
    _emit(_currentState.copyWith(status: LocationLoadingStatus.fetchingLocation));

    try {
      final userLoc = await apiService.saveSelectedLocation({
        'district_id': districtId,
        'upazila_id': upazilaId,
        'union_id': unionId,
        'municipality_id': municipalityId,
        'ward_id': wardId,
        'locality_id': localityId,
        'label': label ?? 'নির্বাচিত সেবা এলাকা',
      });

      _emit(_currentState.copyWith(
        status: LocationLoadingStatus.locationReady,
        selectedLocation: userLoc,
        clearError: true,
      ));
      return true;
    } catch (e) {
      _emit(_currentState.copyWith(
        status: LocationLoadingStatus.locationError,
        errorMessage: 'অবস্থান সংরক্ষণ করা যায়নি: $e',
      ));
      return false;
    }
  }

  /// Explicit user confirmation: Use GPS position as the selected service area.
  /// Rule: NEVER automatically change without user confirmation.
  Future<void> confirmCurrentLocationAsServiceArea(UserLocationModel serviceArea) async {
    _emit(_currentState.copyWith(
      selectedLocation: serviceArea,
      status: LocationLoadingStatus.locationReady,
    ));
  }

  /// Searches locations by Bangla or English keyword.
  Future<List<LocationSearchResult>> search(String query) async {
    if (query.trim().isEmpty) return [];
    try {
      return await apiService.searchLocations(query.trim());
    } catch (_) {
      return [];
    }
  }

  void dispose() {
    _stateController.close();
  }
}
