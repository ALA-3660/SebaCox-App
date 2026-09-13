"""
Django Admin interface for SebaCox Geographic Reference Data.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.contrib import admin
from .models import (
    Country,
    Division,
    District,
    Upazila,
    Municipality,
    CityCorporation,
    Union,
    Ward,
    Locality,
    GeoLocation,
    UserLocation,
    ServiceArea,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'code', 'iso3', 'dial_code', 'currency_code', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code', 'iso3')
    list_filter = ('is_active',)
    actions = ['make_active', 'make_inactive']

    @admin.action(description='সক্রিয় করুন (Activate)')
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='নিষ্ক্রিয় করুন (Deactivate)')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'code', 'country', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code')
    list_filter = ('is_active', 'country')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'code', 'division', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code')
    list_filter = ('is_active', 'division')


@admin.register(Upazila)
class UpazilaAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'code', 'district', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code')
    list_filter = ('is_active', 'district__division', 'district')


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'code', 'district', 'upazila', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code')
    list_filter = ('is_active', 'district')


@admin.register(CityCorporation)
class CityCorporationAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'code', 'district', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code')
    list_filter = ('is_active', 'district')


@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'code', 'upazila', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code')
    list_filter = ('is_active', 'upazila__district', 'upazila')


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_number', 'name_en', 'name_bn', 'municipality', 'city_corporation', 'union', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code')
    list_filter = ('is_active', 'municipality', 'union')


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'code', 'upazila', 'postal_code', 'is_active')
    search_fields = ('name_en', 'name_bn', 'code', 'postal_code')
    list_filter = ('is_active', 'upazila__district', 'upazila')


@admin.register(GeoLocation)
class GeoLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'srid', 'district', 'upazila', 'is_active', 'created_at')
    search_fields = ('address_text',)
    list_filter = ('is_active', 'district')


@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'location_type', 'label', 'district', 'upazila', 'is_default', 'is_active')
    search_fields = ('user__mobile_number', 'label')
    list_filter = ('location_type', 'is_default', 'is_active', 'district')


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_bn', 'area_type', 'district', 'upazila', 'radius_km', 'is_active')
    search_fields = ('name_en', 'name_bn')
    list_filter = ('area_type', 'is_active', 'district')
