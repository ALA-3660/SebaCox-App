# SebaCox — Phase 7: Matching Engine Foundation

## মূল স্লোগান
> **“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”**
> **“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”**

---

## ১. ওভারভিউ (Overview)
Phase 7-এ SebaCox-এর Matching Engine Foundation বাস্তবায়ন করা হয়েছে। এর লক্ষ্য হলো নাগরিক বা ব্যবহারকারীর প্রকাশিত প্রয়োজন (`Demand`) এবং নিবন্ধিত সক্রিয় সেবাদাতাদের (`Provider`) মধ্যে রিয়েল-টাইম, ব্যাখ্যাযোগ্য (explainable) এবং সম্পূর্ণ নির্ধারিত (deterministic) সংযোগ স্থাপন করা।

### মূল নীতিসমূহ (Core Principles)
1. **Matching ≠ Ranking**: ম্যাচিং নির্ধারণ করে সেবাদাতা সেবাটির জন্য উপযুক্ত কি না (Eligibility Filter); আর র‍্যাংকিং নির্ধারণ করে উপযুক্ত সেবাদাতাদের ক্রমানুসার (Order of Relevance)।
2. **Zero Fake Ranking Data**: কোনো কৃত্রিম রেটিং, রিভিও বা কাল্পনিক দূরত্ব ব্যবহার করা নিষিদ্ধ। ডাটাবেজে সংরক্ষিত প্রকৃত প্রশাসনিক স্তর ও কভারেজ তথ্যের ভিত্তিতে ম্যাচিং সম্পাদিত হয়।
3. **No Distance-Only Matching**: দূরত্ব কখনোই একমাত্র মাপকাঠি নয়। সেবা সামঞ্জস্য, সক্রিয়তা, কভারেজ এরিয়া, যাচাইকরণ এবং সময় সমন্বয় ইত্যাদির সমন্বয়ে স্কোর নির্ধারিত হয়।
4. **Separation of Responsibilities**:
   - `rules.py`: প্রতিটি শর্তের জন্য স্বাধীন ও স্বতন্ত্র রুল ক্লাস
   - `scoring.py`: ০ থেকে ১০০ স্কেলের নিশ্চিত গাণিতিক স্কোর গণনা
   - `ranking.py`: বহুস্তরীয় টাই-ব্রেকিং সহ সুশৃঙ্খল র‍্যাংকিং
   - `selectors.py`: N+1 কুয়েরি মুক্ত ডাটাবেজ রিটার্ন
   - `services.py`: পাইপলাইনের সামগ্রিক অর্কেস্ট্রেশন
   - `events.py` & `tasks.py`: ইভেন্ট-ভিত্তিক ও অ্যাসিঙ্ক্রোনাস প্রসেসিং

---

## ২. ডাটাবেজ মডেল ও আর্কিটেকচার (Database Schema)

### `MatchingRun` (ম্যাচিং এক্সিকিউশন ট্র্যাকিং)
| ফিল্ড | টাইপ | বর্ণনা |
|---|---|---|
| `demand` | ForeignKey (`Demand`) | যে প্রয়োজনের জন্য ম্যাচিং চালানো হয়েছে |
| `version` | CharField | ম্যাচিং অ্যালগরিদম সংস্করণ (যেমন: `v1`) |
| `trigger` | CharField | কি কারণে রান হয়েছে (`DEMAND_PUBLISHED`, `RE_MATCH`, `SCHEDULED`) |
| `status` | CharField | রানের অবস্থা (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`) |
| `candidate_count` | PositiveIntegerField | উপযুক্ত প্রাপ্ত প্রোভাইডারের সংখ্যা |
| `execution_duration_ms` | PositiveIntegerField | রান সম্পন্ন হতে মোট ব্যয়িত সময় (মিলিসেকেন্ডে) |
| `started_at` / `completed_at` | DateTimeField | শুরুর এবং সমাপ্তির টাইমস্ট্যাম্প |

### `MatchCandidate` (ম্যাচ ফলাফল ও ব্যাখ্যাযোগ্যতা)
| ফিল্ড | টাইপ | বর্ণনা |
|---|---|---|
| `demand` | ForeignKey (`Demand`) | সংশ্লিষ্ট চাহিদা |
| `provider` | ForeignKey (`Provider`) | উপযুক্ত সেবাদাতা |
| `matching_run` | ForeignKey (`MatchingRun`) | সংশ্লিষ্ট এক্সিকিউশন রান |
| `provider_service` | ForeignKey (`ProviderService`) | সুনির্দিষ্ট অফারিং |
| `match_status` | CharField | `ELIGIBLE`, `CONTACTED`, `INELIGIBLE`, `EXPIRED` |
| `match_score` | DecimalField (5, 2) | ০.০০ থেকে ১০০.০০ স্কোর |
| `rank` | PositiveIntegerField | ১-ভিত্তিক চূড়ান্ত র‍্যাংক |
| `distance_km` | DecimalField (6, 2) | জিপিএস ব্যাসার্ধ দূরত্ব (প্রযোজ্য ক্ষেত্রে) |
| `matched_factors` | JSONField | অর্জিত পয়েন্ট ও ফ্যাক্টরের স্ট্রাকচার্ড লগ |
| `unmatched_factors` | JSONField | অনর্জিত বা বাদ পড়া ফ্যাক্টরের লগ |
| `explanations_bn` | JSONField | ব্যবহারকারীর জন্য সহজ বাংলা ব্যাখ্যা তালিকা |

**আইডেমপোটেন্সি ও ইউনিক কনস্ট্রেইন্ট:**
- `UniqueConstraint(fields=['demand', 'provider', 'matching_version'], name='unique_demand_provider_version_match')`

---

## ৩. স্কোরিং ও ওয়েট পলিসি (Scoring Weights)

| ক্যাটাগরি | ফ্যাক্টর কোড | পয়েন্ট | শর্ত |
|---|---|---|---|
| **Service Match** | `SERVICE_EXACT` | ৪০.০ | হুবহু একই নির্দিষ্ট সেবা |
| | `SERVICE_CATEGORY_COMPATIBLE` | ২৫.০ | একই প্রধান ক্যাটাগরিভুক্ত সেবা |
| **Location Match** | `LOCATION_COVERED_EXACT` | ৩০.০ | নির্দিষ্ট ওয়ার্ড বা ইউনিয়ন কভারেজ |
| | `LOCATION_COVERED_RADIUS` | ২৫.০ | জিপিএস ব্যাসার্ধের মধ্যে অবস্থান |
| | `LOCATION_COVERED_UPAZILA` | ২০.০ | উপজেলা পর্যায়ে কভারেজ |
| | `LOCATION_COVERED_DISTRICT` | ১৫.০ | সমগ্র জেলা পর্যায়ে কভারেজ |
| **Availability** | `AVAILABILITY_AVAILABLE` | ১৫.০ | অনলাইনে ও সেবায় প্রস্তুত |
| | `AVAILABILITY_BUSY` | ৮.০ | বর্তমানে ব্যস্ত |
| | `AVAILABILITY_OFFLINE` | ৪.০ | অফলাইনে রয়েছে |
| **Verification** | `VERIFICATION_VERIFIED` | ১০.০ | প্ল্যাটফর্ম যাচাইকৃত সেবাদাতা |
| | `VERIFICATION_PENDING` | ৩.০ | যাচাইকরণ প্রক্রিয়াধীন |
| | `VERIFICATION_UNVERIFIED` | ৩.০ | সাধারণ সেবাদাতা |
| **Time Fit** | `TIME_COMPATIBLE` | ৫.০ | নির্ধারিত সময়ে সেবা প্রদানে সক্ষম |
| | `TIME_UNKNOWN` | ৫.০ | সময়সূচি উন্মুক্ত |

---

## ৪. র‍্যাংকিং হায়ারার্কি (Ranking Order)
1. **Match Score** (সর্বোচ্চ স্কোর সবার আগে)
2. **Verification Status** (যাচাইকৃত সেবাদাতারা অগ্রাধিকার পাবেন)
3. **Availability Status** (`AVAILABLE` > `BUSY` > `OFFLINE`)
4. **Distance (km)** (নিকটবর্তী সেবাদাতা অগ্রাধিকার পাবেন)
5. **Provider ID** (অপরিবর্তনীয় ও ধারাবাহিক টাই-ব্রেকার)

---

## ৫. এপিআই স্পেসিফিকেশন (API Endpoints)

### ক. উপযুক্ত সেবাদাতাদের তালিকা দর্শন
- **URL**: `GET /api/v1/demands/<demand_id>/matches/`
- **অনুমতি**: চাহিদাকারী (`Requester`), সংশ্লিষ্ট সেবাদাতা (`Provider`), বা প্ল্যাটফর্ম অ্যাডমিন
- **রেসপন্স স্যাম্পল**:
```json
{
  "success": true,
  "demand_id": 42,
  "total_candidates": 3,
  "matching_version": "v1",
  "message_bn": "৩ জন উপযুক্ত সম্ভাব্য সেবাদাতা পাওয়া গেছে।",
  "matches": [
    {
      "id": 101,
      "rank": 1,
      "match_score": "95.00",
      "provider": {
        "id": 12,
        "display_name_bn": "কক্স এসি কেয়ার",
        "is_verified": true,
        "availability_status": "AVAILABLE"
      },
      "explanations_bn": [
        "✓ হুবহু একই সেবা (এসি মেরামত)",
        "✓ আপনার উপজেলায় সেবা দেন (কক্সবাজার সদর)",
        "✓ বর্তমানে সেবায় প্রস্তুত ও সক্রিয়",
        "✓ প্ল্যাটফর্ম কর্তৃক যাচাইকৃত সেবাদাতা"
      ]
    }
  ]
}
```

### খ. ম্যাচ ক্যান্ডিডেট বিস্তারিত
- **URL**: `GET /api/v1/demands/<demand_id>/matches/<match_id>/`

### গ. ম্যানুয়াল রি-ম্যাচিং অনুরোধ
- **URL**: `POST /api/v1/demands/<demand_id>/rematch/`
- **অনুমতি**: শুধুমাত্র চাহিদাকারী বা অ্যাডমিন

### ঘ. অ্যাডমিন অডিট ও টেলিমিতি
- **URL**: `GET /api/v1/matching/runs/`
- **URL**: `GET /api/v1/matching/runs/<run_id>/`
