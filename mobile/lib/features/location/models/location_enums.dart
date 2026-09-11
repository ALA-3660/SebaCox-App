/// Geographic hierarchy enums and permission states for SebaCox.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"

enum LocationLevel {
  country,
  division,
  district,
  upazila,
  municipality,
  union,
  ward,
  locality,
}

enum LocationUsageType {
  selected,
  current,
  preferred,
  home,
  work,
  other,
}

enum LocationPermissionState {
  notRequested,
  requesting,
  granted,
  denied,
  deniedPermanently,
  serviceDisabled,
}

enum LocationLoadingStatus {
  initial,
  requestingPermission,
  permissionGranted,
  permissionDenied,
  fetchingLocation,
  locationReady,
  locationError,
}
