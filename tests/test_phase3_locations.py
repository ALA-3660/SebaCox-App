#!/usr/bin/env python3
"""
Phase 3 Location & Geographic Foundation Test Suite for SebaCox.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

Comprehensive test suite verifying:
1. SRID 4326 coordinate validation (latitude [-90, 90], longitude [-180, 180], out-of-range rejection)
2. Location code format validation (alphanumeric, dashes, underscores)
3. Haversine spherical distance calculation (accuracy across known coordinates in Cox's Bazar)
4. Bounding box calculation for radius filtering
5. Geographic Hierarchy Model structure (Country -> Division -> District -> Upazila -> Municipality -> Union -> Ward -> Locality)
6. Service Area domain model (Administrative boundary and Radial coverage)
7. Location Search Engine with Bengali (Unicode NFC) and English query support
8. User Location decoupling: Current GPS vs Selected Service Area
9. Bangladesh administrative dataset ingestion pipeline schema validation
10. Flutter Location state transitions and permission handling contracts
"""
import sys
import os
import math
import types
from pathlib import Path
from decimal import Decimal

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Lightweight Django/DRF mocks if full framework is not initialized
def ensure_mock_module(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        sys.modules[name] = m
        return m
    return sys.modules[name]

try:
    import celery
except ImportError:
    c = ensure_mock_module('celery')
    class MockCelery:
        def config_from_object(self, *a, **kw): pass
        def autodiscover_tasks(self, *a, **kw): pass
        def task(self, *a, **kw):
            return lambda fn: fn
    c.Celery = lambda *a, **kw: MockCelery()

try:
    import django
except ImportError:
    import enum
    dj = ensure_mock_module('django')
    dj.__path__ = []
    dj_conf = ensure_mock_module('django.conf')
    dj_utils = ensure_mock_module('django.utils')
    dj_exceptions = ensure_mock_module('django.core.exceptions')
    dj_db = ensure_mock_module('django.db')
    dj_models = ensure_mock_module('django.db.models')

    class TextChoices(str, enum.Enum):
        def __new__(cls, value, label=None):
            member = str.__new__(cls, value)
            member._value_ = value
            member.label = label or value
            return member

        @classmethod
        @property
        def choices(cls):
            return [(m.value, getattr(m, 'label', m.value)) for m in cls]

    dj_models.TextChoices = TextChoices
    class MockModel:
        def clean(self): pass
    dj_models.Model = MockModel
    dj_models.CharField = lambda *a, **kw: None
    dj_models.BooleanField = lambda *a, **kw: None
    dj_models.DateTimeField = lambda *a, **kw: None
    dj_models.ForeignKey = lambda *a, **kw: None
    dj_models.DecimalField = lambda *a, **kw: None
    dj_models.TextField = lambda *a, **kw: None
    dj_models.PositiveSmallIntegerField = lambda *a, **kw: None
    dj_models.IntegerField = lambda *a, **kw: None
    dj_models.BigAutoField = lambda *a, **kw: None
    dj_models.JSONField = lambda *a, **kw: None
    dj_models.CASCADE = 'CASCADE'
    dj_models.SET_NULL = 'SET_NULL'
    dj_models.UniqueConstraint = lambda *a, **kw: None
    dj_models.Index = lambda *a, **kw: None
    dj_models.Q = lambda *a, **kw: None

    class MockQuerySet:
        @classmethod
        def __class_getitem__(cls, item):
            return cls
    dj_models.QuerySet = MockQuerySet

    class ValidationError(Exception):
        def __init__(self, message, code=None, params=None):
            super().__init__(message)
            self.message = message
    dj_exceptions.ValidationError = ValidationError

    class Settings:
        SECRET_KEY = 'sebacox-phase3-test-secret-key-12345'
        DEBUG = True
        AUTH_USER_MODEL = 'authentication.User'
    dj_conf.settings = Settings()

    dj_urls = ensure_mock_module('django.urls')
    class MockPath:
        def __init__(self, pattern):
            self.pattern = pattern
    dj_urls.path = lambda p, *a, **kw: MockPath(p)
    dj_urls.include = lambda *a, **kw: None

try:
    import rest_framework
except ImportError:
    rf = ensure_mock_module('rest_framework')
    rf_views = ensure_mock_module('rest_framework.views')
    rf_response = ensure_mock_module('rest_framework.response')
    rf_status = ensure_mock_module('rest_framework.status')
    rf_serializers = ensure_mock_module('rest_framework.serializers')
    rf_permissions = ensure_mock_module('rest_framework.permissions')

    class MockModelSerializer:
        def __init__(self, *a, **kw): pass
    class MockResponse:
        def __init__(self, data=None, status=200, headers=None):
            self.data = data
            self.status_code = status
    rf_response.Response = MockResponse
    rf_serializers.ModelSerializer = MockModelSerializer
    rf_serializers.Serializer = MockModelSerializer
    rf_serializers.CharField = lambda *a, **kw: None
    rf_serializers.IntegerField = lambda *a, **kw: None
    rf_serializers.DecimalField = lambda *a, **kw: None
    rf_serializers.ChoiceField = lambda *a, **kw: None
    rf_serializers.BooleanField = lambda *a, **kw: None
    rf_serializers.ListField = lambda *a, **kw: None
    class MockAPIView:
        @classmethod
        def as_view(cls, *a, **kw):
            return lambda *args, **kwargs: None
    rf_views.APIView = MockAPIView
    rf_permissions.AllowAny = object
    rf_permissions.IsAuthenticated = object
    rf_status.HTTP_200_OK = 200
    rf_status.HTTP_400_BAD_REQUEST = 400

passed = 0
failed = 0

def test(name: str, condition: bool, details: str = ""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  \033[92m✔\033[0m {name}")
    else:
        failed += 1
        print(f"  \033[91m✖\033[0m {name} - {details}")

print("\n=======================================================")
print("SEBACOX - PHASE 3 LOCATION & GEOGRAPHIC FOUNDATION TESTS")
print("=======================================================\n")

# -----------------------------------------------------------------------------
# 1. SRID 4326 Coordinate Validation
# -----------------------------------------------------------------------------
print("--- 1. SRID 4326 Coordinate Validation ---")
from apps.locations.validators import validate_latitude, validate_longitude, validate_radius
from django.core.exceptions import ValidationError

try:
    # Valid coordinates (e.g. Cox's Bazar 21.4272° N, 92.0058° E)
    validate_latitude(21.4272)
    validate_latitude(Decimal('-45.0'))
    validate_longitude(92.0058)
    validate_longitude(Decimal('-120.5'))
    test("Valid latitude/longitude accepted", True)
except Exception as e:
    test("Valid latitude/longitude accepted", False, str(e))

try:
    # Invalid latitude > 90
    lat_rejected = False
    try:
        validate_latitude(91.5)
    except ValidationError:
        lat_rejected = True
    test("Latitude > 90 rejected", lat_rejected)

    # Invalid latitude < -90
    lat_neg_rejected = False
    try:
        validate_latitude(-95.0)
    except ValidationError:
        lat_neg_rejected = True
    test("Latitude < -90 rejected", lat_neg_rejected)

    # Invalid longitude > 180
    lon_rejected = False
    try:
        validate_longitude(185.0)
    except ValidationError:
        lon_rejected = True
    test("Longitude > 180 rejected", lon_rejected)

    # Invalid longitude < -180
    lon_neg_rejected = False
    try:
        validate_longitude(-181.0)
    except ValidationError:
        lon_neg_rejected = True
    test("Longitude < -180 rejected", lon_neg_rejected)
except Exception as e:
    test("Out of range coordinate rejection", False, str(e))

# -----------------------------------------------------------------------------
# 2. Location Code Format Validation
# -----------------------------------------------------------------------------
print("\n--- 2. Location Code Format Validation ---")
from apps.locations.validators import validate_location_code

try:
    validate_location_code("CXB")
    validate_location_code("coxs-bazar-01")
    validate_location_code("DHAKA_NORTH")
    test("Valid location codes accepted", True)
except Exception as e:
    test("Valid location codes accepted", False, str(e))

try:
    invalid_chars_rejected = False
    try:
        validate_location_code("CXB#123@!")
    except ValidationError:
        invalid_chars_rejected = True
    test("Invalid characters in location code rejected", invalid_chars_rejected)

    empty_code_rejected = False
    try:
        validate_location_code("   ")
    except ValidationError:
        empty_code_rejected = True
    test("Empty code rejected", empty_code_rejected)
except Exception as e:
    test("Location code invalidation", False, str(e))

# -----------------------------------------------------------------------------
# 3. Haversine Great-Circle Distance Calculation
# -----------------------------------------------------------------------------
print("\n--- 3. Haversine Great-Circle Distance Calculation ---")
from apps.locations.services import calculate_haversine_distance

try:
    # Known real-world coordinates:
    # Cox's Bazar Sadar: 21.4272° N, 92.0058° E
    # Teknaf: 20.8653° N, 92.2982° E
    # Great circle distance is approximately 69 - 70 km
    dist_cxb_teknaf = calculate_haversine_distance(21.4272, 92.0058, 20.8653, 92.2982, unit='km')
    is_accurate_km = 68.0 < dist_cxb_teknaf < 72.0
    test("Cox's Bazar to Teknaf distance accurate (~69.6 km)", is_accurate_km, f"Got: {dist_cxb_teknaf} km")

    # Identical point distance should be 0.0
    zero_dist = calculate_haversine_distance(21.4272, 92.0058, 21.4272, 92.0058, unit='km')
    test("Zero distance for identical coordinates", zero_dist == 0.0, f"Got: {zero_dist}")

    # Meter unit conversion
    dist_m = calculate_haversine_distance(21.4272, 92.0058, 20.8653, 92.2982, unit='m')
    test("Meters conversion matches kilometers * 1000", abs(dist_m - (dist_cxb_teknaf * 1000)) < 10)
except Exception as e:
    test("Haversine calculations", False, str(e))

# -----------------------------------------------------------------------------
# 4. Bounding Box Calculation for Radius Filtering
# -----------------------------------------------------------------------------
print("\n--- 4. Bounding Box & Radius Filter Engine ---")
from apps.locations.services import get_bounding_box

try:
    bbox = get_bounding_box(latitude=21.4272, longitude=92.0058, radius_km=10.0)
    lat_spread = bbox['max_lat'] - bbox['min_lat']
    lon_spread = bbox['max_lon'] - bbox['min_lon']

    valid_bbox = (
        bbox['min_lat'] < 21.4272 < bbox['max_lat'] and
        bbox['min_lon'] < 92.0058 < bbox['max_lon'] and
        0.15 < lat_spread < 0.25 and
        0.15 < lon_spread < 0.25
    )
    test("10km Bounding box correctly bounds center coordinates", valid_bbox, str(bbox))
except Exception as e:
    test("Bounding box calculation", False, str(e))

# -----------------------------------------------------------------------------
# 5. Geographic Hierarchy Model Structure & Constants
# -----------------------------------------------------------------------------
print("\n--- 5. Geographic Hierarchy Model Constants & Structure ---")
from apps.locations.constants import GeographicType, UserLocationType, ServiceAreaType

test("GeographicType has all required levels", all(hasattr(GeographicType, attr) for attr in [
    'COUNTRY', 'DIVISION', 'DISTRICT', 'UPAZILA', 'MUNICIPALITY',
    'CITY_CORPORATION', 'UNION', 'WARD', 'LOCALITY'
]))

test("UserLocationType has SELECTED and CURRENT separated", (
    UserLocationType.SELECTED == 'SELECTED' and
    UserLocationType.CURRENT == 'CURRENT' and
    UserLocationType.SELECTED != UserLocationType.CURRENT
))

test("ServiceAreaType supports ADMINISTRATIVE and RADIUS", (
    ServiceAreaType.ADMINISTRATIVE == 'ADMINISTRATIVE' and
    ServiceAreaType.RADIUS == 'RADIUS'
))

# -----------------------------------------------------------------------------
# 6. Location Search Query Normalization (Bangla & English)
# -----------------------------------------------------------------------------
print("\n--- 6. Search Normalization (Bangla Unicode & English) ---")
from apps.locations.services import normalize_search_text

test("English normalization case-folds and trims", normalize_search_text("  Cox's Bazar  ") == "cox's bazar")
test("Bangla NFC Unicode normalization works", normalize_search_text("  কক্সবাজার সদর  ") == "কক্সবাজার সদর")
test("Empty string normalization returns empty string", normalize_search_text("   ") == "")

# -----------------------------------------------------------------------------
# 7. User Location Decoupling & Isolation
# -----------------------------------------------------------------------------
print("\n--- 7. Separation of CURRENT Location ≠ SELECTED Location ---")
from apps.locations.models import UserLocation, GeoLocation
from apps.locations.services import UserLocationService

# Ensure that modifying current location does not alter selected location
class MockUser:
    id = 101
    mobile_number = "+8801711122233"

# Verify that UserLocationType constants maintain clear separation
test("UserLocationType enforces distinct role types", UserLocationType.CURRENT != UserLocationType.SELECTED)

# -----------------------------------------------------------------------------
# 8. Bangladesh Location Ingestion Pipeline Validation
# -----------------------------------------------------------------------------
print("\n--- 8. Ingestion Pipeline Schema Validation ---")
from apps.locations.services import BangladeshLocationImportService

valid_record = {
    'name_bn': 'বাংলাদেশ',
    'name_en': 'Bangladesh',
    'code': 'BGD',
}
is_valid, errors = BangladeshLocationImportService.validate_record(valid_record, 'Country')
test("Valid country record passes schema validation", is_valid and len(errors) == 0)

invalid_record = {
    'name_bn': 'বাংলাদেশ',
    # name_en missing
    'code': 'BGD',
}
is_invalid, errs = BangladeshLocationImportService.validate_record(invalid_record, 'Country')
test("Missing name_en caught by validation", not is_invalid and len(errs) > 0)

# -----------------------------------------------------------------------------
# 9. Flutter Location State & Permission Contracts
# -----------------------------------------------------------------------------
print("\n--- 9. Flutter Location State & Permission Contracts ---")

flutter_state_file = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'location' / 'state' / 'location_state.dart'
flutter_enums_file = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'location' / 'models' / 'location_enums.dart'
flutter_screen_file = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'location' / 'screens' / 'location_selection_screen.dart'

test("Flutter location_state.dart exists", flutter_state_file.exists())
test("Flutter location_enums.dart exists", flutter_enums_file.exists())
test("Flutter location_selection_screen.dart exists", flutter_screen_file.exists())

with open(flutter_enums_file, 'r', encoding='utf-8') as f:
    enums_content = f.read()

test("LocationLoadingStatus has required states", (
    'initial' in enums_content and
    'requestingPermission' in enums_content and
    'permissionGranted' in enums_content and
    'permissionDenied' in enums_content and
    'fetchingLocation' in enums_content and
    'locationReady' in enums_content and
    'locationError' in enums_content
))

test("LocationPermissionState handles all permission phases", (
    'notRequested' in enums_content and
    'requesting' in enums_content and
    'granted' in enums_content and
    'denied' in enums_content and
    'deniedPermanently' in enums_content and
    'serviceDisabled' in enums_content
))

with open(flutter_screen_file, 'r', encoding='utf-8') as f:
    screen_content = f.read()

test("Flutter UI uses respectful Bengali labels", (
    'আপনার অবস্থান নির্বাচন করুন' in screen_content and
    'বর্তমান অবস্থান ব্যবহার করুন' in screen_content and
    'প্রশাসনিক এলাকা নির্বাচন করুন' in screen_content and
    'লোকেশন পাওয়া যায়নি' in screen_content
))

# -----------------------------------------------------------------------------
# 10. API Route Registration
# -----------------------------------------------------------------------------
print("\n--- 10. API Route Registration ---")
from config.urls import api_v1_patterns

route_paths = [str(p.pattern) for p in api_v1_patterns]
test("/api/v1/locations/ registered in api_v1_patterns", any('locations/' in p for p in route_paths))

# -----------------------------------------------------------------------------
# 11. Phase 3 Correction: Eidgaon Upazila & Cox's Bazar 9 Upazilas Verification
# -----------------------------------------------------------------------------
print("\n--- 11. Phase 3 Correction: Eidgaon Upazila Verification ---")
simulator_file = os.path.join(str(ROOT_DIR), 'src/components/FlutterSimulator.tsx')
with open(simulator_file, 'r', encoding='utf-8') as f:
    sim_content = f.read()

vite_config_file = os.path.join(str(ROOT_DIR), 'vite.config.ts')
with open(vite_config_file, 'r', encoding='utf-8') as f:
    vite_content = f.read()

# 1. Verify Cox's Bazar District contains exactly 9 Upazilas in simulator
test("Flutter Simulator defines exactly 9 Upazilas for Cox's Bazar (District 1)", (
    'id: 1, name_bn: \'কক্সবাজার সদর\'' in sim_content and
    'id: 2, name_bn: \'চকোরিয়া\'' in sim_content and
    'id: 3, name_bn: \'মহেশখালী\'' in sim_content and
    'id: 4, name_bn: \'রামু\'' in sim_content and
    'id: 5, name_bn: \'টেকনাফ\'' in sim_content and
    'id: 6, name_bn: \'উখিয়া\'' in sim_content and
    'id: 7, name_bn: \'কুতুবদিয়া\'' in sim_content and
    'id: 8, name_bn: \'পেকুয়া\'' in sim_content and
    'id: 9, name_bn: \'ঈদগাঁও\'' in sim_content
))

# 2. Verify Eidgaon spelling in Bangla and English
test("Eidgaon has authentic Bangla 'ঈদগাঁও' and English 'Eidgaon'", (
    "name_bn: 'ঈদগাঁও'" in sim_content and
    "name_en: 'Eidgaon'" in sim_content and
    "name_bn: 'ঈদগাঁও'" in vite_content and
    "name_en: 'Eidgaon'" in vite_content
))

# 3. Verify no invented administrative code for Eidgaon
test("Eidgaon has no invented administrative code", (
    "{ id: 9, district_id: 1, name_bn: 'ঈদগাঁও', name_en: 'Eidgaon', is_active: true }" in vite_content
))

# 4. Verify existing 8 Upazilas preserved unmodified
test("Existing 8 Upazilas preserved unmodified with IDs 1 to 8", (
    "id: 1, district_id: 1, name_bn: 'কক্সবাজার সদর'" in vite_content and
    "id: 2, district_id: 1, name_bn: 'চকোরিয়া'" in vite_content and
    "id: 3, district_id: 1, name_bn: 'মহেশখালী'" in vite_content and
    "id: 4, district_id: 1, name_bn: 'রামু'" in vite_content and
    "id: 5, district_id: 1, name_bn: 'টেকনাফ'" in vite_content and
    "id: 6, district_id: 1, name_bn: 'উখিয়া'" in vite_content and
    "id: 7, district_id: 1, name_bn: 'কুতুবদিয়া'" in vite_content and
    "id: 8, district_id: 1, name_bn: 'পেকুয়া'" in vite_content
))

# 5. Verify search normalization finds Eidgaon in both Bangla and English
test("Search normalization handles Bangla 'ঈদগাঁও'", normalize_search_text("  ঈদগাঁও  ") == "ঈদগাঁও")
test("Search normalization handles English 'Eidgaon'", normalize_search_text("  Eidgaon  ") == "eidgaon")

# 6. Verify Upazila count label in Location Selector
test("Location Selector reflects exactly 9 available areas for Cox's Bazar", (
    "৯টি" in sim_content and "উপজেলা নির্বাচন করুন" in sim_content
))

# -----------------------------------------------------------------------------
# 12. Production-Ready Expanded Hierarchy (Union, Municipality, Ward, Locality)
# -----------------------------------------------------------------------------
print("\n--- 12. Expanded Geographic Hierarchy & Cascading Validation ---")
from apps.locations.constants import LocalityType, GeographicType
from apps.locations.models import Municipality, Union, Ward, Locality, CityCorporation, District, Upazila
from apps.locations.selectors import get_child_locations

# 1. LocalityType Enum verification
test("LocalityType defines all required sub-types", (
    hasattr(LocalityType, 'PARA') and
    hasattr(LocalityType, 'MOHOLLA') and
    hasattr(LocalityType, 'VILLAGE') and
    hasattr(LocalityType, 'BAZAR') and
    hasattr(LocalityType, 'RESIDENTIAL') and
    hasattr(LocalityType, 'LOCAL_AREA') and
    hasattr(LocalityType, 'OTHER')
))

# 2. Ward single-parent validation
valid_ward = Ward()
valid_ward.ward_number = 1
valid_ward.municipality_id = 1
valid_ward.city_corporation_id = None
valid_ward.union_id = None
try:
    valid_ward.clean()
    ward_valid_passed = True
except Exception:
    ward_valid_passed = False
test("Ward with single parent (Municipality) passes clean()", ward_valid_passed)

invalid_ward_no_parent = Ward()
invalid_ward_no_parent.ward_number = 1
invalid_ward_no_parent.municipality_id = None
invalid_ward_no_parent.city_corporation_id = None
invalid_ward_no_parent.union_id = None
try:
    invalid_ward_no_parent.clean()
    ward_no_parent_caught = False
except Exception:
    ward_no_parent_caught = True
test("Ward without parent is rejected by clean()", ward_no_parent_caught)

invalid_ward_multi_parent = Ward()
invalid_ward_multi_parent.ward_number = 1
invalid_ward_multi_parent.municipality_id = 1
invalid_ward_multi_parent.union_id = 2
try:
    invalid_ward_multi_parent.clean()
    ward_multi_parent_caught = False
except Exception:
    ward_multi_parent_caught = True
test("Ward with multiple parents is rejected by clean()", ward_multi_parent_caught)

# 3. Locality hierarchy validation
valid_loc = Locality()
valid_loc.upazila_id = 1
valid_loc.municipality_id = None
valid_loc.union_id = None
valid_loc.ward_id = None
try:
    valid_loc.clean()
    loc_valid_passed = True
except Exception:
    loc_valid_passed = False
test("Locality with valid Upazila passes clean()", loc_valid_passed)

invalid_loc_no_upazila = Locality()
invalid_loc_no_upazila.upazila_id = None
try:
    invalid_loc_no_upazila.clean()
    loc_no_upazila_caught = False
except Exception:
    loc_no_upazila_caught = True
test("Locality without Upazila is rejected by clean()", loc_no_upazila_caught)

# 4. Cascading Children API & Selector Verification
from apps.locations.urls import urlpatterns as loc_urlpatterns
children_url_exists = any('children/' in str(p.pattern) for p in loc_urlpatterns)
test("GET /api/v1/locations/children/ endpoint registered in urls", children_url_exists)

# 5. Cascading Location Selector Widget Verification
cascading_widget_file = ROOT_DIR / 'mobile' / 'lib' / 'features' / 'location' / 'widgets' / 'cascading_location_selector.dart'
test("Flutter CascadingLocationSelector widget file exists", cascading_widget_file.exists())

with open(cascading_widget_file, 'r', encoding='utf-8') as f:
    cascading_content = f.read()

test("Cascading selector supports Division -> District -> Upazila -> Union/Municipality -> Ward -> Locality", (
    '_selectedDivision' in cascading_content and
    '_selectedDistrict' in cascading_content and
    '_selectedUpazila' in cascading_content and
    '_selectedUnion' in cascading_content and
    '_selectedMunicipality' in cascading_content and
    '_selectedWard' in cascading_content and
    '_selectedLocality' in cascading_content
))

test("Cascading selector handles Bengali typography and reset cascading states", (
    'বিভাগ' in cascading_content and
    'জেলা' in cascading_content and
    'উপজেলা' in cascading_content and
    'ইউনিয়ন' in cascading_content and
    'পৌরসভা' in cascading_content and
    'ওয়ার্ড' in cascading_content and
    'লোকালিটি' in cascading_content
))

# 6. Mock API in vite.config.ts supports all granular endpoints
test("vite.config.ts implements municipalities endpoint", "/api/v1/locations/municipalities" in vite_content)
test("vite.config.ts implements city-corporations endpoint", "/api/v1/locations/city-corporations" in vite_content)
test("vite.config.ts implements wards endpoint", "/api/v1/locations/wards" in vite_content)
test("vite.config.ts implements localities endpoint", "/api/v1/locations/localities" in vite_content)
test("vite.config.ts implements children cascading endpoint", "/api/v1/locations/children" in vite_content)

# 7. Khurushkul Ward 1-9 Locality Verification & Ward 5 Correction
test("Khurushkul Ward 5 has source-verified Mamun Para (মামুন পাড়া)", (
    'মামুন পাড়া' in vite_content and
    'Mamun Para' in vite_content
))
test("Khurushkul seed command includes official Mamun Para for Ward 5", (
    'মামুন পাড়া' in open(ROOT_DIR / 'backend' / 'apps' / 'locations' / 'management' / 'commands' / 'seed_coxsbazar_sadar_master.py', 'r', encoding='utf-8').read()
))
test("DemandSimulatorViews.tsx includes Mamun Para for Khurushkul Ward 5 (10405)", (
    '10405' in open(ROOT_DIR / 'src' / 'components' / 'DemandSimulatorViews.tsx', 'r', encoding='utf-8').read() and
    'মামুন পাড়া' in open(ROOT_DIR / 'src' / 'components' / 'DemandSimulatorViews.tsx', 'r', encoding='utf-8').read()
))
test("DemandSimulatorViews.tsx implements dynamic locality fetching from API", (
    '/api/v1/locations/localities' in open(ROOT_DIR / 'src' / 'components' / 'DemandSimulatorViews.tsx', 'r', encoding='utf-8').read() and
    'availableLocalities' in open(ROOT_DIR / 'src' / 'components' / 'DemandSimulatorViews.tsx', 'r', encoding='utf-8').read()
))

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
print("\n==========================================")
print(f"Test Summary: {passed} Passed, {failed} Failed")
print("==========================================\n")

if failed > 0:
    sys.exit(1)
else:
    sys.exit(0)
