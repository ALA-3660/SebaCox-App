"""
Location and Geographic Engine Constants & Enums.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
"""
from django.db import models


class GeographicType(models.TextChoices):
    """
    Standard geographic unit types across the platform.
    Used for categorization, filtering, search indexing, and permission boundaries.
    """
    COUNTRY = 'COUNTRY', 'দেশ (Country)'
    DIVISION = 'DIVISION', 'বিভাগ (Division)'
    DISTRICT = 'DISTRICT', 'জেলা (District)'
    UPAZILA = 'UPAZILA', 'উপজেলা (Upazila/Thana)'
    MUNICIPALITY = 'MUNICIPALITY', 'পৌরসভা (Municipality)'
    CITY_CORPORATION = 'CITY_CORPORATION', 'সিটি কর্পোরেশন (City Corporation)'
    UNION = 'UNION', 'ইউনিয়ন (Union Parishad)'
    WARD = 'WARD', 'ওয়ার্ড (Ward)'
    LOCALITY = 'LOCALITY', 'এলাকা / পাড়া (Locality/Para/Moholla)'
    ADDRESS = 'ADDRESS', 'ঠিকানা (Specific Address)'
    POINT = 'POINT', 'ভৌগোলিক স্থানাঙ্ক (Geographic Coordinate)'


class UserLocationType(models.TextChoices):
    """
    Type of location association for a user.
    Maintains strict separation between the device's CURRENT physical location
    and the user's actively SELECTED operational/service area.
    """
    SELECTED = 'SELECTED', 'নির্বাচিত সেবা এলাকা (Selected Service Area)'
    CURRENT = 'CURRENT', 'বর্তমান জিপিএস অবস্থান (Current GPS Location)'
    PREFERRED = 'PREFERRED', 'পছন্দনীয় এলাকা (Preferred Location)'
    HOME = 'HOME', 'বাসা (Home)'
    WORK = 'WORK', 'কর্মস্থল (Work)'
    OTHER = 'OTHER', 'অন্যান্য (Other Saved Place)'


class ServiceAreaType(models.TextChoices):
    """
    Type of service boundary for future providers/businesses.
    """
    ADMINISTRATIVE = 'ADMINISTRATIVE', 'প্রশাসনিক সীমানা (Administrative Boundaries)'
    RADIUS = 'RADIUS', 'নির্দিষ্ট ব্যাসার্ধ (Radial Distance)'


class LocationPermissionStatus(models.TextChoices):
    """
    Client device location permission states.
    """
    NOT_REQUESTED = 'NOT_REQUESTED', 'অনুরোধ করা হয়নি'
    GRANTED = 'GRANTED', 'অনুমতি দেওয়া হয়েছে'
    DENIED = 'DENIED', 'অনুমতি প্রত্যাখ্যাত'
    DENIED_PERMANENTLY = 'DENIED_PERMANENTLY', 'স্থায়ীভাবে প্রত্যাখ্যাত'
    SERVICE_DISABLED = 'SERVICE_DISABLED', 'জিপিএস নিষ্ক্রিয়'


# Geospatial Standards
DEFAULT_SRID = 4326  # WGS 84 GPS standard
EARTH_RADIUS_KM = 6371.0  # Mean radius of Earth in kilometers

# Coordinate Bounds
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0

# Bangladesh Geodetic Bounding Box (for reference & coarse validation)
BD_BOUNDS = {
    'min_lat': 20.57,
    'max_lat': 26.63,
    'min_lon': 88.01,
    'max_lon': 92.67,
}
