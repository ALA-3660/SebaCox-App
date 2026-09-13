# SebaCox — Demand Engine API Specification (Phase 6)

## 1. Response Contract Baseline
All Demand Engine endpoints adhere to the project-wide standardized JSON response envelop established in Phase 1:

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "বার্তা..."
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "message": "ব্যর্থতার কারণ...",
  "errors": {
    "field_name": ["নির্দিষ্ট ত্রুটি বার্তা"]
  }
}
```

---

## 2. Endpoints Summary

Base Path: `/api/v1/demands/`

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/demands/` | List published public demands with filters | No (masked) |
| `POST` | `/api/v1/demands/` | Create a new demand (Draft or Publish) | Yes |
| `GET` | `/api/v1/demands/{id}/` | Get detailed demand info (phone masked if unauthed) | Optional |
| `PATCH` | `/api/v1/demands/{id}/` | Partially update a demand (Owner only) | Yes |
| `DELETE` | `/api/v1/demands/{id}/` | Soft delete / archive a demand (Owner/Admin) | Yes |
| `POST` | `/api/v1/demands/{id}/publish/` | Transition draft to PUBLISHED | Yes |
| `POST` | `/api/v1/demands/{id}/pause/` | Transition published to PAUSED | Yes |
| `POST` | `/api/v1/demands/{id}/resume/` | Transition paused to PUBLISHED | Yes |
| `POST` | `/api/v1/demands/{id}/fulfill/` | Transition published to FULFILLED | Yes |
| `POST` | `/api/v1/demands/{id}/cancel/` | Transition to CANCELLED | Yes |
| `POST` | `/api/v1/demands/{id}/close/` | Transition fulfilled/expired to CLOSED | Yes |
| `GET` | `/api/v1/demands/me/` | Current user's all demands | Yes |
| `GET` | `/api/v1/demands/me/active/` | Current user's active demands | Yes |
| `GET` | `/api/v1/demands/me/history/` | Current user's fulfilled/cancelled/expired demands | Yes |

---

## 3. Query Filtering Parameters (GET `/api/v1/demands/`)

* `q`: Search query matching Bengali or English title and description
* `upazila_id`: Upazila ID (1 to 8 in Cox's Bazar)
* `service_id`: Taxonomy service filter
* `category_id`: Taxonomy category filter
* `demand_type`: `SERVICE`, `PRODUCT`, `RENTAL`, `BOOKING`, `MARKETPLACE`, `INFORMATION`, `OTHER`
* `priority`: `NORMAL`, `URGENT`
* `ordering`: `newest`, `oldest`, `required_at`, `expires_at`

---

## 4. Sample Payloads

### POST `/api/v1/demands/`
```json
{
  "title_bn": "কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন",
  "description_bn": "বাসার মূল সার্কিট ব্রেকার মেরামত ও ওয়্যারিং চেক করার জন্য জরুরি প্রয়োজন।",
  "demand_type": "SERVICE",
  "priority": "URGENT",
  "upazila_id": 1,
  "location_display_bn": "কলাতলী রোড, কক্সবাজার সদর",
  "budget_min": 800,
  "budget_max": 1500,
  "publish_now": true,
  "contact_preference": "BOTH"
}
```
