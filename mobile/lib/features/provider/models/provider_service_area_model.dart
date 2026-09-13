/// Provider Service Area Model for SebaCox.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

class ProviderServiceAreaItem {
  final int id;
  final int? providerId;
  final String areaType;
  final int? districtId;
  final String? districtNameBn;
  final String? districtNameEn;
  final int? upazilaId;
  final String? upazilaNameBn;
  final String? upazilaNameEn;
  final int? municipalityId;
  final int? unionId;
  final String? unionNameBn;
  final int? wardId;
  final int? localityId;
  final double? radiusKm;
  final double? centerLatitude;
  final double? centerLongitude;
  final bool isActive;
  final DateTime? createdAt;

  const ProviderServiceAreaItem({
    required this.id,
    this.providerId,
    this.areaType = 'ADMINISTRATIVE',
    this.districtId,
    this.districtNameBn,
    this.districtNameEn,
    this.upazilaId,
    this.upazilaNameBn,
    this.upazilaNameEn,
    this.municipalityId,
    this.unionId,
    this.unionNameBn,
    this.wardId,
    this.localityId,
    this.radiusKm,
    this.centerLatitude,
    this.centerLongitude,
    this.isActive = true,
    this.createdAt,
  });

  String get displayNameBn {
    if (upazilaNameBn != null && upazilaNameBn!.isNotEmpty) {
      if (districtNameBn != null && districtNameBn!.isNotEmpty) {
        return '$upazilaNameBn, $districtNameBn';
      }
      return upazilaNameBn!;
    }
    if (districtNameBn != null && districtNameBn!.isNotEmpty) {
      return districtNameBn!;
    }
    if (radiusKm != null) {
      return '$radiusKm কিমি ব্যাসার্ধ এলাকা';
    }
    return 'নির্দিষ্ট এলাকা';
  }

  factory ProviderServiceAreaItem.fromJson(Map<String, dynamic> json) {
    return ProviderServiceAreaItem(
      id: json['id'] as int? ?? 0,
      providerId: json['provider_id'] as int?,
      areaType: json['area_type'] as String? ?? 'ADMINISTRATIVE',
      districtId: json['district'] as int?,
      districtNameBn: json['district_name_bn'] as String?,
      districtNameEn: json['district_name_en'] as String?,
      upazilaId: json['upazila'] as int?,
      upazilaNameBn: json['upazila_name_bn'] as String?,
      upazilaNameEn: json['upazila_name_en'] as String?,
      municipalityId: json['municipality'] as int?,
      unionId: json['union'] as int?,
      unionNameBn: json['union_name_bn'] as String?,
      wardId: json['ward'] as int?,
      localityId: json['locality'] as int?,
      radiusKm: json['radius_km'] != null ? double.tryParse(json['radius_km'].toString()) : null,
      centerLatitude: json['center_latitude'] != null ? double.tryParse(json['center_latitude'].toString()) : null,
      centerLongitude: json['center_longitude'] != null ? double.tryParse(json['center_longitude'].toString()) : null,
      isActive: json['is_active'] as bool? ?? true,
      createdAt: json['created_at'] != null ? DateTime.tryParse(json['created_at'] as String) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'area_type': areaType,
      'district': districtId,
      'upazila': upazilaId,
      'municipality': municipalityId,
      'union': unionId,
      'radius_km': radiusKm,
      'is_active': isActive,
    };
  }
}
