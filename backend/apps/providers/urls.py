"""
URL Routing for Provider Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from django.urls import path
from .views import (
    ProviderListCreateView,
    ProviderDetailView,
    MyProviderProfileView,
    ProviderServiceListCreateView,
    ProviderServiceDetailView,
    ProviderServiceAreaListCreateView,
    ProviderServiceAreaDetailView,
    ProviderAvailabilityView,
)

app_name = 'providers'

urlpatterns = [
    # Core Provider endpoints
    path('', ProviderListCreateView.as_view(), name='provider_list_create'),
    path('me/', MyProviderProfileView.as_view(), name='my_provider_profile'),
    path('<int:pk>/', ProviderDetailView.as_view(), name='provider_detail'),
    path('<slug:pk>/', ProviderDetailView.as_view(), name='provider_detail_slug'),

    # Provider Services mapping
    path('<int:pk>/services/', ProviderServiceListCreateView.as_view(), name='provider_services'),
    path('<int:pk>/services/<int:service_id>/', ProviderServiceDetailView.as_view(), name='provider_service_detail'),

    # Provider Service Area coverage
    path('<int:pk>/service-areas/', ProviderServiceAreaListCreateView.as_view(), name='provider_service_areas'),
    path('<int:pk>/service-areas/<int:area_id>/', ProviderServiceAreaDetailView.as_view(), name='provider_service_area_detail'),

    # Availability management
    path('<int:pk>/availability/', ProviderAvailabilityView.as_view(), name='provider_availability'),
]
