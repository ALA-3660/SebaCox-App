# SebaCox System Architecture — Phase 1 Foundation

> **Product Principle:** *“মানুষের প্রয়োজন থেকে সেবার সমাধান।”*  
> **Initial Target:** Cox's Bazar, Bangladesh (later expanding nationwide).

---

## 1. High-Level Architecture Overview

SebaCox is architected as an **API-First, Scalable Modular Platform**:

```
+-------------------------------------------------------------+
|                      Client Layer                           |
|  - Flutter Mobile Application (iOS & Android)               |
|  - Web Portal / PWA (Future)                                |
+------------------------------+------------------------------+
                               |
                               | HTTPS / WSS / REST (/api/v1/)
                               v
+-------------------------------------------------------------+
|                      Ingress Layer                          |
|  - Nginx Reverse Proxy (SSL Termination, Rate Limiting)     |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                      Backend API Layer                      |
|  - Django 5.x + Django REST Framework (DRF)                 |
|  - Gunicorn / Uvicorn (ASGI/WSGI)                           |
|  - Standard Unified Response & Error Handlers               |
+---------------+-----------------------------+---------------+
                |                             |
                v                             v
+-------------------------------+  +--------------------------+
|      Persistence Layer        |  |     In-Memory / Queue    |
|  - PostgreSQL 16+             |  |  - Redis 7+              |
|  - Clean relational schemas   |  |  - Celery Broker         |
|  - Connection pooling         |  |  - Cache & Rate Limiting |
+-------------------------------+  +--------------------------+
```

---

## 2. Directory Structure Conventions

```
SebaCox/
├── backend/                  # Django REST API Service
│   ├── apps/                 # Modular domain apps (Phase 2+)
│   ├── common/               # Shared cross-cutting components (Responses, Exceptions, Filters)
│   ├── config/               # Project configuration & multi-environment settings
│   ├── requirements/         # Split requirements (base, dev, prod)
│   └── workers/              # Celery worker & async task handlers
├── mobile/                   # Flutter cross-platform mobile client
│   └── lib/
│       ├── core/             # Base configurations, network client, theme, storage
│       ├── features/         # Domain feature screens (Home / Health)
│       └── shared/           # Reusable widgets, models, error mappers
├── infrastructure/           # Dockerfiles, Compose specs, Nginx configs
└── docs/                     # Technical specifications & documentation
```

---

## 3. Core Technical Decisions

1. **Django REST Framework (DRF):**
   - Solid security defaults, robust ORM integration, standardized serializer validation.
   - Versioned endpoint `/api/v1/` ensures backward compatibility.
2. **PostgreSQL:**
   - ACID-compliant relational storage configured completely through environment variables (`DATABASE_URL`).
   - Zero hardcoded credentials in codebase.
3. **Redis:**
   - Caching layer (`django-redis`).
   - Message broker for asynchronous background execution via Celery.
   - Foundation for future OTP limits, session locking, and realtime notifications.
4. **Flutter Client:**
   - Native-performance iOS & Android single codebase.
   - Decoupled `ApiClient` with centralized error handling, configurable base URL, and standardized data models.
