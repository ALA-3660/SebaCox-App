/**
 * SebaCox Phase 5: Provider Foundation Mock Data
 * মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
 * সহায়ক পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
 * Architectural Principle: User ≠ Provider ≠ Service
 */

export interface MockProviderService {
  id: number;
  name_bn: string;
  name_en: string;
  category_name_bn: string;
  pricing_model: 'FIXED' | 'HOURLY' | 'NEGOTIABLE';
  base_price: number;
  is_active: boolean;
}

export interface MockProviderArea {
  upazila_id: number;
  upazila_name_bn: string;
  upazila_name_en: string;
  is_primary: boolean;
}

export interface MockProvider {
  id: number;
  business_name: string;
  owner_name: string;
  provider_type: 'INDIVIDUAL' | 'BUSINESS' | 'ORGANIZATION';
  bio: string;
  experience_years: number;
  status: 'DRAFT' | 'PENDING_VERIFICATION' | 'ACTIVE' | 'SUSPENDED' | 'REJECTED' | 'INACTIVE';
  availability_status: 'ONLINE' | 'OFFLINE' | 'BUSY' | 'ON_BREAK';
  is_verified: boolean;
  rating: number;
  review_count: number;
  total_completed_services: number;
  contact_visibility: 'PUBLIC' | 'REGISTERED_ONLY' | 'ON_REQUEST' | 'HIDDEN';
  phone: string;
  primary_area: {
    id: number;
    name_bn: string;
    name_en: string;
  };
  service_areas: MockProviderArea[];
  services: MockProviderService[];
  created_at: string;
}

export const INITIAL_MOCK_PROVIDERS: MockProvider[] = [
  {
    id: 101,
    business_name: 'সৈকত ইলেকট্রিক্যাল অ্যান্ড এসি সল্যুশন',
    owner_name: 'মো: রফিকুল ইসলাম',
    provider_type: 'BUSINESS',
    bio: 'কক্সবাজার সদর ও কলাতলী বিচ এলাকায় দক্ষ ইলেকট্রিশিয়ান ও ইনভার্টার এসি সার্ভিসিং স্পেশালিস্ট। ৭ বছরের অভিজ্ঞতা।',
    experience_years: 7,
    status: 'ACTIVE',
    availability_status: 'ONLINE',
    is_verified: true,
    rating: 4.9,
    review_count: 38,
    total_completed_services: 142,
    contact_visibility: 'PUBLIC',
    phone: '+8801819234567',
    primary_area: {
      id: 1,
      name_bn: 'কক্সবাজার সদর',
      name_en: "Cox's Bazar Sadar"
    },
    service_areas: [
      { upazila_id: 1, upazila_name_bn: 'কক্সবাজার সদর', upazila_name_en: "Cox's Bazar Sadar", is_primary: true },
      { upazila_id: 4, upazila_name_bn: 'রামু', upazila_name_en: 'Ramu', is_primary: false },
      { upazila_id: 9, upazila_name_bn: 'ঈদগাঁও', upazila_name_en: 'Eidgaon', is_primary: false }
    ],
    services: [
      {
        id: 1,
        name_bn: 'এসি মেরামত ও গ্যাস রিফিল',
        name_en: 'AC Repair & Gas Refill',
        category_name_bn: 'বাসাবাড়ির মেরামত ও রক্ষনাবেক্ষন',
        pricing_model: 'FIXED',
        base_price: 1500,
        is_active: true
      },
      {
        id: 2,
        name_bn: 'বাসাবাড়ি বৈদ্যুতিক ওয়্যারিং সার্ভিস',
        name_en: 'Home Electrical Wiring',
        category_name_bn: 'বাসাবাড়ির মেরামত ও রক্ষনাবেক্ষন',
        pricing_model: 'HOURLY',
        base_price: 350,
        is_active: true
      }
    ],
    created_at: '2026-03-01'
  },
  {
    id: 102,
    business_name: 'হিমছড়ি ট্যুরিস্ট কার ও সি-বীচ জিপ সার্ভিস',
    owner_name: 'তাহমিদ চৌধুরী',
    provider_type: 'BUSINESS',
    bio: 'কক্সবাজার-ইনানী-টেকনাফ মেরিন ড্রাইভে নিরাপদ ও আধুনিক ট্যুরিস্ট কার ও চাঁন্দের গাড়ি সার্ভিস। ২৪/৭ সার্বক্ষণিক সার্ভিস।',
    experience_years: 5,
    status: 'ACTIVE',
    availability_status: 'BUSY',
    is_verified: true,
    rating: 4.8,
    review_count: 52,
    total_completed_services: 215,
    contact_visibility: 'PUBLIC',
    phone: '+8801711987654',
    primary_area: {
      id: 1,
      name_bn: 'কক্সবাজার সদর',
      name_en: "Cox's Bazar Sadar"
    },
    service_areas: [
      { upazila_id: 1, upazila_name_bn: 'কক্সবাজার সদর', upazila_name_en: "Cox's Bazar Sadar", is_primary: true },
      { upazila_id: 4, upazila_name_bn: 'রামু', upazila_name_en: 'Ramu', is_primary: false },
      { upazila_id: 5, upazila_name_bn: 'টেকনাফ', upazila_name_en: 'Teknaf', is_primary: false }
    ],
    services: [
      {
        id: 3,
        name_bn: 'ইনানী-হিমছড়ি ডে-ট্যুর জিপ রেন্টাল',
        name_en: 'Inani-Himchhari Day Tour Jeep',
        category_name_bn: 'পর্যটন ও ভ্রমণ গাইড',
        pricing_model: 'FIXED',
        base_price: 4500,
        is_active: true
      },
      {
        id: 4,
        name_bn: 'কক্সবাজার এয়ারপোর্ট পিক অ্যান্ড ড্রপ',
        name_en: 'Cox Airport Pick & Drop',
        category_name_bn: 'পরিবহন ও যাতায়াত',
        pricing_model: 'FIXED',
        base_price: 600,
        is_active: true
      }
    ],
    created_at: '2026-02-15'
  },
  {
    id: 103,
    business_name: 'কক্স কেয়ার হোম নার্সিং ও ল্যাব স্যাম্পল',
    owner_name: 'সাজেদা পারভীন (ডিপ্লোমা নার্স)',
    provider_type: 'INDIVIDUAL',
    bio: 'বয়স্ক ও রোগীদের ঘরে বসে ইনজেকশন, স্যালাইন, ড্রেসিং ও অভিজ্ঞ প্যাথলজিস্ট দ্বারা রক্ত স্যাম্পল সংগ্রহ সেবা।',
    experience_years: 6,
    status: 'ACTIVE',
    availability_status: 'ONLINE',
    is_verified: true,
    rating: 5.0,
    review_count: 24,
    total_completed_services: 89,
    contact_visibility: 'REGISTERED_ONLY',
    phone: '+8801612345678',
    primary_area: {
      id: 1,
      name_bn: 'কক্সবাজার সদর',
      name_en: "Cox's Bazar Sadar"
    },
    service_areas: [
      { upazila_id: 1, upazila_name_bn: 'কক্সবাজার সদর', upazila_name_en: "Cox's Bazar Sadar", is_primary: true },
      { upazila_id: 9, upazila_name_bn: 'ঈদগাঁও', upazila_name_en: 'Eidgaon', is_primary: false }
    ],
    services: [
      {
        id: 5,
        name_bn: 'বাসায় নার্সিং কেয়ার ও ড্রেসিং',
        name_en: 'Home Nursing Care & Dressing',
        category_name_bn: 'স্বাস্থ্য ও চিকিৎসা সেবা',
        pricing_model: 'HOURLY',
        base_price: 500,
        is_active: true
      },
      {
        id: 6,
        name_bn: 'বাসা থেকে ল্যাব টেস্ট স্যাম্পল কালেকশন',
        name_en: 'Home Blood Sample Collection',
        category_name_bn: 'স্বাস্থ্য ও চিকিৎসা সেবা',
        pricing_model: 'FIXED',
        base_price: 250,
        is_active: true
      }
    ],
    created_at: '2026-03-05'
  },
  {
    id: 104,
    business_name: 'চকোরিয়া অটো ব্রিকস ও নির্মাণ সামগ্রী সরবরাহ',
    owner_name: 'আলহাজ্ব কবির আহমেদ',
    provider_type: 'ORGANIZATION',
    bio: 'চকোরিয়া ও পেকুয়ায় অটো ক্লিংকার ফার্স্ট ক্লাস ইট, বালু ও রড সাইটে দ্রুত ডেলিভারি দেওয়া হয়। পাইকারি মূল্যে অর্ডার নেওয়া হয়।',
    experience_years: 12,
    status: 'ACTIVE',
    availability_status: 'ONLINE',
    is_verified: true,
    rating: 4.7,
    review_count: 45,
    total_completed_services: 178,
    contact_visibility: 'PUBLIC',
    phone: '+8801815555444',
    primary_area: {
      id: 2,
      name_bn: 'চকোরিয়া',
      name_en: 'Chakaria'
    },
    service_areas: [
      { upazila_id: 2, upazila_name_bn: 'চকোরিয়া', upazila_name_en: 'Chakaria', is_primary: true },
      { upazila_id: 8, upazila_name_bn: 'পেকুয়া', upazila_name_en: 'Pekua', is_primary: false },
      { upazila_id: 9, upazila_name_bn: 'ঈদগাঁও', upazila_name_en: 'Eidgaon', is_primary: false }
    ],
    services: [
      {
        id: 7,
        name_bn: '১ম শ্রেণির অটো ব্রিকস (প্রতি হাজার)',
        name_en: 'First Class Auto Bricks',
        category_name_bn: 'নির্মাণ সামগ্রী ও হার্ডওয়্যার',
        pricing_model: 'NEGOTIABLE',
        base_price: 12500,
        is_active: true
      }
    ],
    created_at: '2026-01-20'
  },
  {
    id: 105,
    business_name: 'উখিয়া পাইপলাইন ও স্যানিটারি ওয়ার্কস',
    owner_name: 'করিম উল্লাহ',
    provider_type: 'INDIVIDUAL',
    bio: 'উখিয়া কোর্টবাজার ও মরিচ্যা এলাকায় আবাসিক ও বাণিজ্যিক ভবনের নতুন পানির লাইন স্থাপন ও ড্রেন ক্লিনিং।',
    experience_years: 4,
    status: 'PENDING_VERIFICATION',
    availability_status: 'OFFLINE',
    is_verified: false,
    rating: 4.5,
    review_count: 8,
    total_completed_services: 32,
    contact_visibility: 'PUBLIC',
    phone: '+8801755123987',
    primary_area: {
      id: 6,
      name_bn: 'উখিয়া',
      name_en: 'Ukhiya'
    },
    service_areas: [
      { upazila_id: 6, upazila_name_bn: 'উখিয়া', upazila_name_en: 'Ukhiya', is_primary: true }
    ],
    services: [
      {
        id: 8,
        name_bn: 'প্লাম্বিং লাইন ও পানির মোটর ইনস্টলেশন',
        name_en: 'Plumbing & Water Motor Installation',
        category_name_bn: 'বাসাবাড়ির মেরামত ও রক্ষনাবেক্ষন',
        pricing_model: 'HOURLY',
        base_price: 300,
        is_active: true
      }
    ],
    created_at: '2026-03-10'
  }
];
