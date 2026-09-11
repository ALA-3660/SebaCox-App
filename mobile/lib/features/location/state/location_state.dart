/// Location state container for Flutter.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import '../models/location_enums.dart';
import '../models/geo_point.dart';
import '../models/user_location_model.dart';

class LocationState {
  final LocationLoadingStatus status;
  final LocationPermissionState permissionStatus;
  final UserLocationModel? selectedLocation;
  final GeoPoint? currentGpsLocation;
  final String? errorMessage;

  const LocationState({
    this.status = LocationLoadingStatus.initial,
    this.permissionStatus = LocationPermissionState.notRequested,
    this.selectedLocation,
    this.currentGpsLocation,
    this.errorMessage,
  });

  factory LocationState.initial() => const LocationState();

  LocationState copyWith({
    LocationLoadingStatus? status,
    LocationPermissionState? permissionStatus,
    UserLocationModel? selectedLocation,
    GeoPoint? currentGpsLocation,
    String? errorMessage,
    bool clearError = false,
  }) {
    return LocationState(
      status: status ?? this.status,
      permissionStatus: permissionStatus ?? this.permissionStatus,
      selectedLocation: selectedLocation ?? this.selectedLocation,
      currentGpsLocation: currentGpsLocation ?? this.currentGpsLocation,
      errorMessage: clearError ? null : (errorMessage ?? this.errorMessage),
    );
  }

  bool get hasSelectedLocation => selectedLocation != null;
  bool get hasGpsLocation => currentGpsLocation != null;

  String get currentDisplayNameBn {
    if (selectedLocation != null && selectedLocation!.displayAddressBn.isNotEmpty) {
      return selectedLocation!.displayAddressBn;
    }
    if (currentGpsLocation != null) {
      return currentGpsLocation!.addressText.isNotEmpty
          ? currentGpsLocation!.addressText
          : 'জিপিএস (${currentGpsLocation!.latitude.toStringAsFixed(3)}, ${currentGpsLocation!.longitude.toStringAsFixed(3)})';
    }
    return 'অবস্থান নির্বাচন করুন';
  }
}
