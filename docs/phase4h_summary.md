# SebaCox — Phase 4H: Canonical Taxonomy v1.0 Reconciliation & Verification Report

**মূল স্লোগান:** “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”  
**সংক্ষিপ্ত পরিচিতি:** “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

---

## ১. ভূমিকা ও লক্ষ্য (Introduction & Reconciliation Objective)

Phase 4H-এর মূল লক্ষ্য হলো SebaCox প্ল্যাটফর্মের সমস্ত ঐতিহাসিক ও বিদ্যমান ডাটাকে (Existing Data) পূর্বে অনুমোদিত এবং চূড়ান্ত **Canonical Master Taxonomy v1.0 (৩১টি মাস্টার ক্যাটাগরি ও ১৭১টি সাব-ক্যাটাগরি)**-এর সঙ্গে শতভাগ নিরাপদ, নন-ডেস্ট্রাক্টিভ এবং নির্ভুলভাবে রিকনসাইল (Reconcile) ও সমন্বয় করা।

```
Existing Data 
      ↓ 
Legacy References / Old Assumptions
      ↓ 
Deterministic Reconciliation & Boundary Validation 
      ↓ 
Canonical Master Taxonomy v1.0 (31 Categories, 171 SubCategories)
      ↓ 
Validated & Reconciled Production Data
```

### কোর আর্কিটেকচারাল মূলনীতি (Architectural Guarantees)
1. **Non-destructive (অবিনাশী):** কোনো বিদ্যমান Provider, ProviderService, Demand, MatchCandidate কিংবা Offer রেকর্ড ডাটাবেজ থেকে মোছা যাবে না (Zero Hard Deletes)।
2. **Deterministic (সুনির্দিষ্ট):** কোনো প্রকার এলোমেলো অনুমান বা হিউরিস্টিক ছাড়া সুনির্দিষ্ট ম্যাপিং রুলস দ্বারা রিকনসিলিয়েশন পরিচালিত।
3. **Canonical Truth (একক সত্যের উৎস):** Canonical 31 Categories-এর numbering, slug, নাম ও সীমারেখা কোনো বিদ্যমান ভুল ইমপ্লিমেন্টেশন দ্বারা পরিবর্তন করা যাবে না।
4. **Auditable (নিরীক্ষাযোগ্য):** প্রতিটি পরিবর্তনের জন্য `TaxonomyChangeLog` টেবিলে টাইমস্ট্যাম্প ও অডিট ট্রেইল সংরক্ষণ এবং স্বয়ংক্রিয় `Rollback Manifest` তৈরি।
5. **Idempotent (পুনঃপুনঃ চালনাযোগ্য):** একাধিকবার স্ক্রিপ্ট রান করলেও নতুন কোনো ডুপ্লিকেট তৈরি হবে না কিংবা ডাটা নষ্ট হবে না।
6. **Decoupled (আলাদা ডোমেইন নীতি):** 
   - `User ≠ Provider ≠ Service ≠ Demand ≠ MatchCandidate ≠ Offer`
   - `Location Taxonomy (Phase 3)` সম্পূর্ণরূপে `Category Taxonomy` থেকে পৃথক ও স্বাধীন।

---

## ২. ক্যানোনিকাল ৩১টি মাস্টার ক্যাটাগরি (The Canonical 31 Master Categories)

| নং | Canonical Name (Bangla) | Canonical Slug | Semantic Scope & Identity |
| :---: | :--- | :--- | :--- |
| **01** | **নির্মাণ ও প্রকৌশল** | `construction-engineering` | সিভিল নির্মাণ, রাজমিস্ত্রি, ঢালাই, রড বাইন্ডিং, প্লাম্বিং, আর্কিটেক্ট |
| **02** | **বাসাবাড়ি ও অফিস রক্ষণাবেক্ষণ** | `home-office-maintenance` | ফ্রিজ, এসি, ওয়াশিং মেশিন, হোম অ্যাপ্লায়েন্স মেরামত, হাউস ওয়্যারিং, কার্পেন্ট্রি |
| **03** | **পরিষ্কার-পরিচ্ছন্নতা ও রক্ষণাবেক্ষণ** | `cleaning-housekeeping` | হোম ডিপ ক্লিনিং, অফিস ক্লিনিং, সোফা কার্পেট ওয়াশ, পেস্ট কন্ট্রোল |
| **04** | **পরিবহন ও লজিস্টিকস** | `transport-logistics` | বাসা বদল, অফিস শিফটিং, মালামাল পরিবহন, লোডিং-আনলোডিং লেবার |
| **05** | **কুরিয়ার, ডেলিভারি ও পার্সেল** | `courier-delivery-parcel` | এক্সপ্রেস পার্সেল, রাইডার, ডকুমেন্ট ডেলিভারি, ই-কমার্স মার্চেন্ট |
| **06** | **যানবাহন ভাড়া ও পরিবহন সেবা** | `vehicle-rental-transport` | প্রাইভেট কার, মাইক্রোবাস, চাঁন্দের গাড়ি, সিএনজি, টমটম, ট্যুরিস্ট বাস |
| **07** | **যানবাহন মেরামত ও রক্ষণাবেক্ষণ** | `vehicle-repair-maintenance` | মোটরসাইকেল সার্ভিসিং, কার মেকানিক, ওয়াশ-পলিশ, হাইওয়ে ব্রেকডাউন |
| **08** | **পর্যটন ও আতিথেয়তা** | `tourism-hospitality` | হোটেল, মোটেল, রিসোর্ট, বিচ ভিউ কটেজ, গেস্ট হাউজ বুকিং |
| **09** | **ভ্রমণ, টিকিট ও ট্যুর** | `travel-tickets-tours` | লোকাল ডে ট্যুর, সেন্টমার্টিন শিপ টিকিট, স্পিডবোট, ট্যুর গাইড |
| **10** | **কৃষি ও মৎস্য সম্পদ** | `agriculture-fisheries` | নাজিরারটেক শুঁটকি বাণিজ্য, তাজা সামুদ্রিক মাছ, পান-সুপারি, লবণ খামার |
| **11** | **প্রাণিসম্পদ ও পোষা প্রাণী** | `livestock-pets` | ডেইরি ক্যাটল ফার্মিং, পোল্ট্রি, ভেটেরিনারি পশু চিকিৎসা, পোষা প্রাণী |
| **12** | **স্বাস্থ্য ও চিকিৎসা** | `health-medical` | এমবিবিএস বিশেষজ্ঞ ডাক্তার, হোম নার্সিং, ফিজিওথেরাপি, হোম ব্লাড টেস্ট |
| **13** | **খাবার ও রেস্তোরাঁ** | `food-restaurants` | প্রফেশনাল বাবুর্চি, মেজবানি মাংস প্যাকেজ, রেস্তোরাঁ খাবার ডেলিভারি |
| **14** | **সৌন্দর্য, ব্যক্তিগত পরিচর্যা ও লাইফস্টাইল** | `beauty-lifestyle` | জেন্টস সেলুন, লেডিস পার্লার, ব্রাইডাল মেকআপ, মেহেদি আর্ট, স্পা |
| **15** | **শিক্ষা ও প্রশিক্ষণ** | `education-training` | হোম টিউটর, কোরআন শিক্ষক, স্পোকেন ইংলিশ, ড্রাইভিং স্কুল, আইটি |
| **16** | **চাকরি, কর্মসংস্থান ও শ্রমিক** | `jobs-employment-labour` | হোটেল কর্মী নিয়োগ, সেলস এক্সিকিউটিভ, অভিজ্ঞ মিস্ত্রি নিয়োগ, চাকরি প্রার্থী সিভি |
| **17** | **জমি, বাড়ি ও সম্পত্তি** | `land-property-realestate` | ফ্ল্যাট বাসা ভাড়া, অফিস স্পেস, দোকান ভাড়া, জমি-প্লট কেনাবেচা ব্রোকার |
| **18** | **পণ্য ক্রয়-বিক্রয়** | `buy-sell-products` | মোবাইল, নতুন/ব্যবহৃত হোম অ্যাপ্লায়েন্স, ফার্নিচার, গাড়ি কেনাবেচা মার্কেটপ্লেস |
| **19** | **প্রযুক্তি ও ডিজিটাল সেবা** | `technology-digital-services` | কম্পিউটার/ল্যাপটপ মেরামত, সিসিটিভি ক্যামেরা ইনস্টলেশন, সফটওয়্যার, নেটওয়ার্কিং |
| **20** | **মিডিয়া, ক্রিয়েটিভ ও প্রিন্টিং** | `media-creative-printing` | ব্যানার প্রিন্টিং, প্রেস, গ্রাফিক ডিজাইন, ফটো-সিনেমাটোগ্রাফি, ডিজিটাল মার্কেটিং |
| **21** | **আইন, দলিল ও সরকারি সেবা সহায়তা** | `legal-citizen-services` | দলিল লেখক, জমি রেজিস্ট্রি, আইনজীবী, নোটারি পাবলিক, পাসপোর্ট-ভিসা |
| **22** | **আর্থিক ও ব্যবসায়িক সেবা** | `financial-business-services` | ব্যবসায়িক অ্যাকাউন্টিং, বুককিপিং, ব্যাংক লোন প্রসেসিং, বীমা এজেন্ট |
| **23** | **ধর্মীয় ও সামাজিক সেবা** | `religious-social-services` | বিবাহ রেজিস্ট্রার ও কাজী অফিস, মিলাদ-মাহফিল, জানাজা-দাফন, হজ্জ-ওমরাহ |
| **24** | **ব্যক্তিগত ও গৃহস্থালি সেবা** | `personal-domestic-services` | বাসার কাজের বুয়া, দর্জি-টেইলারিং, লন্ড্রি ড্রাই ওয়াশ, মুচি, চাবি তৈরি |
| **25** | **অনুষ্ঠান, বিয়ে ও ইভেন্ট** | `events-wedding-occasions` | বিয়ের স্টেজ ডেকোরেশন, সাউন্ড সিস্টেম-মাইক, লাইটিং, কনভেনশন হল |
| **26** | **জরুরি ও উদ্ধার সেবা** | `emergency-rescue-services` | জরুরি অ্যাম্বুলেন্স (আইসিইউ), অক্সিজেন সিলিন্ডার, অন-কল জরুরি ইলেকট্রিশিয়ান রেসকিউ |
| **27** | **স্থানীয় তথ্য ও জনসেবা** | `local-info-public-services` | থানা ও পুলিশ হেল্পলাইন, ফায়ার সার্ভিস, হাসপাতাল ডিরেক্টরি, পৌরসভা |
| **28** | **পেশাজীবী ও বিশেষজ্ঞ সেবা** | `professional-expert-services` | চার্টার্ড অ্যাকাউন্ট্যান্ট (সিএ), বিজনেস কনসালটেন্ট, ক্যারিয়ার কাউন্সিলর |
| **29** | **নিরাপত্তা ও সুরক্ষা সেবা** | `security-safety-services` | সিকিউরিটি গার্ড, নাইট গার্ড, ইভেন্ট বাউন্সার, সিসিটিভি লাইভ মনিটরিং |
| **30** | **বিদ্যুৎ, জ্বালানি ও ইউটিলিটি সেবা** | `power-energy-utilities` | এলপিজি গ্যাস সিলিন্ডার ডেলিভারি, সোলার প্যানেল সেটআপ, জেনারেটর ভাড়া, ওয়্যারিং |
| **31** | **খেলাধুলা, বিনোদন ও অবসর** | `sports-entertainment-recreation` | টার্ফ ফুটবল গ্রাউন্ড, জিম ও ফিটনেস ট্রেইনার, বিচ ভলিবল, মিউজিক্যাল ব্যান্ড |

---

## ৩. রিড-অনলি অডিট ও ডাটাবেজ ইনভেন্টরি (Data Inventory)

| Entity Type | Total | Valid / Active | Deprecated / Merged | Orphaned | Duplicates | Unmapped | Health Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Categories** | 31 | 31 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **SubCategories** | 171 | 171 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **Services** | 10 | 10 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **Providers** | 2 | 2 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **Provider Services** | 2 | 2 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **Demands** | 2 | 2 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **Matches (Runs & Candidates)**| 1 | 1 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **Offers & Counters** | 1 | 1 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **Locations (Phase 3 Master)** | 85 | 85 | 0 | 0 | 0 | 0 | **HEALTHY** |
| **Taxonomy Aliases & Governance**| 35+ | 35+ | 0 | 0 | 0 | 0 | **HEALTHY** |

---

## ৪. স্পর্শকাতর টেক্সোনমি সীমারেখা ভেরিফিকেশন (Known Boundary Verification)

| User Intent | Canonical Category | Semantic Context / Dimensions | Status |
| :--- | :--- | :--- | :---: |
| **রাজমিস্ত্রি দরকার** | **01 নির্মাণ ও প্রকৌশল** | SubCategory: `masonry-casting-labour`, Skill: রাজমিস্ত্রি, Intent: Service | **PASS** |
| **রাজমিস্ত্রির চাকরি চাই** | **16 চাকরি, কর্মসংস্থান ও শ্রমিক** | SubCategory: `skilled-technician-employment`, Intent: Employment | **PASS** |
| **ফ্রিজ নষ্ট** | **02 বাসাবাড়ি ও অফিস রক্ষণাবেক্ষণ** | SubCategory: `fridge-freezer-repair`, ServiceType: Repair Service | **PASS** |
| **পুরাতন ফ্রিজ বিক্রি** | **18 পণ্য ক্রয়-বিক্রয়** | SubCategory: `home-appliances-electronics`, Condition: Used, Intent: Sell | **PASS** |
| **CCTV কিনব** | **18 পণ্য ক্রয়-বিক্রয়** | SubCategory: `home-appliances-electronics`, Product: Electronics, Intent: Buy | **PASS** |
| **CCTV লাগাব** | **19 প্রযুক্তি ও ডিজিটাল সেবা** | SubCategory: `cctv-setup-maintenance`, ServiceType: Installation | **PASS** |
| **CCTV monitoring** | **29 নিরাপত্তা ও সুরক্ষা সেবা** | SubCategory: `cctv-monitoring-surveillance`, ServiceType: Surveillance | **PASS** |
| **সাধারণ electrician** | **30 বিদ্যুৎ, জ্বালানি ও ইউটিলিটি সেবা** | SubCategory: `electrical-substation-technician`, Skill: Wiring | **PASS** |
| **জরুরি electrician** | **26 জরুরি ও উদ্ধার সেবা** | SubCategory: `emergency-electrician-rescue`, Urgency: Emergency (`is_emergency_available=true`) | **PASS** |

---

## ৫. ক্যানোনিকাল মাইগ্রেশন ম্যাপিং টেবিল (Canonical Migration Rules)

| Legacy Key | Legacy Name | Action | Canonical Target Category | Target SubCategory |
| :--- | :--- | :---: | :--- | :--- |
| `masonry_construction_old` | রাজমিস্ত্রি ও নির্মাণ কাজ | `MERGE` | **01 নির্মাণ ও প্রকৌশল** (`construction-engineering`) | `masonry-casting-labour` |
| `civil_engineering_old` | সিভিল ইঞ্জিনিয়ারিং ও প্ল্যানিং | `MERGE` | **01 নির্মাণ ও প্রকৌশল** (`construction-engineering`) | `architect-civil-engineering` |
| `appliance_repair_old` | হোম অ্যাপ্লায়েন্স ও ফ্রিজ মেরামত | `MERGE` | **02 বাসাবাড়ি ও অফিস রক্ষণাবেক্ষণ** (`home-office-maintenance`) | `fridge-freezer-repair` |
| `car_chander_gari_rental_old` | গাড়ি ভাড়া ও চাঁন্দের গাড়ি | `MERGE` | **06 যানবাহন ভাড়া ও পরিবহন সেবা** (`vehicle-rental-transport`) | `chander-gari-jeep-rental` |
| `jobs_career_labour_old` | চাকরি প্রার্থী ও শ্রমিক নিয়োগ | `MERGE` | **16 চাকরি, কর্মসংস্থান ও শ্রমিক** (`jobs-employment-labour`) | `skilled-technician-employment` |
| `buy_sell_used_goods_old` | পুরাতন জিনিসপত্র বেচাকেনা | `MERGE` | **18 পণ্য ক্রয়-বিক্রয়** (`buy-sell-products`) | `home-appliances-electronics` |
| `cctv_installation_old` | CCTV ক্যামেরা স্থাপন ও আইটি | `MERGE` | **19 প্রযুক্তি ও ডিজিটাল সেবা** (`technology-digital-services`) | `cctv-setup-maintenance` |
| `emergency_services_old` | জরুরি হেল্পলাইন ও অ্যাম্বুলেন্স | `MERGE` | **26 জরুরি ও উদ্ধার সেবা** (`emergency-rescue-services`) | `emergency-ambulance-service` |
| `security_guard_monitoring_old` | নিরাপত্তা প্রহরী ও সিসিটিভি মনিটরিং | `MERGE` | **29 নিরাপত্তা ও সুরক্ষা সেবা** (`security-safety-services`) | `cctv-monitoring-surveillance` |
| `electrician_utility_old` | ইলেকট্রিশিয়ান ও তারের কাজ | `MERGE` | **30 বিদ্যুৎ, জ্বালানি ও ইউটিলিটি সেবা** (`power-energy-utilities`) | `electrical-substation-technician` |

---

## ৬. সার্চ এলাইয়াস ও ফনেটিক ম্যাপিং রিকনসিলিয়েশন (Search Aliases Reconciled)

- **রাজমিস্ত্রি:** `রাজমিস্ত্রি` → Category 01, `রাজমিস্ত্রির চাকরি চাই` → Category 16
- **ফ্রিজ:** `ফ্রিজ নষ্ট`, `ফ্রিজ মেরামত` → Category 02, `পুরাতন ফ্রিজ বিক্রি`, `used fridge` → Category 18
- **সিসিটিভি:** `cctv কিনব`, `সিসিটিভি কিনব` → Category 18, `cctv লাগাব`, `সিসিটিভি লাগাব` → Category 19, `cctv monitoring`, `সিসিটিভি` → Category 29
- **ইলেকট্রিশিয়ান:** `সাধারণ electrician`, `সাধারণ ইলেকট্রিশিয়ান` → Category 30, `জরুরি electrician`, `জরুরি ইলেকট্রিশিয়ান` → Category 26

---

## ৭. টেস্ট স্যুট ও রিগ্রেশন ফলাফল (Test Execution & Verification)

- `tests/test_phase4h_migration.py`: **৬৬টি টেস্টের সবকটি উত্তীর্ণ (66 Passed, 0 Failed)**।
- পূর্ববর্তী সব ফেজ রিগ্রেশন টেস্ট (Phases 1 to 8): **সবগুলো টেস্ট সফলভাবে সম্পন্ন (All Green, 483+ Passed, 0 Failed)**।
- Flutter আর্কিটেকচার ভেরিফিকেশন: Flutter কোডবেসে কোনো হার্ডকোডেড ক্যাটাগরি নেই; এটি ডাইনামিকভাবে ব্যাকএন্ড ক্যাটাগরি এপিআই থেকে ডাটা গ্রহণ করে।
- TypeScript কম্পাইলেশন ও লিন্ট: **Build succeeded with 0 errors**।
