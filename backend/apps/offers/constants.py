"""
Offer Constants for SebaCox.
Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from django.db import models


class OfferType(models.TextChoices):
    INITIAL = 'INITIAL', 'প্রাথমিক প্রস্তাব (Initial Offer)'
    COUNTER = 'COUNTER', 'পাল্টা প্রস্তাব (Counter Offer)'


class OfferStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'খসড়া'
    PENDING = 'PENDING', 'অপেক্ষমাণ'
    ACCEPTED = 'ACCEPTED', 'গ্রহণ করা হয়েছে'
    REJECTED = 'REJECTED', 'প্রত্যাখ্যাত'
    CANCELLED = 'CANCELLED', 'বাতিল'
    EXPIRED = 'EXPIRED', 'মেয়াদ শেষ'
    SUPERSEDED = 'SUPERSEDED', 'নতুন প্রস্তাবে প্রতিস্থাপিত'


class OfferAuditAction(models.TextChoices):
    CREATED = 'CREATED', 'প্রস্তাব তৈরি'
    COUNTERED = 'COUNTERED', 'পাল্টা প্রস্তাব প্রেরণ'
    ACCEPTED = 'ACCEPTED', 'প্রস্তাব গৃহীত'
    REJECTED = 'REJECTED', 'প্রস্তাব প্রত্যাখ্যাত'
    CANCELLED = 'CANCELLED', 'প্রস্তাব বাতিলকৃত'
    EXPIRED = 'EXPIRED', 'মেয়াদ উত্তীর্ণ'
    SUPERSEDED = 'SUPERSEDED', 'প্রতিস্থাপিত'


# Status Transitions Map
# DRAFT -> PENDING
# PENDING -> ACCEPTED, REJECTED, CANCELLED, EXPIRED, SUPERSEDED
VALID_OFFER_STATUS_TRANSITIONS = {
    OfferStatus.DRAFT: [
        OfferStatus.PENDING,
        OfferStatus.CANCELLED,
    ],
    OfferStatus.PENDING: [
        OfferStatus.ACCEPTED,
        OfferStatus.REJECTED,
        OfferStatus.CANCELLED,
        OfferStatus.EXPIRED,
        OfferStatus.SUPERSEDED,
    ],
    # Terminal states:
    OfferStatus.ACCEPTED: [],
    OfferStatus.REJECTED: [],
    OfferStatus.CANCELLED: [],
    OfferStatus.EXPIRED: [],
    OfferStatus.SUPERSEDED: [],
}

TERMINAL_OFFER_STATUSES = [
    OfferStatus.ACCEPTED,
    OfferStatus.REJECTED,
    OfferStatus.CANCELLED,
    OfferStatus.EXPIRED,
    OfferStatus.SUPERSEDED,
]

LOCKED_HISTORICAL_OFFER_STATUSES = TERMINAL_OFFER_STATUSES

# Bengali Status Display Labels
OFFER_STATUS_LABELS_BN = {
    OfferStatus.DRAFT: 'খসড়া',
    OfferStatus.PENDING: 'অপেক্ষমাণ',
    OfferStatus.ACCEPTED: 'গ্রহণ করা হয়েছে',
    OfferStatus.REJECTED: 'প্রত্যাখ্যাত',
    OfferStatus.CANCELLED: 'বাতিল',
    OfferStatus.EXPIRED: 'মেয়াদ শেষ',
    OfferStatus.SUPERSEDED: 'নতুন প্রস্তাবে প্রতিস্থাপিত',
}

OFFER_TYPE_LABELS_BN = {
    OfferType.INITIAL: 'প্রাথমিক প্রস্তাব',
    OfferType.COUNTER: 'পাল্টা প্রস্তাব',
}

DEFAULT_OFFER_VALIDITY_HOURS = 24
MAX_OFFER_VALIDITY_HOURS = 168 # 7 days max validity
DEFAULT_CURRENCY = 'BDT'

SEBACOX_MAIN_SLOGAN_BN = "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
SEBACOX_SHORT_DESC_BN = "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
