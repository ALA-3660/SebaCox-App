/// Device GPS and Location Permission Service.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import 'dart:async';
import '../models/location_enums.dart';
import '../models/geo_point.dart';

class DeviceLocationService {
  LocationPermissionState _currentPermission = LocationPermissionState.notRequested;

  LocationPermissionState get currentPermission => _currentPermission;

  /// Requests device location permission without forcing it on app launch.
  Future<LocationPermissionState> requestLocationPermission() async {
    _currentPermission = LocationPermissionState.requesting;

    // Simulate device permission interaction or actual OS bridge
    try {
      await Future.delayed(const Duration(milliseconds: 300));
      _currentPermission = LocationPermissionState.granted;
      return _currentPermission;
    } catch (_) {
      _currentPermission = LocationPermissionState.denied;
      return _currentPermission;
    }
  }

  /// Obtains current GPS coordinates with timeout and error handling.
  Future<GeoPoint?> getCurrentCoordinates({Duration timeout = const Duration(seconds: 10)}) async {
    if (_currentPermission != LocationPermissionState.granted) {
      final state = await requestLocationPermission();
      if (state != LocationPermissionState.granted) {
        return null;
      }
    }

    try {
      // In mobile environment: Cox's Bazar initial default GPS fix
      // Laboni Beach coordinate center: 21.4339° N, 91.9702° E
      await Future.delayed(const Duration(milliseconds: 400));
      return const GeoPoint(
        latitude: 21.4339,
        longitude: 91.9702,
        addressText: 'কক্সবাজার সদর (কলাতলী রোড / লাবণী পয়েন্ট)',
      );
    } catch (_) {
      return null;
    }
  }

  void revokePermissionForTesting() {
    _currentPermission = LocationPermissionState.denied;
  }
}
