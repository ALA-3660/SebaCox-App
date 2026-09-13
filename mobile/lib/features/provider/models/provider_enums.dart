/// Enums for SebaCox Provider Engine.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

/// Provider legal/operational type
enum ProviderType {
  individual('INDIVIDUAL', 'ব্যক্তিগত সেবাদাতা', 'Individual Provider'),
  business('BUSINESS', 'ব্যবসায়িক প্রতিষ্ঠান', 'Business / Enterprise'),
  organization('ORGANIZATION', 'সংস্থা বা প্রতিষ্ঠান', 'Organization / Agency');

  final String value;
  final String labelBn;
  final String labelEn;

  const ProviderType(this.value, this.labelBn, this.labelEn);

  static ProviderType fromString(String? val) {
    return ProviderType.values.firstWhere(
      (e) => e.value == val,
      orElse: () => ProviderType.individual,
    );
  }
}

/// Provider operational status
enum ProviderStatus {
  draft('DRAFT', 'খসড়া', 'Draft'),
  pendingReview('PENDING_REVIEW', 'পর্যালোচনার অপেক্ষায়', 'Pending Review'),
  active('ACTIVE', 'সক্রিয় ও অনুমোদিত', 'Active & Approved'),
  suspended('SUSPENDED', 'স্থগিত', 'Suspended'),
  inactive('INACTIVE', 'নিষ্ক্রিয়', 'Inactive'),
  rejected('REJECTED', 'বাতিল / প্রত্যাখ্যান', 'Rejected');

  final String value;
  final String labelBn;
  final String labelEn;

  const ProviderStatus(this.value, this.labelBn, this.labelEn);

  static ProviderStatus fromString(String? val) {
    return ProviderStatus.values.firstWhere(
      (e) => e.value == val,
      orElse: () => ProviderStatus.draft,
    );
  }
}

/// Verification status
enum VerificationStatus {
  unverified('UNVERIFIED', 'অযাচাইকৃত', 'Unverified'),
  pending('PENDING', 'যাচাই পর্যালোচনায়', 'Verification Pending'),
  verified('VERIFIED', 'যাচাইকৃত', 'Verified'),
  rejected('REJECTED', 'প্রত্যাখ্যাত', 'Rejected'),
  expired('EXPIRED', 'মেয়াদোত্তীর্ণ', 'Expired');

  final String value;
  final String labelBn;
  final String labelEn;

  const VerificationStatus(this.value, this.labelBn, this.labelEn);

  static VerificationStatus fromString(String? val) {
    return VerificationStatus.values.firstWhere(
      (e) => e.value == val,
      orElse: () => VerificationStatus.unverified,
    );
  }
}

/// Real-time / Operational availability
enum AvailabilityStatus {
  available('AVAILABLE', 'উপলব্ধ', 'Available'),
  busy('BUSY', 'ব্যস্ত', 'Busy'),
  temporarilyUnavailable('TEMPORARILY_UNAVAILABLE', 'সাময়িক অনুপলব্ধ', 'Temporarily Unavailable'),
  offline('OFFLINE', 'অফলাইন', 'Offline');

  final String value;
  final String labelBn;
  final String labelEn;

  const AvailabilityStatus(this.value, this.labelBn, this.labelEn);

  static AvailabilityStatus fromString(String? val) {
    return AvailabilityStatus.values.firstWhere(
      (e) => e.value == val,
      orElse: () => AvailabilityStatus.available,
    );
  }
}

/// Contact visibility privacy policy
enum ContactVisibility {
  public('PUBLIC', 'সবার জন্য উন্মুক্ত', 'Public'),
  registeredOnly('REGISTERED_ONLY', 'কেবল লগইনকৃত ব্যবহারকারী', 'Registered Users Only'),
  onRequest('ON_REQUEST', 'অনুরোধের পর', 'On Request Only'),
  hidden('HIDDEN', 'গোপন', 'Hidden');

  final String value;
  final String labelBn;
  final String labelEn;

  const ContactVisibility(this.value, this.labelBn, this.labelEn);

  static ContactVisibility fromString(String? val) {
    return ContactVisibility.values.firstWhere(
      (e) => e.value == val,
      orElse: () => ContactVisibility.registeredOnly,
    );
  }
}

/// Price strategy
enum PriceType {
  startingFrom('STARTING_FROM', 'শুরু থেকে', 'Starting From'),
  fixed('FIXED', 'নির্দিষ্ট মূল্য', 'Fixed Price'),
  hourly('HOURLY', 'প্রতি ঘণ্টা', 'Hourly Rate'),
  daily('DAILY', 'প্রতি দিন', 'Daily Rate'),
  perUnit('PER_UNIT', 'প্রতি একক', 'Per Unit'),
  negotiable('NEGOTIABLE', 'আলোচনা সাপেক্ষে', 'Negotiable');

  final String value;
  final String labelBn;
  final String labelEn;

  const PriceType(this.value, this.labelBn, this.labelEn);

  static PriceType fromString(String? val) {
    return PriceType.values.firstWhere(
      (e) => e.value == val,
      orElse: () => PriceType.startingFrom,
    );
  }
}
