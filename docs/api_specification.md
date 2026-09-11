# SebaCox API Specification — Version 1

> Base Path: `/api/v1`

---

## 1. Standard Response Formats

All endpoints conform to standard JSON contracts.

### Success Format (`2xx`)

```json
{
  "success": true,
  "data": {},
  "message": "সফলভাবে সম্পন্ন হয়েছে"
}
```

### Error Format (`4xx` / `5xx`)

```json
{
  "success": false,
  "data": null,
  "message": "অনুরোধটি সম্পন্ন করা যায়নি",
  "errors": {}
}
```

---

## 2. Endpoints

### Health Check

- **Method:** `GET`
- **Route:** `/api/v1/health/`
- **Authentication:** None (Public)
- **Description:** Verifies API liveness and operational responsiveness.

#### Example Response (HTTP 200 OK)

```json
{
  "success": true,
  "data": {
    "status": "healthy"
  },
  "message": "SebaCox API is running"
}
```

---

## 3. Error Handling Rules

- Validation failures return `HTTP 400 Bad Request` with field-level dictionary under `errors`.
- Missing or unauthorized access returns `HTTP 401 Unauthorized` or `HTTP 403 Forbidden`.
- Unknown routes return `HTTP 404 Not Found`.
- Production servers mask internal tracebacks and database error strings to prevent information leakage.
