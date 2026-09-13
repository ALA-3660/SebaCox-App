#!/usr/bin/env python3
"""
Phase 1 Foundation Test Suite for SebaCox.
Validates:
1. Sensitive data logging filter (masking passwords, OTPs, tokens).
2. Standard response format (success & error).
3. Development settings & structure.
4. Production settings hardening & DEBUG=False requirement.
5. All required Phase 1 files presence.
6. Absence of forbidden Phase 2 business models.
"""
import sys
import os
import types
from pathlib import Path

# Add backend directory to PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

# Provide lightweight compatibility mocks if full external packages aren't pre-installed in local test runner
def ensure_mock_module(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        sys.modules[name] = m
        return m
    return sys.modules[name]

# Mock rest_framework if not installed
try:
    import rest_framework
except ImportError:
    rf = ensure_mock_module('rest_framework')
    rf_views = ensure_mock_module('rest_framework.views')
    rf_response = ensure_mock_module('rest_framework.response')
    rf_status = ensure_mock_module('rest_framework.status')
    rf_exceptions = ensure_mock_module('rest_framework.exceptions')
    rf_permissions = ensure_mock_module('rest_framework.permissions')
    
    class MockResponse:
        def __init__(self, data=None, status=200, headers=None):
            self.data = data
            self.status_code = status
            self.headers = headers or {}
    
    class MockAPIView:
        pass

    rf_response.Response = MockResponse
    rf_views.APIView = MockAPIView
    rf_views.exception_handler = lambda exc, ctx: None
    rf_permissions.AllowAny = type('AllowAny', (), {})
    
    rf_status.HTTP_200_OK = 200
    rf_status.HTTP_400_BAD_REQUEST = 400
    rf_status.HTTP_401_UNAUTHORIZED = 401
    rf_status.HTTP_403_FORBIDDEN = 403
    rf_status.HTTP_404_NOT_FOUND = 404
    rf_status.HTTP_405_METHOD_NOT_ALLOWED = 405
    rf_status.HTTP_500_INTERNAL_SERVER_ERROR = 500

    class APIException(Exception): pass
    class ValidationError(APIException): 
        def __init__(self, detail): self.detail = detail
    class AuthenticationFailed(APIException): 
        def __init__(self, detail="Auth failed"): self.detail = detail
    class NotAuthenticated(APIException): 
        def __init__(self, detail="Not auth"): self.detail = detail
    class PermissionDenied(APIException): 
        def __init__(self, detail="Denied"): self.detail = detail
    class NotFound(APIException): 
        def __init__(self, detail="Not found"): self.detail = detail
    class MethodNotAllowed(APIException): 
        def __init__(self, detail="Not allowed"): self.detail = detail

    rf_exceptions.APIException = APIException
    rf_exceptions.ValidationError = ValidationError
    rf_exceptions.AuthenticationFailed = AuthenticationFailed
    rf_exceptions.NotAuthenticated = NotAuthenticated
    rf_exceptions.PermissionDenied = PermissionDenied
    rf_exceptions.NotFound = NotFound
    rf_exceptions.MethodNotAllowed = MethodNotAllowed

# Mock celery if not installed
try:
    import celery
except ImportError:
    c = ensure_mock_module('celery')
    class MockCelery:
        def __init__(self, name): self.name = name
        def config_from_object(self, *args, **kwargs): pass
        def autodiscover_tasks(self): pass
        def task(self, *args, **kwargs):
            return lambda fn: fn
    c.Celery = MockCelery

passed = 0
failed = 0

def test(name, condition, error_msg=""):
    global passed, failed
    if condition:
        print(f" [PASS] {name}")
        passed += 1
    else:
        print(f"❌ [FAIL] {name} - {error_msg}")
        failed += 1

print("\n==========================================")
print("SebaCox Phase 1 Foundation Verification")
print("“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”")
print("“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”")
print("==========================================\n")

# 1. Test Sensitive Data Filter
try:
    from common.filters import SensitiveDataFilter
    import logging
    
    flt = SensitiveDataFilter()
    record = logging.LogRecord(
        'test', logging.INFO, 'test.py', 1,
        "User auth: password=secret123 otp=456789 token=Bearer eyJhbGciOiJIUz", (), None
    )
    flt.filter(record)
    test(
        "Sensitive Data Logging Masking",
        "password=********" in record.msg and "otp=******" in record.msg and "Bearer ********" in record.msg,
        f"Resulting message was: {record.msg}"
    )
except Exception as e:
    test("Sensitive Data Logging Masking", False, str(e))

# 2. Test Standard Response Structure
try:
    from common.responses import StandardResponse
    
    success_resp = StandardResponse.success(data={"status": "healthy"}, message="SebaCox API is running")
    test(
        "Standard Success Response Contract",
        success_resp.data == {
            "success": True,
            "data": {"status": "healthy"},
            "message": "SebaCox API is running"
        } and success_resp.status_code == 200,
        f"Got: {success_resp.data}"
    )
    
    error_resp = StandardResponse.error(message="অনুরোধটি সম্পন্ন করা যায়নি", errors={"detail": "Not found."})
    test(
        "Standard Error Response Contract",
        error_resp.data == {
            "success": False,
            "data": None,
            "message": "অনুরোধটি সম্পন্ন করা যায়নি",
            "errors": {"detail": "Not found."}
        } and error_resp.status_code == 400,
        f"Got: {error_resp.data}"
    )
except Exception as e:
    test("Standard Response Contract", False, str(e))

# 3. Test Development Settings
try:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.development'
    from config.settings import development as dev_settings
    test("Development DEBUG=True", dev_settings.DEBUG is True)
    test("Development Database Configuration Exists", 'DATABASES' in dir(dev_settings))
    test("Development Cache Configuration Exists", 'CACHES' in dir(dev_settings))
    test("Development CORS Allowed Origins Configured", 'CORS_ALLOWED_ORIGIN_REGEXES' in dir(dev_settings))
except Exception as e:
    test("Development Settings", False, str(e))

# 4. Test Production Settings Hardening
try:
    os.environ['SECRET_KEY'] = 'production-very-secure-key-exceeding-50-characters-and-no-insecure'
    os.environ['ALLOWED_HOSTS'] = 'api.sebacox.com,sebacox.com'
    os.environ['CORS_ALLOWED_ORIGINS'] = 'https://sebacox.com,https://app.sebacox.com'
    
    import importlib
    if 'config.settings.production' in sys.modules:
        del sys.modules['config.settings.production']
    prod_settings = importlib.import_module('config.settings.production')
    
    test("Production DEBUG=False Enforcement", prod_settings.DEBUG is False)
    test("Production Disallow Wildcard CORS", prod_settings.CORS_ALLOW_ALL_ORIGINS is False)
    test("Production SSL Redirect Enabled", prod_settings.SECURE_SSL_REDIRECT is True)
    test("Production Session & CSRF Cookie Secure", prod_settings.SESSION_COOKIE_SECURE is True and prod_settings.CSRF_COOKIE_SECURE is True)
    test("Production HSTS Configured (>= 1 Year)", prod_settings.SECURE_HSTS_SECONDS >= 31536000)
except Exception as e:
    test("Production Settings Hardening", False, str(e))

# 5. Check Project Files Existence
files_to_check = [
    'backend/manage.py',
    'backend/requirements/base.txt',
    'backend/requirements/development.txt',
    'backend/requirements/production.txt',
    'backend/config/urls.py',
    'backend/config/asgi.py',
    'backend/config/wsgi.py',
    'backend/config/settings/base.py',
    'backend/config/settings/development.py',
    'backend/config/settings/production.py',
    'backend/common/responses.py',
    'backend/common/exceptions.py',
    'backend/common/filters.py',
    'backend/common/health.py',
    'backend/workers/celery.py',
    'backend/.env.example',
    'mobile/pubspec.yaml',
    'mobile/lib/main.dart',
    'mobile/lib/core/config/env_config.dart',
    'mobile/lib/core/constants/api_constants.dart',
    'mobile/lib/core/constants/app_colors.dart',
    'mobile/lib/core/network/api_client.dart',
    'mobile/lib/core/network/network_exceptions.dart',
    'mobile/lib/core/storage/secure_storage.dart',
    'mobile/lib/core/theme/app_theme.dart',
    'mobile/lib/core/utils/logger.dart',
    'mobile/lib/shared/models/api_response.dart',
    'mobile/lib/shared/models/health_status.dart',
    'mobile/lib/shared/widgets/status_card.dart',
    'mobile/lib/shared/widgets/app_button.dart',
    'mobile/lib/shared/helpers/error_mapper.dart',
    'mobile/lib/features/home/home_screen.dart',
    'infrastructure/docker/Dockerfile.backend',
    'infrastructure/docker/nginx.conf',
    'infrastructure/docker-compose.yml',
    'infrastructure/docker-compose.prod.yml',
    'docs/architecture.md',
    'docs/api_specification.md',
    'docs/phase1_summary.md',
    '.env.example',
    '.gitignore',
    'README.md',
]

missing_files = [f for f in files_to_check if not (ROOT_DIR / f).exists()]
test("All Phase 1 Architecture Files Present", len(missing_files) == 0, f"Missing: {missing_files}")

# 6. Verify NO Future Phase 3+ Business Models Present (Zero Fake Data)
forbidden_terms = [
    'class Provider', 'class Hotel', 'class Doctor',
    'class Bus', 'class Product', 'class Booking', 'class Payment'
]
business_violations = []
backend_apps_dir = ROOT_DIR / 'backend' / 'apps'
for py_file in backend_apps_dir.glob('**/*.py'):
    # Exclude authentication models where User, OTP, and Audit logs legitimately belong
    if 'authentication' in str(py_file) or 'locations' in str(py_file) or 'categories' in str(py_file):
        continue
    content = py_file.read_text(encoding='utf-8')
    # In Phase 5 providers app, Provider is legitimate, but fake models (Hotel, Doctor, Booking, etc.) remain strictly forbidden
    if 'providers' in str(py_file):
        terms_to_check = [t for t in forbidden_terms if t != 'class Provider']
    else:
        terms_to_check = forbidden_terms

    for term in terms_to_check:
        if term in content:
            business_violations.append(f"{py_file.name}: contains {term}")

test("No Future Phase 3+ Business Models Present (Zero Fake Data)", len(business_violations) == 0, f"Violations: {business_violations}")

print("\n==========================================")
print(f"Test Summary: {passed} Passed, {failed} Failed")
print("==========================================\n")

if failed > 0:
    sys.exit(1)
else:
    sys.exit(0)
