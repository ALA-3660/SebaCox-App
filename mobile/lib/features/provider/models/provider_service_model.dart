/// Provider Service Model for SebaCox.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

import 'provider_enums.dart';

class ProviderServiceItem {
  final int id;
  final int? providerId;
  final int serviceId;
  final String serviceNameBn;
  final String serviceNameEn;
  final String serviceSlug;
  final int? categoryId;
  final String? categoryNameBn;
  final String titleBn;
  final String titleEn;
  final String descriptionBn;
  final String descriptionEn;
  final double? startingPrice;
  final PriceType priceType;
  final bool isAvailable;
  final bool isActive;
  final Map<String, dynamic> capabilities;
  final DateTime? createdAt;

  const ProviderServiceItem({
    required this.id,
    this.providerId,
    required this.serviceId,
    required this.serviceNameBn,
    required this.serviceNameEn,
    required this.serviceSlug,
    this.categoryId,
    this.categoryNameBn,
    this.titleBn = '',
    this.titleEn = '',
    this.descriptionBn = '',
    this.descriptionEn = '',
    this.startingPrice,
    this.priceType = PriceType.startingFrom,
    this.isAvailable = true,
    this.isActive = true,
    this.capabilities = const {},
    this.createdAt,
  });

  String get effectiveTitleBn => titleBn.isNotEmpty ? titleBn : serviceNameBn;
  String get effectiveTitleEn => titleEn.isNotEmpty ? titleEn : serviceNameEn;

  factory ProviderServiceItem.fromJson(Map<String, dynamic> json) {
    return ProviderServiceItem(
      id: json['id'] as int? ?? 0,
      providerId: json['provider_id'] as int?,
      serviceId: json['service'] as int? ?? json['service_id'] as int? ?? 0,
      serviceNameBn: json['service_name_bn'] as String? ?? '',
      serviceNameEn: json['service_name_en'] as String? ?? '',
      serviceSlug: json['service_slug'] as String? ?? '',
      categoryId: json['category_id'] as int?,
      categoryNameBn: json['category_name_bn'] as String?,
      titleBn: json['title_bn'] as String? ?? '',
      titleEn: json['title_en'] as String? ?? '',
      descriptionBn: json['description_bn'] as String? ?? '',
      descriptionEn: json['description_en'] as String? ?? '',
      startingPrice: json['starting_price'] != null
          ? double.tryParse(json['starting_price'].toString())
          : null,
      priceType: PriceType.fromString(json['price_type'] as String?),
      isAvailable: json['is_available'] as bool? ?? true,
      isActive: json['is_active'] as bool? ?? true,
      capabilities: (json['capabilities'] as Map<String, dynamic>?) ?? const {},
      createdAt: json['created_at'] != null ? DateTime.tryParse(json['created_at'] as String) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'service_id': serviceId,
      'title_bn': titleBn,
      'title_en': titleEn,
      'description_bn': descriptionBn,
      'description_en': descriptionEn,
      'starting_price': startingPrice,
      'price_type': priceType.value,
      'is_available': isAvailable,
      'is_active': isActive,
    };
  }
}
