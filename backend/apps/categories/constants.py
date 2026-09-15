"""
Constants and enumerations for Category & Service Engine.
Master Taxonomy Version 1.0 (31 Master Categories & Granular Sub-categories)
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
from django.db import models


class CategoryKind(models.TextChoices):
    """
    Architectural segregation:
    - PUBLIC_SERVICE_CATEGORY: Consumer-facing marketplace & service directories.
    - SYSTEM_DOMAIN: Internal platform/system governance & operational domains.
    """
    PUBLIC_SERVICE_CATEGORY = 'PUBLIC_SERVICE_CATEGORY', 'পাবলিক সেবা ক্যাটাগরি (Public Service Category)'
    SYSTEM_DOMAIN = 'SYSTEM_DOMAIN', 'সিস্টেম ডোমেন (System Domain)'


class ServiceType(models.TextChoices):
    """
    Controlled service-type strategy enabling future specialized extensions.
    """
    SERVICE = 'SERVICE', 'সাধারণ সেবা (Service)'
    PRODUCT = 'PRODUCT', 'পণ্য / সামগ্রী (Product)'
    RENTAL = 'RENTAL', 'ভাড়া সেবা (Rental)'
    BOOKING = 'BOOKING', 'বুকিং / অ্যাপয়েন্টমেন্ট (Booking)'
    DIGITAL_SERVICE = 'DIGITAL_SERVICE', 'ডিজিটাল সেবা (Digital Service)'
    INFORMATION = 'INFORMATION', 'তথ্যমূলক সেবা (Information)'
    MARKETPLACE = 'MARKETPLACE', 'মার্কেটপ্লেস লেনদেন (Marketplace)'


class AliasTargetType(models.TextChoices):
    """Target entity type for search synonyms and phonetic aliases."""
    CATEGORY = 'CATEGORY', 'Category'
    SUBCATEGORY = 'SUBCATEGORY', 'SubCategory'
    SERVICE = 'SERVICE', 'Service'
    SKILL = 'SKILL', 'Skill'


class AliasLanguage(models.TextChoices):
    """Language classification for aliases."""
    BN = 'BN', 'Bangla'
    EN = 'EN', 'English'
    ALL = 'ALL', 'All/Bilingual'


# =============================================================================
# SEBACOX MASTER TAXONOMY VERSION 1.0: 31 MASTER CATEGORIES & APPROVED SUBCATEGORIES
# =============================================================================
SEBACOX_31_MASTER_CATEGORIES = [
    # 01. নির্মাণ ও প্রকৌশল
    {
        'id': 1,
        'order': 1,
        'name_bn': 'নির্মাণ ও প্রকৌশল',
        'name_en': 'Construction & Engineering',
        'slug': 'construction-engineering',
        'icon': 'hammer',
        'description_bn': 'ইট, বালু, সিমেন্ট সরবরাহ, নির্মাণ শ্রমিক ও মিস্ত্রি (রাজমিস্ত্রি, ঢালাই), রং, প্লাম্বিং ও আর্কিটেকচারাল প্ল্যানিং',
        'description_en': 'Civil construction, masonry, engineering design, plumbing, painting and building materials',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 101, 'name_bn': 'নির্মাণ সামগ্রী সরবরাহ (ইট, বালু, রড, সিমেন্ট)', 'name_en': 'Construction Materials Supply', 'slug': 'construction-materials-supply', 'order': 1},
            {'id': 102, 'name_bn': 'নির্মাণ শ্রমিক ও মিস্ত্রি (রাজমিস্ত্রি ও ঢালাই)', 'name_en': 'Masonry, Rod Binding & Casting Labour', 'slug': 'masonry-casting-labour', 'order': 2},
            {'id': 103, 'name_bn': 'টাইলস, মার্বেল ও গ্রানাইট ফিটিং', 'name_en': 'Tiles, Marble & Granite Fitting', 'slug': 'tiles-marble-fitting', 'order': 3},
            {'id': 104, 'name_bn': 'রং মিস্ত্রি ও ওয়াল পুটি', 'name_en': 'Painting & Wall Putty', 'slug': 'painting-wall-putty', 'order': 4},
            {'id': 105, 'name_bn': 'প্লাম্বিং ও পাইপলাইন ফিটিং', 'name_en': 'Plumbing & Pipeline Fitting', 'slug': 'plumbing-pipeline-fitting', 'order': 5},
            {'id': 106, 'name_bn': 'আর্কিটেক্ট, সিভিল ইঞ্জিনিয়ার ও বিল্ডিং প্ল্যান', 'name_en': 'Architectural & Civil Engineering Design', 'slug': 'architect-civil-engineering', 'order': 6},
            {'id': 107, 'name_bn': 'মাটি কাটা, পাইলিং ও ভরাট কাজ', 'name_en': 'Piling, Soil Excavation & Earthwork', 'slug': 'piling-earthwork', 'order': 7},
            {'id': 108, 'name_bn': 'গ্রিল, থাই অ্যালুমিনিয়াম ও গ্লাস ওয়ার্ক', 'name_en': 'Grill, Thai Aluminum & Glass Work', 'slug': 'grill-thai-aluminum-glass', 'order': 8},
            {'id': 109, 'name_bn': 'ইন্টেরিয়র ডিজাইন ও ডেকোরেশন', 'name_en': 'Interior Design & Decoration', 'slug': 'interior-design-decoration', 'order': 9},
            {'id': 110, 'name_bn': 'ভারী নির্মাণ যন্ত্রপাতি ভাড়া (মিক্সার, ক্রেন)', 'name_en': 'Heavy Construction Machinery Rental', 'slug': 'construction-machinery-rental', 'order': 10},
        ]
    },

    # 02. বাসাবাড়ি ও অফিস রক্ষণাবেক্ষণ
    {
        'id': 2,
        'order': 2,
        'name_bn': 'বাসাবাড়ি ও অফিস রক্ষণাবেক্ষণ',
        'name_en': 'Home & Office Maintenance',
        'slug': 'home-office-maintenance',
        'icon': 'wrench',
        'description_bn': 'ইলেকট্রিশিয়ান, এসি, ফ্রিজ, ওয়াশিং মেশিন, গ্যাস স্টোভ, পানির পাম্প ও হোম অ্যাপ্লায়েন্স মেরামত',
        'description_en': 'Electrician, AC, refrigerator, washing machine, stove and home appliance repairs',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 201, 'name_bn': 'ইলেকট্রিশিয়ান ও হাউস ওয়্যারিং', 'name_en': 'Electrician & House Wiring', 'slug': 'electrician-house-wiring', 'order': 1},
            {'id': 202, 'name_bn': 'এসি সার্ভিসিং, গ্যাস চার্জ ও মেরামত', 'name_en': 'AC Servicing & Gas Charge', 'slug': 'ac-servicing-gas-charge', 'order': 2},
            {'id': 203, 'name_bn': 'ফ্রিজ ও রেফ্রিজারেটর মেরামত', 'name_en': 'Refrigerator & Deep Freezer Repair', 'slug': 'fridge-freezer-repair', 'order': 3},
            {'id': 204, 'name_bn': 'ওয়াশিং মেশিন ও ড্রায়ার সার্ভিসিং', 'name_en': 'Washing Machine Repair', 'slug': 'washing-machine-repair', 'order': 4},
            {'id': 205, 'name_bn': 'পানির পাম্প ও মোটর সার্ভিস', 'name_en': 'Water Pump & Motor Repair', 'slug': 'water-pump-motor-repair', 'order': 5},
            {'id': 206, 'name_bn': 'গ্যাস স্টোভ, ওভেন ও গিজার মেরামত', 'name_en': 'Gas Stove, Oven & Geyser Repair', 'slug': 'gas-stove-oven-geyser', 'order': 6},
            {'id': 207, 'name_bn': 'আইপিএস, ইউপিএস ও সোলার মেরামত', 'name_en': 'IPS, UPS & Solar Battery Repair', 'slug': 'ips-ups-solar-repair', 'order': 7},
            {'id': 208, 'name_bn': 'টিভি ও হোম অডিও সিস্টেম সার্ভিসিং', 'name_en': 'TV & Audio System Repair', 'slug': 'tv-audio-repair', 'order': 8},
            {'id': 209, 'name_bn': 'কাঠমিস্ত্রি ও ফার্নিচার মেরামত/বার্নিশ', 'name_en': 'Carpentry, Furniture Repair & Polish', 'slug': 'carpentry-furniture-repair', 'order': 9},
        ]
    },

    # 03. পরিষ্কার-পরিচ্ছন্নতা ও রক্ষণাবেক্ষণ
    {
        'id': 3,
        'order': 3,
        'name_bn': 'পরিষ্কার-পরিচ্ছন্নতা ও রক্ষণাবেক্ষণ',
        'name_en': 'Cleaning & Housekeeping',
        'slug': 'cleaning-housekeeping',
        'icon': 'sparkles',
        'description_bn': 'বাসা-অফিস ডিপ ক্লিনিং, সোফা কার্পেট ওয়াশ, পানির ট্যাংক পরিষ্কার ও পেস্ট কন্ট্রোল',
        'description_en': 'Deep cleaning, carpet wash, water tank sanitation and pest control',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 301, 'name_bn': 'বাসা-বাড়ি ও ফ্ল্যাট ডিপ ক্লিনিং', 'name_en': 'Home Deep Cleaning', 'slug': 'home-deep-cleaning', 'order': 1},
            {'id': 302, 'name_bn': 'অফিস, শোরুম ও রেস্তোরাঁ ক্লিনিং', 'name_en': 'Commercial & Office Cleaning', 'slug': 'commercial-office-cleaning', 'order': 2},
            {'id': 303, 'name_bn': 'সোফা, জাজিম ও কার্পেট ওয়াশ', 'name_en': 'Sofa, Mattress & Carpet Wash', 'slug': 'sofa-carpet-wash', 'order': 3},
            {'id': 304, 'name_bn': 'পানির ট্যাংক ও আন্ডারগ্রাউন্ড রিজার্ভার ওয়াশ', 'name_en': 'Water Tank & Reservoir Wash', 'slug': 'water-tank-reservoir-wash', 'order': 4},
            {'id': 305, 'name_bn': 'পোকামাকড় ও পেস্ট কন্ট্রোল সার্ভিস', 'name_en': 'Pest Control & Termite Treatment', 'slug': 'pest-control-treatment', 'order': 5},
            {'id': 306, 'name_bn': 'সেপটিক ট্যাংক ও ড্রেনেজ ক্লিনিং', 'name_en': 'Septic Tank & Drainage Cleaning', 'slug': 'septic-tank-drainage-cleaning', 'order': 6},
            {'id': 307, 'name_bn': 'গ্লাস ও হাই-রাইজ বিল্ডিং এক্সটেরিয়র ক্লিনিং', 'name_en': 'Exterior Glass & Facade Cleaning', 'slug': 'facade-glass-cleaning', 'order': 7},
        ]
    },

    # 04. পরিবহন ও লজিস্টিকস
    {
        'id': 4,
        'order': 4,
        'name_bn': 'পরিবহন ও লজিস্টিকস',
        'name_en': 'Transport & Logistics',
        'slug': 'transport-logistics',
        'icon': 'truck',
        'description_bn': 'বাসা শিফটিং, অফিস শিফটিং, ভারী মালামাল পরিবহন ও লোডিং লেবার',
        'description_en': 'House shifting, cargo transport, heavy logistics and loading labours',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 401, 'name_bn': 'বাসা-বাড়ি বদল ও অফিস শিফটিং', 'name_en': 'House & Office Shifting', 'slug': 'house-office-shifting', 'order': 1},
            {'id': 402, 'name_bn': 'পিকআপ ও মিনি ট্রাক ভাড়া (মালামাল)', 'name_en': 'Pickup & Mini Truck Rental (Cargo)', 'slug': 'pickup-mini-truck-cargo', 'order': 2},
            {'id': 403, 'name_bn': 'বড় ট্রাক, কভার্ড ভ্যান ও ট্রেইলার ভাড়া', 'name_en': 'Heavy Truck & Covered Van Rental', 'slug': 'heavy-truck-covered-van', 'order': 3},
            {'id': 404, 'name_bn': 'মালামাল লোডিং ও আনলোডিং শ্রমিক (লেবার)', 'name_en': 'Loading & Unloading Labour', 'slug': 'loading-unloading-labour', 'order': 4},
            {'id': 405, 'name_bn': 'হিমাগার পরিবহন ও কোল্ড চেইন লজিস্টিকস', 'name_en': 'Cold Storage & Refrigerated Transport', 'slug': 'cold-chain-transport', 'order': 5},
        ]
    },

    # 05. কুরিয়ার, ডেলিভারি ও পার্সেল
    {
        'id': 5,
        'order': 5,
        'name_bn': 'কুরিয়ার, ডেলিভারি ও পার্সেল',
        'name_en': 'Courier, Delivery & Parcel',
        'slug': 'courier-delivery-parcel',
        'icon': 'send',
        'description_bn': 'শহরভিত্তিক ইনস্ট্যান্ট পার্সেল, কুরিয়ার বুকিং, ডকুমেন্ট ডেলিভারি ও ই-কমার্স লজিস্টিকস',
        'description_en': 'Intra-city parcel, courier booking, document delivery and rider services',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 501, 'name_bn': 'কক্সবাজার শহরভিত্তিক ইনস্ট্যান্ট পার্সেল/রাইডার', 'name_en': 'City Express Parcel & Rider', 'slug': 'city-express-parcel-rider', 'order': 1},
            {'id': 502, 'name_bn': 'জেলা ও দেশব্যাপী কুরিয়ার পার্সেল বুকিং', 'name_en': 'Nationwide Courier Booking Support', 'slug': 'nationwide-courier-booking', 'order': 2},
            {'id': 503, 'name_bn': 'জরুরি ডকুমেন্ট ও পাসপোর্ট ডেলিভারি', 'name_en': 'Urgent Document Delivery', 'slug': 'urgent-document-delivery', 'order': 3},
            {'id': 504, 'name_bn': 'ই-কমার্স মার্চেন্ট ডেলিভারি ও সিওডি হাব', 'name_en': 'E-Commerce Merchant Delivery & COD', 'slug': 'ecommerce-merchant-delivery', 'order': 4},
        ]
    },

    # 06. যানবাহন ভাড়া ও পরিবহন সেবা
    {
        'id': 6,
        'order': 6,
        'name_bn': 'যানবাহন ভাড়া ও পরিবহন সেবা',
        'name_en': 'Vehicle Rental & Transport',
        'slug': 'vehicle-rental-transport',
        'icon': 'car',
        'description_bn': 'প্রাইভেট কার, মাইক্রোবাস, চাঁন্দের গাড়ি, সিএনজি, টমটম ও হাইস রেন্টাল',
        'description_en': 'Private car, microbus, chander gari, CNG, tomtom and tourist vehicle rental',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 601, 'name_bn': 'প্রাইভেট কার ও সেডান রেন্টাল', 'name_en': 'Private Car & Sedan Rental', 'slug': 'private-car-sedan-rental', 'order': 1},
            {'id': 602, 'name_bn': 'মাইক্রোবাস ও হাইস রিজার্ভ (ট্যুর/ফ্যামিলি)', 'name_en': 'Microbus & Hiace Reserve', 'slug': 'microbus-hiace-reserve', 'order': 2},
            {'id': 603, 'name_bn': 'চাঁন্দের গাড়ি ও বীচ জিপ রেন্টাল', 'name_en': 'Chander Gari & 4x4 Jeep Rental', 'slug': 'chander-gari-jeep-rental', 'order': 3},
            {'id': 604, 'name_bn': 'সিএনজি ও অটো-রিকশা রিজার্ভ', 'name_en': 'CNG & Auto-rickshaw Reserve', 'slug': 'cng-autorickshaw-reserve', 'order': 4},
            {'id': 605, 'name_bn': 'টমটম (ইজিবাইক) রিজার্ভ ও লোকাল ট্রিপ', 'name_en': 'TomTom (Easybike) Reserve', 'slug': 'tomtom-easybike-reserve', 'order': 5},
            {'id': 606, 'name_bn': 'ট্যুরিস্ট বাস ও মিনিবাস চার্টার', 'name_en': 'Tourist Bus & Minibus Charter', 'slug': 'tourist-bus-charter', 'order': 6},
            {'id': 607, 'name_bn': 'মোটরসাইকেল ও স্কুটার দৈনিক ভাড়া', 'name_en': 'Motorbike & Scooter Daily Rental', 'slug': 'motorbike-scooter-rental', 'order': 7},
        ]
    },

    # 07. যানবাহন মেরামত ও রক্ষণাবেক্ষণ
    {
        'id': 7,
        'order': 7,
        'name_bn': 'যানবাহন মেরামত ও রক্ষণাবেক্ষণ',
        'name_en': 'Vehicle Repair & Maintenance',
        'slug': 'vehicle-repair-maintenance',
        'icon': 'settings',
        'description_bn': 'অটোমোবাইল মেকানিক, কার ওয়াশ, বাইক সার্ভিসিং, টায়ার পাংচার ও ব্রেকডাউন রিকভারি',
        'description_en': 'Automobile mechanic, car wash, bike servicing and highway breakdown assistance',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 701, 'name_bn': 'মোটরসাইকেল ও স্কুটার সার্ভিসিং', 'name_en': 'Motorcycle & Scooter Servicing', 'slug': 'motorcycle-servicing', 'order': 1},
            {'id': 702, 'name_bn': 'কার মেকানিক ও ইঞ্জিন টিউনিং', 'name_en': 'Car Mechanic & Engine Tuning', 'slug': 'car-mechanic-tuning', 'order': 2},
            {'id': 703, 'name_bn': 'গাড়ি ওয়াশ, ফোম ক্লিন ও পলিশ', 'name_en': 'Car Detailing & Foam Wash', 'slug': 'car-wash-polishing', 'order': 3},
            {'id': 704, 'name_bn': 'টায়ার পাংচার, হুইল এলাইনমেন্ট ও ব্যাটারি', 'name_en': 'Tire Puncture & Battery Service', 'slug': 'tire-puncture-battery', 'order': 4},
            {'id': 705, 'name_bn': 'সিএনজি ও টমটম মেকানিক/ব্যাটারি চার্জিং', 'name_en': 'CNG & TomTom Electric Mechanic', 'slug': 'cng-tomtom-mechanic', 'order': 5},
            {'id': 706, 'name_bn': 'হাইওয়ে অন-কল ব্রেকডাউন ও রেসকিউ মেকানিক', 'name_en': 'Highway Breakdown On-Call Mechanic', 'slug': 'highway-breakdown-mechanic', 'order': 6},
        ]
    },

    # 08. পর্যটন ও আতিথেয়তা
    {
        'id': 8,
        'order': 8,
        'name_bn': 'পর্যটন ও আতিথেয়তা',
        'name_en': 'Tourism & Hospitality',
        'slug': 'tourism-hospitality',
        'icon': 'compass',
        'description_bn': 'হোটেল, মোটেল, রিসোর্ট, বীচ কটেজ, হোমস্টে ও অবকাশ যাপন',
        'description_en': 'Hotels, resorts, beach cottages, homestays and hospitality accommodations',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 801, 'name_bn': 'হোটেল, মোটেল ও তারকা রিসোর্ট বুকিং', 'name_en': 'Hotel, Motel & Luxury Resort Booking', 'slug': 'hotel-motel-resort-booking', 'order': 1},
            {'id': 802, 'name_bn': 'বীচ ভিউ কটেজ ও ইকো রিসোর্ট', 'name_en': 'Beach View Cottage & Eco Resort', 'slug': 'beach-cottage-eco-resort', 'order': 2},
            {'id': 803, 'name_bn': 'বাজেট হোমস্টে ও গেস্ট হাউজ', 'name_en': 'Budget Homestay & Guest House', 'slug': 'homestay-guest-house', 'order': 3},
            {'id': 804, 'name_bn': 'হোটেল কনফারেন্স রুম ও ব্যাংকুয়েট হল', 'name_en': 'Conference Room & Banquet Hall', 'slug': 'hotel-banquet-conference', 'order': 4},
        ]
    },

    # 09. ভ্রমণ, টিকিট ও ট্যুর
    {
        'id': 9,
        'order': 9,
        'name_bn': 'ভ্রমণ, টিকিট ও ট্যুর',
        'name_en': 'Travel, Tickets & Tours',
        'slug': 'travel-tickets-tours',
        'icon': 'ticket',
        'description_bn': 'ট্যুর প্যাকেজ, সেন্টমার্টিন শিপ টিকিট, স্পিডবোট, ওয়াটার স্পোর্টস ও ট্যুর গাইড',
        'description_en': 'Tour packages, Saint Martin ship tickets, water sports and certified tour guides',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 901, 'name_bn': 'লোকাল সাইটসিয়িং ও কক্সবাজার ডে ট্যুর', 'name_en': 'Local Sightseeing & Day Tour Package', 'slug': 'local-sightseeing-day-tour', 'order': 1},
            {'id': 902, 'name_bn': 'সেন্টমার্টিন ক্রুজ ও শিপ টিকিট বুকিং', 'name_en': 'Saint Martin Cruise & Ship Booking', 'slug': 'saint-martin-ship-booking', 'order': 2},
            {'id': 903, 'name_bn': 'স্পিডবোট, সী-প্লেন ও প্যারাসেলিং স্পোর্টস', 'name_en': 'Speedboat & Parasailing Water Sports', 'slug': 'parasailing-water-sports', 'order': 3},
            {'id': 904, 'name_bn': 'প্রশিক্ষিত লোকাল ট্যুর গাইড সেবা', 'name_en': 'Certified Local Tour Guide', 'slug': 'certified-tour-guide', 'order': 4},
            {'id': 905, 'name_bn': 'বাস, ট্রেন ও বিমান টিকিট সহায়তা', 'name_en': 'Bus, Train & Air Ticket Assistance', 'slug': 'bus-train-air-ticket', 'order': 5},
        ]
    },

    # 10. কৃষি ও মৎস্য সম্পদ
    {
        'id': 10,
        'order': 10,
        'name_bn': 'কৃষি ও মৎস্য সম্পদ',
        'name_en': 'Agriculture & Fisheries',
        'slug': 'agriculture-fisheries',
        'icon': 'fish',
        'description_bn': 'নাজিরারটেক শুঁটকি পাইকারি, তাজা সামুদ্রিক মাছ, পান-সুপারি, লবণ খামার ও হ্যাচারি পিএল',
        'description_en': 'Dry fish wholesale, marine fresh fish, betel nut, salt farming and shrimp hatchery supplies',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 1001, 'name_bn': 'নাজিরারটেক শুঁটকি পাইকারি ও খুচরা বাণিজ্য', 'name_en': 'Nazirartech Dry Fish Trade', 'slug': 'dry-fish-trade', 'order': 1},
            {'id': 1002, 'name_bn': 'তাজা সামুদ্রিক মাছ ও ফিশিং ট্রলার সাপ্লাই', 'name_en': 'Fresh Marine Fish & Trawler Catch', 'slug': 'marine-fish-trawler-catch', 'order': 2},
            {'id': 1003, 'name_bn': 'মিঠা পান ও সুপারি পাইকারি বাজার', 'name_en': 'Betel Leaf & Areca Nut Wholesale', 'slug': 'betel-leaf-areca-nut-wholesale', 'order': 3},
            {'id': 1004, 'name_bn': 'লবণ উৎপাদন, মাঠ পলিথিন ও মিলিং সামগ্রী', 'name_en': 'Salt Production & Field Supplies', 'slug': 'salt-production-field-supplies', 'order': 4},
            {'id': 1005, 'name_bn': 'চিংড়ি পোনা (পিএল) ও হ্যাচারি সরঞ্জাম', 'name_en': 'Shrimp Fry (PL) & Hatchery Inputs', 'slug': 'shrimp-fry-hatchery-inputs', 'order': 5},
            {'id': 1006, 'name_bn': 'কৃষি সার, কীটনাশক ও উন্নত বীজ', 'name_en': 'Agri Fertilizer, Pesticides & Seeds', 'slug': 'agri-fertilizer-seeds', 'order': 6},
            {'id': 1007, 'name_bn': 'সেচ পাম্প ও কৃষি যন্ত্রপাতি', 'name_en': 'Irrigation Pumps & Agri Machinery', 'slug': 'irrigation-agri-machinery', 'order': 7},
        ]
    },

    # 11. প্রাণিসম্পদ ও পোষা প্রাণী
    {
        'id': 11,
        'order': 11,
        'name_bn': 'প্রাণিসম্পদ ও পোষা প্রাণী',
        'name_en': 'Livestock & Pets',
        'slug': 'livestock-pets',
        'icon': 'smile',
        'description_bn': 'গরু, ছাগল ও ডেইরি ফার্ম, পোল্ট্রি, ভেটেরিনারি চিকিৎসা, পশুর খাদ্য ও পোষা বিড়াল-পাখি',
        'description_en': 'Dairy cattle, poultry farming, veterinary doctor, animal feed and pet care',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': False,
        'subcategories': [
            {'id': 1101, 'name_bn': 'গরু, ছাগল ও ডেইরি ফার্মিং সাপোর্ট', 'name_en': 'Cattle, Goat & Dairy Farming Support', 'slug': 'dairy-cattle-farming', 'order': 1},
            {'id': 1102, 'name_bn': 'পোল্ট্রি ফার্ম ও ব্রয়লার/লেয়ার বাচ্চা সরবরাহ', 'name_en': 'Poultry Farming & Chicks Supply', 'slug': 'poultry-farming-chicks', 'order': 2},
            {'id': 1103, 'name_bn': 'ভেটেরিনারি সার্জন ও পশু চিকিৎসা', 'name_en': 'Veterinary Doctor & Animal Clinic', 'slug': 'veterinary-animal-clinic', 'order': 3},
            {'id': 1104, 'name_bn': 'পশুর খাদ্য, ভুষি ও খৈল পাইকারি', 'name_en': 'Animal Feed, Husk & Fodder Supply', 'slug': 'animal-feed-fodder', 'order': 4},
            {'id': 1105, 'name_bn': 'পোষা বিড়াল, পাখি ও অ্যাকোয়ারিয়াম মাছ', 'name_en': 'Pets (Cat/Birds) & Aquarium Fish Care', 'slug': 'pets-aquarium-care', 'order': 5},
        ]
    },

    # 12. স্বাস্থ্য ও চিকিৎসা
    {
        'id': 12,
        'order': 12,
        'name_bn': 'স্বাস্থ্য ও চিকিৎসা',
        'name_en': 'Health & Medical',
        'slug': 'health-medical',
        'icon': 'activity',
        'description_bn': 'এমবিবিএস বিশেষজ্ঞ ডাক্তার, হোম নার্সিং, ফার্মেসি, ফিজিওথেরাপি ও ডায়াগনস্টিক রক্ত পরীক্ষা',
        'description_en': 'Specialist doctor consultation, home nursing, pharmacy, physiotherapy and blood tests',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 1201, 'name_bn': 'এমবিবিএস ও বিশেষজ্ঞ ডাক্তার অ্যাপয়েন্টমেন্ট', 'name_en': 'Specialist Doctor Appointment', 'slug': 'doctor-appointment', 'order': 1},
            {'id': 1202, 'name_bn': 'হোম নার্সিং ও বয়োবৃদ্ধদের কেয়ারগিভার', 'name_en': 'Home Nursing & Elderly Caregiver', 'slug': 'home-nursing-caregiver', 'order': 2},
            {'id': 1203, 'name_bn': 'হোম ডায়াগনস্টিক ও রক্ত পরীক্ষা স্যাম্পল কালেকশন', 'name_en': 'Home Diagnostic Blood Sample Collection', 'slug': 'home-diagnostic-sample', 'order': 3},
            {'id': 1204, 'name_bn': 'ফিজিওথেরাপি ও পুনর্বাসন থেরাপিস্ট', 'name_en': 'Physiotherapy & Rehabilitation', 'slug': 'physiotherapy-rehabilitation', 'order': 4},
            {'id': 1205, 'name_bn': 'ফার্মেসি ও জরুরি হোম ডেলিভারি ঔষধ', 'name_en': 'Pharmacy & Home Medicine Delivery', 'slug': 'pharmacy-medicine-delivery', 'order': 5},
            {'id': 1206, 'name_bn': 'ডেন্টাল কেয়ার ও দাঁতের চিকিৎসা', 'name_en': 'Dental Care & Clinic Services', 'slug': 'dental-care-clinic', 'order': 6},
            {'id': 1207, 'name_bn': 'চক্ষু বিশেষজ্ঞ ও অপটিক্যাল চশমা সেবা', 'name_en': 'Eye Care Specialist & Optical Care', 'slug': 'eye-care-optical', 'order': 7},
        ]
    },

    # 13. খাবার ও রেস্তোরাঁ
    {
        'id': 13,
        'order': 13,
        'name_bn': 'খাবার ও রেস্তোরাঁ',
        'name_en': 'Food & Restaurants',
        'slug': 'food-restaurants',
        'icon': 'utensils',
        'description_bn': 'বাবুর্চি, মেজবানি রান্না, রেস্টুরেন্ট ফুড ডেলিভারি, ক্যাটারিং ও হোমমেড টিফিন',
        'description_en': 'Professional chef, mezbani cooking, restaurant food delivery, catering and homemade meals',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 1301, 'name_bn': 'বাবুর্চি ও রান্নার দল (বিয়ে/মেজবান/অনুষ্ঠান)', 'name_en': 'Professional Chef & Cooking Team (Events/Mezban)', 'slug': 'chef-cooking-team', 'order': 1},
            {'id': 1302, 'name_bn': 'রেস্তোরাঁ ও সামুদ্রিক সী-ফুড খাবার ডেলিভারি', 'name_en': 'Restaurant & Seafood Delivery', 'slug': 'restaurant-seafood-delivery', 'order': 2},
            {'id': 1303, 'name_bn': 'অফিস ও বাসা হোমমেড টিফিন সার্ভিস', 'name_en': 'Homemade Tiffin & Daily Meal Service', 'slug': 'homemade-tiffin-meal', 'order': 3},
            {'id': 1304, 'name_bn': 'ঐতিহ্যবাহী মেজবানি মাংস ও কাচ্চি প্যাকেজ', 'name_en': 'Traditional Mezbani Meat & Kacchi Package', 'slug': 'mezbani-meat-kacchi-package', 'order': 4},
            {'id': 1305, 'name_bn': 'মিষ্টি, বেকারি ও ক্যাফে ডেজার্ট আইটেম', 'name_en': 'Sweets, Bakery & Cafe Desserts', 'slug': 'sweets-bakery-cafe', 'order': 5},
        ]
    },

    # 14. সৌন্দর্য, ব্যক্তিগত পরিচর্যা ও লাইফস্টাইল
    {
        'id': 14,
        'order': 14,
        'name_bn': 'সৌন্দর্য, ব্যক্তিগত পরিচর্যা ও লাইফস্টাইল',
        'name_en': 'Beauty, Personal Care & Lifestyle',
        'slug': 'beauty-lifestyle',
        'icon': 'scissors',
        'description_bn': 'পুরুষদের সেলুন, লেডিস বিউটি পার্লার, ব্রাইডাল মেকআপ, মেহেদি আর্ট ও স্পা',
        'description_en': 'Men salon, ladies beauty parlour, bridal makeup, mehndi artist and spa',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 1401, 'name_bn': 'পুরুষদের সেলুন ও হেয়ারকাট (হোম/শপ)', 'name_en': 'Gents Salon & Haircut (Home/Shop)', 'slug': 'gents-salon-haircut', 'order': 1},
            {'id': 1402, 'name_bn': 'লেডিস বিউটি পার্লার ও স্কিন কেয়ার', 'name_en': 'Ladies Beauty Parlour & Skincare', 'slug': 'ladies-parlour-skincare', 'order': 2},
            {'id': 1403, 'name_bn': 'ব্রাইডাল মেকআপ ও পার্টি গেটআপ', 'name_en': 'Bridal Makeup & Party Look', 'slug': 'bridal-makeup-party', 'order': 3},
            {'id': 1404, 'name_bn': 'মেহেদি আর্ট ও নেইল এক্সটেনশন', 'name_en': 'Mehndi Art & Nail Extension', 'slug': 'mehndi-art-nails', 'order': 4},
            {'id': 1405, 'name_bn': 'বডি ম্যাসাজ ও রিল্যাক্সিং স্পা', 'name_en': 'Body Massage & Relaxing Spa', 'slug': 'body-massage-spa', 'order': 5},
        ]
    },

    # 15. শিক্ষা ও প্রশিক্ষণ
    {
        'id': 15,
        'order': 15,
        'name_bn': 'শিক্ষা ও প্রশিক্ষণ',
        'name_en': 'Education & Training',
        'slug': 'education-training',
        'icon': 'graduation-cap',
        'description_bn': 'হোম টিউটর, কোরআন শিক্ষা, স্পোকেন ইংলিশ, ড্রাইভিং স্কুল ও কারিগরি প্রশিক্ষণ',
        'description_en': 'Home tutor, Quran coaching, spoken English, driving school and vocational training',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 1501, 'name_bn': 'হোম ও অনলাইন টিউটর (স্কুল/কলেজ)', 'name_en': 'Home & Online Tutor (School/College)', 'slug': 'home-online-tutor', 'order': 1},
            {'id': 1502, 'name_bn': 'কোরআন ও ধর্মীয় শিক্ষক', 'name_en': 'Quran & Religious Studies Teacher', 'slug': 'quran-religious-teacher', 'order': 2},
            {'id': 1503, 'name_bn': 'স্পোকেন ইংলিশ ও ভাষা শিক্ষা', 'name_en': 'Spoken English & Language Courses', 'slug': 'spoken-english-language', 'order': 3},
            {'id': 1504, 'name_bn': 'মোটর ড্রাইভিং প্রশিক্ষণ স্কুল', 'name_en': 'Motor Driving Training School', slug: 'motor-driving-school', 'order': 4},
            {'id': 1505, 'name_bn': 'কম্পিউটার ও তথ্যপ্রযুক্তি প্রশিক্ষণ', 'name_en': 'Computer & IT Skills Training', 'slug': 'computer-it-training', 'order': 5},
            {'id': 1506, 'name_bn': 'চিত্রাঙ্কন, গান ও সৃজনশীল আর্ট ক্লাস', 'name_en': 'Drawing, Music & Creative Arts', 'slug': 'drawing-music-arts', 'order': 6},
        ]
    },

    # 16. চাকরি, কর্মসংস্থান ও শ্রমিক
    {
        'id': 16,
        'order': 16,
        'name_bn': 'চাকরি, কর্মসংস্থান ও শ্রমিক',
        'name_en': 'Jobs, Employment & Labour',
        'slug': 'jobs-employment-labour',
        'icon': 'briefcase',
        'description_bn': 'চাকরি চাই/প্রার্থী, হোটেল কর্মী, সেলসম্যান, একাউন্ট্যান্ট, সিকিউরিটি গার্ড ও দক্ষ/অদক্ষ কর্মী নিয়োগ',
        'description_en': 'Job vacancy, candidate CVs, hotel staff, salesperson, accountant and skilled/unskilled employment',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 1601, 'name_bn': 'হোটেল, মোটেল ও রেস্তোরাঁ কর্মী নিয়োগ', 'name_en': 'Hospitality & Restaurant Staff Recruitment', 'slug': 'hospitality-restaurant-staff', 'order': 1},
            {'id': 1602, 'name_bn': 'দোকান, শোরুম ও সেলস এক্সিকিউটিভ', 'name_en': 'Shop & Showroom Sales Executive', 'slug': 'shop-sales-executive', 'order': 2},
            {'id': 1603, 'name_bn': 'অফিস সহকারী, কম্পিউটার অপারেটর ও একাউন্ট্যান্ট', 'name_en': 'Office Admin, Computer Operator & Accountant', 'slug': 'office-operator-accountant', 'order': 3},
            {'id': 1604, 'name_bn': 'দৈনিক সাধারণ দিনমজুর (লেবার)', 'name_en': 'General Day Labour & Manual Worker', 'slug': 'general-day-labour', 'order': 4},
            {'id': 1605, 'name_bn': 'অভিজ্ঞ টেকনিশিয়ান ও মিস্ত্রি নিয়োগ', 'name_en': 'Skilled Technician & Mistri Employment', 'slug': 'skilled-technician-employment', 'order': 5},
            {'id': 1606, 'name_bn': 'চাকরি প্রার্থী / সিভি ডাটাবেজ', 'name_en': 'Job Seeker Profiles & Candidate CVs', 'slug': 'job-seeker-profiles', 'order': 6},
        ]
    },

    # 17. জমি, বাড়ি ও সম্পত্তি
    {
        'id': 17,
        'order': 17,
        'name_bn': 'জমি, বাড়ি ও সম্পত্তি',
        'name_en': 'Land, Real Estate & Property',
        'slug': 'land-property-realestate',
        'icon': 'building',
        'description_bn': 'ফ্ল্যাট বাসা ভাড়া, অফিস স্পেস, জমি-প্লট কেনাবেচা, দোকান ভাড়া ও প্রপার্টি ব্রোকার',
        'description_en': 'House rent, office space, commercial shops, land-plot buy/sell and real estate brokerage',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 1701, 'name_bn': 'ফ্যামিলি ও ব্যাচেলর ফ্ল্যাট বাসা ভাড়া', 'name_en': 'Family & Bachelor Apartment Rent', 'slug': 'apartment-rent-residential', 'order': 1},
            {'id': 1702, 'name_bn': 'অফিস স্পেস ও বাণিজ্যিক দোকান ভাড়া', 'name_en': 'Commercial Office & Shop Space Rent', 'slug': 'commercial-office-shop-rent', 'order': 2},
            {'id': 1703, 'name_bn': 'জমি ও প্লট কেনাবেচা সহায়তা', 'name_en': 'Land & Plot Buy/Sell Brokerage', 'slug': 'land-plot-buy-sell', 'order': 3},
            {'id': 1704, 'name_bn': 'রেডি ফ্ল্যাট ও কমার্শিয়াল বিল্ডিং বিক্রয়', 'name_en': 'Ready Apartment & Building Sale', 'slug': 'ready-apartment-building-sale', 'order': 4},
            {'id': 1705, 'name_bn': 'গোডাউন ও ওয়্যারহাউজ স্পেস ভাড়া', 'name_en': 'Godown & Warehouse Space Rent', 'slug': 'godown-warehouse-rent', 'order': 5},
        ]
    },

    # 18. পণ্য ক্রয়-বিক্রয়
    {
        'id': 18,
        'order': 18,
        'name_bn': 'পণ্য ক্রয়-বিক্রয়',
        'name_en': 'Buy & Sell Products',
        'slug': 'buy-sell-products',
        'icon': 'shopping-bag',
        'description_bn': 'নতুন ও পুরাতন পণ্য মার্কেটপ্লেস (মোবাইল, ইলেকট্রনিক্স, ফার্নিচার, গাড়ি, পাইকারি সামগ্রী)',
        'description_en': 'Marketplace for buying and selling products (electronics, mobiles, furniture, used items)',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 1801, 'name_bn': 'মোবাইল ফোন ও গ্যাজেট সামগ্রী', 'name_en': 'Mobile Phones & Smart Gadgets', 'slug': 'mobile-phones-gadgets', 'order': 1},
            {'id': 1802, 'name_bn': 'ইলেকট্রনিক্স ও গৃহস্থালি হোম অ্যাপ্লায়েন্স পণ্য', 'name_en': 'Home Appliances & Electronics Trade', 'slug': 'home-appliances-electronics', 'order': 2},
            {'id': 1803, 'name_bn': 'আসবাবপত্র ও ফার্নিচার কেনাবেচা', 'name_en': 'Furniture & Home Decor Trade', 'slug': 'furniture-trade', 'order': 3},
            {'id': 1804, 'name_bn': 'মোটরসাইকেল ও ব্যক্তিগত গাড়ি ক্রয়-বিক্রয়', 'name_en': 'Used & New Vehicles Trading', 'slug': 'vehicles-trading', 'order': 4},
            {'id': 1805, 'name_bn': 'পোশাক, জুতা ও ফ্যাশন পণ্য পাইকারি/খুচরা', 'name_en': 'Clothing, Footwear & Fashion Trade', 'slug': 'clothing-fashion-trade', 'order': 5},
            {'id': 1806, 'name_bn': 'স্থানীয় পাইকারি পণ্য ও জেনারেল স্টোর সামগ্রী', 'name_en': 'Wholesale & General Consumer Goods', 'slug': 'wholesale-consumer-goods', 'order': 6},
        ]
    },

    # 19. প্রযুক্তি ও ডিজিটাল সেবা
    {
        'id': 19,
        'order': 19,
        'name_bn': 'প্রযুক্তি ও ডিজিটাল সেবা',
        'name_en': 'Technology & Digital Services',
        'slug': 'technology-digital-services',
        'icon': 'monitor',
        'description_bn': 'কম্পিউটার-ল্যাপটপ মেরামত, সিসিটিভি ক্যামেরা সেটআপ, ওয়েবসাইট ডেভেলপমেন্ট ও নেটওয়ার্কিং',
        'description_en': 'Computer repair, CCTV installation, website development, software and networking infrastructure',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 1901, 'name_bn': 'কম্পিউটার, ল্যাপটপ ও প্রিন্টার মেরামত', 'name_en': 'Computer, Laptop & Printer Repair', 'slug': 'computer-laptop-printer-repair', 'order': 1},
            {'id': 1902, 'name_bn': 'সিসিটিভি ক্যামেরা ইনস্টলেশন ও রক্ষণাবেক্ষণ', 'name_en': 'CCTV Camera Setup & Maintenance', 'slug': 'cctv-setup-maintenance', 'order': 2},
            {'id': 1903, 'name_bn': 'ওয়াইফাই, রাউটার ও নেটওয়ার্ক অবকাঠামো', 'name_en': 'WiFi, Router & Broadband Setup', 'slug': 'wifi-broadband-setup', 'order': 3},
            {'id': 1904, 'name_bn': 'মোবাইল ফোন ও ট্যাবলেট হার্ডওয়্যার মেরামত', 'name_en': 'Mobile Phone Hardware Servicing', 'slug': 'mobile-hardware-servicing', 'order': 4},
            {'id': 1905, 'name_bn': 'ওয়েবসাইট, সফটওয়্যার ও অ্যাপ ডেভেলপমেন্ট', 'name_en': 'Website, App & Custom Software Development', 'slug': 'website-software-development', 'order': 5},
            {'id': 1906, 'name_bn': 'পস (POS) সফটওয়্যার ও বিলিং সিস্টেম', 'name_en': 'POS Software & Retail Billing Systems', 'slug': 'pos-software-billing', 'order': 6},
        ]
    },

    # 20. মিডিয়া, ক্রিয়েটিভ ও প্রিন্টিং
    {
        'id': 20,
        'order': 20,
        'name_bn': 'মিডিয়া, ক্রিয়েটিভ ও প্রিন্টিং',
        'name_en': 'Media, Creative & Printing',
        'slug': 'media-creative-printing',
        'icon': 'printer',
        'description_bn': 'গ্রাফিক ডিজাইন, ব্যানার ও সাইনবোর্ড প্রিন্টিং, প্রেস, সিনেমাটোগ্রাফি ও ডিজিটাল মার্কেটিং',
        'description_en': 'Graphic design, banner printing, press, photo/videography and digital marketing promotion',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 2001, 'name_bn': 'ব্যানার, ফেস্টুন ও পিভিসি সাইনবোর্ড প্রিন্টিং', 'name_en': 'Banner, Festoon & PVC Printing', 'slug': 'banner-festoon-printing', 'order': 1},
            {'id': 2002, 'name_bn': 'গ্রাফিক ডিজাইন, লোগো ও সোশ্যাল ব্যানার', 'name_en': 'Graphic Design, Logo & Creative Branding', 'slug': 'graphic-design-branding', 'order': 2},
            {'id': 2003, 'name_bn': 'অফসেট প্রেস (বই, লিফলেট, রশিদ ও ভাউচার)', 'name_en': 'Offset Press & Commercial Printing', 'slug': 'offset-press-printing', 'order': 3},
            {'id': 2004, 'name_bn': 'ফটোগ্রাফি ও সিনেমাটোগ্রাফি শ্যুট', 'name_en': 'Photography & Video Production Shoot', 'slug': 'photography-video-shoot', 'order': 4},
            {'id': 2005, 'name_bn': 'ফেসবুক পেজ প্রমোশন ও ডিজিটাল মার্কেটিং', 'name_en': 'Social Media & Digital Marketing Promotion', 'slug': 'digital-marketing-promotion', 'order': 5},
            {'id': 2006, 'name_bn': 'ভিজিটিং কার্ড, আইডি কার্ড ও রাবার সিল', 'name_en': 'Visiting Card, ID Card & Official Seals', 'slug': 'visiting-card-id-seals', 'order': 6},
        ]
    },

    # 21. আইন, দলিল ও সরকারি সেবা সহায়তা
    {
        'id': 21,
        'order': 21,
        'name_bn': 'আইন, দলিল ও সরকারি সেবা সহায়তা',
        'name_en': 'Legal, Deed & Citizen Services',
        'slug': 'legal-citizen-services',
        'icon': 'scale',
        'description_bn': 'দলিল লেখক, জমি রেজিস্ট্রি, নোটারি পাবলিক, ট্রেড লাইসেন্স, পাসপোর্ট ও আইনি পরামর্শ',
        'description_en': 'Deed writing, land registry assistance, notary public, trade license and legal consultancy',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': False,
        'subcategories': [
            {'id': 2101, 'name_bn': 'দলিল লেখক ও জমি রেজিস্ট্রি আইনি সহায়তা', 'name_en': 'Deed Writer & Land Registration Support', 'slug': 'deed-writer-land-registration', 'order': 1},
            {'id': 2102, 'name_bn': 'আইনজীবী ও লিগ্যাল কনসাল্টেন্সি', 'name_en': 'Advocate & Legal Consultation Services', 'slug': 'advocate-legal-consultation', 'order': 2},
            {'id': 2103, 'name_bn': 'নোটারি পাবলিক ও হলফনামা সত্যায়ন', 'name_en': 'Notary Public & Affidavit Attestation', 'slug': 'notary-public-affidavit', 'order': 3},
            {'id': 2104, 'name_bn': 'পাসপোর্ট, ভিসা ও এনআইডি সংশোধন সহায়তা', 'name_en': 'Passport, Visa & NID Documentation Support', 'slug': 'passport-visa-nid-support', 'order': 4},
            {'id': 2105, 'name_bn': 'ট্রেড লাইসেন্স, টিন (TIN) ও ভ্যাট পরামর্শ', 'name_en': 'Trade License, TIN & VAT Consulting', 'slug': 'trade-license-tin-vat', 'order': 5},
        ]
    },

    # 22. আর্থিক ও ব্যবসায়িক সেবা
    {
        'id': 22,
        'order': 22,
        'name_bn': 'আর্থিক ও ব্যবসায়িক সেবা',
        'name_en': 'Financial & Business Services',
        'slug': 'financial-business-services',
        'icon': 'credit-card',
        'description_bn': 'অ্যাকাউন্টিং, বুককিপিং, ব্যাংক লোন প্রসেসিং, বীমা ও ব্যবসা অডিট পরামর্শ',
        'description_en': 'Accounting, bookkeeping, bank loan processing, insurance and business audit',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': False,
        'subcategories': [
            {'id': 2201, 'name_bn': 'ব্যবসায়িক অ্যাকাউন্টিং ও বুককিপিং', 'name_en': 'Business Accounting & Bookkeeping', 'slug': 'accounting-bookkeeping', 'order': 1},
            {'id': 2202, 'name_bn': 'ব্যাংক ঋণ ও এসএমই লোন ফাইল প্রসেসিং', 'name_en': 'Bank & SME Loan File Processing', 'slug': 'bank-loan-processing', 'order': 2},
            {'id': 2203, 'name_bn': 'জীবন ও সাধারণ বীমা (ইনস্যুরেন্স) এজেন্ট', 'name_en': 'Life & General Insurance Agency', 'slug': 'insurance-agency', 'order': 3},
            {'id': 2204, 'name_bn': 'কোম্পানি অডিট ও আর্থিক কনসাল্টিং', 'name_en': 'Company Audit & Financial Advisory', 'slug': 'company-audit-advisory', 'order': 4},
        ]
    },

    # 23. ধর্মীয় ও সামাজিক সেবা
    {
        'id': 23,
        'order': 23,
        'name_bn': 'ধর্মীয় ও সামাজিক সেবা',
        'name_en': 'Religious & Social Services',
        'slug': 'religious-social-services',
        'icon': 'users',
        'description_bn': 'কাজী অফিস, মিলাদ/দোয়া পরিচালনা, জানাজা ও কাফন-দাফন সেবা, হজ্জ ও ওমরাহ কাফেলা',
        'description_en': 'Kazi office, nikah registrar, milad/dua, funeral & burial assistance, hajj & umrah caravans',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': False,
        'subcategories': [
            {'id': 2301, 'name_bn': 'বিবাহ রেজিস্ট্রার ও কাজী অফিস সেবা', 'name_en': 'Marriage Registrar & Kazi Office', 'slug': 'marriage-registrar-kazi', 'order': 1},
            {'id': 2302, 'name_bn': 'মিলাদ, মাহফিল ও ধর্মীয় অনুষ্ঠান পরিচালনা', 'name_en': 'Religious Gathering, Milad & Dua', 'slug': 'milad-dua-management', 'order': 2},
            {'id': 2303, 'name_bn': 'জানাজা, কাফন ও দাফন সহায়তা', 'name_en': 'Funeral & Burial Social Assistance', 'slug': 'funeral-burial-assistance', 'order': 3},
            {'id': 2304, 'name_bn': 'হজ্জ ও ওমরাহ ট্রাভেল কাফেলা', 'name_en': 'Hajj & Umrah Travel Caravans', 'slug': 'hajj-umrah-travel', 'order': 4},
        ]
    },

    # 24. ব্যক্তিগত ও গৃহস্থালি সেবা
    {
        'id': 24,
        'order': 24,
        'name_bn': 'ব্যক্তিগত ও গৃহস্থালি সেবা',
        'name_en': 'Personal & Domestic Services',
        'slug': 'personal-domestic-services',
        'icon': 'user',
        'description_bn': 'কাজের বুয়া, দর্জি, ড্রাই ওয়াশ লন্ড্রি, মুচি, ছাতা মেরামত ও ডুপ্লিকেট চাবি তৈরি',
        'description_en': 'House maid, tailoring, laundry dry wash, cobbler, key maker and domestic artisans',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 2401, 'name_bn': 'বাসার কাজের বুয়া ও গৃহকর্মী নিয়োগ', 'name_en': 'House Maid & Domestic Helper', 'slug': 'house-maid-domestic-helper', 'order': 1},
            {'id': 2402, 'name_bn': 'দর্জি ও কাপড় সেলাই (টেইলারিং ও অল্টারেশন)', 'name_en': 'Custom Tailoring & Alteration', 'slug': 'custom-tailoring-alteration', 'order': 2},
            {'id': 2403, 'name_bn': 'লন্ড্রি ও ড্রাই ওয়াশ সার্ভিস', 'name_en': 'Laundry & Dry Cleaning Service', 'slug': 'laundry-dry-cleaning', 'order': 3},
            {'id': 2404, 'name_bn': 'মুচি ও চামড়ার জুতা-ব্যাগ মেরামত', 'name_en': 'Cobbler & Leather Bag/Shoe Repair', 'slug': 'cobbler-shoe-repair', 'order': 4},
            {'id': 2405, 'name_bn': 'ছাতা ও রেইনকোট মেরামত কারিগর', 'name_en': 'Umbrella & Raincoat Repair', 'slug': 'umbrella-repair', 'order': 5},
            {'id': 2406, 'name_bn': 'ডুপ্লিকেট চাবি তৈরি ও লক মেকার', 'name_en': 'Duplicate Key & Lock Maker', 'slug': 'duplicate-key-maker', 'order': 6},
        ]
    },

    # 25. অনুষ্ঠান, বিয়ে ও ইভেন্ট
    {
        'id': 25,
        'order': 25,
        'name_bn': 'অনুষ্ঠান, বিয়ে ও ইভেন্ট',
        'name_en': 'Events, Wedding & Occasions',
        'slug': 'events-wedding-occasions',
        'icon': 'gift',
        'description_bn': 'বিয়ের স্টেজ ডেকোরেশন, সাউন্ড সিস্টেম ও মাইক, লাইটিং, কনভেনশন হল ও ইভেন্ট অর্গানাইজার',
        'description_en': 'Wedding stage decoration, sound system, event lighting, venue booking and event managers',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 2501, 'name_bn': 'বিয়ের স্টেজ, গেট ও ইভেন্ট ডেকোরেশন', 'name_en': 'Stage & Gate Event Decoration', 'slug': 'event-stage-decoration', 'order': 1},
            {'id': 2502, 'name_bn': 'সাউন্ড সিস্টেম ও মাইক ভাড়া', 'name_en': 'Sound System & Mic Rental', 'slug': 'sound-system-mic-rental', 'order': 2},
            {'id': 2503, 'name_bn': 'ইভেন্ট লাইটিং ও জেনারেটর ব্যাকআপ', 'name_en': 'Event Lighting & Heavy Generator', 'slug': 'event-lighting-generator', 'order': 3},
            {'id': 2504, 'name_bn': 'কমিউনিটি সেন্টার ও কনভেনশন হল বুকিং', 'name_en': 'Community Center & Convention Hall Booking', 'slug': 'convention-hall-booking', 'order': 4},
            {'id': 2505, 'name_bn': 'ইভেন্ট প্ল্যানার ও পূর্ণাঙ্গ অর্গানাইজার', 'name_en': 'Event Planner & Full Coordination', 'slug': 'event-planner-coordination', 'order': 5},
        ]
    },

    # 26. জরুরি ও উদ্ধার সেবা
    {
        'id': 26,
        'order': 26,
        'name_bn': 'জরুরি ও উদ্ধার সেবা',
        'name_en': 'Emergency & Rescue Services',
        'slug': 'emergency-rescue-services',
        'icon': 'alert-triangle',
        'description_bn': 'জরুরি অ্যাম্বুলেন্স, অক্সিজেন সিলিন্ডার, ফায়ার রেসকিউ টিম, অন-কল জরুরি ইলেকট্রিশিয়ান ও দুর্যোগ সহায়তা',
        'description_en': 'Emergency ambulance, medical oxygen, fire rescue coordination, emergency on-call electrician and disaster response',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': True,
        'is_popular': True,
        'subcategories': [
            {'id': 2601, 'name_bn': 'জরুরি অ্যাম্বুলেন্স (আইসিইউ/সাধারণ)', 'name_en': 'Emergency Ambulance (ICU/Standard)', 'slug': 'emergency-ambulance-service', 'order': 1},
            {'id': 2602, 'name_bn': 'মেডিকেল অক্সিজেন সিলিন্ডার জরুরি ডেলিভারি', 'name_en': 'Emergency Medical Oxygen Delivery', 'slug': 'emergency-oxygen-delivery', 'order': 2},
            {'id': 2603, 'name_bn': 'জরুরি রক্তদাতা ও ব্লাড ডোনার নেটওয়ার্ক', 'name_en': 'Emergency Blood Donor Network', 'slug': 'blood-donor-network', 'order': 3},
            {'id': 2604, 'name_bn': 'অন-কল জরুরি ইলেকট্রিশিয়ান ও ফায়ার শর্ট-সার্কিট ফিক্স', 'name_en': 'Emergency On-Call Electrician Rescue', 'slug': 'emergency-electrician-rescue', 'order': 4},
            {'id': 2605, 'name_bn': 'বন্যা, সাইক্লোন ও দুর্যোগ জরুরি উদ্ধার দল', 'name_en': 'Disaster & Cyclone Rescue Volunteers', 'slug': 'disaster-cyclone-rescue', 'order': 5},
        ]
    },

    # 27. স্থানীয় তথ্য ও জনসেবা
    {
        'id': 27,
        'order': 27,
        'name_bn': 'স্থানীয় তথ্য ও জনসেবা',
        'name_en': 'Local Information & Public Services',
        'slug': 'local-info-public-services',
        'icon': 'info',
        'description_bn': 'থানা ও পুলিশ হেল্পলাইন তথ্য, ফায়ার সার্ভিস নম্বর, হাসপাতাল ডিরেক্টরি ও নাগরিক সেবা তথ্য',
        'description_en': 'Police station helpline info, fire service directory, hospital hotline and civic citizen guidance',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': False,
        'subcategories': [
            {'id': 2701, 'name_bn': 'থানা ও পুলিশ কন্ট্রোল রুম যোগাযোগ তথ্য', 'name_en': 'Police Station & Control Room Info', 'slug': 'police-station-control-info', 'order': 1},
            {'id': 2702, 'name_bn': 'ফায়ার সার্ভিস ও সিভিল ডিফেন্স স্টেশন ডিরেক্টরি', 'name_en': 'Fire Service Station Directory Info', 'slug': 'fire-service-directory-info', 'order': 2},
            {'id': 2703, 'name_bn': 'হাসপাতাল, ক্লিনিক ও ব্লাড ব্যাংক হটলাইন তথ্য', 'name_en': 'Hospital & Blood Bank Hotline Directory', 'slug': 'hospital-hotline-directory', 'order': 3},
            {'id': 2704, 'name_bn': 'পৌরসভা ও ইউনিয়ন পরিষদ নাগরিক সহায়তা তথ্য', 'name_en': 'Municipality & Union Parishad Civic Info', 'slug': 'municipality-civic-info', 'order': 4},
        ]
    },

    # 28. পেশাজীবী ও বিশেষজ্ঞ সেবা
    {
        'id': 28,
        'order': 28,
        'name_bn': 'পেশাজীবী ও বিশেষজ্ঞ সেবা',
        'name_en': 'Professional & Expert Services',
        'slug': 'professional-expert-services',
        'icon': 'award',
        'description_bn': 'চার্টার্ড অ্যাকাউন্ট্যান্ট, বিজনেস কনসালটেন্ট, ক্যারিয়ার কাউন্সিলর ও সার্টিফাইড বিশেষজ্ঞ',
        'description_en': 'Chartered accountants, certified consultants, career counsellors and domain specialists',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': False,
        'subcategories': [
            {'id': 2801, 'name_bn': 'বিজনেস ও ম্যানেজমেন্ট কনসালটেন্ট', 'name_en': 'Business & Management Consultant', 'slug': 'business-management-consultant', 'order': 1},
            {'id': 2802, 'name_bn': 'চার্টার্ড অ্যাকাউন্ট্যান্ট ও প্রফেশনাল ট্যাক্স অ্যাডভাইজার', 'name_en': 'Chartered Accountant & Tax Specialist', 'slug': 'ca-tax-specialist', 'order': 2},
            {'id': 2803, 'name_bn': 'ক্যারিয়ার ও স্টাডি অ্যাব্রোড কনসালটেন্সি', 'name_en': 'Career & Study Abroad Consultant', 'slug': 'career-study-abroad', 'order': 3},
            {'id': 2804, 'name_bn': 'মানসিক স্বাস্থ্য ও সাইকোলজিক্যাল কাউন্সিলর', 'name_en': 'Mental Health & Psychological Counsellor', 'slug': 'mental-health-counsellor', 'order': 4},
        ]
    },

    # 29. নিরাপত্তা ও সুরক্ষা সেবা
    {
        'id': 29,
        'order': 29,
        'name_bn': 'নিরাপত্তা ও সুরক্ষা সেবা',
        'name_en': 'Security & Safety Services',
        'slug': 'security-safety-services',
        'icon': 'shield',
        'description_bn': 'সিকিউরিটি গার্ড, নাইট গার্ড, ইভেন্ট বাউন্সার, সিসিটিভি মনিটরিং ও ফায়ার সেফটি',
        'description_en': 'Security guard, night watchman, event bouncers, CCTV surveillance and fire safety refills',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 2901, 'name_bn': 'বাসা ও অফিসের প্রশিক্ষিত সিকিউরিটি গার্ড', 'name_en': 'Trained Residential & Office Security Guard', 'slug': 'security-guard-service', 'order': 1},
            {'id': 2902, 'name_bn': 'মার্কেট ও প্রপার্টি নাইট গার্ড পাহারা', 'name_en': 'Market & Property Night Watchman', 'slug': 'night-watchman-service', 'order': 2},
            {'id': 2903, 'name_bn': 'ইভেন্ট বাউন্সার ও ভিআইপি প্রটেকশন টিম', 'name_en': 'Event Bouncer & VIP Protection Squad', 'slug': 'event-bouncer-vip-squad', 'order': 3},
            {'id': 2904, 'name_bn': 'সিসিটিভি মনিটরিং ও নিরাপত্তা নজরদারি সেবা', 'name_en': 'CCTV Central Monitoring & Surveillance', 'slug': 'cctv-monitoring-surveillance', 'order': 4},
            {'id': 2905, 'name_bn': 'ফায়ার সেফটি ও এক্সটিংগুইশার রিফিল সার্ভিস', 'name_en': 'Fire Safety Equipment & Extinguisher Refill', 'slug': 'fire-safety-refill', 'order': 5},
        ]
    },

    # 30. বিদ্যুৎ, জ্বালানি ও ইউটিলিটি সেবা
    {
        'id': 30,
        'order': 30,
        'name_bn': 'বিদ্যুৎ, জ্বালানি ও ইউটিলিটি সেবা',
        'name_en': 'Power, Energy & Utilities',
        'slug': 'power-energy-utilities',
        'icon': 'zap',
        'description_bn': 'এলপিজি গ্যাস সিলিন্ডার ডেলিভারি, সোলার প্যানেল ইনস্টল, ভারী জেনারেটর পাওয়ার ব্যাকআপ ও বিদ্যুৎ সংক্রান্ত কাজ',
        'description_en': 'LPG cooking gas cylinder delivery, solar panel setup, heavy power generator backups and utilities',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': True,
        'subcategories': [
            {'id': 3001, 'name_bn': 'এলপিজি রান্নার গ্যাস সিলিন্ডার হোম ডেলিভারি', 'name_en': 'LPG Cooking Gas Cylinder Home Delivery', 'slug': 'lpg-gas-cylinder-delivery', 'order': 1},
            {'id': 3002, 'name_bn': 'সোলার প্যানেল ইনস্টলেশন ও অন-গ্রিড সেটআপ', 'name_en': 'Solar Panel & On-Grid Setup', 'slug': 'solar-panel-setup', 'order': 2},
            {'id': 3003, 'name_bn': 'শিল্প ও অনুষ্ঠান পাওয়ার জেনারেটর ভাড়া', 'name_en': 'Industrial & Event Power Generator Rental', 'slug': 'power-generator-rental', 'order': 3},
            {'id': 3004, 'name_bn': 'বিদ্যুৎ সাবস্টেশন ও ট্রান্সফরমার টেকনিশিয়ান', 'name_en': 'Electrical Substation & Transformer Work', 'slug': 'electrical-substation-technician', 'order': 4},
        ]
    },

    # 31. খেলাধুলা, বিনোদন ও অবসর
    {
        'id': 31,
        'order': 31,
        'name_bn': 'খেলাধুলা, বিনোদন ও অবসর',
        'name_en': 'Sports, Entertainment & Recreation',
        'slug': 'sports-entertainment-recreation',
        'icon': 'trophy',
        'description_bn': 'টার্ফ ও ফুটবল মাঠ বুকিং, জিম ও ফিটনেস ট্রেইনার, বিচ ভলিবল, মিউজিক্যাল ব্যান্ড ও বিনোদন আয়োজন',
        'description_en': 'Turf football ground booking, gym fitness trainer, musical band performance and recreational events',
        'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY,
        'is_featured': False,
        'is_popular': False,
        'subcategories': [
            {'id': 3101, 'name_bn': 'টার্ফ ও ফুটবল মাঠ স্লট বুকিং', 'name_en': 'Turf & Football Field Slot Booking', 'slug': 'turf-football-field-booking', 'order': 1},
            {'id': 3102, 'name_bn': 'জিম ও ব্যক্তিগত ফিটনেস ট্রেইনার', 'name_en': 'Gym & Personal Fitness Trainer', 'slug': 'gym-fitness-trainer', 'order': 2},
            {'id': 3103, 'name_bn': 'মিউজিক্যাল ব্যান্ড ও সাউন্ড আর্টিস্ট পারফরম্যান্স', 'name_en': 'Live Musical Band & Vocal Performance', 'slug': 'musical-band-performance', 'order': 3},
            {'id': 3104, 'name_bn': 'বিচ স্পোর্টস ও রিক্রিয়েশন ইভেন্ট', 'name_en': 'Beach Sports & Recreation Activities', 'slug': 'beach-sports-recreation', 'order': 4},
        ]
    },
]


# =============================================================================
# INITIAL TAXONOMY SEARCH SYNONYMS / ALIASES
# =============================================================================
INITIAL_TAXONOMY_ALIASES = [
    # Mason / Construction skills
    {'alias_text': 'রাজমিস্ত্রি', 'normalized_text': 'রাজমিস্ত্রি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 102, 'language': AliasLanguage.BN, 'category_id': 1},
    {'alias_text': 'মেস্ত্রি', 'normalized_text': 'মেস্ত্রি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 102, 'language': AliasLanguage.BN, 'category_id': 1},
    {'alias_text': 'mason', 'normalized_text': 'mason', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 102, 'language': AliasLanguage.EN, 'category_id': 1},
    {'alias_text': 'রড মিস্ত্রি', 'normalized_text': 'রড মিস্ত্রি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 102, 'language': AliasLanguage.BN, 'category_id': 1},
    {'alias_text': 'ঢালাই মিস্ত্রি', 'normalized_text': 'ঢালাই মিস্ত্রি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 102, 'language': AliasLanguage.BN, 'category_id': 1},
    {'alias_text': 'ইট বালু', 'normalized_text': 'ইট বালু', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 101, 'language': AliasLanguage.BN, 'category_id': 1},

    # Electrician
    {'alias_text': 'ইলেকট্রিশিয়ান', 'normalized_text': 'ইলেকট্রিশিয়ান', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 201, 'language': AliasLanguage.BN, 'category_id': 2},
    {'alias_text': 'electrician', 'normalized_text': 'electrician', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 201, 'language': AliasLanguage.EN, 'category_id': 2},
    {'alias_text': 'কারেন্ট মিস্ত্রি', 'normalized_text': 'কারেন্ট মিস্ত্রি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 201, 'language': AliasLanguage.BN, 'category_id': 2},
    {'alias_text': 'এসি মেকানিক', 'normalized_text': 'এসি মেকানিক', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 202, 'language': AliasLanguage.BN, 'category_id': 2},
    {'alias_text': 'ac servicing', 'normalized_text': 'ac servicing', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 202, 'language': AliasLanguage.EN, 'category_id': 2},
    {'alias_text': 'ফ্রিজ মিস্ত্রি', 'normalized_text': 'ফ্রিজ মিস্ত্রি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 203, 'language': AliasLanguage.BN, 'category_id': 2},

    # Transport / Shifting
    {'alias_text': 'বাসা বদল', 'normalized_text': 'বাসা বদল', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 401, 'language': AliasLanguage.BN, 'category_id': 4},
    {'alias_text': 'house shifting', 'normalized_text': 'house shifting', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 401, 'language': AliasLanguage.EN, 'category_id': 4},
    {'alias_text': 'পিকআপ ভাড়া', 'normalized_text': 'পিকআপ ভাড়া', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 402, 'language': AliasLanguage.BN, 'category_id': 4},
    {'alias_text': 'pickup rental', 'normalized_text': 'pickup rental', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 402, 'language': AliasLanguage.EN, 'category_id': 4},
    {'alias_text': 'চাঁন্দের গাড়ি', 'normalized_text': 'চাঁন্দের গাড়ি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 603, 'language': AliasLanguage.BN, 'category_id': 6},
    {'alias_text': 'chander gari', 'normalized_text': 'chander gari', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 603, 'language': AliasLanguage.EN, 'category_id': 6},

    # Hotel & Tourism
    {'alias_text': 'হোটেল বুকিং', 'normalized_text': 'হোটেল বুকিং', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 801, 'language': AliasLanguage.BN, 'category_id': 8},
    {'alias_text': 'hotel room', 'normalized_text': 'hotel room', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 801, 'language': AliasLanguage.EN, 'category_id': 8},
    {'alias_text': 'সেন্টমার্টিন জাহাজ', 'normalized_text': 'সেন্টমার্টিন জাহাজ', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 902, 'language': AliasLanguage.BN, 'category_id': 9},
    {'alias_text': 'saint martin ship', 'normalized_text': 'saint martin ship', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 902, 'language': AliasLanguage.EN, 'category_id': 9},

    # Health & Emergency
    {'alias_text': 'ডাক্তার', 'normalized_text': 'ডাক্তার', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 1201, 'language': AliasLanguage.BN, 'category_id': 12},
    {'alias_text': 'doctor', 'normalized_text': 'doctor', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 1201, 'language': AliasLanguage.EN, 'category_id': 12},
    {'alias_text': 'অ্যাম্বুলেন্স', 'normalized_text': 'অ্যাম্বুলেন্স', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 2601, 'language': AliasLanguage.BN, 'category_id': 26},
    {'alias_text': 'ambulance', 'normalized_text': 'ambulance', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 2601, 'language': AliasLanguage.EN, 'category_id': 26},
    {'alias_text': 'অক্সিজেন', 'normalized_text': 'অক্সিজেন', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 2602, 'language': AliasLanguage.BN, 'category_id': 26},
    {'alias_text': 'oxygen cylinder', 'normalized_text': 'oxygen cylinder', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 2602, 'language': AliasLanguage.EN, 'category_id': 26},

    # Dry Fish & Cox's Bazar specials
    {'alias_text': 'শুঁটকি', 'normalized_text': 'শুঁটকি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 1001, 'language': AliasLanguage.BN, 'category_id': 10},
    {'alias_text': 'নাজিরারটেক শুঁটকি', 'normalized_text': 'নাজিরারটেক শুঁটকি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 1001, 'language': AliasLanguage.BN, 'category_id': 10},
    {'alias_text': 'dry fish', 'normalized_text': 'dry fish', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 1001, 'language': AliasLanguage.EN, 'category_id': 10},
    {'alias_text': 'লবণ মাঠ', 'normalized_text': 'লবণ মাঠ', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 1004, 'language': AliasLanguage.BN, 'category_id': 10},
    {'alias_text': 'পান সুপারি', 'normalized_text': 'পান সুপারি', 'target_type': AliasTargetType.SUBCATEGORY, 'target_id': 1003, 'language': AliasLanguage.BN, 'category_id': 10},
]
