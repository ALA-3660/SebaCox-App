/// Geographic hierarchy models for Flutter.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

class GeographicItem {
  final int id;
  final String nameBn;
  final String nameEn;
  final String code;
  final int? parentId;
  final bool isActive;

  const GeographicItem({
    required this.id,
    required this.nameBn,
    required this.nameEn,
    required this.code,
    this.parentId,
    this.isActive = true,
  });

  factory GeographicItem.fromJson(Map<String, dynamic> json, {String? parentKey}) {
    return GeographicItem(
      id: json['id'] as int,
      nameBn: json['name_bn'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      code: json['code'] as String? ?? '',
      parentId: parentKey != null ? json[parentKey] as int? : null,
      isActive: json['is_active'] as bool? ?? true,
    );
  }

  String get displayName => '$nameBn ($nameEn)';
}

class LocationSearchResult {
  final int id;
  final String type;
  final String typeLabel;
  final String nameBn;
  final String nameEn;
  final String code;
  final String hierarchyPath;
  final String hierarchyPathEn;
  final int? parentId;
  final String? postalCode;

  const LocationSearchResult({
    required this.id,
    required this.type,
    required this.typeLabel,
    required this.nameBn,
    required this.nameEn,
    required this.code,
    required this.hierarchyPath,
    required this.hierarchyPathEn,
    this.parentId,
    this.postalCode,
  });

  factory LocationSearchResult.fromJson(Map<String, dynamic> json) {
    return LocationSearchResult(
      id: json['id'] as int,
      type: json['type'] as String? ?? '',
      typeLabel: json['type_label'] as String? ?? '',
      nameBn: json['name_bn'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      code: json['code'] as String? ?? '',
      hierarchyPath: json['hierarchy_path'] as String? ?? '',
      hierarchyPathEn: json['hierarchy_path_en'] as String? ?? '',
      parentId: json['parent_id'] as int?,
      postalCode: json['postal_code'] as String?,
    );
  }
}
