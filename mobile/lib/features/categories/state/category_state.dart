/// Category State definitions for Flutter.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import '../models/category_model.dart';
import '../models/service_model.dart';

abstract class CategoryState {
  const CategoryState();
}

class CategoryInitial extends CategoryState {
  const CategoryInitial();
}

class CategoryLoading extends CategoryState {
  final String message;
  const CategoryLoading({this.message = 'ক্যাটাগরি ও সেবাসমূহ লোড হচ্ছে...'});
}

class CategoryLoaded extends CategoryState {
  final List<CategoryItem> categoryTree;
  final List<CategoryItem> featuredCategories;
  final List<ServiceItem> featuredServices;
  final List<ServiceItem> searchResults;
  final String? activeSearchQuery;

  const CategoryLoaded({
    required this.categoryTree,
    this.featuredCategories = const [],
    this.featuredServices = const [],
    this.searchResults = const [],
    this.activeSearchQuery,
  });

  bool get isSearching => activeSearchQuery != null && activeSearchQuery!.isNotEmpty;

  CategoryLoaded copyWith({
    List<CategoryItem>? categoryTree,
    List<CategoryItem>? featuredCategories,
    List<ServiceItem>? featuredServices,
    List<ServiceItem>? searchResults,
    String? activeSearchQuery,
  }) {
    return CategoryLoaded(
      categoryTree: categoryTree ?? this.categoryTree,
      featuredCategories: featuredCategories ?? this.featuredCategories,
      featuredServices: featuredServices ?? this.featuredServices,
      searchResults: searchResults ?? this.searchResults,
      activeSearchQuery: activeSearchQuery,
    );
  }
}

class CategoryError extends CategoryState {
  final String errorMessage;
  const CategoryError(this.errorMessage);
}
