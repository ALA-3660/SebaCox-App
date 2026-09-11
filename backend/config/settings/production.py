"""
Production Settings for SebaCox.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"

CRITICAL: Production configuration strictly forbids DEBUG=True and wildcard CORS.
"""
import os
from .base import *  # noqa: F403

# HARD REQUIREMENT: DEBUG must never be True in production
DEBUG = False

# Ensure real SECRET_KEY is set in environment
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY or 'django-insecure' in SECRET_KEY:
    raise ValueError("Production SECRET_KEY environment variable is missing or insecure!")

# Production Allowed Hosts (Strict)
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get('ALLOWED_HOSTS', '').split(',')
    if host.strip()
]
if not ALLOWED_HOSTS:
    raise ValueError("Production ALLOWED_HOSTS environment variable must be configured!")

# Strict CORS: Wildcard is strictly forbidden
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip()
]
if not CORS_ALLOWED_ORIGINS:
    raise ValueError("Production CORS_ALLOWED_ORIGINS environment variable must be specified!")

# Security Hardening
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() == 'true'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Production Logging: High priority events
LOGGING['handlers']['console']['level'] = 'INFO'  # noqa: F405
LOGGING['root']['level'] = 'INFO'  # noqa: F405
