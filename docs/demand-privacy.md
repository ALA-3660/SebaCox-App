# SebaCox — Demand Privacy & Phone Masking Policy (Phase 6)

## 1. Privacy First Architecture
The user account phone number is an authenticated identity credential and must never be leaked directly in public serializers or list views.

### 2. Visibility Levels
* `PUBLIC`: The demand is visible to anyone in Cox's Bazar and surrounding areas.
* `REGISTERED_USERS`: Visible only to authenticated users logged into SebaCox.
* `PRIVATE`: Visible strictly to the requester and staff administrators.

---

## 3. Contact Preferences & Masking Matrix
Users configure how they wish to be contacted:
* `IN_APP_ONLY`: Direct phone is completely suppressed; only in-app messaging (future phase) will be used.
* `PHONE`: Direct voice call is permitted.
* `BOTH`: Both in-app and phone are permitted.

### Masking Rules:
When a demand is viewed by an anonymous or unauthorized user:
* Phone numbers are strictly masked, revealing only the operator prefix and trailing digits:
  ```
  Original: +8801819234567
  Masked:   +88018****4567
  ```
* When `contact_preference == IN_APP_ONLY`, the phone field returns `null` or an empty string in public views.
* The owner user viewing their own demand (`is_owner == True`) always views the unmasked original phone number.
