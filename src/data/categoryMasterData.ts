// SebaCox Master Taxonomy Version 1.0 (31 Master Categories & Granular Sub-categories)
// Centralized schema and master data synchronized with backend database foundation

export interface MasterSubCategory {
  id: number;
  categoryId: number;
  nameBn: string;
  nameEn: string;
  slug: string;
  sortOrder: number;
  isActive: boolean;
  isPopular?: boolean;
}

export interface MasterCategory {
  id: number;
  nameBn: string;
  nameEn: string;
  slug: string;
  icon: string;
  descriptionBn: string;
  descriptionEn: string;
  sortOrder: number;
  isActive: boolean;
  isFeatured: boolean;
  isPopular?: boolean;
  subCategories: MasterSubCategory[];
}

export const SEBACOX_MASTER_CATEGORIES: MasterCategory[] = [
  // 01. নির্মাণ ও প্রকৌশল
  {
    id: 1,
    nameBn: 'নির্মাণ ও প্রকৌশল',
    nameEn: 'Construction & Engineering',
    slug: 'construction-engineering',
    icon: 'hammer',
    descriptionBn: 'ইট, বালু, সিমেন্ট সরবরাহ, নির্মাণ শ্রমিক ও মিস্ত্রি (রাজমিস্ত্রি, ঢালাই), রং, প্লাম্বিং ও আর্কিটেকচারাল প্ল্যানিং',
    descriptionEn: 'Civil construction, masonry, engineering design, plumbing, painting and building materials',
    sortOrder: 1,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 101, categoryId: 1, nameBn: 'নির্মাণ সামগ্রী সরবরাহ (ইট, বালু, রড, সিমেন্ট)', nameEn: 'Construction Materials Supply', slug: 'construction-materials-supply', sortOrder: 1, isActive: true },
      { id: 102, categoryId: 1, nameBn: 'নির্মাণ শ্রমিক ও মিস্ত্রি (রাজমিস্ত্রি ও ঢালাই)', nameEn: 'Masonry, Rod Binding & Casting Labour', slug: 'masonry-casting-labour', sortOrder: 2, isActive: true },
      { id: 103, categoryId: 1, nameBn: 'টাইলস, মার্বেল ও গ্রানাইট ফিটিং', nameEn: 'Tiles, Marble & Granite Fitting', slug: 'tiles-marble-fitting', sortOrder: 3, isActive: true },
      { id: 104, categoryId: 1, nameBn: 'রং মিস্ত্রি ও ওয়াল পুটি', nameEn: 'Painting & Wall Putty', slug: 'painting-wall-putty', sortOrder: 4, isActive: true },
      { id: 105, categoryId: 1, nameBn: 'প্লাম্বিং ও পাইপলাইন ফিটিং', nameEn: 'Plumbing & Pipeline Fitting', slug: 'plumbing-pipeline-fitting', sortOrder: 5, isActive: true },
      { id: 106, categoryId: 1, nameBn: 'আর্কিটেক্ট, সিভিল ইঞ্জিনিয়ার ও বিল্ডিং প্ল্যান', nameEn: 'Architectural & Civil Engineering Design', slug: 'architect-civil-engineering', sortOrder: 6, isActive: true },
      { id: 107, categoryId: 1, nameBn: 'মাটি কাটা, পাইলিং ও ভরাট কাজ', nameEn: 'Piling, Soil Excavation & Earthwork', slug: 'piling-earthwork', sortOrder: 7, isActive: true },
      { id: 108, categoryId: 1, nameBn: 'গ্রিল, থাই অ্যালুমিনিয়াম ও গ্লাস ওয়ার্ক', nameEn: 'Grill, Thai Aluminum & Glass Work', slug: 'grill-thai-aluminum-glass', sortOrder: 8, isActive: true },
      { id: 109, categoryId: 1, nameBn: 'ইন্টেরিয়র ডিজাইন ও ডেকোরেশন', nameEn: 'Interior Design & Decoration', slug: 'interior-design-decoration', sortOrder: 9, isActive: true },
      { id: 110, categoryId: 1, nameBn: 'ভারী নির্মাণ যন্ত্রপাতি ভাড়া (মিক্সার, ক্রেন)', nameEn: 'Heavy Construction Machinery Rental', slug: 'construction-machinery-rental', sortOrder: 10, isActive: true },
    ]
  },

  // 02. বাসাবাড়ি ও অফিস রক্ষণাবেক্ষণ
  {
    id: 2,
    nameBn: 'বাসাবাড়ি ও অফিস রক্ষণাবেক্ষণ',
    nameEn: 'Home & Office Maintenance',
    slug: 'home-office-maintenance',
    icon: 'wrench',
    descriptionBn: 'ইলেকট্রিশিয়ান, এসি, ফ্রিজ, ওয়াশিং মেশিন, গ্যাস স্টোভ, পানির পাম্প ও হোম অ্যাপ্লায়েন্স মেরামত',
    descriptionEn: 'Electrician, AC, refrigerator, washing machine, stove and home appliance repairs',
    sortOrder: 2,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 201, categoryId: 2, nameBn: 'ইলেকট্রিশিয়ান ও হাউস ওয়্যারিং', nameEn: 'Electrician & House Wiring', slug: 'electrician-house-wiring', sortOrder: 1, isActive: true },
      { id: 202, categoryId: 2, nameBn: 'এসি সার্ভিসিং, গ্যাস চার্জ ও মেরামত', nameEn: 'AC Servicing & Gas Charge', slug: 'ac-servicing-gas-charge', sortOrder: 2, isActive: true },
      { id: 203, categoryId: 2, nameBn: 'ফ্রিজ ও রেফ্রিজারেটর মেরামত', nameEn: 'Refrigerator & Deep Freezer Repair', slug: 'fridge-freezer-repair', sortOrder: 3, isActive: true },
      { id: 204, categoryId: 2, nameBn: 'ওয়াশিং মেশিন ও ড্রায়ার সার্ভিসিং', nameEn: 'Washing Machine Repair', slug: 'washing-machine-repair', sortOrder: 4, isActive: true },
      { id: 205, categoryId: 2, nameBn: 'পানির পাম্প ও মোটর সার্ভিস', nameEn: 'Water Pump & Motor Repair', slug: 'water-pump-motor-repair', sortOrder: 5, isActive: true },
      { id: 206, categoryId: 2, nameBn: 'গ্যাস স্টোভ, ওভেন ও গিজার মেরামত', nameEn: 'Gas Stove, Oven & Geyser Repair', slug: 'gas-stove-oven-geyser', sortOrder: 6, isActive: true },
      { id: 207, categoryId: 2, nameBn: 'আইপিএস, ইউপিএস ও সোলার মেরামত', nameEn: 'IPS, UPS & Solar Battery Repair', slug: 'ips-ups-solar-repair', sortOrder: 7, isActive: true },
      { id: 208, categoryId: 2, nameBn: 'টিভি ও হোম অডিও সিস্টেম সার্ভিসিং', nameEn: 'TV & Audio System Repair', slug: 'tv-audio-repair', sortOrder: 8, isActive: true },
      { id: 209, categoryId: 2, nameBn: 'কাঠমিস্ত্রি ও ফার্নিচার মেরামত/বার্নিশ', nameEn: 'Carpentry, Furniture Repair & Polish', slug: 'carpentry-furniture-repair', sortOrder: 9, isActive: true },
    ]
  },

  // 03. পরিষ্কার-পরিচ্ছন্নতা ও রক্ষণাবেক্ষণ
  {
    id: 3,
    nameBn: 'পরিষ্কার-পরিচ্ছন্নতা ও রক্ষণাবেক্ষণ',
    nameEn: 'Cleaning & Housekeeping',
    slug: 'cleaning-housekeeping',
    icon: 'sparkles',
    descriptionBn: 'বাসা-অফিস ডিপ ক্লিনিং, সোফা কার্পেট ওয়াশ, পানির ট্যাংক পরিষ্কার ও পেস্ট কন্ট্রোল',
    descriptionEn: 'Deep cleaning, carpet wash, water tank sanitation and pest control',
    sortOrder: 3,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 301, categoryId: 3, nameBn: 'বাসা-বাড়ি ও ফ্ল্যাট ডিপ ক্লিনিং', nameEn: 'Home Deep Cleaning', slug: 'home-deep-cleaning', sortOrder: 1, isActive: true },
      { id: 302, categoryId: 3, nameBn: 'অফিস, শোরুম ও রেস্তোরাঁ ক্লিনিং', nameEn: 'Commercial & Office Cleaning', slug: 'commercial-office-cleaning', sortOrder: 2, isActive: true },
      { id: 303, categoryId: 3, nameBn: 'সোফা, জাজিম ও কার্পেট ওয়াশ', nameEn: 'Sofa, Mattress & Carpet Wash', slug: 'sofa-carpet-wash', sortOrder: 3, isActive: true },
      { id: 304, categoryId: 3, nameBn: 'পানির ট্যাংক ও আন্ডারগ্রাউন্ড রিজার্ভার ওয়াশ', nameEn: 'Water Tank & Reservoir Wash', slug: 'water-tank-reservoir-wash', sortOrder: 4, isActive: true },
      { id: 305, categoryId: 3, nameBn: 'পোকামাকড় ও পেস্ট কন্ট্রোল সার্ভিস', nameEn: 'Pest Control & Termite Treatment', slug: 'pest-control-treatment', sortOrder: 5, isActive: true },
      { id: 306, categoryId: 3, nameBn: 'সেপটিক ট্যাংক ও ড্রেনেজ ক্লিনিং', nameEn: 'Septic Tank & Drainage Cleaning', slug: 'septic-tank-drainage-cleaning', sortOrder: 6, isActive: true },
      { id: 307, categoryId: 3, nameBn: 'গ্লাস ও হাই-রাইজ বিল্ডিং এক্সটেরিয়র ক্লিনিং', nameEn: 'Exterior Glass & Facade Cleaning', slug: 'facade-glass-cleaning', sortOrder: 7, isActive: true },
    ]
  },

  // 04. পরিবহন ও লজিস্টিকস
  {
    id: 4,
    nameBn: 'পরিবহন ও লজিস্টিকস',
    nameEn: 'Transport & Logistics',
    slug: 'transport-logistics',
    icon: 'truck',
    descriptionBn: 'বাসা শিফটিং, অফিস শিফটিং, ভারী মালামাল পরিবহন ও লোডিং লেবার',
    descriptionEn: 'House shifting, cargo transport, heavy logistics and loading labours',
    sortOrder: 4,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 401, categoryId: 4, nameBn: 'বাসা-বাড়ি বদল ও অফিস শিফটিং', nameEn: 'House & Office Shifting', slug: 'house-office-shifting', sortOrder: 1, isActive: true },
      { id: 402, categoryId: 4, nameBn: 'পিকআপ ও মিনি ট্রাক ভাড়া (মালামাল)', nameEn: 'Pickup & Mini Truck Rental (Cargo)', slug: 'pickup-mini-truck-cargo', sortOrder: 2, isActive: true },
      { id: 403, categoryId: 4, nameBn: 'বড় ট্রাক, কভার্ড ভ্যান ও ট্রেইলার ভাড়া', nameEn: 'Heavy Truck & Covered Van Rental', slug: 'heavy-truck-covered-van', sortOrder: 3, isActive: true },
      { id: 404, categoryId: 4, nameBn: 'মালামাল লোডিং ও আনলোডিং শ্রমিক (লেবার)', nameEn: 'Loading & Unloading Labour', slug: 'loading-unloading-labour', sortOrder: 4, isActive: true },
      { id: 405, categoryId: 4, nameBn: 'হিমাগার পরিবহন ও কোল্ড চেইন লজিস্টিকস', nameEn: 'Cold Storage & Refrigerated Transport', slug: 'cold-chain-transport', sortOrder: 5, isActive: true },
    ]
  },

  // 05. গাড়ি ও যানবাহন ভাড়া
  {
    id: 5,
    nameBn: 'গাড়ি ও যানবাহন ভাড়া',
    nameEn: 'Vehicle Rental & Fleet',
    slug: 'vehicle-rental-fleet',
    icon: 'car',
    descriptionBn: 'প্রাইভেট কার, মাইক্রোবাস, পর্যটক জিপ (চান্দের গাড়ি), মোটরসাইকেল ও স্কুটি ভাড়া',
    descriptionEn: 'Private car, microbus, tourist jeep (Chander Gari), bike and scooter rental',
    sortOrder: 5,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 501, categoryId: 5, nameBn: 'প্রাইভেট কার ও সিডান রেন্টাল', nameEn: 'Private Sedan Car Rental', slug: 'sedan-car-rental', sortOrder: 1, isActive: true },
      { id: 502, categoryId: 5, nameBn: 'মাইক্রোবাস ও হাইস রেন্টাল (গ্রুপ ভ্রমণ)', nameEn: 'Microbus & Hiace Rental', slug: 'microbus-hiace-rental', sortOrder: 2, isActive: true },
      { id: 503, categoryId: 5, nameBn: 'পর্যটক জিপ ও চাঁন্দের গাড়ি ভাড়া', nameEn: 'Tourist Open Jeep (Chander Gari)', slug: 'tourist-jeep-chander-gari', sortOrder: 3, isActive: true },
      { id: 504, categoryId: 5, nameBn: 'মোটরসাইকেল ও স্কুটি ভাড়া (দৈনিক/সাপ্তাহিক)', nameEn: 'Motorbike & Scooter Daily Rental', slug: 'motorbike-scooter-rental', sortOrder: 4, isActive: true },
      { id: 505, categoryId: 5, nameBn: 'টুরিস্ট বাস ও মিনিবাস রিজার্ভ', nameEn: 'Tourist Bus & Minibus Reserve', slug: 'tourist-bus-reserve', sortOrder: 5, isActive: true },
      { id: 506, categoryId: 5, nameBn: 'সিএনজি ও ব্যাটারি অটো-রিকশা রিজার্ভ', nameEn: 'CNG & TomTom Reserve Trip', slug: 'cng-tomtom-reserve', sortOrder: 6, isActive: true },
      { id: 507, categoryId: 5, nameBn: 'স্পিডবোট ও ওয়াটার ট্যাক্সি রিজার্ভেশন', nameEn: 'Speedboat & Water Taxi Booking', slug: 'speedboat-water-taxi', sortOrder: 7, isActive: true },
      { id: 508, categoryId: 5, nameBn: 'পেশাদার ড্রাইভার ভাড়া (ব্যক্তিগত/ট্রিপ)', nameEn: 'Professional On-Demand Driver', slug: 'ondemand-driver-service', sortOrder: 8, isActive: true },
    ]
  },

  // 06. অটোমোবাইল ও গ্যারেজ সেবা
  {
    id: 6,
    nameBn: 'অটোমোবাইল ও গ্যারেজ সেবা',
    nameEn: 'Automobile & Garage Services',
    slug: 'automobile-garage-services',
    icon: 'disc',
    descriptionBn: 'অন-রোড কার ব্রেকডাউন মেকানিক, বাইক সার্ভিসিং, ডেন্টিং-পেইন্টিং ও কার ওয়াশ',
    descriptionEn: 'On-road breakdown assistance, bike servicing, car denting-painting and car wash',
    sortOrder: 6,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 601, categoryId: 6, nameBn: 'জরুরি অন-রোড কার ব্রেকডাউন মেকানিক', nameEn: 'Emergency On-Road Car Breakdown', slug: 'emergency-roadside-assistance', sortOrder: 1, isActive: true },
      { id: 602, categoryId: 6, nameBn: 'মোটরসাইকেল মেকানিক ও টিউনিং', nameEn: 'Motorbike Repair & Tuning', slug: 'motorbike-repair-tuning', sortOrder: 2, isActive: true },
      { id: 603, categoryId: 6, nameBn: 'কার অটো ডেন্টিং, পেইন্টিং ও বডি ওয়ার্ক', nameEn: 'Car Auto Denting & Body Painting', slug: 'car-denting-painting', sortOrder: 3, isActive: true },
      { id: 604, categoryId: 6, nameBn: 'কার এসি ও অটো ইলেকট্রিক্যাল মেরামত', nameEn: 'Car AC & Auto Electrical Repair', slug: 'car-ac-electrical-repair', sortOrder: 4, isActive: true },
      { id: 605, categoryId: 6, nameBn: 'টায়ার পাংচার, হুইল এলাইনমেন্ট ও ব্যালেন্সিং', nameEn: 'Tyre Puncture & Wheel Alignment', slug: 'tyre-wheel-alignment', sortOrder: 5, isActive: true },
      { id: 606, categoryId: 6, nameBn: 'অটো মোবাইল কার ওয়াশ ও পলিশিং', nameEn: 'Auto Car Wash & Detailing', slug: 'auto-car-wash-detailing', sortOrder: 6, isActive: true },
      { id: 607, categoryId: 6, nameBn: 'গাড়ি টোয়িং ও রিকভারি সার্ভিস', nameEn: 'Vehicle Towing & Recovery', slug: 'vehicle-towing-recovery', sortOrder: 7, isActive: true },
    ]
  },

  // 07. স্বাস্থ্য ও চিকিৎসা সেবা
  {
    id: 7,
    nameBn: 'স্বাস্থ্য ও চিকিৎসা সেবা',
    nameEn: 'Health & Medical Services',
    slug: 'health-medical-services',
    icon: 'activity',
    descriptionBn: 'বিশেষজ্ঞ ডাক্তার কনসালটেশন, হোম নার্সিং, ফিজিওথেরাপিস্ট ও ডায়াগনস্টিক টেস্ট',
    descriptionEn: 'Specialist doctors, home nursing, physiotherapy, diagnostic tests and elder care',
    sortOrder: 7,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 701, categoryId: 7, nameBn: 'বিশেষজ্ঞ ডাক্তার অ্যাপয়েন্টমেন্ট ও কনসালটেন্সি', nameEn: 'Specialist Doctor Appointments', slug: 'specialist-doctor-appointment', sortOrder: 1, isActive: true },
      { id: 702, categoryId: 7, nameBn: 'হোম নার্সিং ও বয়োবৃদ্ধ রোগীর সেবা', nameEn: 'Home Nursing & Elderly Care', slug: 'home-nursing-elderly-care', sortOrder: 2, isActive: true },
      { id: 703, categoryId: 7, nameBn: 'হোম ফিজিওথেরাপি ও রিহ্যাবিলিটেশন', nameEn: 'Home Physiotherapy Service', slug: 'home-physiotherapy-service', sortOrder: 3, isActive: true },
      { id: 704, categoryId: 7, nameBn: 'হোম ডায়াগনস্টিক ও ল্যাব স্যাম্পল কালেকশন', nameEn: 'Diagnostic Sample Collection at Home', slug: 'home-diagnostic-sample-collection', sortOrder: 4, isActive: true },
      { id: 705, categoryId: 7, nameBn: 'জরুরি অক্সিজেন সিলিন্ডার হোম ডেলিভারি', nameEn: 'Emergency Oxygen Cylinder Delivery', slug: 'oxygen-cylinder-delivery', sortOrder: 5, isActive: true },
      { id: 706, categoryId: 7, nameBn: 'মেডিকেল ইকুইপমেন্ট ও বেড ভাড়া', nameEn: 'Medical Equipment & Hospital Bed Rental', slug: 'medical-equipment-rental', sortOrder: 6, isActive: true },
      { id: 707, categoryId: 7, nameBn: 'ডেন্টাল কেয়ার ও হোম ডেন্টিস্ট্রি', nameEn: 'Dental Consultation & Oral Care', slug: 'dental-consultation-care', sortOrder: 7, isActive: true },
    ]
  },

  // 08. পর্যটন, হোটেল ও রিসোর্ট
  {
    id: 8,
    nameBn: 'পর্যটন, হোটেল ও রিসোর্ট',
    nameEn: 'Tourism, Hotels & Resorts',
    slug: 'tourism-hotels-resorts',
    icon: 'compass',
    descriptionBn: 'হোটেল রুম বুকিং, বিচ রিসোর্ট, সেন্টমার্টিন শিপ টিকিট, ট্যুর গাইড ও ক্যাম্পিং',
    descriptionEn: 'Hotel booking, beach resort, Saint Martin ship ticket, tourist guide and camping',
    sortOrder: 8,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 801, categoryId: 8, nameBn: 'হোটেল, মোটেল ও বিচ রিসোর্ট রুম বুকিং', nameEn: 'Hotel, Motel & Beach Resort Booking', slug: 'hotel-resort-booking', sortOrder: 1, isActive: true },
      { id: 802, categoryId: 8, nameBn: 'সেন্টমার্টিন ও কুশিয়ারা ক্রুজ শিপ টিকিট', nameEn: 'Saint Martin Cruise Ship Ticket', slug: 'saint-martin-cruise-ticket', sortOrder: 2, isActive: true },
      { id: 803, categoryId: 8, nameBn: 'সার্টিফাইড লোকাল ট্যুর গাইড', nameEn: 'Certified Local Tourist Guide', slug: 'certified-tourist-guide', sortOrder: 3, isActive: true },
      { id: 804, categoryId: 8, nameBn: 'বিচ অ্যাক্টিভিটি, সার্ফিং ও ওয়াটার স্পোর্টস', nameEn: 'Surfing, Jet Ski & Beach Activities', slug: 'beach-activities-watersports', sortOrder: 4, isActive: true },
      { id: 805, categoryId: 8, nameBn: 'ক্যাম্পিং গিয়ার, তাঁবু ভাড়া ও বারবিকিউ সেটআপ', nameEn: 'Camping Tent & BBQ Setup Rental', slug: 'camping-bbq-rental', sortOrder: 5, isActive: true },
      { id: 806, categoryId: 8, nameBn: 'কক্সবাজার কাস্টমাইজড ডে-ট্যুর ও সাফারি ট্রিপ', nameEn: 'Custom Day Tours & Safari Trip', slug: 'custom-day-tours-safari', sortOrder: 6, isActive: true },
      { id: 807, categoryId: 8, nameBn: 'ফটোগ্রাফি ও বিচ ড্রোন শুট প্যাকেজ', nameEn: 'Tourist Beach & Drone Photography', slug: 'tourist-drone-photography', sortOrder: 7, isActive: true },
    ]
  },

  // 09. তথ্য ও জরুরি সেবা
  {
    id: 9,
    nameBn: 'তথ্য ও জরুরি সেবা',
    nameEn: 'Emergency & Public Information',
    slug: 'emergency-public-information',
    icon: 'phone',
    descriptionBn: 'জরুরি অ্যাম্বুলেন্স, ব্লাড ডোনার ডিরেক্টরি, ফায়ার সার্ভিস, থানা ও বিদ্যুৎ হেল্পলাইন',
    descriptionEn: 'Ambulance service, blood donors, fire service, police and electricity helpline',
    sortOrder: 9,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 901, categoryId: 9, nameBn: 'জরুরি অ্যাম্বুলেন্স (আইসিইউ ও নরমাল)', nameEn: 'Emergency Ambulance (ICU & Normal)', slug: 'emergency-ambulance-service', sortOrder: 1, isActive: true },
      { id: 902, categoryId: 9, nameBn: 'জরুরি রক্তদাতা ও ব্লাড ব্যাংক ডিরেক্টরি', nameEn: 'Blood Donors & Blood Bank Directory', slug: 'blood-donor-directory', sortOrder: 2, isActive: true },
      { id: 903, categoryId: 9, nameBn: 'ফায়ার সার্ভিস ও সিভিল ডিফেন্স কক্সবাজার', nameEn: 'Fire Service & Civil Defense Helpline', slug: 'fire-service-helpline', sortOrder: 3, isActive: true },
      { id: 904, categoryId: 9, nameBn: 'পুলিশ স্টেশন ও ট্যুরিস্ট পুলিশ কক্সবাজার', nameEn: 'Police & Tourist Police Helpline', slug: 'police-tourist-police-helpline', sortOrder: 4, isActive: true },
      { id: 905, categoryId: 9, nameBn: 'পল্লী বিদ্যুৎ ও পিডিবি বিদ্যুৎ অভিযোগ কেন্দ্র', nameEn: 'Electricity Complaint Center (Palli Bidyut)', slug: 'electricity-complaint-center', sortOrder: 5, isActive: true },
      { id: 906, categoryId: 9, nameBn: 'ওয়াসা ও পানির লাইন জরুরি সমস্যা কেন্দ্র', nameEn: 'WASA & Drinking Water Supply Support', slug: 'wasa-water-supply-support', sortOrder: 6, isActive: true },
      { id: 907, categoryId: 9, nameBn: 'উপজেলা ও জেলা হাসপাতাল ইমার্জেন্সি ডেস্ক', nameEn: 'District Hospital Emergency Helpline', slug: 'hospital-emergency-helpline', sortOrder: 7, isActive: true },
    ]
  },

  // 10. শিক্ষা, শিক্ষক ও প্রশিক্ষণ
  {
    id: 10,
    nameBn: 'শিক্ষা, শিক্ষক ও প্রশিক্ষণ',
    nameEn: 'Education, Tutoring & Training',
    slug: 'education-tutoring-training',
    icon: 'book',
    descriptionBn: 'হোম টিউটর, কোরআন ও ধর্মীয় শিক্ষক, স্পোকেন ইংলিশ, কম্পিউটার ও ড্রাইভিং স্কুল',
    descriptionEn: 'Home tutors, Quran teacher, spoken English, computer courses and driving school',
    sortOrder: 10,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 1001, categoryId: 10, nameBn: 'হোম টিউটর (ক্লাস ১-১২ ও একাডেমিক)', nameEn: 'Academic Home Tutors', slug: 'academic-home-tutors', sortOrder: 1, isActive: true },
      { id: 1002, categoryId: 10, nameBn: 'কোরআন শিক্ষা ও ধর্মীয় শিক্ষক', nameEn: 'Quran & Religious Education', slug: 'quran-religious-education', sortOrder: 2, isActive: true },
      { id: 1003, categoryId: 10, nameBn: 'স্পোকেন ইংলিশ ও আইইএলটিএস ট্রেইনার', nameEn: 'Spoken English & IELTS Trainer', slug: 'spoken-english-ielts-trainer', sortOrder: 3, isActive: true },
      { id: 1004, categoryId: 10, nameBn: 'কম্পিউটার স্কিল ও গ্রাফিক্স ট্রেইনার', nameEn: 'Computer & IT Skills Training', slug: 'computer-it-skills-training', sortOrder: 4, isActive: true },
      { id: 1005, categoryId: 10, nameBn: 'ড্রাইভিং প্রশিক্ষণ স্কুল ও প্রশিক্ষক', nameEn: 'Driving Training School & Instructor', slug: 'driving-training-school', sortOrder: 5, isActive: true },
      { id: 1006, categoryId: 10, nameBn: 'গান, আবৃত্তি ও চিত্রাঙ্কন শিক্ষক', nameEn: 'Music, Art & Recitation Teacher', slug: 'music-art-recitation-teacher', sortOrder: 6, isActive: true },
    ]
  },

  // 11. অনুষ্ঠান, বিবাহ ও ক্যাটারিং
  {
    id: 11,
    nameBn: 'অনুষ্ঠান, বিবাহ ও ক্যাটারিং',
    nameEn: 'Events, Wedding & Catering',
    slug: 'events-wedding-catering',
    icon: 'calendar',
    descriptionBn: 'কমিউনিটি সেন্টার, ওয়েডিং ইভেন্ট প্ল্যানার, বাবুর্চি ও ক্যাটারিং, স্টেজ ডেকোরেশন ও সাউন্ড',
    descriptionEn: 'Community center, wedding planner, chef & catering, stage decoration and sound system',
    sortOrder: 11,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 1101, categoryId: 11, nameBn: 'কমিউনিটি সেন্টার ও কনভেনশন হল বুকিং', nameEn: 'Community Center & Convention Hall', slug: 'community-center-booking', sortOrder: 1, isActive: true },
      { id: 1102, categoryId: 11, nameBn: 'ওয়েডিং ও ইভেন্ট ম্যানেজমেন্ট টিম', nameEn: 'Wedding & Event Planners', slug: 'wedding-event-planners', sortOrder: 2, isActive: true },
      { id: 1103, categoryId: 11, nameBn: 'বাবুর্চি ও ইভেন্ট ক্যাটারিং সার্ভিস', nameEn: 'Traditional Chef & Catering Service', slug: 'traditional-chef-catering', sortOrder: 3, isActive: true },
      { id: 1104, categoryId: 11, nameBn: 'স্টেজ ডেকোরেশন ও লাইটিং সেটআপ', nameEn: 'Stage Decoration & Floral Setup', slug: 'stage-decoration-floral-setup', sortOrder: 4, isActive: true },
      { id: 1105, categoryId: 11, nameBn: 'সাউন্ড সিস্টেম ও ডিজে সেটআপ ভাড়া', nameEn: 'Sound System & DJ Setup Rental', slug: 'sound-system-dj-rental', sortOrder: 5, isActive: true },
      { id: 1106, categoryId: 11, nameBn: 'ওয়েডিং ও ইভেন্ট ফটোগ্রাফি / সিনেমাটোগ্রাফি', nameEn: 'Wedding Photography & Cinematography', slug: 'wedding-photography-cinematography', sortOrder: 6, isActive: true },
    ]
  },

  // 12. রিয়েল এস্টেট ও প্রোপার্টি
  {
    id: 12,
    nameBn: 'রিয়েল এস্টেট ও প্রোপার্টি',
    nameEn: 'Real Estate & Properties',
    slug: 'real-estate-properties',
    icon: 'home',
    descriptionBn: 'বাসা ভাড়া (ফ্যামিলি/ব্যাচেলর), কমার্শিয়াল দোকান/অফিস স্পেস ও জমি ক্রয়-বিক্রয়',
    descriptionEn: 'To-let family flat, bachelor room, commercial shop/office and land purchase',
    sortOrder: 12,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 1201, categoryId: 12, nameBn: 'বাসা ও ফ্ল্যাট ভাড়া (ফ্যামিলি বাসা)', nameEn: 'To-Let Family Flat & Apartment', slug: 'tolet-family-flat-apartment', sortOrder: 1, isActive: true },
      { id: 1202, categoryId: 12, nameBn: 'ব্যাচেলর ও মেস রুম ভাড়া', nameEn: 'Bachelor & Sublet Room To-Let', slug: 'bachelor-sublet-room', sortOrder: 2, isActive: true },
      { id: 1203, categoryId: 12, nameBn: 'দোকান, শোরুম ও কমার্শিয়াল অফিস স্পেস ভাড়া', nameEn: 'Commercial Shop & Office Space', slug: 'commercial-shop-office-space', sortOrder: 3, isActive: true },
      { id: 1204, categoryId: 12, nameBn: 'জমি, প্লট ও প্রোপার্টি ক্রয়-বিক্রয়', nameEn: 'Land & Plot Buy-Sale', slug: 'land-plot-buy-sale', sortOrder: 4, isActive: true },
      { id: 1205, categoryId: 12, nameBn: 'প্রোপার্টি কেয়ারটেকার ও লিগ্যাল ভেরিফিকেশন', nameEn: 'Property Caretaker & Title Verification', slug: 'property-title-verification', sortOrder: 5, isActive: true },
    ]
  },

  // 13. আইনি ও প্রফেশনাল কনসালটেন্সি
  {
    id: 13,
    nameBn: 'আইনি ও প্রফেশনাল কনসালটেন্সি',
    nameEn: 'Legal & Professional Consultancy',
    slug: 'legal-professional-consultancy',
    icon: 'shield',
    descriptionBn: 'আইনজীবী ও অ্যাডভোকেট, দলিল লেখক ও নোটারি, অডিট ও ইনকাম ট্যাক্স কনসালটেন্ট',
    descriptionEn: 'Advocate & lawyer, deed writer & notary, audit, trade license and tax consultant',
    sortOrder: 13,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 1301, categoryId: 13, nameBn: 'আইনজীবী ও অ্যাডভোকেট আইনি পরামর্শ', nameEn: 'Advocate & Legal Consultation', slug: 'advocate-legal-consultation', sortOrder: 1, isActive: true },
      { id: 1302, categoryId: 13, nameBn: 'দলিল লেখক, নোটারি পাবলিক ও স্ট্যাম্প ভেন্ডার', nameEn: 'Deed Writer & Notary Public', slug: 'deed-writer-notary-public', sortOrder: 2, isActive: true },
      { id: 1303, categoryId: 13, nameBn: 'ইনকাম ট্যাক্স, ভ্যাট ও অডিট কনসালটেন্ট', nameEn: 'Income Tax, VAT & Audit Consultant', slug: 'tax-vat-audit-consultant', sortOrder: 3, isActive: true },
      { id: 1304, categoryId: 13, nameBn: 'ট্রেড লাইসেন্স ও বিজনেস রেজিস্ট্রেশন সেবা', nameEn: 'Trade License & Company Registration', slug: 'trade-license-registration', sortOrder: 4, isActive: true },
    ]
  },

  // 14. আর্থিক ও ব্যাংকিং সেবা
  {
    id: 14,
    nameBn: 'আর্থিক ও ব্যাংকিং সেবা',
    nameEn: 'Financial & Banking Services',
    slug: 'financial-banking-services',
    icon: 'credit-card',
    descriptionBn: 'বিকাশ/নগদ এজেন্ট পয়েন্ট, মানি এক্সচেঞ্জ ও এটিএম বুথ লোকেশন গাইড',
    descriptionEn: 'Agent banking point, currency exchange and ATM booth location guide',
    sortOrder: 14,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 1401, categoryId: 14, nameBn: 'এজেন্ট ব্যাংকিং ও ক্যাশ পয়েন্ট ডিরেক্টরি', nameEn: 'Agent Banking & Cash Point Guide', slug: 'agent-banking-cash-point', sortOrder: 1, isActive: true },
      { id: 1402, categoryId: 14, nameBn: 'অনুমোদিত মানি এক্সচেঞ্জ ও মুদ্রা বিনিময়', nameEn: 'Authorized Currency Exchange', slug: 'authorized-currency-exchange', sortOrder: 2, isActive: true },
      { id: 1403, categoryId: 14, nameBn: 'এটিএম বুথ ও ব্যাংক শাখা তথ্য কেন্দ্র', nameEn: 'ATM Booth & Bank Branch Information', slug: 'atm-bank-branch-info', sortOrder: 3, isActive: true },
    ]
  },

  // 15. কৃষি, মৎস্য ও পশুপালন
  {
    id: 15,
    nameBn: 'কৃষি, মৎস্য ও পশুপালন',
    nameEn: 'Agriculture, Fisheries & Livestock',
    slug: 'agriculture-fisheries-livestock',
    icon: 'leaf',
    descriptionBn: 'হাঁস-মুরগি ও গবাদিপশু চিকিৎসা, মৎস্য চাষ পরামর্শ, পান-সুপারি ও বীজ-সার সরবরাহ',
    descriptionEn: 'Veterinary doctor, fisheries guidance, betel-leaf farm and seeds/fertilizer',
    sortOrder: 15,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 1501, categoryId: 15, nameBn: 'পশু চিকিৎসক (ভেটেরিনারি সার্জন)', nameEn: 'Veterinary Doctor (Livestock & Poultry)', slug: 'veterinary-doctor-service', sortOrder: 1, isActive: true },
      { id: 1502, categoryId: 15, nameBn: 'চিংড়ি ঘের ও আধুনিক মৎস্য চাষ পরামর্শ', nameEn: 'Shrimp Hatchery & Aquaculture Consulting', slug: 'shrimp-hatchery-aquaculture', sortOrder: 2, isActive: true },
      { id: 1503, categoryId: 15, nameBn: 'পান বরজ ও কৃষি রোগবালাই সমাধান', nameEn: 'Betel Leaf Farming & Agriculture Support', slug: 'betel-leaf-farming-support', sortOrder: 3, isActive: true },
      { id: 1504, categoryId: 15, nameBn: 'উন্নত জাতের বীজ, সার ও কীটনাশক সরবরাহ', nameEn: 'Quality Seeds, Fertilizer & Pesticides', slug: 'seeds-fertilizer-pesticides', sortOrder: 4, isActive: true },
      { id: 1505, categoryId: 15, nameBn: 'পাওয়ার টিলার ও সেচ পাম্প মেকানিক', nameEn: 'Tractor & Irrigation Pump Mechanic', slug: 'tractor-pump-mechanic', sortOrder: 5, isActive: true },
    ]
  },

  // 16. সামুদ্রিক মৎস্য ও শুঁটকি শিল্প
  {
    id: 16,
    nameBn: 'সামুদ্রিক মৎস্য ও শুঁটকি শিল্প',
    nameEn: 'Marine Fisheries & Dry Fish',
    slug: 'marine-fisheries-dry-fish',
    icon: 'anchor',
    descriptionBn: 'কক্সবাজার ট্র্যাডিশনাল শুঁটকি পাইকারি ও কুরিয়ার, ফ্রেশ সি-ফুড সরবরাহ ও ফিশিং বোট',
    descriptionEn: 'Coxs Bazar dry fish wholesale & courier, fresh sea fish supply and fishing boat repairs',
    sortOrder: 16,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 1601, categoryId: 16, nameBn: 'কক্সবাজার ট্র্যাডিশনাল শুঁটকি পাইকারি ও হোম ডেলিভারি', nameEn: 'Traditional Dry Fish Wholesale & Delivery', slug: 'dry-fish-wholesale-delivery', sortOrder: 1, isActive: true },
      { id: 1602, categoryId: 16, nameBn: 'তাজা সামুদ্রিক মাছ পাইকারি ও খুচরা সরবরাহ', nameEn: 'Fresh Marine Fish Supply', slug: 'fresh-marine-fish-supply', sortOrder: 2, isActive: true },
      { id: 1603, categoryId: 16, nameBn: 'ফিশিং ট্রলার ইঞ্জিন মেরামত ও ডকইয়ার্ড সেবা', nameEn: 'Fishing Trawler Engine & Dockyard Service', slug: 'fishing-trawler-dockyard', sortOrder: 3, isActive: true },
      { id: 1604, categoryId: 16, nameBn: 'ফিশিং নেট, রশি ও সামুদ্রিক ফিশিং সামগ্রী', nameEn: 'Fishing Net & Marine Accessories', slug: 'fishing-net-accessories', sortOrder: 4, isActive: true },
    ]
  },

  // 17. লবণ শিল্প ও বাণিজ্য
  {
    id: 17,
    nameBn: 'লবণ শিল্প ও বাণিজ্য',
    nameEn: 'Salt Industry & Trade',
    slug: 'salt-industry-trade',
    icon: 'layers',
    descriptionBn: 'অপরিশোধিত ক্রুড সল্ট উৎপাদন, আয়োডাইজড লবণ মিলিং ও লবণ পরিবহন লজিস্টিকস',
    descriptionEn: 'Crude salt production, iodized salt milling, wholesale and salt transport logistics',
    sortOrder: 17,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 1701, categoryId: 17, nameBn: 'অপরিশোধিত ক্রুড সল্ট (মাঠের লবণ) পাইকারি ক্রয়-বিক্রয়', nameEn: 'Crude Field Salt Wholesale', slug: 'crude-field-salt-wholesale', sortOrder: 1, isActive: true },
      { id: 1702, categoryId: 17, nameBn: 'আয়োডাইজড ও রিফাইন্ড লবণ মিলিং সাপ্লাই', nameEn: 'Iodized Refined Salt Supply', slug: 'iodized-salt-supply', sortOrder: 2, isActive: true },
      { id: 1703, categoryId: 17, nameBn: 'লবণ মাঠের পলিথিন ও ওয়াটার পাম্প সামগ্রী', nameEn: 'Salt Field Polythene & Water Pumps', slug: 'salt-field-accessories', sortOrder: 3, isActive: true },
      { id: 1704, categoryId: 17, nameBn: 'বাল্ক সল্ট কার্গো পরিবহন ও বোট চার্টার', nameEn: 'Bulk Salt Cargo Transport & Boat Charter', slug: 'bulk-salt-cargo-transport', sortOrder: 4, isActive: true },
    ]
  },

  // 18. স্থানীয় হস্তশিল্প ও কুটির শিল্প
  {
    id: 18,
    nameBn: 'স্থানীয় হস্তশিল্প ও কুটির শিল্প',
    nameEn: 'Local Handicrafts & Cottage Craft',
    slug: 'local-handicrafts-cottage-craft',
    icon: 'shopping-bag',
    descriptionBn: 'রাখাইন হস্তচালিত তাঁতবস্ত্র, ঝিনুক ও শামুকের হস্তশিল্প ও বাঁশ-বেতের ঐতিহ্যবাহী পণ্য',
    descriptionEn: 'Rakhine handloom fabrics, seashell ornaments, pearl jewelry and cane craft',
    sortOrder: 18,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 1801, categoryId: 18, nameBn: 'রাখাইন ঐতিহ্যবাহী তাঁতবস্ত্র ও লুঙ্গি', nameEn: 'Rakhine Traditional Handloom Fabrics', slug: 'rakhine-handloom-fabrics', sortOrder: 1, isActive: true },
      { id: 1802, categoryId: 18, nameBn: 'ঝিনুক, শামুক ও পার্ল জুয়েলারি কারুশিল্প', nameEn: 'Seashell & Pearl Handicrafts', slug: 'seashell-pearl-handicrafts', sortOrder: 2, isActive: true },
      { id: 1803, categoryId: 18, nameBn: 'বাঁশ, বেত ও পাটের পরিবেশবান্ধব পণ্য', nameEn: 'Bamboo, Cane & Jute Eco-Products', slug: 'bamboo-cane-jute-products', sortOrder: 3, isActive: true },
    ]
  },

  // 19. তথ্যপ্রযুক্তি ও ডিজিটাল সেবা
  {
    id: 19,
    nameBn: 'তথ্যপ্রযুক্তি ও ডিজিটাল সেবা',
    nameEn: 'IT & Digital Services',
    slug: 'it-digital-services',
    icon: 'cpu',
    descriptionBn: 'কম্পিউটার ও ল্যাপটপ মেরামত, সিসিটিভি ক্যামেরা ইনস্টলেশন, ওয়েব ডেভেলপমেন্ট ও প্রিন্টিং',
    descriptionEn: 'Computer repair, CCTV installation, WiFi networking, web development and printing',
    sortOrder: 19,
    isActive: true,
    isFeatured: true,
    isPopular: true,
    subCategories: [
      { id: 1901, categoryId: 19, nameBn: 'কম্পিউটার, ল্যাপটপ ও প্রিন্টার মেরামত', nameEn: 'Computer, Laptop & Printer Repair', slug: 'computer-laptop-printer-repair', sortOrder: 1, isActive: true },
      { id: 1902, categoryId: 19, nameBn: 'সিসিটিভি ক্যামেরা ইনস্টলেশন ও সিকিউরিটি', nameEn: 'CCTV Camera Installation & Security', slug: 'cctv-installation-security', sortOrder: 2, isActive: true },
      { id: 1903, categoryId: 19, nameBn: 'ওয়াইফাই রাউটার ও নেটওয়ার্ক সেটআপ', nameEn: 'WiFi Router & Local Networking', slug: 'wifi-networking-setup', sortOrder: 3, isActive: true },
      { id: 1904, categoryId: 19, nameBn: 'ওয়েবসাইট, সফটওয়্যার ও মোবাইল অ্যাপ ডেভেলপমেন্ট', nameEn: 'Web & Software Development', slug: 'web-software-development', sortOrder: 4, isActive: true },
      { id: 1905, categoryId: 19, nameBn: 'কম্পিউটার কম্পোজ, ফটোকপি ও ডিজিটাল প্রিন্টিং', nameEn: 'Document Composing & Color Printing', slug: 'document-composing-printing', sortOrder: 5, isActive: true },
    ]
  },

  // 20. ব্যক্তিগত যত্ন ও সৌন্দর্য সেবা
  {
    id: 20,
    nameBn: 'ব্যক্তিগত যত্ন ও সৌন্দর্য সেবা',
    nameEn: 'Personal Care & Beauty Services',
    slug: 'personal-care-beauty',
    icon: 'user-check',
    descriptionBn: 'লেডিস বিউটি পার্লার, হোম ব্রাইডাল মেকআপ, জেন্টস সেলুন ও স্কিন কেয়ার',
    descriptionEn: 'Ladies beauty parlor, home bridal makeup, gents salon, haircut and skincare',
    sortOrder: 20,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 2001, categoryId: 20, nameBn: 'লেডিস বিউটি পার্লার ও স্কিন কেয়ার', nameEn: 'Ladies Beauty Parlour & Skincare', slug: 'ladies-beauty-parlour', sortOrder: 1, isActive: true },
      { id: 2002, categoryId: 20, nameBn: 'হোম ব্রাইডাল ও পার্টি মেকআপ আর্টিস্ট', nameEn: 'Home Bridal & Party Makeup Artist', slug: 'home-bridal-makeup-artist', sortOrder: 2, isActive: true },
      { id: 2003, categoryId: 20, nameBn: 'জেন্টস সেলুন ও হোম হেয়ারকাট সার্ভিস', nameEn: 'Gents Hair Salon & Grooming', slug: 'gents-hair-salon-grooming', sortOrder: 3, isActive: true },
      { id: 2004, categoryId: 20, nameBn: 'মেহেদি ডিজাইন আর্টিস্ট (বিয়ে ও উৎসব)', nameEn: 'Mehndi & Henna Design Artist', slug: 'mehndi-henna-artist', sortOrder: 4, isActive: true },
    ]
  },

  // 21. দর্জি ও পোশাক সেবা
  {
    id: 21,
    nameBn: 'দর্জি ও পোশাক সেবা',
    nameEn: 'Tailoring & Garment Services',
    slug: 'tailoring-garment-services',
    icon: 'scissors',
    descriptionBn: 'লেডিস টেইলার্স ও বুটিক ড্রেস মেকিং, জেন্টস টেইলার্স, স্যুট কাটিং ও ড্রাই ক্লিনিং',
    descriptionEn: 'Ladies tailors, gents suiting & tailoring, alteration and laundry dry wash',
    sortOrder: 21,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 2101, categoryId: 21, nameBn: 'লেডিস টেইলার্স ও কাস্টম বুটিক মেকিং', nameEn: 'Ladies Tailors & Boutique Stitching', slug: 'ladies-tailors-boutique', sortOrder: 1, isActive: true },
      { id: 2102, categoryId: 21, nameBn: 'জেন্টস টেইলার্স ও স্যুট কাটিং', nameEn: 'Gents Tailors & Suit Stitching', slug: 'gents-tailors-suit-stitching', sortOrder: 2, isActive: true },
      { id: 2103, categoryId: 21, nameBn: 'পোশাক অলটারেশন ও রিকভারি', nameEn: 'Garment Alteration & Repair', slug: 'garment-alteration-repair', sortOrder: 3, isActive: true },
      { id: 2104, categoryId: 21, nameBn: 'লন্ড্রি ও ড্রাই ওয়াশ হোম পিকআপ', nameEn: 'Laundry & Dry Wash Home Pickup', slug: 'laundry-dry-wash-pickup', sortOrder: 4, isActive: true },
    ]
  },

  // 22. নিরাপত্তা ও নজরদারি সেবা
  {
    id: 22,
    nameBn: 'নিরাপত্তা ও নজরদারি সেবা',
    nameEn: 'Security & Surveillance Services',
    slug: 'security-surveillance-services',
    icon: 'lock',
    descriptionBn: 'পেশাদার সিকিউরিটি গার্ড সরবরাহ, বডিগার্ড ও ফায়ার সেফটি ইকুইপমেন্ট ইনস্টলেশন',
    descriptionEn: 'Security guard, bodyguard, fire extinguisher and access control systems',
    sortOrder: 22,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 2201, categoryId: 22, nameBn: 'পেশাদার সিকিউরিটি গার্ড সরবরাহ (বাসা/অফিস)', nameEn: 'Professional Security Guard Supply', slug: 'security-guard-supply', sortOrder: 1, isActive: true },
      { id: 2202, categoryId: 22, nameBn: 'ব্যক্তিগত দেহরক্ষী (বডিগার্ড) সার্ভিস', nameEn: 'Personal Bodyguard & VIP Escort', slug: 'personal-bodyguard-escort', sortOrder: 2, isActive: true },
      { id: 2203, categoryId: 22, nameBn: 'ফায়ার এক্সটিংগুইশার রিফিল ও অগ্নি নির্বাপক ব্যবস্থা', nameEn: 'Fire Extinguisher Refill & Safety Setup', slug: 'fire-extinguisher-safety', sortOrder: 3, isActive: true },
      { id: 2204, categoryId: 22, nameBn: 'বায়োমেট্রিক ও ডিজিটাল অ্যাক্সেস কন্ট্রোল সেটআপ', nameEn: 'Biometric & Smart Access Control', slug: 'biometric-access-control', sortOrder: 4, isActive: true },
    ]
  },

  // 23. প্রচার, প্রিন্টিং ও সাইনবোর্ড
  {
    id: 23,
    nameBn: 'প্রচার, প্রিন্টিং ও সাইনবোর্ড',
    nameEn: 'Advertising, Printing & Signboard',
    slug: 'advertising-printing-signboard',
    icon: 'tag',
    descriptionBn: 'ডিজিটাল ব্যানার ও সাইনবোর্ড মেকিং, এলইডি ডিসপ্লে বোর্ড, মাইকিং ও লিফলেট বিতরণ',
    descriptionEn: 'Digital banner, neon/acrylic signboard, LED display board, miking and publicity',
    sortOrder: 23,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 2301, categoryId: 23, nameBn: 'ডিজিটাল ব্যানার, ফেস্টুন ও পিভিসি প্রিন্ট', nameEn: 'Digital Banner & PVC Printing', slug: 'digital-banner-pvc-printing', sortOrder: 1, isActive: true },
      { id: 2302, categoryId: 23, nameBn: 'নিয়ন সাইন, এক্রিলিক ও এলইডি ডিসপ্লে বোর্ড', nameEn: 'Neon Sign & LED Acrylic Display Board', slug: 'neon-led-signboard', sortOrder: 2, isActive: true },
      { id: 2303, categoryId: 23, nameBn: 'শহুরে মাইকিং ও অটোরিকশা প্রচার সার্ভিস', nameEn: 'Publicity Miking & Loudspeaker Campaign', slug: 'publicity-miking-campaign', sortOrder: 3, isActive: true },
      { id: 2304, categoryId: 23, nameBn: 'লিফলেট, ভিজিটিং কার্ড ও ব্রোশিওর ডিজাইন ও প্রিন্টিং', nameEn: 'Visiting Card & Brochure Printing', slug: 'visiting-card-brochure-printing', sortOrder: 4, isActive: true },
    ]
  },

  // 24. খাবার, মিষ্টান্ন ও বেকারি
  {
    id: 24,
    nameBn: 'খাবার, মিষ্টান্ন ও বেকারি',
    nameEn: 'Food, Sweets & Bakery',
    slug: 'food-sweets-bakery',
    icon: 'utensils',
    descriptionBn: 'হোমমেড খাবার টিফিন বক্স, কাস্টমাইজড বার্থডে কেক ও ঐতিহ্যবাহী খাঁটি মিষ্টি সরবরাহ',
    descriptionEn: 'Homemade lunch box, customized birthday cakes, traditional sweets and food delivery',
    sortOrder: 24,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 2401, categoryId: 24, nameBn: 'হোমমেড স্বাস্থ্যকর খাবার ও অফিস লাঞ্চ বক্স', nameEn: 'Homemade Food & Office Lunch Box', slug: 'homemade-food-office-lunch', sortOrder: 1, isActive: true },
      { id: 2402, categoryId: 24, nameBn: 'কাস্টমাইজড বার্থডে ও ওয়েডিং কেক বেকারি', nameEn: 'Custom Birthday & Wedding Cake Bakery', slug: 'custom-cake-bakery', sortOrder: 2, isActive: true },
      { id: 2403, categoryId: 24, nameBn: 'কক্সবাজার ট্র্যাডিশনাল মিষ্টি ও দই সরবরাহ', nameEn: 'Traditional Sweets & Curd Supply', slug: 'traditional-sweets-curd', sortOrder: 3, isActive: true },
      { id: 2404, categoryId: 24, nameBn: 'ফাস্টফুড ও ক্যাফে ডেলিভারি সার্ভিস', nameEn: 'Fast Food & Cafe Delivery Service', slug: 'fast-food-cafe-delivery', sortOrder: 4, isActive: true },
    ]
  },

  // 25. গৃহস্থালি সাহায্য ও কেয়ারটেকিং
  {
    id: 25,
    nameBn: 'গৃহস্থালি সাহায্য ও কেয়ারটেকিং',
    nameEn: 'Domestic Help & Caretaking',
    slug: 'domestic-help-caretaking',
    icon: 'heart',
    descriptionBn: 'বাসার কাজের সাহায্যকারী (বুয়া/খালা), শিশু দিবাযত্ন বেবিসিটার ও বাগান মালী',
    descriptionEn: 'Maid helper, babysitter, cook assistant and gardener',
    sortOrder: 25,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 2501, categoryId: 25, nameBn: 'বাসার কাজের সাহায্যকারী (খণ্ডকালীন/পূর্ণকালীন)', nameEn: 'Domestic Maid & Housekeeper', slug: 'domestic-maid-housekeeper', sortOrder: 1, isActive: true },
      { id: 2502, categoryId: 25, nameBn: 'শিশু দিবাযত্ন (বেবিসিটার) কেয়ারটেকার', nameEn: 'Child Daycare & Babysitter', slug: 'child-daycare-babysitter', sortOrder: 2, isActive: true },
      { id: 2503, categoryId: 25, nameBn: 'রান্নার সাহায্যকারী খালা / গৃহ রন্ধনশিল্পী', nameEn: 'Home Cooking Assistant', slug: 'home-cooking-assistant', sortOrder: 3, isActive: true },
      { id: 2504, categoryId: 25, nameBn: 'বাগান পরিচর্যা ও মালী সার্ভিস', nameEn: 'Gardener & Lawn Care Service', slug: 'gardener-lawn-care', sortOrder: 4, isActive: true },
    ]
  },

  // 26. বর্জ্য ব্যবস্থাপনা ও পুনর্ব্যবহার
  {
    id: 26,
    nameBn: 'বর্জ্য ব্যবস্থাপনা ও পুনর্ব্যবহার',
    nameEn: 'Waste Management & Recycling',
    slug: 'waste-management-recycling',
    icon: 'trash',
    descriptionBn: 'বাসাবাড়ি ও হোটেল ময়লা কালেকশন, পুরাতন ভাঙ্গারি স্ক্র্যাপ ও ই-বর্জ্য রিসাইক্লিং',
    descriptionEn: 'Door-to-door trash pickup, scrap metals and e-waste recycling',
    sortOrder: 26,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 2601, categoryId: 26, nameBn: 'বাসাবাড়ি ও বাণিজ্যিক প্রতিষ্ঠান বর্জ্য সংগ্রহ', nameEn: 'Residential & Commercial Waste Pickup', slug: 'waste-pickup-service', sortOrder: 1, isActive: true },
      { id: 2602, categoryId: 26, nameBn: 'পুরাতন ভাঙ্গারি ও স্ক্র্যাপ লোহা ক্রয়-বিক্রয়', nameEn: 'Scrap Metal & Material Buying', slug: 'scrap-metal-buying', sortOrder: 2, isActive: true },
      { id: 2603, categoryId: 26, nameBn: 'ই-বর্জ্য (পুরাতন ইলেকট্রনিক্স) রিসাইক্লিং', nameEn: 'Electronic E-Waste Recycling', slug: 'electronic-ewaste-recycling', sortOrder: 3, isActive: true },
    ]
  },

  // 27. হস্তনির্মিত ফার্নিচার ও বাঁশ শিল্প
  {
    id: 27,
    nameBn: 'হস্তনির্মিত ফার্নিচার ও বাঁশ শিল্প',
    nameEn: 'Handmade Furniture & Bamboo Craft',
    slug: 'handmade-furniture-bamboo',
    icon: 'package',
    descriptionBn: 'সেগুন ও মেহগনি কাঠের কাস্টম ফার্নিচার মেকিং, বেতের সোফা ও ব্যাম্বু কটেজ ডেকোর',
    descriptionEn: 'Teak wood custom furniture, cane sofa set and eco bamboo cottage architecture',
    sortOrder: 27,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 2701, categoryId: 27, nameBn: 'কাঠের কাস্টম ফার্নিচার প্রস্তুতকারী (সেগুন/মেহগনি)', nameEn: 'Custom Solid Wood Furniture Maker', slug: 'custom-wood-furniture-maker', sortOrder: 1, isActive: true },
      { id: 2702, categoryId: 27, nameBn: 'বেত ও বাঁশের সোফাসেট ও কটেজ ফার্নিচার', nameEn: 'Cane & Bamboo Sofa Furniture', slug: 'cane-bamboo-sofa-furniture', sortOrder: 2, isActive: true },
      { id: 2703, categoryId: 27, nameBn: 'ইকো-রিসোর্ট ব্যাম্বু কটেজ আর্কিটেকচার মেকার', nameEn: 'Eco-Resort Bamboo Cottage Architecture', slug: 'eco-bamboo-cottage-architecture', sortOrder: 3, isActive: true },
    ]
  },

  // 28. নার্সারি ও ল্যান্ডস্কেপিং
  {
    id: 28,
    nameBn: 'নার্সারি ও ল্যান্ডস্কেপিং',
    nameEn: 'Nursery & Landscaping',
    slug: 'nursery-landscaping',
    icon: 'sun',
    descriptionBn: 'ফলজ, বনজ ও শোভাবর্ধক চারা নার্সারি, ছাদ বাগান সেটআপ ও রিসোর্ট ল্যান্ডস্কেপিং',
    descriptionEn: 'Plant nursery, rooftop garden setup, indoor bonsai and resort landscaping',
    sortOrder: 28,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 2801, categoryId: 28, nameBn: 'ফলজ, বনজ ও শোভাবর্ধক চারা নার্সারি', nameEn: 'Plant Nursery (Fruit & Decorative)', slug: 'plant-nursery-decorative', sortOrder: 1, isActive: true },
      { id: 2802, categoryId: 28, nameBn: 'ছাদ বাগান (রুফটপ গার্ডেন) সেটআপ ও পরিচর্যা', nameEn: 'Rooftop Garden Setup & Maintenance', slug: 'rooftop-garden-setup', sortOrder: 2, isActive: true },
      { id: 2803, categoryId: 28, nameBn: 'হোটেল ও রিসোর্ট গ্রিন ল্যান্ডস্কেপিং আর্কিটেকচার', nameEn: 'Hotel & Resort Green Landscaping', slug: 'resort-green-landscaping', sortOrder: 3, isActive: true },
      { id: 2804, categoryId: 28, nameBn: 'ইনডোর প্ল্যান্ট, বনসাই ও হাইড্রোফোনিক কিট', nameEn: 'Indoor Plants & Bonsai Supply', slug: 'indoor-plants-bonsai', sortOrder: 4, isActive: true },
    ]
  },

  // 29. মুদ্রণ, প্যাকেজিং ও স্টেশনারি
  {
    id: 29,
    nameBn: 'মুদ্রণ, প্যাকেজিং ও স্টেশনারি',
    nameEn: 'Packaging & Stationery Supplies',
    slug: 'packaging-stationery-supplies',
    icon: 'file-text',
    descriptionBn: 'শুটকি ও সি-ফুড কুরিয়ার প্যাকেজিং কার্টুন, হোটেল কাস্টম ব্র্যান্ডেড কিটস ও স্টেশনারি',
    descriptionEn: 'Dry fish packaging cartoon box, branded hotel kit and school/office stationery',
    sortOrder: 29,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 2901, categoryId: 29, nameBn: 'শুটকি ও সি-ফুড কুরিয়ার প্যাকেজিং বক্স ও কার্টুন', nameEn: 'Dry Fish Packaging Carton Box', slug: 'dry-fish-packaging-box', sortOrder: 1, isActive: true },
      { id: 2902, categoryId: 29, nameBn: 'হোটেল ও রেস্তোরাঁ কাস্টম ব্র্যান্ডেড কিটস সাপ্লাই', nameEn: 'Hotel Custom Amenities & Toiletries Supply', slug: 'hotel-amenities-supplies', sortOrder: 2, isActive: true },
      { id: 2903, categoryId: 29, nameBn: 'স্কুল, কলেজ ও অফিস পাইকারি স্টেশনারি', nameEn: 'School & Office Wholesale Stationery', slug: 'wholesale-office-stationery', sortOrder: 3, isActive: true },
    ]
  },

  // 30. পরিবেশ, সৌরশক্তি ও সোলার
  {
    id: 30,
    nameBn: 'পরিবেশ, সৌরশক্তি ও সোলার',
    nameEn: 'Solar Energy & Eco-Solutions',
    slug: 'solar-energy-ecosolutions',
    icon: 'zap',
    descriptionBn: 'অন-গ্রিড ও অফ-গ্রিড সোলার সিস্টেম সেটআপ, সোলার প্যানেল ব্যাটারি ও সোলার ওয়াটার পাম্প',
    descriptionEn: 'On-grid/off-grid solar system setup, solar panel battery and solar water pump',
    sortOrder: 30,
    isActive: true,
    isFeatured: false,
    isPopular: true,
    subCategories: [
      { id: 3001, categoryId: 30, nameBn: 'অন-গ্রিড ও অফ-গ্রিড হোম সোলার সিস্টেম সেটআপ', nameEn: 'Home Solar Panel System Setup', slug: 'home-solar-panel-setup', sortOrder: 1, isActive: true },
      { id: 3002, categoryId: 30, nameBn: 'সোলার প্যানেল ও ডিপ সাইকেল ব্যাটারি রিপেয়ার', nameEn: 'Solar Panel & Deep Cycle Battery Repair', slug: 'solar-panel-battery-repair', sortOrder: 2, isActive: true },
      { id: 3003, categoryId: 30, nameBn: 'কৃষি ও মৎস্য খামারে সোলার ওয়াটার পাম্প সেটআপ', nameEn: 'Solar Irrigation & Aerator Setup', slug: 'solar-irrigation-setup', sortOrder: 3, isActive: true },
      { id: 3004, categoryId: 30, nameBn: 'সোলার স্ট্রিট লাইট ও গার্ডেন লাইটিং ইনস্টলেশন', nameEn: 'Solar Street Light Installation', slug: 'solar-street-light-installation', sortOrder: 4, isActive: true },
    ]
  },

  // 31. কমিউনিটি ও সামাজিক উন্নয়ন
  {
    id: 31,
    nameBn: 'কমিউনিটি ও সামাজিক উন্নয়ন',
    nameEn: 'Community & Social Development',
    slug: 'community-social-development',
    icon: 'users',
    descriptionBn: 'স্বেচ্ছাসেবী সংস্থা ও এনজিও কার্যক্রম, দুর্যোগকালীন ত্রাণ ও পরিবেশ সচেতনতা ক্যাম্পেইন',
    descriptionEn: 'Volunteer organization, NGO social work, disaster relief and environmental beach campaigns',
    sortOrder: 31,
    isActive: true,
    isFeatured: false,
    isPopular: false,
    subCategories: [
      { id: 3101, categoryId: 31, nameBn: 'স্বেচ্ছাসেবী ও রক্তদান যুব নেটওয়ার্ক', nameEn: 'Volunteer & Youth Blood Network', slug: 'volunteer-youth-network', sortOrder: 1, isActive: true },
      { id: 3102, categoryId: 31, nameBn: 'এনজিও ও সামাজিক উন্নয়ন প্রকল্পের ফিল্ড সাপোর্ট', nameEn: 'NGO & Social Project Field Support', slug: 'ngo-social-project-support', sortOrder: 2, isActive: true },
      { id: 3103, categoryId: 31, nameBn: 'দুর্যোগ ব্যবস্থাপনা ও উপকূলীয় ত্রাণ কার্যক্রম', nameEn: 'Coastal Disaster Relief & Rescue Support', slug: 'coastal-disaster-relief', sortOrder: 3, isActive: true },
      { id: 3104, categoryId: 31, nameBn: 'বিচ ও সমুদ্র পরিবেশ পরিচ্ছন্নতা ক্যাম্পেইন', nameEn: 'Beach Cleanliness & Marine Eco-Campaign', slug: 'marine-eco-cleanliness-campaign', sortOrder: 4, isActive: true },
    ]
  }
];

export const ALL_MASTER_SUB_CATEGORIES: MasterSubCategory[] = SEBACOX_MASTER_CATEGORIES.flatMap(c => c.subCategories);

export function getMasterCategoryById(id: number): MasterCategory | undefined {
  return SEBACOX_MASTER_CATEGORIES.find(c => c.id === id);
}

export function getSubCategoriesByCategoryId(categoryId: number): MasterSubCategory[] {
  const cat = getMasterCategoryById(categoryId);
  return cat ? cat.subCategories : [];
}

export function getSubCategoryById(subCategoryId: number): MasterSubCategory | undefined {
  for (const cat of SEBACOX_MASTER_CATEGORIES) {
    const sub = cat.subCategories.find(s => s.id === subCategoryId);
    if (sub) return sub;
  }
  return undefined;
}
