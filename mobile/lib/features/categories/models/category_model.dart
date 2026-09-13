/// Universal Category Model for Flutter.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

class CategoryItem {
  final int id;
  final String nameBn;
  final String nameEn;
  final String slug;
  final String icon;
  final String descriptionBn;
  final String descriptionEn;
  final int? parentId;
  final int level;
  final int sortOrder;
  final String kind;
  final bool isActive;
  final bool isFeatured;
  final int activeChildrenCount;
  final int activeServicesCount;
  final List<CategoryItem> children;

  const CategoryItem({
    required this.id,
    required this.nameBn,
    required this.nameEn,
    required this.slug,
    required this.icon,
    this.descriptionBn = '',
    this.descriptionEn = '',
    this.parentId,
    this.level = 0,
    this.sortOrder = 0,
    this.kind = 'PUBLIC_SERVICE_CATEGORY',
    this.isActive = true,
    this.isFeatured = false,
    this.activeChildrenCount = 0,
    this.activeServicesCount = 0,
    this.children = const [],
  });

  factory CategoryItem.fromJson(Map<String, dynamic> json) {
    var rawChildren = json['children'] as List<dynamic>? ?? [];
    List<CategoryItem> parsedChildren = rawChildren
        .map((c) => CategoryItem.fromJson(c as Map<String, dynamic>))
        .toList();

    return CategoryItem(
      id: json['id'] as int,
      nameBn: json['name_bn'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      slug: json['slug'] as String? ?? '',
      icon: json['icon'] as String? ?? 'grid',
      descriptionBn: json['description_bn'] as String? ?? '',
      descriptionEn: json['description_en'] as String? ?? '',
      parentId: json['parent_id'] as int? ?? json['parent'] as int?,
      level: json['level'] as int? ?? 0,
      sortOrder: json['sort_order'] as int? ?? 0,
      kind: json['kind'] as String? ?? 'PUBLIC_SERVICE_CATEGORY',
      isActive: json['is_active'] as bool? ?? true,
      isFeatured: json['is_featured'] as bool? ?? false,
      activeChildrenCount: json['active_children_count'] as int? ?? parsedChildren.length,
      activeServicesCount: json['active_services_count'] as int? ?? json['services_count'] as int? ?? 0,
      children: parsedChildren,
    );
  }

  bool get isPublicServiceCategory => kind == 'PUBLIC_SERVICE_CATEGORY';
  bool get isSystemDomain => kind == 'SYSTEM_DOMAIN';
  bool get hasChildren => children.isNotEmpty || activeChildrenCount > 0;
}
