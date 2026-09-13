"""
Constants and enumerations for SebaCox Provider Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from django.db import models


class ProviderType(models.TextChoices):
    """
    Categorization of provider legal and operational structure.
    Extensible for future specialized entities.
    """
    INDIVIDUAL = 'INDIVIDUAL', 'ব্যক্তিগত সেবাদাতা (Individual Provider)'
    BUSINESS = 'BUSINESS', 'ব্যবসায়িক প্রতিষ্ঠান (Business / Enterprise)'
    ORGANIZATION = 'ORGANIZATION', 'সংস্থা বা প্রতিষ্ঠান (Organization / Agency)'


class ProviderStatus(models.TextChoices):
    """
    Controlled lifecycle status for a Service Provider.
    Enforces clear operational stages.
    """
    DRAFT = 'DRAFT', 'খসড়া (Draft)'
    PENDING_REVIEW = 'PENDING_REVIEW', 'পর্যালোচনার অপেক্ষায় (Pending Review)'
    ACTIVE = 'ACTIVE', 'সক্রিয় ও অনুমোদিত (Active & Approved)'
    SUSPENDED = 'SUSPENDED', 'স্থগিত (Suspended)'
    INACTIVE = 'INACTIVE', 'নিষ্ক্রিয় (Inactive)'
    REJECTED = 'REJECTED', 'বাতিল / প্রত্যাখ্যান (Rejected)'


class VerificationStatus(models.TextChoices):
    """
    Verification state of provider profile.
    Foundation only: Full KYC document uploads reserved for future phase.
    """
    UNVERIFIED = 'UNVERIFIED', 'অযাচাইকৃত (Unverified)'
    PENDING = 'PENDING', 'যাচাই পর্যালোচনায় (Verification Pending)'
    VERIFIED = 'VERIFIED', 'যাচাইকৃত (Verified)'
    REJECTED = 'REJECTED', 'যাচাই প্রত্যাখ্যাত (Verification Rejected)'
    EXPIRED = 'EXPIRED', 'যাচাই মেয়াদোত্তীর্ণ (Verification Expired)'


class AvailabilityStatus(models.TextChoices):
    """
    Real-time or operational availability status of provider.
    """
    AVAILABLE = 'AVAILABLE', 'উপলব্ধ (Available)'
    BUSY = 'BUSY', 'ব্যস্ত (Busy)'
    TEMPORARILY_UNAVAILABLE = 'TEMPORARILY_UNAVAILABLE', 'সাময়িক অনুপলব্ধ (Temporarily Unavailable)'
    OFFLINE = 'OFFLINE', 'অফলাইন (Offline)'


class ContactVisibility(models.TextChoices):
    """
    Privacy control governing who can view provider contact details (phone, email).
    """
    PUBLIC = 'PUBLIC', 'সবার জন্য উন্মুক্ত (Public)'
    REGISTERED_ONLY = 'REGISTERED_ONLY', 'কেবল লগইনকৃত ব্যবহারকারী (Registered Users Only)'
    ON_REQUEST = 'ON_REQUEST', 'অনুরোধের পর (On Request Only)'
    HIDDEN = 'HIDDEN', 'গোপন (Hidden)'


class PriceType(models.TextChoices):
    """
    Pricing strategy for mapped service offerings.
    """
    STARTING_FROM = 'STARTING_FROM', 'শুরু থেকে (Starting From)'
    FIXED = 'FIXED', 'নির্দিষ্ট মূল্য (Fixed Price)'
    HOURLY = 'HOURLY', 'প্রতি ঘণ্টা (Hourly Rate)'
    DAILY = 'DAILY', 'প্রতি দিন (Daily Rate)'
    PER_UNIT = 'PER_UNIT', 'প্রতি একক (Per Unit)'
    NEGOTIABLE = 'NEGOTIABLE', 'আলোচনা সাপেক্ষে (Negotiable)'


class ProviderAuditAction(models.TextChoices):
    """
    Audit log action types.
    """
    CREATED = 'CREATED', 'প্রোফাইল তৈরি (Profile Created)'
    UPDATED = 'UPDATED', 'প্রোফাইল আপডেট (Profile Updated)'
    STATUS_CHANGED = 'STATUS_CHANGED', 'অবস্থা পরিবর্তন (Status Changed)'
    VERIFICATION_CHANGED = 'VERIFICATION_CHANGED', 'যাচাই পরিবর্তন (Verification Status Changed)'
    SERVICE_ADDED = 'SERVICE_ADDED', 'সেবা যুক্ত (Service Added)'
    SERVICE_REMOVED = 'SERVICE_REMOVED', 'সেবা অপসারণ (Service Removed)'
    SERVICE_AREA_ADDED = 'SERVICE_AREA_ADDED', 'সেবা এলাকা যুক্ত (Service Area Added)'
    SERVICE_AREA_REMOVED = 'SERVICE_AREA_REMOVED', 'সেবা এলাকা অপসারণ (Service Area Removed)'
    AVAILABILITY_CHANGED = 'AVAILABILITY_CHANGED', 'উপলব্ধতা পরিবর্তন (Availability Changed)'


# Explicit State Transition Rules for Provider Lifecycle
# Every state change must be validated against this dictionary
VALID_STATUS_TRANSITIONS = {
    ProviderStatus.DRAFT: [
        ProviderStatus.PENDING_REVIEW,
        ProviderStatus.INACTIVE,
    ],
    ProviderStatus.PENDING_REVIEW: [
        ProviderStatus.ACTIVE,
        ProviderStatus.REJECTED,
        ProviderStatus.DRAFT,
    ],
    ProviderStatus.ACTIVE: [
        ProviderStatus.SUSPENDED,
        ProviderStatus.INACTIVE,
    ],
    ProviderStatus.SUSPENDED: [
        ProviderStatus.ACTIVE,
        ProviderStatus.INACTIVE,
    ],
    ProviderStatus.INACTIVE: [
        ProviderStatus.DRAFT,
        ProviderStatus.PENDING_REVIEW,
        ProviderStatus.ACTIVE,  # Re-activation if previously approved
    ],
    ProviderStatus.REJECTED: [
        ProviderStatus.DRAFT,
        ProviderStatus.PENDING_REVIEW,
    ],
}
