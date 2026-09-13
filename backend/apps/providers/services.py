"""
Domain Services for Provider Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
import unicodedata
from typing import Optional, List, Dict, Any
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError

from .models import Provider, ProviderService, ProviderServiceArea, ProviderAuditLog
from .constants import ProviderStatus, AvailabilityStatus, ProviderAuditAction, VALID_STATUS_TRANSITIONS
from .validators import validate_status_transition


class ProviderDomainService:
    """
    Core Domain Logic for Provider lifecycle, queries, and constraints.
    """

    @staticmethod
    def filter_providers(
        query: Optional[str] = None,
        service_id: Optional[int] = None,
        category_id: Optional[int] = None,
        upazila_id: Optional[int] = None,
        district_id: Optional[int] = None,
        provider_type: Optional[str] = None,
        status: Optional[str] = ProviderStatus.ACTIVE,
        is_verified: Optional[bool] = None,
        availability: Optional[str] = None,
    ):
        """
        Filters providers with bilingual normalized search and location/service scoping.
        """
        qs = Provider.objects.filter(is_active=True)

        if status:
            qs = qs.filter(status=status)

        if is_verified is not None:
            qs = qs.filter(is_verified=is_verified)

        if provider_type:
            qs = qs.filter(provider_type=provider_type)

        if availability:
            qs = qs.filter(availability_status=availability)

        # Filter by service ID
        if service_id:
            qs = qs.filter(services__service_id=service_id, services__is_active=True).distinct()

        # Filter by category ID
        if category_id:
            qs = qs.filter(
                Q(services__service__category_id=category_id) |
                Q(services__service__category__parent_id=category_id),
                services__is_active=True
            ).distinct()

        # Filter by location
        if upazila_id:
            qs = qs.filter(
                Q(service_areas__upazila_id=upazila_id) |
                Q(service_areas__district__upazilas__id=upazila_id),
                service_areas__is_active=True
            ).distinct()
        elif district_id:
            qs = qs.filter(
                service_areas__district_id=district_id,
                service_areas__is_active=True
            ).distinct()

        # Search query (Bengali / English NFC normalized)
        if query:
            clean_q = unicodedata.normalize('NFC', query).strip()
            qs = qs.filter(
                Q(display_name_bn__icontains=clean_q) |
                Q(display_name_en__icontains=clean_q) |
                Q(short_description_bn__icontains=clean_q) |
                Q(short_description_en__icontains=clean_q) |
                Q(slug__icontains=clean_q) |
                Q(services__title_bn__icontains=clean_q) |
                Q(services__service__name_bn__icontains=clean_q) |
                Q(services__service__name_en__icontains=clean_q)
            ).distinct()

        return qs.order_by('-is_featured', '-is_verified', '-created_at')

    @staticmethod
    @transaction.atomic
    def change_provider_status(
        provider: Provider,
        new_status: str,
        actor=None,
        note: str = ''
    ) -> Provider:
        """
        Transitions provider status adhering strictly to VALID_STATUS_TRANSITIONS.
        Creates audit log.
        """
        old_status = provider.status
        if old_status == new_status:
            return provider

        validate_status_transition(old_status, new_status)
        provider.status = new_status
        if new_status == ProviderStatus.ACTIVE and provider.verification_status == 'UNVERIFIED':
            # Active status activates provider
            provider.is_active = True
        provider.save(update_fields=['status', 'is_active', 'updated_at'])

        ProviderAuditLog.objects.create(
            provider=provider,
            actor=actor,
            action=ProviderAuditAction.STATUS_CHANGED,
            from_state=old_status,
            to_state=new_status,
            note=note or f"Status transitioned from {old_status} to {new_status}"
        )
        return provider

    @staticmethod
    @transaction.atomic
    def update_availability(
        provider: Provider,
        new_availability: str,
        actor=None,
        note: str = ''
    ) -> Provider:
        """
        Updates provider availability and records audit log.
        """
        old_avail = provider.availability_status
        if old_avail == new_availability:
            return provider

        provider.availability_status = new_availability
        provider.save(update_fields=['availability_status', 'updated_at'])

        ProviderAuditLog.objects.create(
            provider=provider,
            actor=actor,
            action=ProviderAuditAction.AVAILABILITY_CHANGED,
            from_state=old_avail,
            to_state=new_availability,
            note=note
        )
        return provider

    @staticmethod
    def add_service_to_provider(
        provider: Provider,
        service_id: int,
        title_bn: str = '',
        title_en: str = '',
        description_bn: str = '',
        description_en: str = '',
        starting_price: Optional[float] = None,
        price_type: str = 'STARTING_FROM',
        actor=None,
    ) -> ProviderService:
        """
        Maps a service to provider. Enforces uniqueness.
        """
        if ProviderService.objects.filter(provider=provider, service_id=service_id).exists():
            raise ValidationError("এই সেবাটি ইতিমধ্যে এই সেবাদাতার তালিকায় যুক্ত রয়েছে।")

        ps = ProviderService.objects.create(
            provider=provider,
            service_id=service_id,
            title_bn=title_bn,
            title_en=title_en,
            description_bn=description_bn,
            description_en=description_en,
            starting_price=starting_price,
            price_type=price_type,
            is_available=True,
            is_active=True
        )

        ProviderAuditLog.objects.create(
            provider=provider,
            actor=actor,
            action=ProviderAuditAction.SERVICE_ADDED,
            from_state='',
            to_state=f"service_id:{service_id}",
            note=f"Service #{service_id} mapped to provider #{provider.id}"
        )
        return ps

    @staticmethod
    def add_service_area_to_provider(
        provider: Provider,
        upazila_id: Optional[int] = None,
        district_id: Optional[int] = None,
        union_id: Optional[int] = None,
        radius_km: Optional[float] = None,
        center_lat: Optional[float] = None,
        center_lon: Optional[float] = None,
        actor=None,
    ) -> ProviderServiceArea:
        """
        Adds service area to provider. Prevents duplicate administrative coverage.
        """
        # Duplicate check for upazila
        if upazila_id and ProviderServiceArea.objects.filter(provider=provider, upazila_id=upazila_id).exists():
            raise ValidationError("এই উপজেলাটি ইতিমধ্যে সেবাদাতার সেবাকভারেজে অন্তর্ভুক্ত রয়েছে।")

        area = ProviderServiceArea.objects.create(
            provider=provider,
            district_id=district_id,
            upazila_id=upazila_id,
            union_id=union_id,
            radius_km=radius_km,
            center_latitude=center_lat,
            center_longitude=center_lon,
            is_active=True
        )

        ProviderAuditLog.objects.create(
            provider=provider,
            actor=actor,
            action=ProviderAuditAction.SERVICE_AREA_ADDED,
            from_state='',
            to_state=f"upazila:{upazila_id or district_id or 'radius'}",
            note=f"Service area added for provider #{provider.id}"
        )
        return area
