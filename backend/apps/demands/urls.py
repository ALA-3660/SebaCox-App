"""
URL Routing for SebaCox Demand Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from django.urls import path
from .views import (
    DemandListCreateView,
    DemandDetailView,
    DemandPublishView,
    DemandPauseView,
    DemandResumeView,
    DemandCancelView,
    DemandFulfillView,
    DemandCloseView,
    MyDemandListView,
    MyActiveDemandListView,
    MyHistoryDemandListView,
)
from apps.matching.views import (
    DemandMatchesListView,
    DemandMatchDetailView,
    DemandRematchView,
)

app_name = 'demands'

urlpatterns = [
    # Primary List & Creation
    path('', DemandListCreateView.as_view(), name='demand-list-create'),

    # User-specific lists
    path('me/', MyDemandListView.as_view(), name='my-demands'),
    path('me/active/', MyActiveDemandListView.as_view(), name='my-active-demands'),
    path('me/history/', MyHistoryDemandListView.as_view(), name='my-history-demands'),

    # Single Demand Detail, Update, and Soft-Delete
    path('<int:pk>/', DemandDetailView.as_view(), name='demand-detail'),

    # Matching Engine Integration (Phase 7)
    path('<int:demand_id>/matches/', DemandMatchesListView.as_view(), name='demand-matches'),
    path('<int:demand_id>/matches/<int:match_id>/', DemandMatchDetailView.as_view(), name='demand-match-detail'),
    path('<int:demand_id>/rematch/', DemandRematchView.as_view(), name='demand-rematch'),

    # Controlled State Machine Lifecycle Endpoints
    path('<int:pk>/publish/', DemandPublishView.as_view(), name='demand-publish'),
    path('<int:pk>/pause/', DemandPauseView.as_view(), name='demand-pause'),
    path('<int:pk>/resume/', DemandResumeView.as_view(), name='demand-resume'),
    path('<int:pk>/cancel/', DemandCancelView.as_view(), name='demand-cancel'),
    path('<int:pk>/fulfill/', DemandFulfillView.as_view(), name='demand-fulfill'),
    path('<int:pk>/close/', DemandCloseView.as_view(), name='demand-close'),
]
