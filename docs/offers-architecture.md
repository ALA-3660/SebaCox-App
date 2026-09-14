# SebaCox Phase 8: Offer & Counter-Offer Architecture
## “ম্যাচ থেকে প্রস্তাব”

**মূল স্লোগান:** “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”  
**ছোট পরিচিতি:** “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

---

## 1. Architectural Overview

Phase 8 builds the structured **Offer & Counter-Offer Engine** directly on top of Phase 7's deterministic Matching Engine (`MatchCandidate`). When an eligible Provider is matched with a Demand, or discovers an active Demand within their qualified service/geographic scope, they can submit an initial structured proposal (Offer). The Requester can then evaluate, accept, reject, or submit a Counter-Offer.

```text
USER (Requester)
  ↓
DEMAND (Phase 6: Published)
  ↓
MATCHING ENGINE (Phase 7: Ranked MatchCandidates)
  ↓
PROVIDER (Phase 5: Active & Eligible)
  ↓
OFFER (Phase 8: INITIAL, Pending)
  ↓
COUNTER OFFER (Phase 8: Immutable Chain, v1 → v2 → v3)
  ↓
ACCEPTED OFFER (Phase 8: Terminal Agreement)
  ↓ [STRICT BOUNDARY]
FUTURE DEAL ENGINE (Phase 9+)
```

---

## 2. Core Entities & Relationships

### 2.1 Entity Model
- **`Offer`**: Represents a single immutable version of a proposal or counter-proposal between a Provider and a Requester for a specific Demand.
  - `demand`: ForeignKey to `demands.Demand`
  - `match_candidate`: Nullable ForeignKey to `matching.MatchCandidate`
  - `provider`: ForeignKey to `providers.Provider`
  - `requester`: ForeignKey to `authentication.User` (the creator of the Demand)
  - `proposer`: ForeignKey to `authentication.User` (the party who drafted this specific version)
  - `parent_offer`: Nullable self-referential ForeignKey (the previous offer being revised)
  - `root_offer`: Nullable self-referential ForeignKey (the initial v1 offer in the chain)
  - `version`: Sequential integer (1, 2, 3...)
  - `offer_type`: `INITIAL` | `COUNTER`
  - `status`: `DRAFT` | `PENDING` | `ACCEPTED` | `REJECTED` | `CANCELLED` | `EXPIRED` | `SUPERSEDED`
  - `price`, `delivery_fee`, `service_fee`, `total_amount`: `Decimal(12, 2)`
  - `currency`: Default `BDT`
  - `snapshot`: JSON metadata containing historical state of service/demand/provider at creation time
- **`OfferAuditLog`**: Immutable append-only audit trail logging every lifecycle transition, actor ID, action label, and timestamp.

---

## 3. Strict Boundary Rules

1. **Accepted Offer ≠ Deal**: In Phase 8, when an offer is marked `ACCEPTED`, it signifies mutual agreement on terms and pricing. No Deal, Booking, Order, Payment, Escrow, or Delivery records are created.
2. **Server-Side Authority**: All pricing calculations (`total_amount = price + delivery_fee + service_fee`), expiry verifications, eligibility validations, and version sequences are authoritative on the backend.
3. **Immutability**: Once created, an Offer record's monetary and structural terms are never overwritten. Revisions create new records with incremented version numbers.
4. **One Accepted Offer per Demand**: A Demand cannot have multiple concurrently accepted offers.
