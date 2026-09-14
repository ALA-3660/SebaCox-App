"""
URL patterns for SebaCox Location & Geographic Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    # Reference Hierarchy Endpoints (Public)
    path('countries/', views.CountryListView.as_view(), name='country-list'),
    path('divisions/', views.DivisionListView.as_view(), name='division-list'),
    path('districts/', views.DistrictListView.as_view(), name='district-list'),
    path('upazilas/', views.UpazilaListView.as_view(), name='upazila-list'),
    path('municipalities/', views.MunicipalityListView.as_view(), name='municipality-list'),
    path('city-corporations/', views.CityCorporationListView.as_view(), name='city-corporation-list'),
    path('unions/', views.UnionListView.as_view(), name='union-list'),
    path('wards/', views.WardListView.as_view(), name='ward-list'),
    path('localities/', views.LocalityListView.as_view(), name='locality-list'),
    path('postal-locations/', views.PostalLocationListView.as_view(), name='postal-location-list'),
    path('post-offices/', views.PostalLocationListView.as_view(), name='post-office-list'),
    path('children/', views.LocationChildrenView.as_view(), name='location-children'),

    # Search & Proximity (Public)
    path('search/', views.LocationSearchView.as_view(), name='location-search'),
    path('nearby/', views.NearbyCalculateView.as_view(), name='nearby-calculate'),

    # User Location Context (Protected)
    path('user/', views.UserLocationListView.as_view(), name='user-location-list'),
    path('user/selected/', views.UserSelectedLocationView.as_view(), name='user-selected-location'),
    path('user/current/', views.UserCurrentLocationView.as_view(), name='user-current-location'),
]
