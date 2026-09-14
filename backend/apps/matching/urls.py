"""
URL configuration for SebaCox Matching Engine.
Phase 7: Endpoints for Matching Runs and Monitoring.
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from django.urls import path
from .views import (
    MatchingRunListView,
    MatchingRunDetailView,
)

app_name = 'matching'

urlpatterns = [
    path('runs/', MatchingRunListView.as_view(), name='run-list'),
    path('runs/<int:run_id>/', MatchingRunDetailView.as_view(), name='run-detail'),
]
