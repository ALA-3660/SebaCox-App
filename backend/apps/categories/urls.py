"""
URLs for Category API endpoints.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
"""
from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    CategoryChildrenView,
    CategoryTreeViewView,
    CategoryFeaturedView,
)

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('tree/', CategoryTreeViewView.as_view(), name='category-tree'),
    path('featured/', CategoryFeaturedView.as_view(), name='category-featured'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('<int:pk>/children/', CategoryChildrenView.as_view(), name='category-children'),
]
