"""
Constants and enumerations for Category & Service Engine.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
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


# The 46 Master Taxonomy Modules of SebaCox
INITIAL_46_TAXONOMY_MODULES = [
    # 1-7: System & Operational Domains
    {'order': 1, 'name_bn': 'ব্যবহারকারী', 'name_en': 'User', 'slug': 'user', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'user'},
    {'order': 2, 'name_bn': 'স্থান ও অবস্থান', 'name_en': 'Location & Places', 'slug': 'location-places', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'map-pin'},
    {'order': 3, 'name_bn': 'সেবাসমূহ', 'name_en': 'Services Directory', 'slug': 'services-directory', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'grid'},
    {'order': 4, 'name_bn': 'সেবাদাতা', 'name_en': 'Service Providers', 'slug': 'service-providers', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'briefcase'},
    {'order': 5, 'name_bn': 'আমার প্রয়োজন', 'name_en': 'My Demands', 'slug': 'my-demands', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'help-circle'},
    {'order': 6, 'name_bn': 'বুকিং ও সময় নির্ধারণ', 'name_en': 'Booking & Scheduling', 'slug': 'booking-scheduling', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'calendar'},
    {'order': 7, 'name_bn': 'অর্ডার ও কেনাকাটা', 'name_en': 'Orders & Shopping', 'slug': 'orders-shopping', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'shopping-bag'},

    # 8-40: Public Service Categories
    {'order': 8, 'name_bn': 'ভাড়া সেবা', 'name_en': 'Rental Services', 'slug': 'rental-services', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'key'},
    {'order': 9, 'name_bn': 'লেনদেন ও অর্থ', 'name_en': 'Transactions & Finance', 'slug': 'transactions-finance', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'credit-card'},
    {'order': 10, 'name_bn': 'যোগাযোগ ও চ্যাট', 'name_en': 'Communication & Chat', 'slug': 'communication-chat', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'message-circle'},
    {'order': 11, 'name_bn': 'ভ্রমণ ও পর্যটন', 'name_en': 'Travel & Tourism', 'slug': 'travel-tourism', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'compass', 'featured': True},
    {'order': 12, 'name_bn': 'হোটেল ও আবাসন', 'name_en': 'Hotel & Accommodation', 'slug': 'hotel-accommodation', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'home', 'featured': True},
    {'order': 13, 'name_bn': 'খাবার ও রেস্তোরাঁ', 'name_en': 'Food & Restaurants', 'slug': 'food-restaurants', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'coffee', 'featured': True},
    {'order': 14, 'name_bn': 'যাতায়াত ও টিকিট', 'name_en': 'Transport & Tickets', 'slug': 'transport-tickets', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'ticket', 'featured': True},
    {'order': 15, 'name_bn': 'যানবাহন সেবা', 'name_en': 'Vehicle Services', 'slug': 'vehicle-services', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'truck'},
    {'order': 16, 'name_bn': 'নির্মাণ ও প্রকৌশল', 'name_en': 'Construction & Engineering', 'slug': 'construction-engineering', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'tool', 'featured': True},
    {'order': 17, 'name_bn': 'নির্মাণ সামগ্রী', 'name_en': 'Building Materials', 'slug': 'building-materials', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'package'},
    {'order': 18, 'name_bn': 'বাড়ি ও ব্যক্তিগত সেবা', 'name_en': 'Home & Personal Services', 'slug': 'home-personal-services', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'wrench', 'featured': True},
    {'order': 19, 'name_bn': 'স্বাস্থ্য ও চিকিৎসা', 'name_en': 'Health & Medical', 'slug': 'health-medical', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'activity', 'featured': True},
    {'order': 20, 'name_bn': 'শিক্ষা ও প্রশিক্ষণ', 'name_en': 'Education & Training', 'slug': 'education-training', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'book'},
    {'order': 21, 'name_bn': 'চাকরি ও কর্মসংস্থান', 'name_en': 'Jobs & Employment', 'slug': 'jobs-employment', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'user-check'},
    {'order': 22, 'name_bn': 'কৃষি ও কৃষিসেবা', 'name_en': 'Agriculture & Farming', 'slug': 'agriculture-farming', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'sun'},
    {'order': 23, 'name_bn': 'মৎস্য ও সামুদ্রিক পণ্য', 'name_en': 'Fisheries & Marine Products', 'slug': 'fisheries-marine-products', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'anchor'},
    {'order': 24, 'name_bn': 'পশু, পাখি ও চিকিৎসা', 'name_en': 'Veterinary & Animal Care', 'slug': 'veterinary-animal-care', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'heart'},
    {'order': 25, 'name_bn': 'ব্যবসা ও স্থানীয় দোকান', 'name_en': 'Local Business & Shops', 'slug': 'local-business-shops', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'shopping-cart'},
    {'order': 26, 'name_bn': 'জমি-জমা ক্রয়-বিক্রয়', 'name_en': 'Land & Property Trading', 'slug': 'land-property-trading', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'map'},
    {'order': 27, 'name_bn': 'আইন ও পেশাগত সেবা', 'name_en': 'Legal & Professional Services', 'slug': 'legal-professional-services', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'award'},
    {'order': 28, 'name_bn': 'ব্যাংক, অর্থ ও বীমা', 'name_en': 'Banking, Finance & Insurance', 'slug': 'banking-finance-insurance', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'dollar-sign'},
    {'order': 29, 'name_bn': 'ডিজিটাল ও তথ্যপ্রযুক্তি', 'name_en': 'Digital & IT Services', 'slug': 'digital-it-services', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'monitor'},
    {'order': 30, 'name_bn': 'পোশাক, সৌন্দর্য ও জীবনধারা', 'name_en': 'Fashion, Beauty & Lifestyle', 'slug': 'fashion-beauty-lifestyle', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'scissors'},
    {'order': 31, 'name_bn': 'ছাপাখানা, গণমাধ্যম ও সৃজনশীল সেবা', 'name_en': 'Printing, Media & Creative', 'slug': 'printing-media-creative', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'printer'},
    {'order': 32, 'name_bn': 'অনুষ্ঠান ও বিয়ের সেবা', 'name_en': 'Events & Wedding Services', 'slug': 'events-wedding-services', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'gift'},
    {'order': 33, 'name_bn': 'ডেলিভারি ও পণ্য পরিবহন', 'name_en': 'Delivery & Logistics', 'slug': 'delivery-logistics', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'send'},
    {'order': 34, 'name_bn': 'পুরাতন পণ্য ক্রয়-বিক্রয়', 'name_en': 'Buy & Sell Used Items', 'slug': 'buy-sell-used-items', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'repeat'},
    {'order': 35, 'name_bn': 'ধর্ম ও সমাজ', 'name_en': 'Religion & Community', 'slug': 'religion-community', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'users'},
    {'order': 36, 'name_bn': 'সরকারি ও নাগরিক সেবা', 'name_en': 'Government & Citizen Services', 'slug': 'government-citizen-services', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'flag'},
    {'order': 37, 'name_bn': 'জরুরি ও নিরাপত্তা', 'name_en': 'Emergency & Safety', 'slug': 'emergency-safety', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'alert-triangle', 'featured': True},
    {'order': 38, 'name_bn': 'প্রাণী ও পোষা প্রাণী', 'name_en': 'Pets & Animals', 'slug': 'pets-animals', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'smile'},
    {'order': 39, 'name_bn': 'অনুষ্ঠান ও স্থানীয় কার্যক্রম', 'name_en': 'Local Events & Activities', 'slug': 'local-events-activities', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'calendar'},
    {'order': 40, 'name_bn': 'বিজ্ঞাপন ও প্রচার', 'name_en': 'Advertising & Promotion', 'slug': 'advertising-promotion', 'kind': CategoryKind.PUBLIC_SERVICE_CATEGORY, 'icon': 'volume-2'},

    # 41-46: Governance, Security & Administrative System Domains
    {'order': 41, 'name_bn': 'মূল্যায়ন ও সুনাম', 'name_en': 'Reviews & Reputation', 'slug': 'reviews-reputation', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'star'},
    {'order': 42, 'name_bn': 'বিজ্ঞপ্তি', 'name_en': 'Notices & Announcements', 'slug': 'notices-announcements', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'bell'},
    {'order': 43, 'name_bn': 'সহায়তা ও অভিযোগ', 'name_en': 'Help & Support', 'slug': 'help-support', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'phone'},
    {'order': 44, 'name_bn': 'প্রশাসন ও নিরাপত্তা', 'name_en': 'Administration & Security', 'slug': 'administration-security', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'shield'},
    {'order': 45, 'name_bn': 'তথ্য ও প্রতিবেদন', 'name_en': 'Reports & Analytics', 'slug': 'reports-analytics', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'file-text'},
    {'order': 46, 'name_bn': 'সিস্টেম ও নিরাপত্তা', 'name_en': 'System & Platform Settings', 'slug': 'system-platform-settings', 'kind': CategoryKind.SYSTEM_DOMAIN, 'icon': 'settings'},
]
