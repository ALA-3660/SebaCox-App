# SebaCox Phase 8: Offer Security, Permissions & IDOR Protection
## “ম্যাচ থেকে প্রস্তাব”

**মূল স্লোগান:** “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”  
**ছোট পরিচিতি:** “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

---

## 1. Permission Matrix & Access Control

Access to Offer resources is strictly governed by object-level permissions (`IsOfferParticipantOrStaff`):

| User Persona | View Offer | Create Initial Offer | Accept Offer | Reject Offer | Cancel Offer | Counter Offer | View History |
|---|---|---|---|---|---|---|---|
| **Demand Requester** | ✅ (Own demand) | ❌ (Cannot offer self) | ✅ (If recipient) | ✅ (If recipient) | ✅ (If countered) | ✅ (If recipient) | ✅ |
| **Provider Owner** | ✅ (Own provider) | ✅ (Eligible demand) | ✅ (If recipient) | ✅ (If recipient) | ✅ (If proposer) | ✅ (If recipient) | ✅ |
| **Unrelated User (Stranger)** | ❌ (403/404 IDOR block) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Staff / Admin** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 2. IDOR (Insecure Direct Object References) Prevention

1. **Queryset Scoping**: Selectors and views automatically scope list and search querysets to offers where `requester = user` OR `provider.user = user`.
2. **Object Level Checks**: Direct lookups via `pk` enforce `has_object_permission` verifying the requester identity or provider owner identity.
3. **Impersonation Prevention**: In mutation actions, the acting user is derived strictly from `request.user`, never trusted from payload parameters.
