# SebaCox Phase 8: Offer Engine REST API Specification
## “ম্যাচ থেকে প্রস্তাব”

**মূল স্লোগান:** “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”  
**ছোট পরিচিতি:** “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

---

## 1. Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/offers/` | List offers where current user is requester or provider | Yes |
| `POST` | `/api/v1/offers/` | Create initial offer (Provider only) | Yes |
| `GET` | `/api/v1/offers/{id}/` | Get offer detail | Yes |
| `POST` | `/api/v1/offers/{id}/accept/` | Accept pending offer (Recipient only) | Yes |
| `POST` | `/api/v1/offers/{id}/reject/` | Reject pending offer (Recipient only) | Yes |
| `POST` | `/api/v1/offers/{id}/cancel/` | Cancel pending offer (Proposer only) | Yes |
| `POST` | `/api/v1/offers/{id}/counter/` | Submit counter-offer (Recipient only) | Yes |
| `GET` | `/api/v1/offers/{id}/history/` | View full revision chain and audit logs | Yes |
| `GET` | `/api/v1/offers/demand/{demand_id}/` | List all offers for a specific Demand (Requester only) | Yes |

---

## 2. Standard Response Envelope

All API endpoints strictly return standardized JSON envelopes:

```json
{
  "success": true,
  "data": { ... },
  "message": "প্রস্তাবটি সফলভাবে গ্রহণ করা হয়েছে।"
}
```

Error response format:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "প্রস্তাবের মেয়াদ ইতোমধ্যে উত্তীর্ণ হয়ে গেছে।"
  }
}
```
