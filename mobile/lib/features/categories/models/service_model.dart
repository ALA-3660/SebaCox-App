/// Universal Service Model for Flutter.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"

class ServiceItem {
  final int id;
  final int categoryId;
  final String categoryNameBn;
  final String categoryNameEn;
  final String nameBn;
  final String nameEn;
  final String slug;
  final String shortDescriptionBn;
  final String shortDescriptionEn;
  final String icon;
  final String serviceType;

  // Capability Flags (Single source of truth from backend)
  final bool requiresBooking;
  final bool supportsDemand;
  final bool supportsOffer;
  final bool supportsNegotiation;
  final bool supportsDelivery;
  final bool supportsLocation;
  final bool supportsOnline;
  final bool supportsOrder;
  final bool supportsRental;
  final bool supportsPayment;

  final bool isActive;
  final bool isFeatured;
  final int sortOrder;

  const ServiceItem({
    required this.id,
    required this.categoryId,
    required this.categoryNameBn,
    required this.categoryNameEn,
    required this.nameBn,
    required this.nameEn,
    required this.slug,
    this.shortDescriptionBn = '',
    this.shortDescriptionEn = '',
    this.icon = 'tool',
    this.serviceType = 'SERVICE',
    this.requiresBooking = false,
    this.supportsDemand = false,
    this.supportsOffer = false,
    this.supportsNegotiation = false,
    this.supportsDelivery = false,
    this.supportsLocation = true,
    this.supportsOnline = false,
    this.supportsOrder = false,
    this.supportsRental = false,
    this.supportsPayment = false,
    this.isActive = true,
    this.isFeatured = false,
    this.sortOrder = 0,
  });

  factory ServiceItem.fromJson(Map<String, dynamic> json) {
    var catDetail = json['category_detail'] as Map<String, dynamic>?;
    return ServiceItem(
      id: json['id'] as int,
      categoryId: json['category'] as int? ?? catDetail?['id'] as int? ?? 0,
      categoryNameBn: json['category_name_bn'] as String? ?? catDetail?['name_bn'] as String? ?? '',
      categoryNameEn: json['category_name_en'] as String? ?? catDetail?['name_en'] as String? ?? '',
      nameBn: json['name_bn'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      slug: json['slug'] as String? ?? '',
      shortDescriptionBn: json['short_description_bn'] as String? ?? '',
      shortDescriptionEn: json['short_description_en'] as String? ?? '',
      icon: json['icon'] as String? ?? 'tool',
      serviceType: json['service_type'] as String? ?? 'SERVICE',
      requiresBooking: json['requires_booking'] as bool? ?? false,
      supportsDemand: json['supports_demand'] as bool? ?? false,
      supportsOffer: json['supports_offer'] as bool? ?? false,
      supportsNegotiation: json['supports_negotiation'] as bool? ?? false,
      supportsDelivery: json['supports_delivery'] as bool? ?? false,
      supportsLocation: json['supports_location'] as bool? ?? true,
      supportsOnline: json['supports_online'] as bool? ?? false,
      supportsOrder: json['supports_order'] as bool? ?? false,
      supportsRental: json['supports_rental'] as bool? ?? false,
      supportsPayment: json['supports_payment'] as bool? ?? false,
      isActive: json['is_active'] as bool? ?? true,
      isFeatured: json['is_featured'] as bool? ?? false,
      sortOrder: json['sort_order'] as int? ?? 0,
    );
  }

  /// Human-friendly Bangla badge labels for active capabilities
  List<String> get capabilityBadges {
    List<String> badges = [];
    if (requiresBooking) badges.add('বুকিং প্রযোজ্য');
    if (supportsDemand) badges.add('চাহিদা পাঠানো যাবে');
    if (supportsNegotiation) badges.add('দর কষাকষি');
    if (supportsDelivery) badges.add('ডেলিভারি সুবিধা');
    if (supportsRental) badges.add('ভাড়া সেবা');
    if (supportsOrder) badges.add('সরাসরি অর্ডার');
    if (supportsOnline) badges.add('অনলাইন সেবা');
    return badges;
  }
}
