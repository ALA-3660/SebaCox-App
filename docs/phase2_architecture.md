# SebaCox Phase 2: Authentication & Identity Architecture
**Motto:** *“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”*

---

## 1. Phase 2 Architecture Overview

SebaCox utilizes a **Unified Single Account Model**. Every participant in the Cox's Bazar ecosystem—whether a customer, service provider, seller, landlord, renter, job seeker, or employer—authenticates through a single canonical user account identified primarily by their Bangladeshi mobile number. 

Future business roles will be modeled as capability extensions or attached profiles, preventing fragmented multi-account credential management.

```
+-------------------------------------------------------------+
|                      Flutter Mobile Client                  |
|  [AuthScreen] ---> [OtpScreen] ---> [AuthHomeScreen]        |
|          |                |                  ^              |
|          v                v                  |              |
|  [AuthRepository]  <------------> [Stream<AuthState>]       |
|          |                                                  |
|  [ApiClient] (with automatic Bearer & 401 Refresh handler)  |
+-------------------------------------------------------------+
                              |
                     HTTPS (REST / JSON)
                              |
                              v
+-------------------------------------------------------------+
|                     Django REST Framework                   |
|  /api/v1/auth/register/request-otp/                         |
|  /api/v1/auth/register/verify-otp/                          |
|  /api/v1/auth/login/request-otp/                            |
|  /api/v1/auth/login/verify-otp/                             |
|  /api/v1/auth/token/refresh/                                |
|  /api/v1/auth/logout/                                       |
|  /api/v1/auth/me/                                           |
+-------------------------------------------------------------+
                              |
    +-------------------------+-------------------------+
    |                                                   |
    v                                                   v
[PostgreSQL Database]                           [Redis Cache / Store]
- User (Custom Model)                           - OTP Rate Limiting
- OTPVerification (Salted Hashes)               - Refresh Token Blacklist
- AuthAuditLog (Security audit)                 - Active Session Metadata
```

---

## 2. Authentication Data Flow

### 2.1 Registration & Login Flow
1. **Initiation:** User provides their mobile number (local format `017XXXXXXXX`, with `88`, or `+88`).
2. **Normalization:** The mobile number is cleaned and transformed to canonical E.164 (`+8801XXXXXXXXX`). Operator prefix is verified against active Bangladeshi telecom prefixes (`013`, `014`, `015`, `016`, `017`, `018`, `019`).
3. **OTP Generation:**
   - Rate limit check: verifies that 60 seconds have elapsed since the last OTP request for this number.
   - A 6-digit random code is generated via cryptographically secure pseudo-random number generator (CSPRNG).
   - A 32-byte cryptographic salt is generated.
   - The SHA-256 hash of `salt + otp_code` is computed and stored in `OTPVerification` table.
   - The plain-text OTP is dispatched via SMS gateway (or console in development).
4. **OTP Verification:**
   - User submits the 6-digit OTP.
   - The backend retrieves the latest pending OTP record for the canonical number.
   - Expiration (5 minutes) and attempt counter (< 5 attempts) are validated.
   - The hash of `stored_salt + submitted_code` is compared using constant-time comparison.
   - On success: marked as verified (`is_consumed=True`). User is created or updated as `is_verified=True`.
5. **Token Issuance:**
   - Access token (JWT, valid for 60 minutes) signed with `SECRET_KEY`.
   - Refresh token (JWT, valid for 30 days) signed with `SECRET_KEY`.
   - Tokens returned in the standard response envelope.

---

## 3. Token Lifecycle

| Token Type | Lifetime | Purpose | Storage on Device | Revocation / Invalidation |
|---|---|---|---|---|
| **Access Token** | 60 minutes | Authenticates API requests in `Authorization: Bearer <token>` header | In-memory & `FlutterSecureStorage` | Expiration; refreshed via refresh token |
| **Refresh Token** | 30 days | Exchanged for new access tokens at `/api/v1/auth/token/refresh/` | `FlutterSecureStorage` (iOS Keychain / Android Keystore) | Explicit logout (blacklisted) or expiry |

### Token Refresh Flow
When a protected API endpoint responds with `HTTP 401 Unauthorized` due to token expiration:
1. `ApiClient` intercepts the 401 response.
2. Invokes `_refreshTokenCallback` managed by `AuthRepository`.
3. `AuthRepository` reads stored `refresh_token` and calls `POST /api/v1/auth/token/refresh/`.
4. If successful, new `access_token` is saved, and the original failed request is retried seamlessly.
5. If the refresh token is invalid or expired, the user session is cleared and transitioned to `UnauthenticatedState`.

---

## 4. OTP Security Policy

1. **No Plain-Text Storage:**
   - Plain OTP is never saved to the database.
   - Stored as `hashlib.sha256((salt + otp_code).encode()).hexdigest()`.
2. **Short Lifetime:**
   - OTP expires exactly 5 minutes (300 seconds) after generation.
3. **Resend Cooldown:**
   - Minimum 60-second cooldown between consecutive OTP requests for the same number.
4. **Brute-Force Limit:**
   - Maximum 5 failed attempts per OTP session.
   - Exceeding 5 attempts permanently invalidates the OTP record.
5. **Single-Use Consumption:**
   - Once successfully verified, `is_consumed=True` prevents replay attacks.
6. **Audit Trail:**
   - All OTP requests, failed attempts, and successful logins log an entry to `AuthAuditLog` with IP address and User Agent.

---

## 5. Mobile Number Normalization Rules

* Canonical standard: **E.164** (`+8801XXXXXXXXX`, length 14).
* Valid Bangladeshi operator prefixes:
  * Grameenphone / Skitto: `017`, `013`
  * Banglalink: `019`, `014`
  * Robi / Airtel: `018`, `016`
  * Teletalk: `015`

### Normalization Table

| User Input Format | Canonical E.164 Result | Status |
|---|---|---|
| `01711223344` | `+8801711223344` | Valid (Prepends +88) |
| `8801811223344` | `+8801811223344` | Valid (Prepends +) |
| `+8801911223344` | `+8801911223344` | Valid (Canonical format) |
| `01711-223344` | `+8801711223344` | Valid (Strips formatting) |
| `01211223344` | *ValidationError* | Rejected (Invalid operator 012) |
| `0171122334` | *ValidationError* | Rejected (Too short - 10 digits) |
| `+14155552671` | *ValidationError* | Rejected (Non-Bangladeshi number) |

---

## 6. API Request / Response Contracts

All endpoints strictly adhere to the unified SebaCox JSON envelope.

### 6.1 Register: Request OTP
* **Endpoint:** `POST /api/v1/auth/register/request-otp/`
* **Request:**
  ```json
  {
    "mobile_number": "01712345678"
  }
  ```
* **Response (HTTP 200):**
  ```json
  {
    "success": true,
    "data": {
      "mobile_number": "+8801712345678",
      "expires_in": 300,
      "purpose": "registration"
    },
    "message": "ওটিপি সফলভাবে পাঠানো হয়েছে।"
  }
  ```

### 6.2 Register: Verify OTP
* **Endpoint:** `POST /api/v1/auth/register/verify-otp/`
* **Request:**
  ```json
  {
    "mobile_number": "01712345678",
    "otp_code": "123456"
  }
  ```
* **Response (HTTP 200):**
  ```json
  {
    "success": true,
    "data": {
      "user": {
        "id": 101,
        "mobile_number": "+8801712345678",
        "email": null,
        "is_verified": true,
        "created_at": "2026-09-11T08:00:00Z"
      },
      "tokens": {
        "access_token": "<jwt_access_token>",
        "refresh_token": "<jwt_refresh_token>",
        "token_type": "Bearer",
        "expires_in": 3600
      }
    },
    "message": "রেজিস্ট্রেশন এবং ওটিপি যাচাই সফল হয়েছে।"
  }
  ```

### 6.3 Token Refresh
* **Endpoint:** `POST /api/v1/auth/token/refresh/`
* **Request:**
  ```json
  {
    "refresh_token": "<jwt_refresh_token>"
  }
  ```
* **Response (HTTP 200):**
  ```json
  {
    "success": true,
    "data": {
      "access_token": "<new_jwt_access_token>",
      "token_type": "Bearer",
      "expires_in": 3600
    },
    "message": "টোকেন সফলভাবে রিফ্রেশ করা হয়েছে।"
  }
  ```

### 6.4 Current User Profile
* **Endpoint:** `GET /api/v1/auth/me/`
* **Headers:** `Authorization: Bearer <access_token>`
* **Response (HTTP 200):**
  ```json
  {
    "success": true,
    "data": {
      "id": 101,
      "mobile_number": "+8801712345678",
      "email": null,
      "is_verified": true
    },
    "message": "ব্যবহারকারী প্রোফাইল সফলভাবে পাওয়া গেছে।"
  }
  ```

### 6.5 Logout
* **Endpoint:** `POST /api/v1/auth/logout/`
* **Headers:** `Authorization: Bearer <access_token>`
* **Request:**
  ```json
  {
    "refresh_token": "<jwt_refresh_token>"
  }
  ```
* **Response (HTTP 200):**
  ```json
  {
    "success": true,
    "data": null,
    "message": "লগআউট সফলভাবে সম্পন্ন হয়েছে।"
  }
  ```

---

## 7. Mobile State Flow

The Flutter application architecture uses the **Repository Pattern** with a reactive `Stream<AuthState>` stream:

```
                  [App Initialization]
                           |
               Check Secure Storage for Token
               /                            \
      [Tokens Found]                   [No Tokens]
            |                               |
       Validate / Refresh              UnauthenticatedState
            |                               |
    AuthenticatedState                 AuthScreen
            |                               |
      AuthHomeScreen               Enter Mobile Number
                                            |
                                      Request OTP
                                            |
                                        OtpScreen
                                            |
                                      Verify 6 Digits
                                            |
                                  Save Tokens to Keystore
                                            |
                                    AuthenticatedState
```

---

## 8. Testing Checklist

The test suite in `tests/test_phase2_auth.py` validates all 11 core Phase 2 behaviors:
1. Valid Bangladeshi Phone Accepts & Normalizes (E.164)
2. Invalid Phone Numbers Rejected (Lengths, operators, foreign country codes)
3. Cryptographic Salted OTP Generation & Hash Storage
4. OTP Verified Successfully with Correct Code
5. Wrong OTP Rejected & Attempt Counter Tracked
6. Expiration, Cooldown, and Max Attempt Limits Enforced
7. JWT Access & Refresh Tokens Issued (Bearer Format)
8. Protected Endpoints Reject Requests Without Valid Token (HTTP 401)
9. Protected Endpoints Succeed with Valid Token (Identity Resolution)
10. Refresh Token Creates New Access Token
11. Logout Invalidates Refresh Token
