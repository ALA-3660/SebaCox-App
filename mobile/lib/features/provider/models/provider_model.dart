/// Provider Profile Model for SebaCox.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

import 'provider_enums.dart';
import 'provider_service_model.dart';
import 'provider_service_area_model.dart';

class ProviderProfile {
  final int id;
  final int userId;
  final ProviderType providerType;
  final String displayNameBn;
  final String displayNameEn;
  final String slug;
  final String shortDescriptionBn;
  final String shortDescriptionEn;
  final String descriptionBn;
  final String descriptionEn;
  final String profileImage;
  final String coverImage;
  final String? contactPhone;
  final String? safeContactPhone;
  final String? contactEmail;
  final ContactVisibility contactVisibility;
  final ProviderStatus status;
  final bool isVerified;
  final VerificationStatus verificationStatus;
  final AvailabilityStatus availabilityStatus;
  final bool isFeatured;
  final bool isActive;
  final int servicesCount;
  final List<ProviderServiceItem> services;
  final List<ProviderServiceAreaItem> serviceAreas;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  const ProviderProfile({
    required this.id,
    required this.userId,
    this.providerType = ProviderType.individual,
    required this.displayNameBn,
    required this.displayNameEn,
    required this.slug,
    this.shortDescriptionBn = '',
    this.shortDescriptionEn = '',
    this.descriptionBn = '',
    this.descriptionEn = '',
    this.profileImage = '',
    this.coverImage = '',
    this.contactPhone,
    this.safeContactPhone,
    this.contactEmail,
    this.contactVisibility = ContactVisibility.registeredOnly,
    this.status = ProviderStatus.draft,
    this.isVerified = false,
    this.verificationStatus = VerificationStatus.unverified,
    this.availabilityStatus = AvailabilityStatus.available,
    this.isFeatured = false,
    this.isActive = true,
    this.servicesCount = 0,
    this.services = const [],
    this.serviceAreas = const [],
    this.createdAt,
    this.updatedAt,
  });

  bool get isOperational => status == ProviderStatus.active && isActive;

  factory ProviderProfile.fromJson(Map<String, dynamic> json) {
    var rawServices = json['services'] as List<dynamic>? ?? [];
    var parsedServices = rawServices
        .map((s) => ProviderServiceItem.fromJson(s as Map<String, dynamic>))
        .toList();

    var rawAreas = json['service_areas'] as List<dynamic>? ?? [];
    var parsedAreas = rawAreas
        .map((a) => ProviderServiceAreaItem.fromJson(a as Map<String, dynamic>))
        .toList();

    return ProviderProfile(
      id: json['id'] as int? ?? 0,
      userId: json['user_id'] as int? ?? 0,
      providerType: ProviderType.fromString(json['provider_type'] as String?),
      displayNameBn: json['display_name_bn'] as String? ?? '',
      displayNameEn: json['display_name_en'] as String? ?? '',
      slug: json['slug'] as String? ?? '',
      shortDescriptionBn: json['short_description_bn'] as String? ?? '',
      shortDescriptionEn: json['short_description_en'] as String? ?? '',
      descriptionBn: json['description_bn'] as String? ?? '',
      descriptionEn: json['description_en'] as String? ?? '',
      profileImage: json['profile_image'] as String? ?? '',
      coverImage: json['cover_image'] as String? ?? '',
      contactPhone: json['contact_phone'] as String?,
      safeContactPhone: json['safe_contact_phone'] as String?,
      contactEmail: json['contact_email'] as String?,
      contactVisibility: ContactVisibility.fromString(json['contact_visibility'] as String?),
      status: ProviderStatus.fromString(json['status'] as String?),
      isVerified: json['is_verified'] as bool? ?? false,
      verificationStatus: VerificationStatus.fromString(json['verification_status'] as String?),
      availabilityStatus: AvailabilityStatus.fromString(json['availability_status'] as String?),
      isFeatured: json['is_featured'] as bool? ?? false,
      isActive: json['is_active'] as bool? ?? true,
      servicesCount: json['services_count'] as int? ?? parsedServices.length,
      services: parsedServices,
      serviceAreas: parsedAreas,
      createdAt: json['created_at'] != null ? DateTime.tryParse(json['created_at'] as String) : null,
      updatedAt: json['updated_at'] != null ? DateTime.tryParse(json['updated_at'] as String) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'provider_type': providerType.value,
      'display_name_bn': displayNameBn,
      'display_name_en': displayNameEn,
      'slug': slug,
      'short_description_bn': shortDescriptionBn,
      'short_description_en': shortDescriptionEn,
      'description_bn': descriptionBn,
      'description_en': descriptionEn,
      'profile_image': profileImage,
      'cover_image': coverImage,
      'contact_phone': contactPhone,
      'contact_visibility': contactVisibility.value,
      'status': status.value,
      'availability_status': availabilityStatus.value,
    };
  }
}
