/// Universal Category, SubCategory & Taxonomy Search Models for Flutter.
/// Master Taxonomy v1.0 Universal Hierarchy & Search Routing.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
/// "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

import 'service_model.dart';

class SubCategoryItem {
  final int id;
  final int categoryId;
  final String categoryNameBn;
  final String categoryNameEn;
  final String nameBn;
  final String nameEn;
  final String slug;
  final String icon;
  final String shortDescriptionBn;
  final String shortDescriptionEn;
  final int sortOrder;
  final bool isActive;
  final bool isPopular;
  final int servicesCount;

  const SubCategoryItem({
    required this.id,
    required this.categoryId,
    this.categoryNameBn = '',
    this.categoryNameEn = '',
    required this.nameBn,
    required this.nameEn,
    required this.slug,
    this.icon = 'layers',
    this.shortDescriptionBn = '',
    this.shortDescriptionEn = '',
    this.sortOrder = 0,
    this.isActive = true,
    this.isPopular = false,
    this.servicesCount = 0,
  });

  factory SubCategoryItem.fromJson(Map<String, dynamic> json) {
    return SubCategoryItem(
      id: json['id'] as int? ?? 0,
      categoryId: json['category_id'] as int? ?? json['category'] as int? ?? 0,
      categoryNameBn: json['category_name_bn'] as String? ?? '',
      categoryNameEn: json['category_name_en'] as String? ?? '',
      nameBn: json['name_bn'] as String? ?? '',
      nameEn: json['name_en'] as String? ?? '',
      slug: json['slug'] as String? ?? '',
      icon: json['icon'] as String? ?? 'layers',
      shortDescriptionBn: json['short_description_bn'] as String? ?? '',
      shortDescriptionEn: json['short_description_en'] as String? ?? '',
      sortOrder: json['sort_order'] as int? ?? 0,
      isActive: json['is_active'] as bool? ?? true,
      isPopular: json['is_popular'] as bool? ?? false,
      servicesCount: json['services_count'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'category_id': categoryId,
      'category_name_bn': categoryNameBn,
      'category_name_en': categoryNameEn,
      'name_bn': nameBn,
      'name_en': nameEn,
      'slug': slug,
      'icon': icon,
      'short_description_bn': shortDescriptionBn,
      'short_description_en': shortDescriptionEn,
      'sort_order': sortOrder,
      'is_active': isActive,
      'is_popular': isPopular,
      'services_count': servicesCount,
    };
  }
}

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
  final bool isPopular;
  final int activeSubcategoriesCount;
  final int activeServicesCount;
  final List<SubCategoryItem> subcategories;
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
    this.isPopular = false,
    this.activeSubcategoriesCount = 0,
    this.activeServicesCount = 0,
    this.subcategories = const [],
    this.children = const [],
  });

  factory CategoryItem.fromJson(Map<String, dynamic> json) {
    // Parse subcategories list
    var rawSubs = json['subcategories'] as List<dynamic>? ?? [];
    List<SubCategoryItem> parsedSubs = rawSubs
        .map((s) => SubCategoryItem.fromJson(s as Map<String, dynamic>))
        .toList();

    // Parse children list (backward compatibility)
    var rawChildren = json['children'] as List<dynamic>? ?? [];
    List<CategoryItem> parsedChildren = rawChildren
        .map((c) => CategoryItem.fromJson(c as Map<String, dynamic>))
        .toList();

    return CategoryItem(
      id: json['id'] as int? ?? 0,
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
      isPopular: json['is_popular'] as bool? ?? false,
      activeSubcategoriesCount: json['active_subcategories_count'] as int? ?? parsedSubs.length,
      activeServicesCount: json['active_services_count'] as int? ?? json['services_count'] as int? ?? 0,
      subcategories: parsedSubs,
      children: parsedChildren,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name_bn': nameBn,
      'name_en': nameEn,
      'slug': slug,
      'icon': icon,
      'description_bn': descriptionBn,
      'description_en': descriptionEn,
      'parent_id': parentId,
      'level': level,
      'sort_order': sortOrder,
      'kind': kind,
      'is_active': isActive,
      'is_featured': isFeatured,
      'is_popular': isPopular,
      'active_subcategories_count': activeSubcategoriesCount,
      'active_services_count': activeServicesCount,
      'subcategories': subcategories.map((s) => s.toJson()).toList(),
      'children': children.map((c) => c.toJson()).toList(),
    };
  }

  bool get isPublicServiceCategory => kind == 'PUBLIC_SERVICE_CATEGORY';
  bool get isSystemDomain => kind == 'SYSTEM_DOMAIN';
  bool get hasChildren => children.isNotEmpty || subcategories.isNotEmpty || activeSubcategoriesCount > 0;
  bool get hasSubcategories => subcategories.isNotEmpty;
}

class TaxonomyAliasItem {
  final int id;
  final String aliasText;
  final String normalizedText;
  final String targetType;
  final int targetId;
  final String categoryNameBn;
  final String subcategoryNameBn;
  final String language;
  final bool isActive;

  const TaxonomyAliasItem({
    required this.id,
    required this.aliasText,
    required this.normalizedText,
    required this.targetType,
    required this.targetId,
    this.categoryNameBn = '',
    this.subcategoryNameBn = '',
    this.language = 'BN',
    this.isActive = true,
  });

  factory TaxonomyAliasItem.fromJson(Map<String, dynamic> json) {
    return TaxonomyAliasItem(
      id: json['id'] as int? ?? 0,
      aliasText: json['alias_text'] as String? ?? '',
      normalizedText: json['normalized_text'] as String? ?? '',
      targetType: json['target_type'] as String? ?? '',
      targetId: json['target_id'] as int? ?? 0,
      categoryNameBn: json['category_name_bn'] as String? ?? '',
      subcategoryNameBn: json['subcategory_name_bn'] as String? ?? '',
      language: json['language'] as String? ?? 'BN',
      isActive: json['is_active'] as bool? ?? true,
    );
  }
}

class TaxonomySearchResult {
  final String query;
  final String normalized;
  final List<CategoryItem> categories;
  final List<SubCategoryItem> subcategories;
  final List<ServiceItem> services;
  final List<TaxonomyAliasItem> aliases;

  const TaxonomySearchResult({
    required this.query,
    this.normalized = '',
    this.categories = const [],
    this.subcategories = const [],
    this.services = const [],
    this.aliases = const [],
  });

  factory TaxonomySearchResult.fromJson(Map<String, dynamic> json) {
    var rawCats = json['categories'] as List<dynamic>? ?? [];
    var rawSubs = json['subcategories'] as List<dynamic>? ?? [];
    var rawServices = json['services'] as List<dynamic>? ?? [];
    var rawAliases = json['aliases'] as List<dynamic>? ?? [];

    return TaxonomySearchResult(
      query: json['query'] as String? ?? '',
      normalized: json['normalized'] as String? ?? '',
      categories: rawCats.map((c) => CategoryItem.fromJson(c as Map<String, dynamic>)).toList(),
      subcategories: rawSubs.map((s) => SubCategoryItem.fromJson(s as Map<String, dynamic>)).toList(),
      services: rawServices.map((sv) => ServiceItem.fromJson(sv as Map<String, dynamic>)).toList(),
      aliases: rawAliases.map((a) => TaxonomyAliasItem.fromJson(a as Map<String, dynamic>)).toList(),
    );
  }

  bool get isEmpty =>
      categories.isEmpty && subcategories.isEmpty && services.isEmpty && aliases.isEmpty;
  bool get isNotEmpty => !isEmpty;
}
