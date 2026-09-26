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
    TaxonomyManifestView,
    TaxonomyVersionListView,
    TaxonomyChangeLogListView,
    TaxonomyImpactAnalysisView,
    TaxonomyRenameView,
    TaxonomyDeactivateView,
    TaxonomyReactivateView,
    TaxonomyDeprecateView,
    TaxonomyMergeCategoryView,
    TaxonomyMergeSubCategoryView,
    TaxonomyMoveSubCategoryView,
    TaxonomyIntegrityCheckView,
    TaxonomyInventoryView,
    TaxonomyMigrationRulesView,
    TaxonomyOrphansView,
    TaxonomyDryRunView,
    TaxonomyExecuteMigrationView,
    TaxonomyRollbackManifestView,
)

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('tree/', CategoryTreeViewView.as_view(), name='category-tree'),
    path('manifest/', TaxonomyManifestView.as_view(), name='taxonomy-manifest'),
    path('featured/', CategoryFeaturedView.as_view(), name='category-featured'),
    path('subcategories/', SubCategoryListView.as_view(), name='subcategory-list'),
    path('subcategories/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory-detail'),
    path('taxonomy/search/', TaxonomySearchView.as_view(), name='taxonomy-search'),
    path('taxonomy/aliases/', TaxonomyAliasListView.as_view(), name='taxonomy-aliases'),
    # Governance & Versioning Endpoints (Phase 4D)
    path('governance/versions/', TaxonomyVersionListView.as_view(), name='taxonomy-versions'),
    path('governance/audit-logs/', TaxonomyChangeLogListView.as_view(), name='taxonomy-audit-logs'),
    path('governance/impact/', TaxonomyImpactAnalysisView.as_view(), name='taxonomy-impact'),
    path('governance/rename/', TaxonomyRenameView.as_view(), name='taxonomy-rename'),
    path('governance/deactivate/', TaxonomyDeactivateView.as_view(), name='taxonomy-deactivate'),
    path('governance/reactivate/', TaxonomyReactivateView.as_view(), name='taxonomy-reactivate'),
    path('governance/deprecate/', TaxonomyDeprecateView.as_view(), name='taxonomy-deprecate'),
    path('governance/merge/category/', TaxonomyMergeCategoryView.as_view(), name='taxonomy-merge-category'),
    path('governance/merge/subcategory/', TaxonomyMergeSubCategoryView.as_view(), name='taxonomy-merge-subcategory'),
    path('governance/move/subcategory/', TaxonomyMoveSubCategoryView.as_view(), name='taxonomy-move-subcategory'),
    path('governance/integrity/', TaxonomyIntegrityCheckView.as_view(), name='taxonomy-integrity'),
    # Migration & Data Inventory Endpoints (Phase 4H)
    path('governance/inventory/', TaxonomyInventoryView.as_view(), name='taxonomy-inventory'),
    path('governance/migration-map/', TaxonomyMigrationRulesView.as_view(), name='taxonomy-migration-map'),
    path('governance/orphans/', TaxonomyOrphansView.as_view(), name='taxonomy-orphans'),
    path('governance/dry-run/', TaxonomyDryRunView.as_view(), name='taxonomy-dry-run'),
    path('governance/migrate/', TaxonomyExecuteMigrationView.as_view(), name='taxonomy-migrate'),
    path('governance/rollback-manifest/', TaxonomyRollbackManifestView.as_view(), name='taxonomy-rollback-manifest'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/subcategories/', CategorySubcategoriesView.as_view(), name='category-subcategories'),
    path('<int:pk>/children/', CategoryChildrenView.as_view(), name='category-children'),
]
