"""
URL configuration for SebaCox backend.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

Routes:
- /api/v1/health/ : Foundation Health Endpoint
- /api/v1/auth/ : Authentication
- /api/v1/locations/ : Locations Engine
- /api/v1/categories/ : Categories & Services Engine
- /api/v1/providers/ : Provider Foundation Engine
- /api/v1/demands/ : Demand / “আমার প্রয়োজন” Engine
"""
from django.urls import path, include
from common.health import HealthCheckView

api_v1_patterns = [
    path('health/', HealthCheckView.as_view(), name='api-v1-health'),
    path('auth/', include('apps.authentication.urls', namespace='auth')),
    path('locations/', include('apps.locations.urls', namespace='locations')),
    path('categories/', include('apps.categories.urls', namespace='categories')),
    path('services/', include('apps.categories.urls_services', namespace='services')),
    path('providers/', include('apps.providers.urls', namespace='providers')),
    path('demands/', include('apps.demands.urls', namespace='demands')),
]

urlpatterns = [
    # API Version 1 routes
    path('api/v1/', include((api_v1_patterns, 'v1'))),
]
