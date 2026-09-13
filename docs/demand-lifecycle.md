# SebaCox — Demand Lifecycle State Machine (Phase 6)

## 1. State Machine Overview

Demand lifecycle operates under a strict finite state machine (FSM) to safeguard data integrity and audit trails.

### The 7 Canonical States
1. **`DRAFT` (খসড়া)**: Private, fully editable by requester. Invisible in public listings and discovery.
2. **`PUBLISHED` (প্রকাশিত)**: Active, validated, visible in feed/search, can receive responses in future phases.
3. **`PAUSED` (সাময়িক স্থগিত)**: Temporarily hidden from discovery by requester, editable or resumable.
4. **`FULFILLED` (পূরণ হয়েছে)**: Requirement satisfied. Terminal business state, locked from edits.
5. **`CANCELLED` (বাতিলকৃত)**: Withdrawn by requester or admin. Locked from re-activation.
6. **`EXPIRED` (মেয়াদোত্তীর্ণ)**: Automatically transitioned when `expires_at < current_time`.
7. **`CLOSED` (স্থায়ীভাবে বন্ধ)**: Terminal archived historical record.

---

## 2. Transition Matrix

| Source State | Target State | Trigger / Condition | Permitted Actor |
|---|---|---|---|
| `DRAFT` | `PUBLISHED` | Manual action (`/publish/`) with full validation | Owner |
| `DRAFT` | `CANCELLED` | Manual cancellation | Owner / Admin |
| `PUBLISHED` | `PAUSED` | Manual pause (`/pause/`) | Owner |
| `PUBLISHED` | `FULFILLED` | Requirement met (`/fulfill/`) | Owner |
| `PUBLISHED` | `CANCELLED` | Manual cancellation (`/cancel/`) | Owner / Admin |
| `PUBLISHED` | `EXPIRED` | Automatic expiration engine / worker | System |
| `PAUSED` | `PUBLISHED` | Manual resume (`/resume/`) | Owner |
| `PAUSED` | `CANCELLED` | Manual cancellation | Owner / Admin |
| `FULFILLED` | `CLOSED` | Archive / final settlement | Owner / Admin |
| `EXPIRED` | `CLOSED` | Archive | Owner / Admin |

### Strictly Forbidden Jumps
* `DRAFT` ➔ `FULFILLED` (Must be published first)
* `CANCELLED` ➔ `PUBLISHED` (Cancelled demands cannot be reopened)
* `CLOSED` ➔ Any other status (Terminal lock)
* `EXPIRED` ➔ `PUBLISHED` (Expired demands require a new demand to be created)

---

## 3. Server-Side Validation on Publish
Transitioning from `DRAFT` to `PUBLISHED` executes rigorous server-side checks:
1. **Title Length**: Bengali title must be at least 5 characters.
2. **Description Length**: Bengali description must be at least 10 characters.
3. **Location Assignment**: Valid Upazila and location text must be provided.
4. **Expiration Date**: Must be in the future (Asia/Dhaka).
5. **Budget Integrity**: `budget_min` must be <= `budget_max`, and both must be non-negative.
6. **Quantity Integrity**: Must be greater than 0 if specified.
