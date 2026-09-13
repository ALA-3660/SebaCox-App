/// Enums for SebaCox Demand Engine / “আমার প্রয়োজন”.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
/// "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
library;

/// Demand classification types
enum DemandType {
  service('SERVICE', 'সেবামূলক প্রয়োজন', 'Service Demand'),
  product('PRODUCT', 'পণ্য সামগ্রী প্রয়োজন', 'Product Demand'),
  rental('RENTAL', 'ভাড়া বা রেন্টাল', 'Rental Demand'),
  booking('BOOKING', 'অগ্রিম বুকিং', 'Booking'),
  marketplace('MARKETPLACE', 'মার্কেটপ্লেস ক্রয়/বিক্রয়', 'Marketplace'),
  information('INFORMATION', 'তথ্য বা পরামর্শ', 'Information'),
  other('OTHER', 'অন্যান্য প্রয়োজন', 'Other');

  final String value;
  final String labelBn;
  final String labelEn;

  const DemandType(this.value, this.labelBn, this.labelEn);

  static DemandType fromString(String? val) {
    return DemandType.values.firstWhere(
      (e) => e.value == val,
      orElse: () => DemandType.service,
    );
  }
}

/// Controlled Lifecycle Status
enum DemandStatus {
  draft('DRAFT', 'খসড়া', 'Draft'),
  published('PUBLISHED', 'প্রকাশিত', 'Published'),
  paused('PAUSED', 'সাময়িক বন্ধ', 'Paused'),
  fulfilled('FULFILLED', 'প্রয়োজন পূরণ হয়েছে', 'Fulfilled'),
  cancelled('CANCELLED', 'বাতিল', 'Cancelled'),
  expired('EXPIRED', 'মেয়াদ শেষ', 'Expired'),
  closed('CLOSED', 'বন্ধ', 'Closed');

  final String value;
  final String labelBn;
  final String labelEn;

  const DemandStatus(this.value, this.labelBn, this.labelEn);

  static DemandStatus fromString(String? val) {
    return DemandStatus.values.firstWhere(
      (e) => e.value == val,
      orElse: () => DemandStatus.draft,
    );
  }

  bool get isEditable => this == draft || this == published || this == paused;
  bool get isHistorical => this == fulfilled || this == cancelled || this == expired || this == closed;
}

/// Urgency Priority
enum DemandPriority {
  normal('NORMAL', 'সাধারণ', 'Normal'),
  urgent('URGENT', 'জরুরি', 'Urgent');

  final String value;
  final String labelBn;
  final String labelEn;

  const DemandPriority(this.value, this.labelBn, this.labelEn);

  static DemandPriority fromString(String? val) {
    return DemandPriority.values.firstWhere(
      (e) => e.value == val,
      orElse: () => DemandPriority.normal,
    );
  }
}

/// Visibility scope
enum DemandVisibility {
  public('PUBLIC', 'সবার জন্য উন্মুক্ত', 'Public'),
  registeredUsers('REGISTERED_USERS', 'নিবন্ধিত ব্যবহারকারী', 'Registered Users Only'),
  private('PRIVATE', 'ব্যক্তিগত', 'Private');

  final String value;
  final String labelBn;
  final String labelEn;

  const DemandVisibility(this.value, this.labelBn, this.labelEn);

  static DemandVisibility fromString(String? val) {
    return DemandVisibility.values.firstWhere(
      (e) => e.value == val,
      orElse: () => DemandVisibility.public,
    );
  }
}

/// Contact channel preferences
enum DemandContactPreference {
  inAppOnly('IN_APP_ONLY', 'ইন-অ্যাপ বার্তা', 'In-App Only'),
  phone('PHONE', 'সরাসরি ফোন', 'Direct Phone'),
  both('BOTH', 'ফোন ও ইন-অ্যাপ', 'Both Phone & In-App');

  final String value;
  final String labelBn;
  final String labelEn;

  const DemandContactPreference(this.value, this.labelBn, this.labelEn);

  static DemandContactPreference fromString(String? val) {
    return DemandContactPreference.values.firstWhere(
      (e) => e.value == val,
      orElse: () => DemandContactPreference.inAppOnly,
    );
  }
}
