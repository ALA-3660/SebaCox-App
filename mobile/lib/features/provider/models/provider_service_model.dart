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
  final int? subcategoryId;
  final String? subcategoryNameBn;
  final String titleBn;
  final String titleEn;
  final String descriptionBn;
  final String descriptionEn;
  final double? startingPrice;
  final double? maxPrice;
  final PriceType priceType;
  final String unitBn;
  final String unitEn;
  final int? experienceYears;
  final bool isEmergencyAvailable;
  final double? emergencyFee;
  final String warrantyTextBn;
  final String warrantyTextEn;
  final List<String> skills;
  final String customSpecialty;
  final List<String> tags;
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
    this.subcategoryId,
    this.subcategoryNameBn,
    this.titleBn = '',
    this.titleEn = '',
    this.descriptionBn = '',
    this.descriptionEn = '',
    this.startingPrice,
    this.maxPrice,
    this.priceType = PriceType.startingFrom,
    this.unitBn = '',
    this.unitEn = '',
    this.experienceYears,
    this.isEmergencyAvailable = false,
    this.emergencyFee,
    this.warrantyTextBn = '',
    this.warrantyTextEn = '',
    this.skills = const [],
    this.customSpecialty = '',
    this.tags = const [],
    this.isAvailable = true,
    this.isActive = true,
    this.capabilities = const {},
    this.createdAt,
  });

  String get effectiveTitleBn => titleBn.isNotEmpty ? titleBn : serviceNameBn;
  String get effectiveTitleEn => titleEn.isNotEmpty ? titleEn : serviceNameEn;

  String get formattedPriceString {
    if (startingPrice == null) return 'আলোচনা সাপেক্ষে';
    final priceStr = '৳${startingPrice!.toStringAsFixed(0)}';
    final unitStr = unitBn.isNotEmpty ? '/$unitBn' : '';
    switch (priceType) {
      case PriceType.fixed:
        return '$priceStr (নির্দিষ্ট $unitStr)';
      case PriceType.hourly:
        return '$priceStr (প্রতি ঘণ্টা)';
      case PriceType.daily:
        return '$priceStr (প্রতি দিন)';
      case PriceType.perUnit:
        return '$priceStr (প্রতি $unitStr)';
      case PriceType.visitingCharge:
        return '$priceStr (ভিজিট ফি)';
      case PriceType.negotiable:
        return 'আলোচনা সাপেক্ষে';
      case PriceType.startingFrom:
      default:
        return 'শুরু $priceStr $unitStr';
    }
  }

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
      subcategoryId: json['subcategory_id'] as int?,
      subcategoryNameBn: json['subcategory_name_bn'] as String?,
      titleBn: json['title_bn'] as String? ?? '',
      titleEn: json['title_en'] as String? ?? '',
      descriptionBn: json['description_bn'] as String? ?? '',
      descriptionEn: json['description_en'] as String? ?? '',
      startingPrice: json['starting_price'] != null
          ? double.tryParse(json['starting_price'].toString())
          : null,
      maxPrice: json['max_price'] != null
          ? double.tryParse(json['max_price'].toString())
          : null,
      priceType: PriceType.fromString(json['price_type'] as String?),
      unitBn: json['unit_bn'] as String? ?? '',
      unitEn: json['unit_en'] as String? ?? '',
      experienceYears: json['experience_years'] as int?,
      isEmergencyAvailable: json['is_emergency_available'] as bool? ?? false,
      emergencyFee: json['emergency_fee'] != null
          ? double.tryParse(json['emergency_fee'].toString())
          : null,
      warrantyTextBn: json['warranty_text_bn'] as String? ?? '',
      warrantyTextEn: json['warranty_text_en'] as String? ?? '',
      skills: (json['skills'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? const [],
      customSpecialty: json['custom_specialty'] as String? ?? '',
      tags: (json['tags'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? const [],
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
      'max_price': maxPrice,
      'price_type': priceType.value,
      'unit_bn': unitBn,
      'unit_en': unitEn,
      'experience_years': experienceYears,
      'is_emergency_available': isEmergencyAvailable,
      'emergency_fee': emergencyFee,
      'warranty_text_bn': warrantyTextBn,
      'warranty_text_en': warrantyTextEn,
      'skills': skills,
      'custom_specialty': customSpecialty,
      'tags': tags,
      'is_available': isAvailable,
      'is_active': isActive,
    };
  }
}

