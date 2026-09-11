"""
URL configuration for SebaCox backend.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"

Routes:
- /api/v1/health/ : Foundation Health Endpoint
"""
from django.urls import path, include
from common.health import HealthCheckView

api_v1_patterns = [
    path('health/', HealthCheckView.as_view(), name='api-v1-health'),
    # Future Phase 2+ business modules will be mounted here:
    # path('auth/', include('apps.authentication.urls')),
    # path('services/', include('apps.services.urls')),
]

urlpatterns = [
    # API Version 1 routes
    path('api/v1/', include((api_v1_patterns, 'v1'))),
]
