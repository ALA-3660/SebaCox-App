"""
URLs for Service API endpoints.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.urls import path
from .views import (
    ServiceListView,
    ServiceDetailView,
    ServicesByCategoryView,
    ServiceFeaturedView,
    ServiceSearchView,
)

app_name = 'services'

urlpatterns = [
    path('', ServiceListView.as_view(), name='service-list'),
    path('featured/', ServiceFeaturedView.as_view(), name='service-featured'),
    path('search/', ServiceSearchView.as_view(), name='service-search'),
    path('by-category/<int:category_id>/', ServicesByCategoryView.as_view(), name='services-by-category'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]
