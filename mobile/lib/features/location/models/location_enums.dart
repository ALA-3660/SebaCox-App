/// Geographic hierarchy enums and permission states for SebaCox.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

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
