# SebaCox — Demand Engine Architecture (Phase 6)

## 1. Executive Summary & Brand Foundation
SebaCox-এর মূল দর্শন ও ব্র্যান্ড পরিচয়:
* **মূল স্লোগান**: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
* **সংক্ষিপ্ত পরিচিতি**: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

Phase 6-এ SebaCox প্ল্যাটফর্মে যুক্ত হয়েছে একটি উৎপাদনমুখী, নিরাপদ এবং এক্সটেনসিবল **Demand Engine (“আমার প্রয়োজন”)**। এটি ব্যবহারকারীকে যেকোনো জরুরি বা পরিকল্পিত সেবা, পণ্য, ভাড়া বা বুকিংয়ের চাহিদা কাঠামোবদ্ধভাবে প্রকাশ করার সুযোগ দেয়।

---

## 2. Core Architectural Principles

### 2.1 The Cardinal Separation Rule
```
User  ≠  Provider  ≠  Service  ≠  Demand
```
1. **User**: প্ল্যাটফর্মের আসল পরিচয়ধারী গ্রাহক (Requester)।
2. **Provider**: সেবাদাতা প্রতিষ্ঠান বা পেশাজীবী (Phase 5-এ তৈরি)।
3. **Service**: ক্যাটালগের প্রমিত সেবার ধরন (Phase 4-এ তৈরি)।
4. **Demand**: কোনো নির্দিষ্ট মুহূর্তে ব্যবহারকারীর একটি সুনির্দিষ্ট চাহিদার প্রকাশ।

> **বাউন্ডারি নোট**: Phase 6-এ কোনো স্বয়ংক্রিয় প্রোভাইডার ম্যাচিং বা অফার সিস্টেম নেই। ডিমান্ড কেবল একটি সুনির্দিষ্ট রিকোয়েস্ট সত্ত্বা।

### 2.2 Domain Relationship Diagram
```
User (Requester)
       │ 1
       │ has many
       ▼
   Demand ──────────┐
       │ 1          │ 1
       │ belongs to │ references
       ▼            ▼
 Master Service   Location Engine (SRID 4326)
       │            ├── Upazila (e.g., Cox's Bazar Sadar, Ramu)
       ▼            ├── Union / Ward
 Master Category    └── Point (Lat, Lng)
```

---

## 3. Demand Model Schema

| Field Name | Type | Constraints / Details |
|---|---|---|
| `id` | BigAutoField | Primary Key |
| `requester` | ForeignKey(User) | Related name `demands`, on_delete=CASCADE |
| `service` | ForeignKey(Service) | Nullable/Optional, related name `demands` |
| `category` | ForeignKey(Category) | Nullable/Optional, related name `demands` |
| `title_bn` | CharField(255) | বাংলা শিরোনাম (Min 5 chars) |
| `title_en` | CharField(255) | ইংরেজি রূপান্তর/শিরোনাম |
| `description_bn` | TextField | বিস্তারিত বাংলা বিবরণ (Min 10 chars) |
| `description_en` | TextField | ইংরেজি বিবরণ |
| `demand_type` | CharField(30) | `SERVICE`, `PRODUCT`, `RENTAL`, `BOOKING`, `MARKETPLACE`, `INFORMATION`, `OTHER` |
| `status` | CharField(20) | `DRAFT`, `PUBLISHED`, `PAUSED`, `FULFILLED`, `CANCELLED`, `EXPIRED`, `CLOSED` |
| `priority` | CharField(10) | `NORMAL`, `URGENT` |
| `quantity` | DecimalField | Optional, positive numeric value |
| `unit` | CharField(50) | Optional (e.g., ট্রাক, জন, ব্যাগ, দিন, টি) |
| `budget_min` | DecimalField | Optional BDT, non-negative, <= budget_max |
| `budget_max` | DecimalField | Optional BDT, non-negative |
| `currency` | CharField(3) | Default `'BDT'` |
| `required_at` | DateTimeField | Asia/Dhaka timezone aware |
| `expires_at` | DateTimeField | Asia/Dhaka timezone aware, must be > required_at |
| `upazila` | ForeignKey(Upazila) | Cox's Bazar 8 Upazilas (Phase 3) |
| `union_ward` | ForeignKey(UnionWard)| Optional granular administrative zone |
| `location_point` | PointField | SRID 4326 spatial coordinate (Optional) |
| `location_display_bn` | CharField(255) | ব্যবহারকারীর দেওয়া পরিচিত ঠিকানা |
| `visibility` | CharField(20) | `PUBLIC`, `REGISTERED_USERS`, `PRIVATE` |
| `contact_preference` | CharField(20) | `IN_APP_ONLY`, `PHONE`, `BOTH` |
| `is_active` | BooleanField | Default True (soft deletion / archive flag) |
| `published_at` | DateTimeField | Nullable, set upon publish transition |
| `created_at` | DateTimeField | Auto now add |
| `updated_at` | DateTimeField | Auto now |

---

## 4. Distinction: Demand Location vs. User GPS
Phase 3-এর ভূ-স্থানিক নিয়ম অনুসারে:
```
CURRENT USER GPS ≠ DEMAND LOCATION ≠ PROVIDER SERVICE AREA
```
ব্যবহারকারী বর্তমানে কক্সবাজার সদরে বসে থাকলেও তিনি রামু বা টেকনাফের জন্য কোনো চাহিদাপত্র প্রকাশ করতে পারেন। ডিমান্ডের ভৌগোলিক অবস্থান নির্ধারিত হয় তার নির্বাচিত `upazila` ও `location_display_bn` দ্বারা।
