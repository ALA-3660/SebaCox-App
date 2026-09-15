"""
URLs for Category API endpoints.
Master Taxonomy v1.0 Universal Hierarchy & Search Routing.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    CategoryChildrenView,
    CategorySubcategoriesView,
    CategoryTreeViewView,
    CategoryFeaturedView,
    SubCategoryListView,
    SubCategoryDetailView,
    TaxonomySearchView,
    TaxonomyAliasListView,
)

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('tree/', CategoryTreeViewView.as_view(), name='category-tree'),
    path('featured/', CategoryFeaturedView.as_view(), name='category-featured'),
    path('subcategories/', SubCategoryListView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory-detail'),
    path('taxonomy/search/', TaxonomySearchView.as_view(), name='taxonomy-search'),
    path('taxonomy/aliases/', TaxonomyAliasListView.as_view(), name='taxonomy-aliases'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/subcategories/', CategorySubcategoriesView.as_view(), name='category-subcategories'),
    path('<int:pk>/children/', CategoryChildrenView.as_view(), name='category-children'),
]
