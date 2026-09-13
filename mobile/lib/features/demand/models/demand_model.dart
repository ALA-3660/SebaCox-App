/// Production-ready Demand Model / “আমার প্রয়োজন” for Flutter client.
/// Architecture: User -> Demand -> Service -> Location
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
/// "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
library;

import 'demand_enums.dart';

class DemandModel {
  final int id;
  final int requesterId;
  final String requesterName;
  final String? contactPhone;
  final String titleBn;
  final String? titleEn;
  final String descriptionBn;
  final String? descriptionEn;
  final DemandType demandType;
  final DemandStatus status;
  final DemandPriority priority;
  final int? serviceId;
  final String? serviceNameBn;
  final String? serviceNameEn;
  final int? categoryId;
  final String? categoryNameBn;
  final double? quantity;
  final String? unit;
  final double? budgetMin;
  final double? budgetMax;
  final String currency;
  final DateTime? requiredAt;
  final DateTime? expiresAt;
  final int? districtId;
  final String? districtNameBn;
  final int? upazilaId;
  final String? upazilaNameBn;
  final String? locationDisplayBn;
  final DemandVisibility visibility;
  final DemandContactPreference contactPreference;
  final bool isOwner;
  final bool canEdit;
  final DateTime? publishedAt;
  final DateTime createdAt;

  const DemandModel({
    required this.id,
    required this.requesterId,
    required this.requesterName,
    this.contactPhone,
    required this.titleBn,
    this.titleEn,
    required this.descriptionBn,
    this.descriptionEn,
    required this.demandType,
    required this.status,
    required this.priority,
    this.serviceId,
    this.serviceNameBn,
    this.serviceNameEn,
    this.categoryId,
    this.categoryNameBn,
    this.quantity,
    this.unit,
    this.budgetMin,
    this.budgetMax,
    this.currency = 'BDT',
    this.requiredAt,
    this.expiresAt,
    this.districtId,
    this.districtNameBn,
    this.upazilaId,
    this.upazilaNameBn,
    this.locationDisplayBn,
    this.visibility = DemandVisibility.public,
    this.contactPreference = DemandContactPreference.inAppOnly,
    this.isOwner = false,
    this.canEdit = false,
    this.publishedAt,
    required this.createdAt,
  });

  factory DemandModel.fromJson(Map<String, dynamic> json) {
    return DemandModel(
      id: json['id'] as int? ?? 0,
      requesterId: json['requester_id'] as int? ?? 0,
      requesterName: json['requester_name'] as String? ?? 'ব্যবহারকারী',
      contactPhone: json['contact_phone'] as String?,
      titleBn: json['title_bn'] as String? ?? '',
      titleEn: json['title_en'] as String?,
      descriptionBn: json['description_bn'] as String? ?? '',
      descriptionEn: json['description_en'] as String?,
      demandType: DemandType.fromString(json['demand_type'] as String?),
      status: DemandStatus.fromString(json['status'] as String?),
      priority: DemandPriority.fromString(json['priority'] as String?),
      serviceId: json['service_id'] as int?,
      serviceNameBn: json['service_name_bn'] as String?,
      serviceNameEn: json['service_name_en'] as String?,
      categoryId: json['category_id'] as int?,
      categoryNameBn: json['category_name_bn'] as String?,
      quantity: json['quantity'] != null ? double.tryParse(json['quantity'].toString()) : null,
      unit: json['unit'] as String?,
      budgetMin: json['budget_min'] != null ? double.tryParse(json['budget_min'].toString()) : null,
      budgetMax: json['budget_max'] != null ? double.tryParse(json['budget_max'].toString()) : null,
      currency: json['currency'] as String? ?? 'BDT',
      requiredAt: json['required_at'] != null ? DateTime.tryParse(json['required_at'].toString()) : null,
      expiresAt: json['expires_at'] != null ? DateTime.tryParse(json['expires_at'].toString()) : null,
      districtId: json['district_id'] as int?,
      districtNameBn: json['district_name_bn'] as String?,
      upazilaId: json['upazila_id'] as int?,
      upazilaNameBn: json['upazila_name_bn'] as String?,
      locationDisplayBn: json['location_display_bn'] as String?,
      visibility: DemandVisibility.fromString(json['visibility'] as String?),
      contactPreference: DemandContactPreference.fromString(json['contact_preference'] as String?),
      isOwner: json['is_owner'] as bool? ?? false,
      canEdit: json['can_edit'] as bool? ?? false,
      publishedAt: json['published_at'] != null ? DateTime.tryParse(json['published_at'].toString()) : null,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'].toString()) ?? DateTime.now()
          : DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title_bn': titleBn,
      'title_en': titleEn,
      'description_bn': descriptionBn,
      'demand_type': demandType.value,
      'priority': priority.value,
      'service_id': serviceId,
      'category_id': categoryId,
      'quantity': quantity,
      'unit': unit,
      'budget_min': budgetMin,
      'budget_max': budgetMax,
      'currency': currency,
      'required_at': requiredAt?.toIso8601String(),
      'expires_at': expiresAt?.toIso8601String(),
      'upazila_id': upazilaId,
      'location_display_bn': locationDisplayBn,
      'visibility': visibility.value,
      'contact_preference': contactPreference.value,
    };
  }

  String get budgetDisplay {
    if (budgetMin != null && budgetMax != null) {
      return '৳${budgetMin!.toInt()} - ৳${budgetMax!.toInt()}';
    } else if (budgetMin != null) {
      return '৳${budgetMin!.toInt()}+';
    } else if (budgetMax != null) {
      return 'সর্বোচ্চ ৳${budgetMax!.toInt()}';
    }
    return 'আলোচনা সাপেক্ষে';
  }
}
