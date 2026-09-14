# SebaCox Phase 8: Offer & Counter-Offer Foundation Summary
## “ম্যাচ থেকে প্রস্তাব”

**মূল স্লোগান:** “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”  
**ছোট পরিচিতি:** “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

---

## 1. Overview & Objectives

Phase 8 introduces the **Offer & Counter-Offer Engine** to SebaCox, bridging the gap between matched service providers (Phase 7) and potential transactions. It establishes an immutable, versioned, server-authoritative negotiation mechanism allowing Service Providers and Demand Requesters to exchange binding proposals while respecting strict boundaries (No Deal/Booking/Payment logic until future phases).

---

## 2. Completed Deliverables

### 2.1 Backend Architecture (`backend/apps/offers/`)
- **`models.py`**:
  - `Offer`: Comprehensive Django model featuring `Decimal(12, 2)` monetary fields, self-referential `parent_offer` and `root_offer`, sequential `version`, immutable snapshotting, and strict foreign keys.
  - `OfferAuditLog`: Append-only audit log capturing transitions with user IDs, timestamps, and Bengali action descriptions.
- **`constants.py`**:
  - `OfferType` (`INITIAL`, `COUNTER`).
  - `OfferStatus` (`DRAFT`, `PENDING`, `ACCEPTED`, `REJECTED`, `CANCELLED`, `EXPIRED`, `SUPERSEDED`).
  - Bengali display dictionaries (`OFFER_STATUS_LABELS_BN`, `OFFER_TYPE_LABELS_BN`).
  - `VALID_OFFER_STATUS_TRANSITIONS` and `TERMINAL_OFFER_STATUSES`.
- **`validators.py`**:
  - `validate_offer_pricing`: Strict positive price, non-negative delivery/service fees.
  - `validate_offer_quantity`: Quantity and unit alignment.
  - `validate_offer_expiry`: Timezone-aware validation with 24-hour default and maximum bounds.
  - `validate_demand_eligibility_for_offer` & `validate_provider_eligibility_for_offer`.
  - `validate_offer_status_transition`: State machine transition enforcement.
  - `validate_counter_offer_eligibility`: Strict role and pending-state checks.
- **`services.py`**:
  - `OfferService.create_initial_offer`: Server-side price calculation, snapshot capture, and `OfferCreatedEvent` dispatch.
  - `OfferService.create_counter_offer`: Sequential versioning (`v1 -> v2 -> v3`), auto-superseding of parent offer, role swapping.
  - `OfferService.accept_offer`: One-accepted-offer invariant per demand, demand and offer row locking (`select_for_update`).
  - `OfferService.reject_offer` & `OfferService.cancel_offer`: Reason capture and state progression.
  - `OfferService.expire_pending_offers`: Batch expiration with event dispatching.
- **`selectors.py`**:
  - `get_offer_by_id`, `list_user_offers`, `list_demand_offers`, `get_offer_history_chain`.
- **`permissions.py`**:
  - `IsOfferPartyOrAdmin`, `CanAcceptOffer`, `CanCancelOffer`, `CanRejectOffer`, `CanCounterOffer`.
- **`serializers.py`**:
  - `OfferDetailSerializer`, `OfferListSerializer`, `InitialOfferCreateSerializer`, `CounterOfferCreateSerializer`, `OfferAuditLogSerializer`.
- **`views.py` & `urls.py`**:
  - REST API routes under `/api/v1/offers/` with standard `{success, data, message}` JSON envelopes.
- **`events.py`**:
  - Typed domain events: `OfferCreatedEvent`, `OfferCounteredEvent`, `OfferAcceptedEvent`, `OfferRejectedEvent`, `OfferCancelledEvent`, `OfferExpiredEvent`, `OfferSupersededEvent`.
- **`tasks.py`**:
  - Idempotent periodic task `expire_pending_offers_task` with automatic retry support.

### 2.2 Mobile Application (`mobile/lib/features/offers/`)
- **Models**: `offer_enums.dart`, `offer_model.dart`.
- **Services**: `offer_service.dart`.
- **Widgets**: `offer_status_badge.dart`, `offer_card.dart`.
- **Screens**:
  - `OfferListScreen`: Filter by status tabs with pull-to-refresh.
  - `OfferDetailScreen`: Visual breakdown of price, delivery fee, service fee, total amount, and action triggers.
  - `CreateOfferScreen`: Provider proposal submission with Bengali field labels.
  - `CounterOfferScreen`: Counter-proposal submission with side-by-side comparison.
  - `OfferHistoryScreen`: Complete timeline of revisions and audit events.
- **Typography & Brand**:
  - Enforced *Hind Siliguri* for headings, *Baloo Da 2* for buttons/chips, *Tiro Bangla* for descriptions.

---

## 3. Test Suite & Verification Results

All 8 phases tested and passing:
- Phase 1 (Foundation): **30 Passed**
- Phase 2 (Authentication): **38 Passed**
- Phase 3 (Locations): **42 Passed**
- Phase 4 (Categories): **26 Passed**
- Phase 5 (Providers): **26 Passed**
- Phase 6 (Demands): **62 Passed**
- Phase 7 (Matching): **54 Passed**
- Phase 8 (Offers): **78 Passed**

**Total: 356 Passed, 0 Failed.**
