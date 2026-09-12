/// User location association model for Flutter.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
import 'geo_point.dart';

class UserLocationModel {
  final int id;
  final String locationType;
  final String label;
  final bool isDefault;
  final bool isActive;
  final int? districtId;
  final String? districtName;
  final String? districtNameBn;
  final int? upazilaId;
  final String? upazilaName;
  final String? upazilaNameBn;
  final int? unionId;
  final String? unionName;
  final int? municipalityId;
  final String? municipalityName;
  final int? wardId;
  final int? localityId;
  final String? localityName;
  final GeoPoint? geoLocation;
  final DateTime? createdAt;

  const UserLocationModel({
    required this.id,
    required this.locationType,
    this.label = '',
    this.isDefault = false,
    this.isActive = true,
    this.districtId,
    this.districtName,
    this.districtNameBn,
    this.upazilaId,
    this.upazilaName,
    this.upazilaNameBn,
    this.unionId,
    this.unionName,
    this.municipalityId,
    this.municipalityName,
    this.wardId,
    this.localityId,
    this.localityName,
    this.geoLocation,
    this.createdAt,
  });

  factory UserLocationModel.fromJson(Map<String, dynamic> json) {
    return UserLocationModel(
      id: json['id'] as int? ?? 0,
      locationType: json['location_type'] as String? ?? 'SELECTED',
      label: json['label'] as String? ?? '',
      isDefault: json['is_default'] as bool? ?? false,
      isActive: json['is_active'] as bool? ?? true,
      districtId: json['district'] as int?,
      districtName: json['district_name'] as String?,
      districtNameBn: json['district_name_bn'] as String?,
      upazilaId: json['upazila'] as int?,
      upazilaName: json['upazila_name'] as String?,
      upazilaNameBn: json['upazila_name_bn'] as String?,
      unionId: json['union'] as int?,
      unionName: json['union_name'] as String?,
      municipalityId: json['municipality'] as int?,
      municipalityName: json['municipality_name'] as String?,
      wardId: json['ward'] as int?,
      localityId: json['locality'] as int?,
      localityName: json['locality_name'] as String?,
      geoLocation: json['geo_location'] != null
          ? GeoPoint.fromJson(json['geo_location'] as Map<String, dynamic>)
          : null,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'].toString())
          : null,
    );
  }

  /// Human-readable display text in Bengali
  String get displayAddressBn {
    final parts = <String>[];
    if (localityName != null && localityName!.isNotEmpty) parts.add(localityName!);
    if (municipalityName != null && municipalityName!.isNotEmpty) parts.add(municipalityName!);
    if (unionName != null && unionName!.isNotEmpty) parts.add(unionName!);
    if (upazilaNameBn != null && upazilaNameBn!.isNotEmpty) parts.add(upazilaNameBn!);
    if (districtNameBn != null && districtNameBn!.isNotEmpty) parts.add(districtNameBn!);

    if (parts.isEmpty && geoLocation != null) {
      return geoLocation!.addressText.isNotEmpty
          ? geoLocation!.addressText
          : '${geoLocation!.latitude.toStringAsFixed(4)}, ${geoLocation!.longitude.toStringAsFixed(4)}';
    }
    return parts.join(', ');
  }
}
