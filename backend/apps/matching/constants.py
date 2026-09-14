"""
Constants and Enums for SebaCox Matching Engine.
Phase 7 Foundation: “প্রয়োজনের সাথে উপযুক্ত সেবাদাতার সংযোগ”
“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
"""
from django.db import models

# Official Brand Slogan and Platform Identity
SEBACOX_MAIN_SLOGAN_BN = "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
SEBACOX_SHORT_DESC_BN = "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

# Global Bangla Typography Standard Contract
BANGLA_TYPOGRAPHY_CONTRACT = {
    'large_heading': 'Hind Siliguri',
    'medium_heading': 'Baloo Da 2',
    'body_and_labels': 'Tiro Bangla',
    'buttons_and_chips': 'Baloo Da 2',
    'latin_numerals_allowed': True,
}


class MatchStatus(models.TextChoices):
    """
    Lifecycle status of a match candidate.
    """
    CANDIDATE = 'CANDIDATE', 'প্রাথমিক সম্ভাব্য (Candidate)'
    ELIGIBLE = 'ELIGIBLE', 'উপযুক্ত নির্বাচিত (Eligible)'
    INELIGIBLE = 'INELIGIBLE', 'অনুপযুক্ত (Ineligible)'
    DISMISSED = 'DISMISSED', 'বাতিলকৃত (Dismissed)'
    EXPIRED = 'EXPIRED', 'মেয়াদোত্তীর্ণ (Expired)'


class MatchingRunStatus(models.TextChoices):
    """
    Execution status of an orchestration matching run.
    """
    PENDING = 'PENDING', 'অপেক্ষমান (Pending)'
    RUNNING = 'RUNNING', 'চলমান (Running)'
    COMPLETED = 'COMPLETED', 'সম্পন্ন (Completed)'
    FAILED = 'FAILED', 'ব্যর্থ (Failed)'


class MatchingTrigger(models.TextChoices):
    """
    Trigger that initiated the matching process.
    """
    DEMAND_PUBLISHED = 'DEMAND_PUBLISHED', 'প্রয়োজন প্রকাশ (Demand Published)'
    MANUAL = 'MANUAL', 'ম্যানুয়াল অনুরোধ (Manual)'
    RE_MATCH = 'RE_MATCH', 'পুনঃম্যাচিং (Re-Match)'
    SCHEDULED = 'SCHEDULED', 'নির্ধারিত শিডিউল (Scheduled)'


class ServiceMatchLevel(models.TextChoices):
    """
    Taxonomy service compatibility level.
    """
    EXACT = 'EXACT', 'একই সেবা (Exact Service Match)'
    CATEGORY = 'CATEGORY', 'একই ক্যাটাগরি (Same Category Compatibility)'
    NONE = 'NONE', 'অসংগত সেবা (Incompatible Service)'


class LocationMatchLevel(models.TextChoices):
    """
    Geographic containment match level.
    """
    EXACT_WARD = 'EXACT_WARD', 'একই ওয়ার্ড/মহল্লা (Exact Ward Match)'
    UNION = 'UNION', 'একই ইউনিয়ন (Union Match)'
    UPAZILA = 'UPAZILA', 'উপজেলা কভারেজ (Upazila Coverage)'
    DISTRICT = 'DISTRICT', 'জেলা কভারেজ (District-wide Coverage)'
    RADIUS = 'RADIUS', 'ব্যাসার্ধ কভারেজ (GPS Radial Coverage)'
    NONE = 'NONE', 'কভারেজের বাইরে (Out of Coverage)'


class TimeCompatibilityLevel(models.TextChoices):
    """
    Availability signal compatibility relative to demand required_at.
    """
    COMPATIBLE = 'COMPATIBLE', 'সময়ানুযায়ী উপযুক্ত (Time Compatible)'
    UNKNOWN = 'UNKNOWN', 'অনিশ্চিত সময়সূচি (Schedule Unknown)'
    INCOMPATIBLE = 'INCOMPATIBLE', 'অনুপলব্ধ (Incompatible)'


class MatchFactorCode(models.TextChoices):
    """
    Structured explainable factor codes for matching dimensions.
    """
    # Service Factors
    SERVICE_EXACT = 'SERVICE_EXACT', 'একই সেবা মিল'
    SERVICE_CATEGORY_COMPATIBLE = 'SERVICE_CATEGORY_COMPATIBLE', 'সম্পর্কিত ক্যাটাগরি মিল'
    SERVICE_INCOMPATIBLE = 'SERVICE_INCOMPATIBLE', 'অসংগত সেবা'

    # Location Factors
    LOCATION_COVERED_EXACT = 'LOCATION_COVERED_EXACT', 'সুনির্দিষ্ট এলাকার সেবাদাতা'
    LOCATION_COVERED_UPAZILA = 'LOCATION_COVERED_UPAZILA', 'উপজেলা কভারেজ'
    LOCATION_COVERED_DISTRICT = 'LOCATION_COVERED_DISTRICT', 'জেলাব্যাপী কভারেজ'
    LOCATION_COVERED_RADIUS = 'LOCATION_COVERED_RADIUS', 'নিকটবর্তী জিপিএস কভারেজ'
    LOCATION_NOT_COVERED = 'LOCATION_NOT_COVERED', 'কভারেজের বাইরে'

    # Provider & Service Status Factors
    PROVIDER_ACTIVE = 'PROVIDER_ACTIVE', 'সেবাদাতা সক্রিয়'
    PROVIDER_NOT_ACTIVE = 'PROVIDER_NOT_ACTIVE', 'সেবাদাতা নিষ্ক্রিয়'
    PROVIDER_SERVICE_ACTIVE_AVAILABLE = 'PROVIDER_SERVICE_ACTIVE_AVAILABLE', 'সেবা সক্রিয় ও প্রদানযোগ্য'
    PROVIDER_SERVICE_UNAVAILABLE = 'PROVIDER_SERVICE_UNAVAILABLE', 'সেবা বর্তমানে বন্ধ'

    # Availability Signals
    AVAILABILITY_AVAILABLE = 'AVAILABILITY_AVAILABLE', 'বর্তমানে সেবায় প্রস্তুত'
    AVAILABILITY_BUSY = 'AVAILABILITY_BUSY', 'ব্যস্ত অবস্থায় আছেন'
    AVAILABILITY_OFFLINE = 'AVAILABILITY_OFFLINE', 'অফলাইনে আছেন'

    # Verification Factors
    VERIFICATION_VERIFIED = 'VERIFICATION_VERIFIED', 'যাচাইকৃত সেবাদাতা'
    VERIFICATION_PENDING = 'VERIFICATION_PENDING', 'যাচাই প্রক্রিয়াধীন'
    VERIFICATION_UNVERIFIED = 'VERIFICATION_UNVERIFIED', 'সাধারণ সেবাদাতা'

    # Time Compatibility Factors
    TIME_COMPATIBLE = 'TIME_COMPATIBLE', 'প্রয়োজনের সময়ে সেবা প্রদানে প্রস্তুত'
    TIME_UNKNOWN = 'TIME_UNKNOWN', 'নির্দিষ্ট সময়সূচি নির্ধারিত নয়'
    TIME_INCOMPATIBLE = 'TIME_INCOMPATIBLE', 'অনুরোধের সময়ে অনুপলব্ধ'


# -------------------------------------------------------------------------
# Deterministic Scoring Weights (0 - 100 Range)
# -------------------------------------------------------------------------
DEFAULT_SCORING_WEIGHTS = {
    # Service Match (Max 40.0)
    'SERVICE_EXACT': 40.0,
    'SERVICE_CATEGORY_COMPATIBLE': 20.0,
    'SERVICE_INCOMPATIBLE': 0.0,

    # Location Match (Max 25.0)
    'LOCATION_COVERED_EXACT': 25.0,
    'LOCATION_COVERED_RADIUS': 24.0,
    'LOCATION_COVERED_UPAZILA': 22.0,
    'LOCATION_COVERED_DISTRICT': 18.0,
    'LOCATION_NOT_COVERED': 0.0,

    # Availability Signal (Max 15.0)
    'AVAILABILITY_AVAILABLE': 15.0,
    'AVAILABILITY_BUSY': 8.0,
    'AVAILABILITY_OFFLINE': 4.0,

    # Verification Status (Max 10.0)
    'VERIFICATION_VERIFIED': 10.0,
    'VERIFICATION_PENDING': 5.0,
    'VERIFICATION_UNVERIFIED': 3.0,

    # Time Compatibility (Max 10.0)
    'TIME_COMPATIBLE': 10.0,
    'TIME_UNKNOWN': 5.0,
    'TIME_INCOMPATIBLE': 0.0,
}

# Maximum possible score for validation
MAX_POSSIBLE_SCORE = 100.0
MIN_POSSIBLE_SCORE = 0.0

# Minimum threshold for considering a candidate eligible
DEFAULT_ELIGIBILITY_SCORE_THRESHOLD = 30.0

# Bengali explanations mapped from factor codes
FACTOR_EXPLANATIONS_BN = {
    MatchFactorCode.SERVICE_EXACT: "✓ হুবহু একই সেবা প্রদান করেন",
    MatchFactorCode.SERVICE_CATEGORY_COMPATIBLE: "✓ সম্পর্কিত ক্যাটাগরির সেবা প্রদান করেন",
    MatchFactorCode.LOCATION_COVERED_EXACT: "✓ আপনার নির্দিষ্ট এলাকায় সেবা দেন",
    MatchFactorCode.LOCATION_COVERED_UPAZILA: "✓ আপনার উপজেলায় কভারেজ রয়েছে",
    MatchFactorCode.LOCATION_COVERED_DISTRICT: "✓ জেলাব্যাপী সেবাদানকারী প্রতিষ্ঠান",
    MatchFactorCode.LOCATION_COVERED_RADIUS: "✓ আপনার অবস্থানের নিকটবর্তী আওতাভুক্ত",
    MatchFactorCode.AVAILABILITY_AVAILABLE: "✓ বর্তমানে অনলাইনে সক্রিয় ও প্রস্তুত",
    MatchFactorCode.AVAILABILITY_BUSY: "⚠ বর্তমানে ব্যস্ত, তবে কাজ গ্রহণ করতে পারেন",
    MatchFactorCode.AVAILABILITY_OFFLINE: "⚠ বর্তমানে অফলাইনে আছেন",
    MatchFactorCode.VERIFICATION_VERIFIED: "✓ প্ল্যাটফর্ম কর্তৃক যাচাইকৃত সেবাদাতা",
    MatchFactorCode.VERIFICATION_UNVERIFIED: "— সাধারণ সেবাদাতা প্রোফাইল",
    MatchFactorCode.TIME_COMPATIBLE: "✓ প্রয়োজনের সময়ে সেবা দিতে সক্ষম",
    MatchFactorCode.TIME_UNKNOWN: "— নির্দিষ্ট সময়সূচি এখনো নির্ধারিত নয়",
}
