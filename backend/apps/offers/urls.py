"""
URL Configuration for Offers Engine.
Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from django.urls import path
from .views import (
    OfferListCreateView,
    OfferDetailView,
    OfferAcceptView,
    OfferRejectView,
    OfferCancelView,
    OfferCounterView,
    OfferHistoryView,
    DemandOffersListView,
)

app_name = 'offers'

urlpatterns = [
    # List offers or create initial offer
    path('', OfferListCreateView.as_view(), name='offer-list-create'),

    # Detail of a specific offer
    path('<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),

    # Lifecycle Actions
    path('<int:pk>/accept/', OfferAcceptView.as_view(), name='offer-accept'),
    path('<int:pk>/reject/', OfferRejectView.as_view(), name='offer-reject'),
    path('<int:pk>/cancel/', OfferCancelView.as_view(), name='offer-cancel'),
    path('<int:pk>/counter/', OfferCounterView.as_view(), name='offer-counter'),

    # History & Chain
    path('<int:pk>/history/', OfferHistoryView.as_view(), name='offer-history'),

    # Demand-specific offers list
    path('demand/<int:demand_id>/', DemandOffersListView.as_view(), name='demand-offers'),
]
