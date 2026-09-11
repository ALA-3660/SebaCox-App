# SebaCox (সেবাকক্স) — Phase 1 Foundation

> **Product Principle:** *“মানুষের প্রয়োজন থেকে সেবার সমাধান।”*  
> **Mission:** Location-based multi-service platform starting in Cox's Bazar and expanding throughout Bangladesh.

---

## 📌 Phase 1 Scope & Architecture

Phase 1 establishes the rock-solid technical foundation for:
1. **Django REST API** (Modular architecture, unified error handling, versioned `/api/v1/`)
2. **Flutter Mobile Client** (Clean network client, dynamic base URL, standardized response parsing)
3. **PostgreSQL 16+** (Relational storage with connection pooling, credentials managed strictly via environment variables)
4. **Redis 7+** (In-memory cache, Celery task broker, rate limiting foundation)
5. **Docker Infrastructure** (Production & local docker-compose configurations)

> **Important Rule:** Phase 1 contains **NO business models** (No User, Provider, Hotel, Doctor, Bus, Product, Booking, Payment). These will be developed in Phase 2+.

---

## 📁 Project Structure

```text
SebaCox/
├── backend/                      # Django REST API Service
│   ├── apps/                     # Modular domain apps (Phase 2+)
│   ├── common/                   # Reusable foundation modules
│   │   ├── exceptions.py         # Unified error response handler
│   │   ├── filters.py            # Sensitive data masking logger
│   │   ├── health.py             # Health check endpoint view
│   │   └── responses.py          # Standard API response helpers
│   ├── config/                   # Django core settings & routing
│   │   ├── settings/
│   │   │   ├── base.py           # Base settings
│   │   │   ├── development.py    # Local dev configuration
│   │   │   └── production.py     # Production settings (DEBUG=False strictly enforced)
│   │   ├── asgi.py               # ASGI async server entry point
│   │   ├── urls.py               # Root URL dispatcher (/api/v1/)
│   │   └── wsgi.py               # WSGI production server entry point
│   ├── requirements/             # Pinned requirements
│   │   ├── base.txt
│   │   ├── development.txt
│   │   └── production.txt
│   ├── workers/                  # Celery async workers
│   │   └── celery.py
│   ├── manage.py
│   └── .env.example
├── mobile/                       # Flutter Mobile Client (iOS / Android)
│   ├── lib/
│   │   ├── core/
│   │   │   ├── config/           # Environment configuration & dynamic base URL
│   │   │   ├── constants/        # API routes & design tokens
│   │   │   ├── network/          # Reusable ApiClient with timeout & error handling
│   │   │   ├── storage/          # Secure & local preferences storage
│   │   │   ├── theme/            # Material 3 custom branding theme
│   │   │   └── utils/            # Masked logger
│   │   ├── features/
│   │   │   └── home/             # Phase 1 Connection status screen
│   │   ├── shared/
│   │   │   ├── helpers/          # Localized error mappers
│   │   │   ├── models/           # Generic ApiResponse & HealthStatus models
│   │   │   └── widgets/          # StatusCard, AppButton
│   │   └── main.dart             # Flutter app entry point
│   └── pubspec.yaml
├── infrastructure/               # Docker & Orchestration
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   └── nginx.conf
│   ├── docker-compose.yml        # Development multi-container stack
│   └── docker-compose.prod.yml   # Production hardened stack
├── docs/                         # Technical specifications & documentation
│   ├── api_specification.md
│   ├── architecture.md
│   └── phase1_summary.md
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 How to Run Backend (Django REST API)

### 1. Prerequisites
- Python 3.10+
- PostgreSQL 14+ (or Docker)
- Redis 6+ (or Docker)

### 2. Setup Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/development.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Update DATABASE_URL and REDIS_URL with your local credentials if needed
```

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
The API is now live at: `http://localhost:8000/api/v1/health/`

### 5. Running with Docker Compose (Recommended)
```bash
cd infrastructure
docker compose up --build
```
This boots Django, PostgreSQL, Redis, and Celery Worker together.

---

## 📱 How to Run Mobile App (Flutter)

### 1. Prerequisites
- Flutter SDK 3.16+
- Android Studio / Xcode / Chrome

### 2. Install Dependencies
```bash
cd mobile
flutter pub get
```

### 3. Run on Device / Simulator / Chrome
```bash
# Run on connected phone or emulator
flutter run

# Or run in Chrome browser
flutter run -d chrome
```

The Flutter app connects to `http://127.0.0.1:8000` by default. You can change the base URL directly within the app screen or via `EnvConfig.setEnvironment(...)`.

---

## 🌐 Health Endpoint & Response Contracts

### Endpoint: `GET /api/v1/health/`

#### Standard Success Response
```json
{
  "success": true,
  "data": {
    "status": "healthy"
  },
  "message": "SebaCox API is running"
}
```

#### Standard Error Response
```json
{
  "success": false,
  "data": null,
  "message": "অনুরোধটি সম্পন্ন করা যায়নি",
  "errors": {}
}
```

---

## 🔒 Security Baseline

- **Zero Hardcoded Secrets**: Loaded purely via environment variables.
- **Production Guardrails**: `DEBUG=False` is strictly enforced in `production.py`.
- **CORS Protection**: Restricted to verified origins; wildcard `*` is strictly disabled in production.
- **Log Privacy**: Automatic regex masking filter suppresses passwords, OTPs, auth tokens, and secret keys from logs.
- **Security Headers**: HSTS, SSL redirect, nosniff, and X-Frame-Options configured.
