"""
Constants, Enumerations, and State Transition Rules for SebaCox Demand Engine.
User-facing Bengali Name: “আমার প্রয়োজন”
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.db import models


class DemandType(models.TextChoices):
    """
    Extensible Demand Classification.
    Compatible with Phase 4 ServiceType taxonomy.
    """
    SERVICE = 'SERVICE', 'সেবামূলক প্রয়োজন (Service Demand)'
    PRODUCT = 'PRODUCT', 'পণ্য সামগ্রী প্রয়োজন (Product Demand)'
    RENTAL = 'RENTAL', 'ভাড়া বা রেন্টাল প্রয়োজন (Rental Demand)'
    BOOKING = 'BOOKING', 'অগ্রিম বুকিং প্রয়োজন (Booking / Reservation)'
    MARKETPLACE = 'MARKETPLACE', 'মার্কেটপ্লেস ক্রয়/বিক্রয় (Marketplace Need)'
    INFORMATION = 'INFORMATION', 'তথ্য বা পরামর্শ অনুসন্ধান (Information / Advice)'
    OTHER = 'OTHER', 'অন্যান্য প্রয়োজন (Other)'


class DemandStatus(models.TextChoices):
    """
    Strict lifecycle state machine for Demand / “আমার প্রয়োজন”.
    Transitions are controlled at the domain service layer.
    """
    DRAFT = 'DRAFT', 'খসড়া (Draft)'
    PUBLISHED = 'PUBLISHED', 'প্রকাশিত (Published)'
    PAUSED = 'PAUSED', 'সাময়িক বন্ধ (Paused)'
    FULFILLED = 'FULFILLED', 'প্রয়োজন পূরণ হয়েছে (Fulfilled)'
    CANCELLED = 'CANCELLED', 'বাতিল (Cancelled)'
    EXPIRED = 'EXPIRED', 'মেয়াদ শেষ (Expired)'
    CLOSED = 'CLOSED', 'বন্ধ (Closed)'


class DemandPriority(models.TextChoices):
    """
    Urgency priority indicator.
    Kept concise as requested (NORMAL and URGENT).
    """
    NORMAL = 'NORMAL', 'সাধারণ (Normal)'
    URGENT = 'URGENT', 'জরুরি (Urgent)'


class DemandVisibility(models.TextChoices):
    """
    Visibility scope controlling who can view the demand.
    """
    PUBLIC = 'PUBLIC', 'সবার জন্য উন্মুক্ত (Public)'
    REGISTERED_USERS = 'REGISTERED_USERS', 'কেবল নিবন্ধিত ব্যবহারকারী (Registered Users Only)'
    PRIVATE = 'PRIVATE', 'ব্যক্তিগত / শুধুমাত্র অনুরোধকারী (Private)'


class DemandContactPreference(models.TextChoices):
    """
    Communication channel preference for responders.
    """
    IN_APP_ONLY = 'IN_APP_ONLY', 'ইন-অ্যাপ বার্তা (In-App Only)'
    PHONE = 'PHONE', 'সরাসরি ফোন কল (Direct Phone)'
    BOTH = 'BOTH', 'ফোন ও ইন-অ্যাপ উভয়ই (Both Phone & In-App)'


class DemandAuditAction(models.TextChoices):
    """
    Audit log action types recording full demand lifecycle events.
    """
    CREATED = 'CREATED', 'তৈরি করা হয়েছে (Created)'
    UPDATED = 'UPDATED', 'আপডেট করা হয়েছে (Updated)'
    PUBLISHED = 'PUBLISHED', 'প্রকাশ করা হয়েছে (Published)'
    PAUSED = 'PAUSED', 'সাময়িক বন্ধ করা হয়েছে (Paused)'
    RESUMED = 'RESUMED', 'পুনরায় চালু করা হয়েছে (Resumed)'
    CANCELLED = 'CANCELLED', 'বাতিল করা হয়েছে (Cancelled)'
    FULFILLED = 'FULFILLED', 'সম্পন্ন হয়েছে (Fulfilled)'
    EXPIRED = 'EXPIRED', 'মেয়াদ উত্তীর্ণ হয়েছে (Expired)'
    CLOSED = 'CLOSED', 'বন্ধ করা হয়েছে (Closed)'
    SOFT_DELETED = 'SOFT_DELETED', 'মুছে ফেলা হয়েছে (Soft Deleted / Archived)'


# Strict State Machine Transition Graph
VALID_DEMAND_STATUS_TRANSITIONS = {
    DemandStatus.DRAFT: [
        DemandStatus.PUBLISHED,
        DemandStatus.CANCELLED,
    ],
    DemandStatus.PUBLISHED: [
        DemandStatus.PAUSED,
        DemandStatus.FULFILLED,
        DemandStatus.CANCELLED,
        DemandStatus.EXPIRED,
        DemandStatus.CLOSED,
    ],
    DemandStatus.PAUSED: [
        DemandStatus.PUBLISHED,
        DemandStatus.CANCELLED,
        DemandStatus.EXPIRED,
        DemandStatus.CLOSED,
    ],
    DemandStatus.FULFILLED: [
        DemandStatus.CLOSED,
    ],
    DemandStatus.CANCELLED: [],  # Terminal state
    DemandStatus.EXPIRED: [
        DemandStatus.CLOSED,
    ],
    DemandStatus.CLOSED: [],     # Terminal state
}

# Editable status groups
EDITABLE_DEMAND_STATUSES = [
    DemandStatus.DRAFT,
    DemandStatus.PUBLISHED,
    DemandStatus.PAUSED,
]

LOCKED_HISTORICAL_STATUSES = [
    DemandStatus.FULFILLED,
    DemandStatus.CANCELLED,
    DemandStatus.EXPIRED,
    DemandStatus.CLOSED,
]

# Standard Brand Slogans
MAIN_SLOGAN = "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
SHORT_DESCRIPTION = "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
SEBACOX_MAIN_SLOGAN_BN = MAIN_SLOGAN
SEBACOX_SHORT_DESC_BN = SHORT_DESCRIPTION

# Global Typography Standard
FONT_DISPLAY_HEADINGS = "Hind Siliguri"
FONT_UI_ELEMENTS = "Baloo Da 2"
FONT_BODY_TEXT = "Tiro Bangla"

BANGLA_TYPOGRAPHY_CONTRACT = {
    "large_headings": FONT_DISPLAY_HEADINGS,
    "medium_headings_buttons": FONT_UI_ELEMENTS,
    "body_text": FONT_BODY_TEXT,
}
