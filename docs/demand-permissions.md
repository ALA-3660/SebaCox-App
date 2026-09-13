# SebaCox — Demand Permissions & IDOR Protection (Phase 6)

## 1. Object-Level Ownership Model

Every Demand is bound to a single `requester` (the authenticated user who created it).

### Rules Matrix

| Action | Owner | Other Authenticated User | Anonymous | Staff / Admin |
|---|---|---|---|---|
| View Public Demands | ✅ Allowed | ✅ Allowed | ✅ Allowed (Masked) | ✅ Allowed |
| View Draft Demands | ✅ Allowed | ❌ 403 Forbidden | ❌ 401 Unauthorized | ✅ Allowed |
| Create Demand | ✅ Allowed | ✅ Allowed | ❌ 401 Unauthorized | ✅ Allowed |
| Edit Draft Demand | ✅ Allowed | ❌ 403 Forbidden | ❌ 401 Unauthorized | ✅ Allowed |
| Edit Published (Core) | ⚠️ Restricted | ❌ 403 Forbidden | ❌ 401 Unauthorized | ✅ Allowed |
| Pause / Resume | ✅ Allowed | ❌ 403 Forbidden | ❌ 401 Unauthorized | ✅ Allowed |
| Fulfill Demand | ✅ Allowed | ❌ 403 Forbidden | ❌ 401 Unauthorized | ✅ Allowed |
| Cancel Demand | ✅ Allowed | ❌ 403 Forbidden | ❌ 401 Unauthorized | ✅ Allowed (Moderation) |
| Hard Delete | ❌ Blocked | ❌ Blocked | ❌ Blocked | ⚠️ Superuser Only |
| Soft Delete / Archive | ✅ Allowed | ❌ 403 Forbidden | ❌ 401 Unauthorized | ✅ Allowed |

---

## 2. Insecure Direct Object Reference (IDOR) Safeguards

1. **Explicit Ownership Queryset**: Endpoints under `/me/` filter strictly on `requester=request.user`.
2. **Object Permission Hook**: In DRF `DemandViewSet`, `check_object_permissions(request, obj)` executes `IsDemandOwnerOrReadOnly` or `IsDemandOwnerForActions`.
3. **Status-Based Mutation Guard**: If a demand has reached a terminal state (`FULFILLED`, `CANCELLED`, `EXPIRED`, `CLOSED`), mutation is rejected with `400 Bad Request` regardless of ownership.
