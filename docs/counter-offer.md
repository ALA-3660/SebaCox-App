# SebaCox Phase 8: Counter-Offer Architecture & Chain Integrity
## “ম্যাচ থেকে প্রস্তাব”

**মূল স্লোগান:** “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”  
**ছোট পরিচিতি:** “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

---

## 1. Counter-Offer Flow

A Counter-Offer is a structured revision of an existing pending proposal. Rather than mutating existing records, each counter-offer creates a new distinct `Offer` row linked to its parent, guaranteeing full auditability and historical integrity.

```text
[v1: INITIAL] Provider proposes ৳85,000  (Status: SUPERSEDED)
      │
      ▼ (Counter by Requester)
[v2: COUNTER] Requester offers ৳80,000   (Status: SUPERSEDED)
      │
      ▼ (Counter by Provider)
[v3: COUNTER] Provider offers ৳82,000    (Status: ACCEPTED)
```

---

## 2. Chain Invariants & Integrity Rules

1. **Sequential Versioning**: Version increments monotonically (`version = parent_offer.version + 1`).
2. **Root Offer Propagation**: All items in a chain point to the initial proposal via `root_offer_id`.
3. **Automatic Superseding**: When a valid counter-offer is persisted inside a database transaction, the immediate parent offer is automatically marked `SUPERSEDED`.
4. **Active Party Inversion**: Proposer and recipient roles alternate naturally:
   - Initial Offer: Proposer = Provider User, Recipient = Requester User.
   - Requester Counter: Proposer = Requester User, Recipient = Provider User.
   - Provider Counter: Proposer = Provider User, Recipient = Requester User.
5. **Pre-condition Validation**:
   - Parent offer must be strictly in `PENDING` status.
   - Parent offer must not be expired (`now() < expires_at`).
   - Counterparty submitting the counter must be the intended recipient (proposer cannot counter their own offer).
   - Demand must remain active (`PUBLISHED`).
   - Provider must remain `ACTIVE`.
