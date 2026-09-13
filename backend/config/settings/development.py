"""
Development Settings for SebaCox.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import os
from .base import *  # noqa: F403

DEBUG = True

# Allow emulator and local network in development
ALLOWED_HOSTS = ['*']

# Extended CORS for local development and mobile emulators (Android 10.0.2.2, iOS simulator)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
    r"^http://10\.0\.2\.2:\d+$",
]

# Database fallback for seamless local testing if DATABASE_URL is not set or Postgres unavailable
if not os.environ.get('DATABASE_URL') and not os.environ.get('DB_PASSWORD'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
        }
    }

# Cache fallback for development if Redis is not running locally
if os.environ.get('USE_LOCAL_CACHE', 'false').lower() == 'true':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'sebacox-dev-cache',
        }
    }

# Development specific logging
LOGGING['loggers']['sebacox']['level'] = 'DEBUG'  # noqa: F405
LOGGING['loggers']['common']['level'] = 'DEBUG'  # noqa: F405
