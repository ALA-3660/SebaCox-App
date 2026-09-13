# SebaCox Phase 3: Location & Geographic Architecture
**Motto:** *“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”*

---

## 1. Phase 3 Architecture Overview

SebaCox Phase 3 implements the foundational geographic and location data engine designed specifically for the administrative structure of Bangladesh and hyper-localized hyper-density operations in Cox's Bazar district.

```
+-------------------------------------------------------------------------+
|                          Flutter Mobile Client                          |
|  [LocationHeaderChip]  --->  [LocationSelectorModal / Screen]           |
|            |                                |                           |
|            v                                v                           |
|  [LocationBloc / State] <--------> [CurrentGps vs SelectedServiceArea]  |
|            |                                                            |
|  [LocationRepository] (Local Cache + Remote API)                        |
+-------------------------------------------------------------------------+
                                    |
                           HTTPS (REST / JSON)
                                    |
                                    v
+-------------------------------------------------------------------------+
|                        Django REST Framework                            |
|  /api/v1/locations/countries/                                           |
|  /api/v1/locations/divisions/                                           |
|  /api/v1/locations/districts/                                           |
|  /api/v1/locations/upazilas/                                            |
|  /api/v1/locations/municipalities/                                      |
|  /api/v1/locations/city-corporations/                                   |
|  /api/v1/locations/unions/                                              |
|  /api/v1/locations/wards/                                               |
|  /api/v1/locations/localities/                                          |
|  /api/v1/locations/search/?q=...                                        |
|  /api/v1/locations/nearby/?lat=...&lon=...                              |
|  /api/v1/locations/user/                                                |
|  /api/v1/locations/user/selected/                                       |
|  /api/v1/locations/user/current/                                        |
+-------------------------------------------------------------------------+
                                    |
       +----------------------------+----------------------------+
       |                                                         |
       v                                                         v
[PostgreSQL Database / PostGIS]                          [Redis Cache]
- Country, Division, District                             - Hierarchy Caching
- Upazila, Municipality, Union, Ward                     - Search Suggestion Index
- Point(SRID 4326), Polygon/MultiPolygon                 - Proximity Spatial Buckets
- UserLocation (SELECTED vs CURRENT contexts)
```

---

## 2. Core Architectural Principles

### 2.1 The Cardinal Principle: GPS ≠ Selected Service Area
A customer might currently be physically located in Dhaka, Chittagong, or at the beach, but wishes to book home appliance repair, food delivery, or rental services for their family residence in Chakaria or Maheshkhali.
- **`CURRENT`**: Device hardware GPS coordinates, ephemeral, updated on telemetry broadcast or user request.
- **`SELECTED`**: Explicitly chosen service location driving marketplace catalog filtering, provider availability, and localized pricing.
- **`SAVED`**: Named bookmarks (Home, Work, Parents) with explicit labels for instant switching.

### 2.2 Complete Administrative Hierarchy of Bangladesh
Standard normalized representation supporting Bangladesh's multi-tier governance:
1. **Country** (Bangladesh, ISO3: BGD, Dial: +880)
2. **Division** (8 Divisions: Chittagong, Dhaka, Rajshahi, Khulna, Barisal, Sylhet, Rangpur, Mymensingh)
3. **District (Zila)** (64 Districts, focused on Cox's Bazar and neighboring regions)
4. **Upazila (Sub-district)** (All 9 Upazilas of Cox's Bazar: Sadar, Chakaria, Eidgaon, Ramu, Maheshkhali, Kutubdia, Pekua, Ukhia, Teknaf)
5. **Municipality (Pourashava)** & **City Corporation** (Urban local government entities)
6. **Union Parishad** (Rural lowest administrative local government units)
7. **Ward** (Sub-division of Pourashavas and Unions)
8. **Locality / Mahalla / Village** (Informal micro-neighborhood landmarks like Kolatoli, Laboni, Sugandha, Burmese Market)

### 2.3 Spatial Coordinate Standards & Proximity
- **CRS / SRID**: EPSG:4326 (WGS 84 coordinate system using decimal degrees).
- **Bounding Box Validation**: Bangladesh national boundary (`20.57°N` to `26.63°N`, `88.01°E` to `92.68°E`).
- **Cox's Bazar Regional Bounding Box**: `20.6°N` to `21.9°N`, `91.8°E` to `92.4°E`.
- **Haversine Distance**: Great-circle distance calculation between user coordinates and service provider coordinates.

### 2.4 Bilingual First-Class Support
Every geographic node carries both:
- `name_bn`: Authentic Bengali Unicode name (e.g., 'কক্সবাজার সদর', 'চকোরিয়া').
- `name_en`: Standardized Latin transliteration (e.g., "Cox's Bazar Sadar", "Chakaria").

---

## 3. Data Schema & Models

### 3.1 Hierarchical Entities (`apps.locations.models`)
- **`Country`**: ISO codes, currency code, dial prefix.
- **`Division`**: Linked to Country.
- **`District`**: Linked to Division, center coordinates, bounding box.
- **`Upazila`**: Linked to District, center coordinates, bounding box.
- **`Municipality`**: Pourashava linked to District or Upazila.
- **`CityCorporation`**: Major urban administrative bodies.
- **`Union`**: Rural parishads linked to Upazila.
- **`Ward`**: Urban/rural wards linked to Municipality or Union.
- **`Locality`**: Granular neighborhood hotspots, markets, and tourist points with polygon or point anchors.

### 3.2 User Location Context (`UserLocation`)
```python
class LocationType(models.TextChoices):
    CURRENT = 'CURRENT', _('বর্তমান জিপিএস অবস্থান (Current GPS)')
    SELECTED = 'SELECTED', _('নির্বাচিত সেবা এলাকা (Selected Service Area)')
    SAVED = 'SAVED', _('সংরক্ষিত ঠিকানা (Saved Bookmark)')

class AddressLabel(models.TextChoices):
    HOME = 'HOME', _('বাসা (Home)')
    WORK = 'WORK', _('কর্মস্থল (Work)')
    OTHER = 'OTHER', _('অন্যান্য (Other)')
```

---

## 4. Flutter Client Implementation

- **`LocationBloc`**: Emits `LocationState` with `selectedServiceArea` and optional `currentGpsPosition`.
- **`LocationHeaderChip`**: Top app bar persistent indicator displaying selected Upazila / locality with modal trigger.
- **`LocationSelectorModal`**:
  - Tab 1: Administrative drilldown (Division → District → Upazila → Union/Ward).
  - Tab 2: Live bilingual instant search with debouncing.
  - Quick action: "Detect current GPS location" with explicit prompt to set as service area.
