# SebaCox Phase 8: Offer Lifecycle & State Machine
## “ম্যাচ থেকে প্রস্তাব”

**মূল স্লোগান:** “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”  
**ছোট পরিচিতি:** “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

---

## 1. Offer Status State Machine

The Offer model follows a deterministic, controlled finite state machine:

```text
       [DRAFT]
          │ (submit)
          ▼
      [PENDING] ◄────────────────────────────────┐
       │   │   │   │                             │
       │   │   │   └─► [SUPERSEDED] (Counter) ───┘
       │   │   │
       │   │   └─────► [CANCELLED] (Proposer withdraws)
       │   │
       │   └─────────► [REJECTED]  (Recipient declines)
       │
       ├─────────────► [EXPIRED]   (Time elapsed > expires_at)
       │
       └─────────────► [ACCEPTED]  (Recipient accepts proposal)
```

---

## 2. Status Definitions & Bengali Representations

| Status | Bengali Label (`status_bn`) | Description | Terminal? |
|---|---|---|---|
| `DRAFT` | খসড়া | Initial draft saved by proposer, not yet visible to counterparty. | No |
| `PENDING` | অপেক্ষমাণ | Active proposal awaiting response (Accept/Reject/Counter/Cancel). | No |
| `ACCEPTED` | গ্রহণ করা হয়েছে | Recipient accepted terms. Concludes negotiation chain. | **Yes** |
| `REJECTED` | প্রত্যাখ্যাত | Recipient rejected offer with optional reason. | **Yes** |
| `CANCELLED` | বাতিল | Proposer voluntarily withdrew/cancelled their offer. | **Yes** |
| `EXPIRED` | মেয়াদ শেষ | Automatic expiration after validity window (`expires_at` passed). | **Yes** |
| `SUPERSEDED` | নতুন প্রস্তাবে প্রতিস্থাপিত | Replaced by a newer Counter-Offer version in the chain. | **Yes** |

---

## 3. State Transition Matrix

| Current State | Allowed Next States | Triggered By |
|---|---|---|
| `DRAFT` | `PENDING`, `CANCELLED` | Proposer submit or discard |
| `PENDING` | `ACCEPTED` | Recipient (Requester if Provider offered; Provider if Requester countered) |
| `PENDING` | `REJECTED` | Recipient |
| `PENDING` | `CANCELLED` | Proposer |
| `PENDING` | `SUPERSEDED` | Counter-offer creation |
| `PENDING` | `EXPIRED` | Expiry cron/task or validation check on access |
| `ACCEPTED` | None (Terminal) | Locked |
| `REJECTED` | None (Terminal) | Locked |
| `CANCELLED` | None (Terminal) | Locked |
| `EXPIRED` | None (Terminal) | Locked |
| `SUPERSEDED` | None (Terminal) | Locked |
