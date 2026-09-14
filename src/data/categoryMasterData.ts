// SebaCox Master Taxonomy: 21 Master Categories & Granular Sub-categories
// Standard Schema: Category -> SubCategory with full metadata

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
  subCategories: MasterSubCategory[];
}

export interface MasterSubCategory {
  id: number;
  categoryId: number;
  nameBn: string;
  nameEn: string;
  slug: string;
  sortOrder: number;
  isActive: boolean;
  isFeatured?: boolean;
}

export const SEBACOX_MASTER_CATEGORIES: MasterCategory[] = [
  // 1. বাড়ি ও ভবন নির্মাণ (Home & Building Construction)
  {
    id: 1,
    nameBn: 'বাড়ি ও ভবন নির্মাণ',
    nameEn: 'Home & Building Construction',
    slug: 'home-building-construction',
    icon: 'hammer',
    descriptionBn: 'ইট, বালু, সিমেন্ট সরবরাহ, রাজমিস্ত্রি, ঢালাই, রং ও নির্মাণ পরামর্শ',
    descriptionEn: 'Construction materials, masonry, casting, painting and engineering',
    sortOrder: 1,
    isActive: true,
    isFeatured: true,
    subCategories: [
      { id: 101, categoryId: 1, nameBn: 'ইট ও বালু সরবরাহ', nameEn: 'Brick & Sand Supply', slug: 'brick-sand-supply', sortOrder: 1, isActive: true },
      { id: 102, categoryId: 1, nameBn: 'সিমেন্ট ও রড সরবরাহ', nameEn: 'Cement & Rod Supply', slug: 'cement-rod-supply', sortOrder: 2, isActive: true },
      { id: 103, categoryId: 1, nameBn: 'রাজমিস্ত্রি ও সহকারী', nameEn: 'Mason & Helper', slug: 'mason-helper', sortOrder: 3, isActive: true },
      { id: 104, categoryId: 1, nameBn: 'রড বাইন্ডিং ও ঢালাই মিস্ত্রি', nameEn: 'Rod Binding & Slab Casting', slug: 'rod-binding-slab-casting', sortOrder: 4, isActive: true },
      { id: 105, categoryId: 1, nameBn: 'টাইলস ও মার্বেল মিস্ত্রি', nameEn: 'Tiles & Marble Fitting', slug: 'tiles-marble-fitting', sortOrder: 5, isActive: true },
      { id: 106, categoryId: 1, nameBn: 'রং মিস্ত্রি ও ওয়াল পুটি', nameEn: 'Painting & Wall Putty', slug: 'painting-wall-putty', sortOrder: 6, isActive: true },
      { id: 107, categoryId: 1, nameBn: 'প্লাম্বিং ও স্যানিটারি ফিটিং', nameEn: 'Plumbing & Sanitary Fitting', slug: 'plumbing-sanitary-fitting', sortOrder: 7, isActive: true },
      { id: 108, categoryId: 1, nameBn: 'বিল্ডিং প্ল্যান ও আর্কিটেক্ট', nameEn: 'Building Plan & Architecture', slug: 'building-plan-architecture', sortOrder: 8, isActive: true },
      { id: 109, categoryId: 1, nameBn: 'মাটি কাটা ও ভরাট কাজ', nameEn: 'Earth Excavation & Land Filling', slug: 'earth-excavation-land-filling', sortOrder: 9, isActive: true },
      { id: 110, categoryId: 1, nameBn: 'গ্রিল, থাই অ্যালুমিনিয়াম ও গ্লাস ফিটিং', nameEn: 'Grill, Thai Aluminum & Glass', slug: 'grill-thai-glass', sortOrder: 10, isActive: true },
    ]
  },

  // 2. মেরামত ও টেকনিশিয়ান (Repair & Maintenance)
  {
    id: 2,
    nameBn: 'মেরামত ও টেকনিশিয়ান',
    nameEn: 'Repair & Maintenance',
    slug: 'repair-maintenance',
    icon: 'wrench',
    descriptionBn: 'ইলেকট্রিশিয়ান, এসি, ফ্রিজ, টিভি, গ্যাস স্টোভ ও পানির পাম্প মেরামত',
    descriptionEn: 'Electrician, AC, refrigerator, TV, stove and water pump repair',
    sortOrder: 2,
    isActive: true,
    isFeatured: true,
    subCategories: [
      { id: 201, categoryId: 2, nameBn: 'ইলেকট্রিশিয়ান ও হাউস ওয়্যারিং', nameEn: 'Electrician & House Wiring', slug: 'electrician-house-wiring', sortOrder: 1, isActive: true },
      { id: 202, categoryId: 2, nameBn: 'এসি সার্ভিসিং ও মেরামত', nameEn: 'AC Servicing & Repair', slug: 'ac-servicing-repair', sortOrder: 2, isActive: true },
      { id: 203, categoryId: 2, nameBn: 'ফ্রিজ মেরামত ও গ্যাস চার্জ', nameEn: 'Refrigerator Repair & Gas Charge', slug: 'fridge-repair-gas-charge', sortOrder: 3, isActive: true },
      { id: 204, categoryId: 2, nameBn: 'ওয়াশিং মেশিন মেরামত', nameEn: 'Washing Machine Repair', slug: 'washing-machine-repair', sortOrder: 4, isActive: true },
      { id: 205, categoryId: 2, nameBn: 'পানির পাম্প ও মোটর সার্ভিস', nameEn: 'Water Pump & Motor Service', slug: 'water-pump-motor-service', sortOrder: 5, isActive: true },
      { id: 206, categoryId: 2, nameBn: 'গ্যাস স্টোভ ও ওভেন মেরামত', nameEn: 'Gas Stove & Oven Repair', slug: 'gas-stove-oven-repair', sortOrder: 6, isActive: true },
      { id: 207, categoryId: 2, nameBn: 'আইপিএস ও ইউপিএস ব্যাটারি মেরামত', nameEn: 'IPS & UPS Battery Repair', slug: 'ips-ups-repair', sortOrder: 7, isActive: true },
      { id: 208, categoryId: 2, nameBn: 'টিভি ও অডিও সিস্টেম মেরামত', nameEn: 'TV & Audio System Repair', slug: 'tv-audio-repair', sortOrder: 8, isActive: true },
      { id: 209, categoryId: 2, nameBn: 'সিলিং ফ্যান ও হোম অ্যাপ্লায়েন্স', nameEn: 'Ceiling Fan & Home Appliances', slug: 'fan-home-appliances', sortOrder: 9, isActive: true },
    ]
  },

  // 3. পরিবহন ও মালামাল স্থানান্তর (Transport & Logistics)
  {
    id: 3,
    nameBn: 'পরিবহন ও মালামাল স্থানান্তর',
    nameEn: 'Transport & Logistics',
    slug: 'transport-logistics',
    icon: 'truck',
    descriptionBn: 'বাসা বদল, ট্রাক, পিকআপ, সিএনজি, কার ও ট্রাভেলার ভাড়া',
    descriptionEn: 'House shifting, truck, pickup, CNG, car and tourist vehicle rental',
    sortOrder: 3,
    isActive: true,
    isFeatured: true,
    subCategories: [
      { id: 301, categoryId: 3, nameBn: 'বাসা বদল ও অফিস শিফটিং', nameEn: 'House & Office Shifting', slug: 'house-office-shifting', sortOrder: 1, isActive: true },
      { id: 302, categoryId: 3, nameBn: 'পিকআপ ও মিনি ট্রাক ভাড়া', nameEn: 'Pickup & Mini Truck Rental', slug: 'pickup-mini-truck-rental', sortOrder: 2, isActive: true },
      { id: 303, categoryId: 3, nameBn: 'বড় ট্রাক ও লরি ভাড়া', nameEn: 'Heavy Truck & Lorry Rental', slug: 'heavy-truck-lorry-rental', sortOrder: 3, isActive: true },
      { id: 304, categoryId: 3, nameBn: 'কার ও মাইক্রোবাস রেন্টাল', nameEn: 'Car & Microbus Rental', slug: 'car-microbus-rental', sortOrder: 4, isActive: true },
      { id: 305, categoryId: 3, nameBn: 'টমটম ও অটোরিকশা রিজার্ভ', nameEn: 'TomTom & Auto-rickshaw Reserve', slug: 'tomtom-autorickshaw-reserve', sortOrder: 5, isActive: true },
      { id: 306, categoryId: 3, nameBn: 'সিএনজি ও মাহিন্দ্রা রিজার্ভ', nameEn: 'CNG & Mahindra Reserve', slug: 'cng-mahindra-reserve', sortOrder: 6, isActive: true },
      { id: 307, categoryId: 3, nameBn: 'মালামাল লোডিং-আনলোডিং শ্রমিক (লেবার)', nameEn: 'Loading & Unloading Labour', slug: 'loading-unloading-labour', sortOrder: 7, isActive: true },
      { id: 308, categoryId: 3, nameBn: 'পার্সেল ও কুরিয়ার ড্রপ', nameEn: 'Parcel & Courier Delivery', slug: 'parcel-courier-delivery', sortOrder: 8, isActive: true },
    ]
  },

  // 4. পর্যটন ও হোটেল-রিসোর্ট (Tourism & Hospitality)
  {
    id: 4,
    nameBn: 'পর্যটন ও হোটেল-রিসোর্ট',
    nameEn: 'Tourism & Hospitality',
    slug: 'tourism-hospitality',
    icon: 'compass',
    descriptionBn: 'হোটেল, কটেজ, ট্যুর গাইড, জিপ ও বোট ক্রুজ সেবা',
    descriptionEn: 'Hotels, cottages, tour guides, beach jeep and marine cruises',
    sortOrder: 4,
    isActive: true,
    isFeatured: true,
    subCategories: [
      { id: 401, categoryId: 4, nameBn: 'হোটেল, মোটেল ও রিসোর্ট বুকিং', nameEn: 'Hotel, Motel & Resort Booking', slug: 'hotel-motel-resort-booking', sortOrder: 1, isActive: true },
      { id: 402, categoryId: 4, nameBn: 'বীচ ভিউ কটেজ ও হোমস্টে', nameEn: 'Beach View Cottage & Homestay', slug: 'beach-cottage-homestay', sortOrder: 2, isActive: true },
      { id: 403, categoryId: 4, nameBn: 'ট্যুর গাইড ও সাইটসিয়িং প্যাকেজ', nameEn: 'Tour Guide & Sightseeing Packages', slug: 'tour-guide-sightseeing', sortOrder: 3, isActive: true },
      { id: 404, categoryId: 4, nameBn: 'চাঁন্দের গাড়ি ও জিপ রেন্টাল', nameEn: 'Chander Gari & Jeep Rental', slug: 'chander-gari-jeep-rental', sortOrder: 4, isActive: true },
      { id: 405, categoryId: 4, nameBn: 'বোট, স্পিডবোট ও ওয়াটার স্কিইং', nameEn: 'Speedboat & Water Sports', slug: 'speedboat-water-sports', sortOrder: 5, isActive: true },
      { id: 406, categoryId: 4, nameBn: 'সেন্টমার্টিন ক্রুজ ও শিপ টিকিট সহায়তা', nameEn: 'Saint Martin Ship & Cruise Booking', slug: 'saint-martin-cruise-booking', sortOrder: 6, isActive: true },
      { id: 407, categoryId: 4, nameBn: 'ফটোগ্রাফি ও ড্রোন শ্যুট (বীচ)', nameEn: 'Beach Photography & Drone Shoot', slug: 'beach-photography-drone', sortOrder: 7, isActive: true },
    ]
  },

  // 5. কৃষি, মৎস্য ও শুঁটকি (Agriculture & Fisheries)
  {
    id: 5,
    nameBn: 'কৃষি, মৎস্য ও শুঁটকি',
    nameEn: 'Agriculture & Fisheries',
    slug: 'agriculture-fisheries',
    icon: 'fish',
    descriptionBn: 'নাজিরারটেক শুঁটকি পাইকারি, সামুদ্রিক মাছ, পান, সুপারি ও লবণ খামার',
    descriptionEn: 'Dry fish wholesale, sea fish, betel nut, salt production and agri inputs',
    sortOrder: 5,
    isActive: true,
    isFeatured: true,
    subCategories: [
      { id: 501, categoryId: 5, nameBn: 'নাজিরারটেক শুঁটকি পাইকারি ও খুচরা', nameEn: 'Nazirartech Dry Fish Wholesale', slug: 'dry-fish-wholesale', sortOrder: 1, isActive: true },
      { id: 502, categoryId: 5, nameBn: 'তাজা সামুদ্রিক মাছ সরবরাহ', nameEn: 'Fresh Marine Fish Supply', slug: 'fresh-marine-fish-supply', sortOrder: 2, isActive: true },
      { id: 503, categoryId: 5, nameBn: 'মিঠা পান ও সুপারি পাইকারি', nameEn: 'Sweet Betel Leaf & Areca Nut', slug: 'betel-leaf-areca-nut', sortOrder: 3, isActive: true },
      { id: 504, categoryId: 5, nameBn: 'লবণ উৎপাদন সামগ্রী ও পলিথিন', nameEn: 'Salt Production Material & Polythene', slug: 'salt-production-polythene', sortOrder: 4, isActive: true },
      { id: 505, categoryId: 5, nameBn: 'চিংড়ি পোনা (পিএল) ও হ্যাচারি সামগ্রী', nameEn: 'Shrimp Fry (PL) & Hatchery Supplies', slug: 'shrimp-fry-hatchery', sortOrder: 5, isActive: true },
      { id: 506, categoryId: 5, nameBn: 'মাছের খাদ্য ও সার-কীটনাশক', nameEn: 'Fish Feed, Fertilizer & Pesticides', slug: 'fish-feed-fertilizer', sortOrder: 6, isActive: true },
      { id: 507, categoryId: 5, nameBn: 'কৃষি যন্ত্রপাতি ও সেচ সরঞ্জাম', nameEn: 'Agri Machinery & Irrigation Tools', slug: 'agri-machinery-irrigation', sortOrder: 7, isActive: true },
    ]
  },

  // 6. স্বাস্থ্য, চিকিৎসা ও জরুরি সেবা (Healthcare & Emergency)
  {
    id: 6,
    nameBn: 'স্বাস্থ্য, চিকিৎসা ও জরুরি সেবা',
    nameEn: 'Healthcare & Emergency',
    slug: 'healthcare-emergency',
    icon: 'activity',
    descriptionBn: 'ডাক্তার অ্যাপয়েন্টমেন্ট, হোম নার্সিং, অক্সিজেন ও অ্যাম্বুলেন্স সেবা',
    descriptionEn: 'Doctor appointments, home nursing, oxygen cylinder and ambulance',
    sortOrder: 6,
    isActive: true,
    isFeatured: true,
    subCategories: [
      { id: 601, categoryId: 6, nameBn: 'এমবিবিএস ও বিশেষজ্ঞ ডাক্তার অ্যাপয়েন্টমেন্ট', nameEn: 'Doctor Appointments & Consultation', slug: 'doctor-appointments', sortOrder: 1, isActive: true },
      { id: 602, categoryId: 6, nameBn: 'হোম নার্সিং ও বয়োবৃদ্ধদের কেয়ারগিভার', nameEn: 'Home Nursing & Senior Caregiver', slug: 'home-nursing-senior-care', sortOrder: 2, isActive: true },
      { id: 603, categoryId: 6, nameBn: 'জরুরি অ্যাম্বুলেন্স সেবা', nameEn: 'Emergency Ambulance Service', slug: 'emergency-ambulance', sortOrder: 3, isActive: true },
      { id: 604, categoryId: 6, nameBn: 'মেডিকেল অক্সিজেন সিলিন্ডার সরবরাহ', nameEn: 'Medical Oxygen Cylinder Supply', slug: 'medical-oxygen-cylinder', sortOrder: 4, isActive: true },
      { id: 605, categoryId: 6, nameBn: 'হোম ডায়াগনস্টিক ও রক্ত পরীক্ষা', nameEn: 'Home Sample Collection & Blood Test', slug: 'home-blood-test', sortOrder: 5, isActive: true },
      { id: 606, categoryId: 6, nameBn: 'ফিজিওথেরাপি ও থেরাপিস্ট', nameEn: 'Physiotherapy & Rehabilitation', slug: 'physiotherapy-rehabilitation', sortOrder: 6, isActive: true },
      { id: 607, categoryId: 6, nameBn: 'ফার্মেসি ও হোম ডেলিভারি ঔষধ', nameEn: 'Pharmacy & Medicine Delivery', slug: 'pharmacy-medicine-delivery', sortOrder: 7, isActive: true },
    ]
  },

  // 7. ক্লিনিং ও গৃহস্থালি সাহায্য (Cleaning & Housekeeping)
  {
    id: 7,
    nameBn: 'ক্লিনিং ও গৃহস্থালি সাহায্য',
    nameEn: 'Cleaning & Housekeeping',
    slug: 'cleaning-housekeeping',
    icon: 'sparkles',
    descriptionBn: 'বাসা, অফিস ডিপ ক্লিনিং, সোফা কার্পেট ওয়াশ ও পেস্ট কন্ট্রোল',
    descriptionEn: 'Home deep cleaning, sofa carpet wash and pest control',
    sortOrder: 7,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 701, categoryId: 7, nameBn: 'বাসা-বাড়ি ও ফ্ল্যাট ডিপ ক্লিনিং', nameEn: 'Home & Apartment Deep Cleaning', slug: 'home-deep-cleaning', sortOrder: 1, isActive: true },
      { id: 702, categoryId: 7, nameBn: 'অফিস ও শোরুম ক্লিনিং', nameEn: 'Office & Showroom Cleaning', slug: 'office-showroom-cleaning', sortOrder: 2, isActive: true },
      { id: 703, categoryId: 7, nameBn: 'সোফা, জাজিম ও কার্পেট ওয়াশ', nameEn: 'Sofa, Mattress & Carpet Wash', slug: 'sofa-carpet-wash', sortOrder: 3, isActive: true },
      { id: 704, categoryId: 7, nameBn: 'পানির ট্যাংক ও রিজার্ভার পরিষ্কার', nameEn: 'Water Tank & Reservoir Cleaning', slug: 'water-tank-cleaning', sortOrder: 4, isActive: true },
      { id: 705, categoryId: 7, nameBn: 'পোকামাকড় ও পেস্ট কন্ট্রোল (উইপোকা/ছারপোকা)', nameEn: 'Pest Control & Termite Treatment', slug: 'pest-control-treatment', sortOrder: 5, isActive: true },
      { id: 706, categoryId: 7, nameBn: 'বাসার কাজের বুয়া ও গৃহকর্মী', nameEn: 'House Maid & Domestic Helper', slug: 'house-maid-helper', sortOrder: 6, isActive: true },
    ]
  },

  // 8. ড্রাইভার ও যানবাহন সেবা (Driver & Vehicle Services)
  {
    id: 8,
    nameBn: 'ড্রাইভার ও যানবাহন সেবা',
    nameEn: 'Driver & Vehicle Services',
    slug: 'driver-vehicle-services',
    icon: 'car',
    descriptionBn: 'ব্যক্তিগত ড্রাইভার, কার ওয়াশ, বাইক ও অটোমোবাইল গ্যারেজ মেরামত',
    descriptionEn: 'Personal driver, car wash, bike and automobile garage repair',
    sortOrder: 8,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 801, categoryId: 8, nameBn: 'দৈনিক / মাসিক ব্যক্তিগত ড্রাইভার', nameEn: 'Daily / Monthly Personal Driver', slug: 'daily-monthly-driver', sortOrder: 1, isActive: true },
      { id: 802, categoryId: 8, nameBn: 'গাড়ি ওয়াশ, পলিশ ও ফোম ক্লিনিং', nameEn: 'Car Wash, Polish & Detailing', slug: 'car-wash-detailing', sortOrder: 2, isActive: true },
      { id: 803, categoryId: 8, nameBn: 'মোটরসাইকেল ও স্কুটার সার্ভিসিং', nameEn: 'Motorcycle & Scooter Servicing', slug: 'motorcycle-servicing', sortOrder: 3, isActive: true },
      { id: 804, categoryId: 8, nameBn: 'অটোমোবাইল গ্যারেজ ও মেকানিক', nameEn: 'Automobile Garage & Mechanic', slug: 'automobile-mechanic', sortOrder: 4, isActive: true },
      { id: 805, categoryId: 8, nameBn: 'টায়ার পাংচার ও নতুন ব্যাটারি সার্ভিস', nameEn: 'Tire Puncture & Battery Service', slug: 'tire-puncture-battery', sortOrder: 5, isActive: true },
      { id: 806, categoryId: 8, nameBn: 'হাইওয়ে ব্রেকডাউন ও রেসকিউ সার্ভিস', nameEn: 'Highway Breakdown & Recovery', slug: 'highway-breakdown-rescue', sortOrder: 6, isActive: true },
    ]
  },

  // 9. অনুষ্ঠান, ওয়েডিং ও ইভেন্ট ম্যানেজমেন্ট (Events & Wedding Services)
  {
    id: 9,
    nameBn: 'অনুষ্ঠান, ওয়েডিং ও ইভেন্ট ম্যানেজমেন্ট',
    nameEn: 'Events & Wedding Services',
    slug: 'events-wedding-management',
    icon: 'party-popper',
    descriptionBn: 'বিয়ের ডেকোরেশন, সাউন্ড, লাইটিং, ফটোগ্রাফি ও কমিউনিটি সেন্টার',
    descriptionEn: 'Wedding decoration, sound, lighting, photography and hall booking',
    sortOrder: 9,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 901, categoryId: 9, nameBn: 'বিয়ের স্টেজ ও গেট ডেকোরেশন', nameEn: 'Wedding Stage & Gate Decoration', slug: 'wedding-stage-decoration', sortOrder: 1, isActive: true },
      { id: 902, categoryId: 9, nameBn: 'ইভেন্ট সাউন্ড সিস্টেম ও মাইক ভাড়া', nameEn: 'Sound System & Mic Rental', slug: 'sound-system-mic-rental', sortOrder: 2, isActive: true },
      { id: 903, categoryId: 9, nameBn: 'ইভেন্ট লাইটিং ও জেনারেটর ব্যাকআপ', nameEn: 'Event Lighting & Generator Backup', slug: 'event-lighting-generator', sortOrder: 3, isActive: true },
      { id: 904, categoryId: 9, nameBn: 'ফটোগ্রাফি ও সিনেমাটোগ্রাফি', nameEn: 'Event Photography & Cinematography', slug: 'photography-cinematography', sortOrder: 4, isActive: true },
      { id: 905, categoryId: 9, nameBn: 'কমিউনিটি সেন্টার ও কনভেনশন হল বুকিং', nameEn: 'Community Center & Convention Hall', slug: 'community-center-hall', sortOrder: 5, isActive: true },
      { id: 906, categoryId: 9, nameBn: 'ব্রাইডাল মেকআপ ও মেহেদি আর্টিস্ট', nameEn: 'Bridal Makeup & Mehndi Artist', slug: 'bridal-makeup-mehndi', sortOrder: 6, isActive: true },
    ]
  },

  // 10. খাবার, ক্যাটারিং ও হোম ডেলিভারি (Food & Catering)
  {
    id: 10,
    nameBn: 'খাবার, ক্যাটারিং ও হোম ডেলিভারি',
    nameEn: 'Food & Catering',
    slug: 'food-catering-delivery',
    icon: 'utensils',
    descriptionBn: 'বাবুর্চি, ইভেন্ট ক্যাটারিং, হোমমেড ফুড ও রেস্টুরেন্ট অর্ডার',
    descriptionEn: 'Professional chef, event catering, homemade food and restaurant meals',
    sortOrder: 10,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1001, categoryId: 10, nameBn: 'অভিজ্ঞ বাবুর্চি ও রান্নার দল (মেজ্জান/বিয়ে)', nameEn: 'Professional Chef & Cooking Team (Mezban/Wedding)', slug: 'chef-cooking-team-mezban', sortOrder: 1, isActive: true },
      { id: 1002, categoryId: 10, nameBn: 'ইভেন্ট ও অফিস ক্যাটারিং সার্ভিস', nameEn: 'Event & Corporate Catering', slug: 'event-corporate-catering', sortOrder: 2, isActive: true },
      { id: 1003, categoryId: 10, nameBn: 'হোমমেড টিফিন ও ডেলিভারি খাবার', nameEn: 'Homemade Tiffin & Meal Delivery', slug: 'homemade-tiffin-meals', sortOrder: 3, isActive: true },
      { id: 1004, categoryId: 10, nameBn: 'ঐতিহ্যবাহী মেজবানি ও বিরিয়ানি প্যাকেজ', nameEn: 'Traditional Mezbani & Biryani Package', slug: 'mezbani-biryani-package', sortOrder: 4, isActive: true },
      { id: 1005, categoryId: 10, nameBn: 'মিষ্টি, দধি ও স্ন্যাক্স সরবরাহ', nameEn: 'Sweets, Yogurt & Snacks Supply', slug: 'sweets-snacks-supply', sortOrder: 5, isActive: true },
    ]
  },

  // 11. শিক্ষা, টিউশন ও স্কিল ট্রেইনিং (Education & Tuition)
  {
    id: 11,
    nameBn: 'শিক্ষা, টিউশন ও স্কিল ট্রেইনিং',
    nameEn: 'Education & Tuition',
    slug: 'education-tuition-skills',
    icon: 'graduation-cap',
    descriptionBn: 'হোম টিউটর, কোরআন শিক্ষা, ইংরেজি ভাষা ও কম্পিউটার প্রশিক্ষণ',
    descriptionEn: 'Home tutor, Quran coaching, English language and computer IT skills',
    sortOrder: 11,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1101, categoryId: 11, nameBn: 'হোম টিউটর (বাংলা/ইংরেজি মাধ্যম)', nameEn: 'Home Tutor (Bangla/English Medium)', slug: 'home-tutor-bangla-english', sortOrder: 1, isActive: true },
      { id: 1102, categoryId: 11, nameBn: 'কোরআন ও ধর্মীয় শিক্ষক', nameEn: 'Quran & Islamic Studies Tutor', slug: 'quran-islamic-studies-tutor', sortOrder: 2, isActive: true },
      { id: 1103, categoryId: 11, nameBn: 'স্পোকেন ইংলিশ ও আইইএলটিএস কোচিং', nameEn: 'Spoken English & IELTS Coaching', slug: 'spoken-english-ielts', sortOrder: 3, isActive: true },
      { id: 1104, categoryId: 11, nameBn: 'কম্পিউটার ও আইটি স্কিল কোর্স', nameEn: 'Computer & Basic IT Training', slug: 'computer-it-skills', sortOrder: 4, isActive: true },
      { id: 1105, categoryId: 11, nameBn: 'ড্রাইভিং প্রশিক্ষণ স্কুল', nameEn: 'Motor Driving Training School', slug: 'driving-training-school', sortOrder: 5, isActive: true },
      { id: 1106, categoryId: 11, nameBn: 'সঙ্গীত, অঙ্কন ও হস্তশিল্প শিক্ষা', nameEn: 'Music, Drawing & Art Classes', slug: 'music-drawing-art-classes', sortOrder: 6, isActive: true },
    ]
  },

  // 12. আইটি, ফ্রিল্যান্সিং ও ডিজিটাল সেবা (IT & Digital Services)
  {
    id: 12,
    nameBn: 'আইটি, ফ্রিল্যান্সিং ও ডিজিটাল সেবা',
    nameEn: 'IT & Digital Services',
    slug: 'it-digital-services',
    icon: 'monitor',
    descriptionBn: 'কম্পিউটার মেরামত, সিসিটিভি, ওয়েব ডিজাইন ও ডিজিটাল মার্কেটিং',
    descriptionEn: 'Computer repair, CCTV installation, web design and digital marketing',
    sortOrder: 12,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1201, categoryId: 12, nameBn: 'কম্পিউটার, ল্যাপটপ ও প্রিন্টার মেরামত', nameEn: 'Computer, Laptop & Printer Repair', slug: 'computer-laptop-printer-repair', sortOrder: 1, isActive: true },
      { id: 1202, categoryId: 12, nameBn: 'সিসিটিভি ক্যামেরা ইনস্টলেশন ও রক্ষণাবেক্ষণ', nameEn: 'CCTV Camera Setup & Maintenance', slug: 'cctv-setup-maintenance', sortOrder: 2, isActive: true },
      { id: 1203, categoryId: 12, nameBn: 'ওয়াইফাই ও ব্রডব্যান্ড নেটওয়ার্ক সাপোর্ট', nameEn: 'WiFi & Network Infrastructure', slug: 'wifi-network-support', sortOrder: 3, isActive: true },
      { id: 1204, categoryId: 12, nameBn: 'গ্রাফিক ডিজাইন ও ব্যানার ডিজাইন', nameEn: 'Graphic Design & Banner Art', slug: 'graphic-design-banner', sortOrder: 4, isActive: true },
      { id: 1205, categoryId: 12, nameBn: 'ওয়েবসাইট ও সফটওয়্যার ডেভেলপমেন্ট', nameEn: 'Website & Custom Software Development', slug: 'website-software-dev', sortOrder: 5, isActive: true },
      { id: 1206, categoryId: 12, nameBn: 'ফেসবুক পেজ প্রমোশন ও ডিজিটাল মার্কেটিং', nameEn: 'Social Media & Digital Marketing', slug: 'social-digital-marketing', sortOrder: 6, isActive: true },
    ]
  },

  // 13. পার্সোনাল কেয়ার ও বিউটি সেলুন (Personal Care & Beauty)
  {
    id: 13,
    nameBn: 'পার্সোনাল কেয়ার ও বিউটি সেলুন',
    nameEn: 'Personal Care & Beauty',
    slug: 'personal-care-beauty',
    icon: 'scissors',
    descriptionBn: 'হোম সেলুন, লেডিস বিউটি পার্লার, ফেসিয়াল ও স্পা',
    descriptionEn: 'Home salon haircut, ladies parlor, facial care and spa',
    sortOrder: 13,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1301, categoryId: 13, nameBn: 'পুরুষদের হোম সেলুন ও চুল কাটা', nameEn: 'Men Home Salon & Haircut', slug: 'men-home-salon-haircut', sortOrder: 1, isActive: true },
      { id: 1302, categoryId: 13, nameBn: 'লেডিস পার্লার ও স্কিন কেয়ার', nameEn: 'Ladies Beauty Parlour & Skin Care', slug: 'ladies-parlour-skincare', sortOrder: 2, isActive: true },
      { id: 1303, categoryId: 13, nameBn: 'ফেসিয়াল, ম্যানিকিউর ও পেডিকিউর', nameEn: 'Facial, Manicure & Pedicure', slug: 'facial-manicure-pedicure', sortOrder: 3, isActive: true },
      { id: 1304, categoryId: 13, nameBn: 'বডি ম্যাসাজ ও স্পা সেবা', nameEn: 'Body Massage & Relaxing Spa', slug: 'body-massage-spa', sortOrder: 4, isActive: true },
    ]
  },

  // 14. কাঠমিস্ত্রি ও ফার্নিচার (Carpentry & Furniture)
  {
    id: 14,
    nameBn: 'কাঠমিস্ত্রি ও ফার্নিচার',
    nameEn: 'Carpentry & Furniture',
    slug: 'carpentry-furniture',
    icon: 'layers',
    descriptionBn: 'নতুন ফার্নিচার তৈরি, সোফা মেরামত, বার্নিশ ও দরজা-জানালা ফিটিং',
    descriptionEn: 'Custom furniture, sofa repair, wood polish and door-window fitting',
    sortOrder: 14,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1401, categoryId: 14, nameBn: 'নতুন কাঠের ফার্নিচার তৈরি', nameEn: 'Custom Wooden Furniture Making', slug: 'custom-furniture-making', sortOrder: 1, isActive: true },
      { id: 1402, categoryId: 14, nameBn: 'পুরাতন ফার্নিচার মেরামত ও রিকভারি', nameEn: 'Old Furniture Repair & Recovery', slug: 'furniture-repair-recovery', sortOrder: 2, isActive: true },
      { id: 1403, categoryId: 14, nameBn: 'কাঠের বার্নিশ ও হ্যান্ড পলিশ', nameEn: 'Wood Varnish & Hand Polish', slug: 'wood-varnish-polish', sortOrder: 3, isActive: true },
      { id: 1404, categoryId: 14, nameBn: 'দরজা, জানালা ও লক ফিটিং', nameEn: 'Door, Window & Lock Fitting', slug: 'door-window-lock-fitting', sortOrder: 4, isActive: true },
      { id: 1405, categoryId: 14, nameBn: 'কিচেন ক্যাবিনেট ও ইন্টেরিয়র উডওয়ার্ক', nameEn: 'Kitchen Cabinet & Interior Woodwork', slug: 'kitchen-cabinet-woodwork', sortOrder: 5, isActive: true },
    ]
  },

  // 15. দর্জি ও সেলাই সেবা (Tailoring & Garments)
  {
    id: 15,
    nameBn: 'দর্জি ও সেলাই সেবা',
    nameEn: 'Tailoring & Garments',
    slug: 'tailoring-garments',
    icon: 'shirt',
    descriptionBn: 'জেন্টস ও লেডিস টেইলারিং, অল্টারেশন ও পর্দা-কুশন কভার সেলাই',
    descriptionEn: 'Gents and ladies custom tailoring, alteration and curtain making',
    sortOrder: 15,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1501, categoryId: 15, nameBn: 'জেন্টস টেইলারিং (শার্ট/প্যান্ট/স্যুট)', nameEn: 'Gents Tailoring (Shirt/Pant/Suit)', slug: 'gents-tailoring', sortOrder: 1, isActive: true },
      { id: 1502, categoryId: 15, nameBn: 'লেডিস টেইলারিং (থ্রি-পিস/ব্লাউজ/বোরকা)', nameEn: 'Ladies Tailoring (Dress/Blouse/Burqa)', slug: 'ladies-tailoring', sortOrder: 2, isActive: true },
      { id: 1503, categoryId: 15, nameBn: 'কাপড় অল্টারেশন ও মাপ ঠিক করা', nameEn: 'Cloth Alteration & Size Adjustment', slug: 'cloth-alteration', sortOrder: 3, isActive: true },
      { id: 1504, categoryId: 15, nameBn: 'পর্দা, সোফা ও কুশন কভার সেলাই', nameEn: 'Curtain, Sofa & Cushion Cover Sewing', slug: 'curtain-cushion-sewing', sortOrder: 4, isActive: true },
    ]
  },

  // 16. নিরাপত্তা ও গার্ড সার্ভিস (Security & Guard Services)
  {
    id: 16,
    nameBn: 'নিরাপত্তা ও গার্ড সার্ভিস',
    nameEn: 'Security & Guard Services',
    slug: 'security-guard-services',
    icon: 'shield',
    descriptionBn: 'সিকিউরিটি গার্ড, নাইট গার্ড, ইভেন্ট বাউন্সার ও নিরাপত্তা সিস্টেম',
    descriptionEn: 'Security guard, night watchman, event bouncer and access systems',
    sortOrder: 16,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1601, categoryId: 16, nameBn: 'বাসা ও অফিসের সিকিউরিটি গার্ড', nameEn: 'Residential & Office Security Guard', slug: 'residential-office-guard', sortOrder: 1, isActive: true },
      { id: 1602, categoryId: 16, nameBn: 'মার্কেট ও নাইট গার্ড পাহারা', nameEn: 'Market & Night Watchman Service', slug: 'market-night-guard', sortOrder: 2, isActive: true },
      { id: 1603, categoryId: 16, nameBn: 'ইভেন্ট বাউন্সার ও ভিআইপি প্রটেকশন', nameEn: 'Event Bouncer & VIP Protection', slug: 'event-bouncer-vip', sortOrder: 3, isActive: true },
      { id: 1604, categoryId: 16, nameBn: 'ফায়ার সেফটি ও এক্সটিংগুইশার রিফিল', nameEn: 'Fire Safety & Extinguisher Refill', slug: 'fire-safety-extinguisher', sortOrder: 4, isActive: true },
    ]
  },

  // 17. আইন, দলিল ও আইনি পরামর্শ (Legal & Documentation)
  {
    id: 17,
    nameBn: 'আইন, দলিল ও আইনি পরামর্শ',
    nameEn: 'Legal & Documentation',
    slug: 'legal-documentation',
    icon: 'scale',
    descriptionBn: 'দলিল লেখক, জমি রেজিস্ট্রি, নোটারি পাবলিক ও ট্রেড লাইসেন্স পরামর্শ',
    descriptionEn: 'Deed writer, land registry, notary public and trade license consultancy',
    sortOrder: 17,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1701, categoryId: 17, nameBn: 'দলিল লেখক ও জমি রেজিস্ট্রি সহায়তা', nameEn: 'Deed Writer & Land Registration Help', slug: 'deed-writer-land-registration', sortOrder: 1, isActive: true },
      { id: 1702, categoryId: 17, nameBn: 'আইনজীবী ও লিগ্যাল অ্যাডভাইজার', nameEn: 'Advocate & Legal Consultation', slug: 'advocate-legal-consultation', sortOrder: 2, isActive: true },
      { id: 1703, categoryId: 17, nameBn: 'নোটারি পাবলিক ও হলফনামা তৈরি', nameEn: 'Notary Public & Affidavit Service', slug: 'notary-public-affidavit', sortOrder: 3, isActive: true },
      { id: 1704, categoryId: 17, nameBn: 'পাসপোর্ট, ভিসা ও এনআইডি ডকুমেন্টেশন', nameEn: 'Passport, Visa & NID Documentation', slug: 'passport-visa-nid-docs', sortOrder: 4, isActive: true },
      { id: 1705, categoryId: 17, nameBn: 'ট্রেড লাইসেন্স ও ট্যাক্স/ভ্যাট ফাইল কনসাল্টিং', nameEn: 'Trade License, Tax & VAT Consultancy', slug: 'trade-license-tax-vat', sortOrder: 5, isActive: true },
    ]
  },

  // 18. প্রিন্টিং, সাইনবোর্ড ও বিজ্ঞাপন (Printing & Advertising)
  {
    id: 18,
    nameBn: 'প্রিন্টিং, সাইনবোর্ড ও বিজ্ঞাপন',
    nameEn: 'Printing & Advertising',
    slug: 'printing-advertising',
    icon: 'printer',
    descriptionBn: 'প্রেস প্রিন্টিং, ব্যানার, এলইডি সাইনবোর্ড, ভিজিটিং কার্ড ও সিল তৈরি',
    descriptionEn: 'Press printing, PVC banner, LED signage, business cards and seals',
    sortOrder: 18,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1801, categoryId: 18, nameBn: 'ব্যানার, ফেস্টুন ও পিভিসি প্রিন্টিং', nameEn: 'Banner, Festoon & PVC Printing', slug: 'banner-festoon-pvc-printing', sortOrder: 1, isActive: true },
      { id: 1802, categoryId: 18, nameBn: 'এলইডি ও নিয়ন সাইনবোর্ড তৈরি', nameEn: 'LED & Neon Signboard Manufacturing', slug: 'led-neon-signboard', sortOrder: 2, isActive: true },
      { id: 1803, categoryId: 18, nameBn: 'অফসেট প্রেস (বই/লিফলেট/রশিদ)', nameEn: 'Offset Press (Books/Leaflets/Receipts)', slug: 'offset-press-printing', sortOrder: 3, isActive: true },
      { id: 1804, categoryId: 18, nameBn: 'ভিজিটিং কার্ড, আইডি কার্ড ও সিল তৈরি', nameEn: 'Visiting Card, ID Card & Official Seal', slug: 'visiting-card-seal', sortOrder: 4, isActive: true },
    ]
  },

  // 19. রিয়েল এস্টেট ও বাসা ভাড়া (Real Estate & Rentals)
  {
    id: 19,
    nameBn: 'রিয়েল এস্টেট ও বাসা ভাড়া',
    nameEn: 'Real Estate & Rentals',
    slug: 'real-estate-rentals',
    icon: 'building',
    descriptionBn: 'ফ্ল্যাট বাসা ভাড়া, অফিস স্পেস, দোকান ও কমার্শিয়াল জমি কেনাবেচা',
    descriptionEn: 'Apartment rent, commercial space, shop and land buy-sell broker',
    sortOrder: 19,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 1901, categoryId: 19, nameBn: 'ফ্যামিলি ও ব্যাচেলর বাসা ভাড়া', nameEn: 'Family & Bachelor Apartment Rent', slug: 'apartment-rent-family-bachelor', sortOrder: 1, isActive: true },
      { id: 1902, categoryId: 19, nameBn: 'অফিস স্পেস ও দোকান ভাড়া', nameEn: 'Office Space & Commercial Shop Rent', slug: 'office-shop-rent', sortOrder: 2, isActive: true },
      { id: 1903, categoryId: 19, nameBn: 'জমি ও প্লট কেনাবেচা সহায়তা', nameEn: 'Land & Plot Buy/Sell Brokerage', slug: 'land-plot-brokerage', sortOrder: 3, isActive: true },
      { id: 1904, categoryId: 19, nameBn: 'রেডি ফ্ল্যাট কেনাবেচা', nameEn: 'Ready Apartment Buy/Sell', slug: 'ready-apartment-buysell', sortOrder: 4, isActive: true },
    ]
  },

  // 20. যন্ত্রপাতি ও সরঞ্জাম ভাড়া (Equipment & Tool Rental)
  {
    id: 20,
    nameBn: 'যন্ত্রপাতি ও সরঞ্জাম ভাড়া',
    nameEn: 'Equipment & Tool Rental',
    slug: 'equipment-tool-rental',
    icon: 'package',
    descriptionBn: 'জেনারেটর, সাটারিং পাইপ, কংক্রিট মিক্সার মেশিন ও পাওয়ার টুলস ভাড়া',
    descriptionEn: 'Generator, scaffolding pipes, concrete mixer and power tools rental',
    sortOrder: 20,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 2001, categoryId: 20, nameBn: 'শিল্প ও ইভেন্ট জেনারেটর ভাড়া', nameEn: 'Industrial & Event Generator Rental', slug: 'industrial-generator-rental', sortOrder: 1, isActive: true },
      { id: 2002, categoryId: 20, nameBn: 'ঢালাই মিক্সার মেশিন ও ভাইব্রেটর ভাড়া', nameEn: 'Concrete Mixer & Vibrator Rental', slug: 'concrete-mixer-rental', sortOrder: 2, isActive: true },
      { id: 2003, categoryId: 20, nameBn: 'সাটারিং পাইপ, প্রপস ও বাঁশ-মাচা ভাড়া', nameEn: 'Scaffolding Pipe, Props & Bamboo Rental', slug: 'scaffolding-pipe-rental', sortOrder: 3, isActive: true },
      { id: 2004, categoryId: 20, nameBn: 'পাওয়ার টুলস ও ড্রিল মেশিন ভাড়া', nameEn: 'Power Tools & Drill Machine Rental', slug: 'power-tools-rental', sortOrder: 4, isActive: true },
    ]
  },

  // 21. অন্যান্য স্থানীয় সেবা (Other Local Services)
  {
    id: 21,
    nameBn: 'অন্যান্য স্থানীয় সেবা',
    nameEn: 'Other Local Services',
    slug: 'other-local-services',
    icon: 'grid',
    descriptionBn: 'লন্ড্রি, জুতা মেরামত, ছাতা মেরামত, চাবি প্রস্তুত ও স্থানীয় বিবিধ কারিগর',
    descriptionEn: 'Laundry, cobbler, umbrella repair, duplicate key and other artisan skills',
    sortOrder: 21,
    isActive: true,
    isFeatured: false,
    subCategories: [
      { id: 2101, categoryId: 21, nameBn: 'লন্ড্রি ও ড্রাই ওয়াশ', nameEn: 'Laundry & Dry Cleaning', slug: 'laundry-dry-cleaning', sortOrder: 1, isActive: true },
      { id: 2102, categoryId: 21, nameBn: 'মুচি ও চামড়ার ব্যাগ-জুতা মেরামত', nameEn: 'Cobbler & Leather Bag/Shoe Repair', slug: 'cobbler-leather-repair', sortOrder: 2, isActive: true },
      { id: 2103, categoryId: 21, nameBn: 'ছাতা ও রেইনকোট মেরামত', nameEn: 'Umbrella & Raincoat Repair', slug: 'umbrella-raincoat-repair', sortOrder: 3, isActive: true },
      { id: 2104, categoryId: 21, nameBn: 'ডুপ্লিকেট চাবি তৈরি ও লক মেকার', nameEn: 'Duplicate Key & Lock Maker', slug: 'duplicate-key-lock-maker', sortOrder: 4, isActive: true },
      { id: 2105, categoryId: 21, nameBn: 'স্থানীয় সাধারণ দিনমজুর (অদক্ষ লেবার)', nameEn: 'General Day Labour & Daily Worker', slug: 'general-day-labour', sortOrder: 5, isActive: true },
    ]
  }
];

// Flat export of all sub-categories with parent category name for search indexing
export const ALL_MASTER_SUB_CATEGORIES: MasterSubCategory[] = SEBACOX_MASTER_CATEGORIES.flatMap(
  cat => cat.subCategories
);
