// SebaCox Cox's Bazar Sadar Complete Address Master
// Production-Grade Address Data Architecture
// Covers: Upazilas, Postal Locations, Unions/Municipalities, Wards, and Ward-level Localities/Paras/Mohollas

export interface CoxUpazila {
  id: number;
  nameBn: string;
  nameEn: string;
}

export interface CoxPostalLocation {
  id: number;
  upazilaId: number;
  nameBn: string;
  nameEn: string;
  postCode: string;
  defaultUnionId?: number;
}

export interface CoxUnion {
  id: number;
  nameBn: string;
  nameEn?: string;
  type: 'MUNICIPALITY' | 'UNION';
  defaultPostCode: string;
}

export interface CoxWard {
  id: number;
  nameBn: string;
  wardNumber: number;
}

export interface CoxLocality {
  id: number;
  nameBn: string;
  nameEn?: string;
  type: string;
}

export const COX_UPAZILAS: CoxUpazila[] = [
  { id: 1, nameBn: 'কক্সবাজার সদর', nameEn: "Cox's Bazar Sadar" },
  { id: 2, nameBn: 'চকোরিয়া', nameEn: 'Chakaria' },
  { id: 3, nameBn: 'মহেশখালী', nameEn: 'Maheshkhali' },
  { id: 4, nameBn: 'রামু', nameEn: 'Ramu' },
  { id: 5, nameBn: 'টেকনাফ', nameEn: 'Teknaf' },
  { id: 6, nameBn: 'উখিয়া', nameEn: 'Ukhiya' },
  { id: 7, nameBn: 'কুতুবদিয়া', nameEn: 'Kutubdia' },
  { id: 8, nameBn: 'পেকুয়া', nameEn: 'Pekua' },
  { id: 9, nameBn: 'ঈদগাঁও', nameEn: 'Eidgaon' },
];

export const COX_POSTAL_LOCATIONS: CoxPostalLocation[] = [
  { id: 1, upazilaId: 1, nameBn: 'কক্সবাজার প্রধান ডাকঘর', nameEn: "Cox's Bazar Head Post Office", postCode: '4700', defaultUnionId: 101 },
  { id: 2, upazilaId: 1, nameBn: 'ঝিলংঝা সাব-পোস্ট অফিস', nameEn: 'Jhilongjha Sub Post Office', postCode: '4701', defaultUnionId: 102 },
  { id: 3, upazilaId: 1, nameBn: 'ঈদগাঁও সাব-পোস্ট অফিস', nameEn: 'Eidgaon Sub Post Office', postCode: '4702' },
  { id: 4, upazilaId: 1, nameBn: 'খুরুশকুল শাখা ডাকঘর', nameEn: 'Khurushkul Branch Post Office', postCode: '4700', defaultUnionId: 104 },
  { id: 5, upazilaId: 1, nameBn: 'চৌফলদণ্ডী শাখা ডাকঘর', nameEn: 'Chowfaldandi Branch Post Office', postCode: '4700', defaultUnionId: 105 },
  { id: 6, upazilaId: 1, nameBn: 'ভারুয়াখালী শাখা ডাকঘর', nameEn: 'Varuakhali Branch Post Office', postCode: '4700', defaultUnionId: 106 },
  { id: 7, upazilaId: 1, nameBn: 'পিএমখালী শাখা ডাকঘর', nameEn: 'PM Khali Branch Post Office', postCode: '4700', defaultUnionId: 103 },
];

export const COX_UNIONS: Record<number, CoxUnion[]> = {
  1: [
    { id: 101, nameBn: 'কক্সবাজার পৌরসভা', nameEn: "Cox's Bazar Municipality", type: 'MUNICIPALITY', defaultPostCode: '4700' },
    { id: 102, nameBn: 'ঝিলংঝা ইউনিয়ন', nameEn: 'Jhilongjha Union', type: 'UNION', defaultPostCode: '4701' },
    { id: 103, nameBn: 'পিএমখালী ইউনিয়ন', nameEn: 'PM Khali Union', type: 'UNION', defaultPostCode: '4700' },
    { id: 104, nameBn: 'খুরুশকুল ইউনিয়ন', nameEn: 'Khurushkul Union', type: 'UNION', defaultPostCode: '4700' },
    { id: 105, nameBn: 'চৌফলদণ্ডী ইউনিয়ন', nameEn: 'Chowfaldandi Union', type: 'UNION', defaultPostCode: '4700' },
    { id: 106, nameBn: 'ভারুয়াখালী ইউনিয়ন', nameEn: 'Varuakhali Union', type: 'UNION', defaultPostCode: '4700' },
  ],
  2: [
    { id: 201, nameBn: 'চকোরিয়া পৌরসভা', nameEn: 'Chakaria Municipality', type: 'MUNICIPALITY', defaultPostCode: '4740' },
    { id: 202, nameBn: 'কাকারা ইউনিয়ন', nameEn: 'Kakara Union', type: 'UNION', defaultPostCode: '4740' },
    { id: 203, nameBn: 'ডুলাহাজারা ইউনিয়ন', nameEn: 'Dulahazara Union', type: 'UNION', defaultPostCode: '4742' },
    { id: 204, nameBn: 'হারবাং ইউনিয়ন', nameEn: 'Harbang Union', type: 'UNION', defaultPostCode: '4740' },
  ],
  4: [
    { id: 401, nameBn: 'ফতেখাঁরকূল ইউনিয়ন', nameEn: 'Fatekharkul Union', type: 'UNION', defaultPostCode: '4730' },
    { id: 402, nameBn: 'জোয়ারিয়ানালা ইউনিয়ন', nameEn: 'Joarianala Union', type: 'UNION', defaultPostCode: '4730' },
    { id: 403, nameBn: 'রশিদনগর ইউনিয়ন', nameEn: 'Rashidnagar Union', type: 'UNION', defaultPostCode: '4730' },
  ],
};

export const COX_WARDS: Record<number, CoxWard[]> = {
  // কক্সবাজার পৌরসভা (Wards 1-12)
  101: [
    { id: 10101, nameBn: '১ নং ওয়ার্ড', wardNumber: 1 },
    { id: 10102, nameBn: '২ নং ওয়ার্ড', wardNumber: 2 },
    { id: 10103, nameBn: '৩ নং ওয়ার্ড', wardNumber: 3 },
    { id: 10104, nameBn: '৪ নং ওয়ার্ড', wardNumber: 4 },
    { id: 10105, nameBn: '৫ নং ওয়ার্ড', wardNumber: 5 },
    { id: 10106, nameBn: '৬ নং ওয়ার্ড', wardNumber: 6 },
    { id: 10107, nameBn: '৭ নং ওয়ার্ড', wardNumber: 7 },
    { id: 10108, nameBn: '৮ নং ওয়ার্ড', wardNumber: 8 },
    { id: 10109, nameBn: '৯ নং ওয়ার্ড', wardNumber: 9 },
    { id: 10110, nameBn: '১০ নং ওয়ার্ড', wardNumber: 10 },
    { id: 10111, nameBn: '১১ নং ওয়ার্ড', wardNumber: 11 },
    { id: 10112, nameBn: '১২ নং ওয়ার্ড', wardNumber: 12 },
  ],
  // ঝিলংঝা ইউনিয়ন (Wards 1-9)
  102: [
    { id: 10201, nameBn: '১ নং ওয়ার্ড', wardNumber: 1 },
    { id: 10202, nameBn: '২ নং ওয়ার্ড', wardNumber: 2 },
    { id: 10203, nameBn: '৩ নং ওয়ার্ড', wardNumber: 3 },
    { id: 10204, nameBn: '৪ নং ওয়ার্ড', wardNumber: 4 },
    { id: 10205, nameBn: '৫ নং ওয়ার্ড', wardNumber: 5 },
    { id: 10206, nameBn: '৬ নং ওয়ার্ড', wardNumber: 6 },
    { id: 10207, nameBn: '৭ নং ওয়ার্ড', wardNumber: 7 },
    { id: 10208, nameBn: '৮ নং ওয়ার্ড', wardNumber: 8 },
    { id: 10209, nameBn: '৯ নং ওয়ার্ড', wardNumber: 9 },
  ],
  // পিএমখালী ইউনিয়ন (Wards 1-9)
  103: [
    { id: 10301, nameBn: '১ নং ওয়ার্ড', wardNumber: 1 },
    { id: 10302, nameBn: '২ নং ওয়ার্ড', wardNumber: 2 },
    { id: 10303, nameBn: '৩ নং ওয়ার্ড', wardNumber: 3 },
    { id: 10304, nameBn: '৪ নং ওয়ার্ড', wardNumber: 4 },
    { id: 10305, nameBn: '৫ নং ওয়ার্ড', wardNumber: 5 },
    { id: 10306, nameBn: '৬ নং ওয়ার্ড', wardNumber: 6 },
    { id: 10307, nameBn: '৭ নং ওয়ার্ড', wardNumber: 7 },
    { id: 10308, nameBn: '৮ নং ওয়ার্ড', wardNumber: 8 },
    { id: 10309, nameBn: '৯ নং ওয়ার্ড', wardNumber: 9 },
  ],
  // খুরুশকুল ইউনিয়ন (Wards 1-9)
  104: [
    { id: 10401, nameBn: '১ নং ওয়ার্ড', wardNumber: 1 },
    { id: 10402, nameBn: '২ নং ওয়ার্ড', wardNumber: 2 },
    { id: 10403, nameBn: '৩ নং ওয়ার্ড', wardNumber: 3 },
    { id: 10404, nameBn: '৪ নং ওয়ার্ড', wardNumber: 4 },
    { id: 10405, nameBn: '৫ নং ওয়ার্ড', wardNumber: 5 },
    { id: 10406, nameBn: '৬ নং ওয়ার্ড', wardNumber: 6 },
    { id: 10407, nameBn: '৭ নং ওয়ার্ড', wardNumber: 7 },
    { id: 10408, nameBn: '৮ নং ওয়ার্ড', wardNumber: 8 },
    { id: 10409, nameBn: '৯ নং ওয়ার্ড', wardNumber: 9 },
  ],
  // চৌফলদণ্ডী ইউনিয়ন (Wards 1-9)
  105: [
    { id: 10501, nameBn: '১ নং ওয়ার্ড', wardNumber: 1 },
    { id: 10502, nameBn: '২ নং ওয়ার্ড', wardNumber: 2 },
    { id: 10503, nameBn: '৩ নং ওয়ার্ড', wardNumber: 3 },
    { id: 10504, nameBn: '৪ নং ওয়ার্ড', wardNumber: 4 },
    { id: 10505, nameBn: '৫ নং ওয়ার্ড', wardNumber: 5 },
    { id: 10506, nameBn: '৬ নং ওয়ার্ড', wardNumber: 6 },
    { id: 10507, nameBn: '৭ নং ওয়ার্ড', wardNumber: 7 },
    { id: 10508, nameBn: '৮ নং ওয়ার্ড', wardNumber: 8 },
    { id: 10509, nameBn: '৯ নং ওয়ার্ড', wardNumber: 9 },
  ],
  // ভারুয়াখালী ইউনিয়ন (Wards 1-9)
  106: [
    { id: 10601, nameBn: '১ নং ওয়ার্ড', wardNumber: 1 },
    { id: 10602, nameBn: '২ নং ওয়ার্ড', wardNumber: 2 },
    { id: 10603, nameBn: '৩ নং ওয়ার্ড', wardNumber: 3 },
    { id: 10604, nameBn: '৪ নং ওয়ার্ড', wardNumber: 4 },
    { id: 10605, nameBn: '৫ নং ওয়ার্ড', wardNumber: 5 },
    { id: 10606, nameBn: '৬ নং ওয়ার্ড', wardNumber: 6 },
    { id: 10607, nameBn: '৭ নং ওয়ার্ড', wardNumber: 7 },
    { id: 10608, nameBn: '৮ নং ওয়ার্ড', wardNumber: 8 },
    { id: 10609, nameBn: '৯ নং ওয়ার্ড', wardNumber: 9 },
  ],
};

export const COX_LOCALITIES: Record<number, CoxLocality[]> = {
  // পৌরসভা Ward 1-12
  10101: [
    { id: 101011, nameBn: 'সমিতি পাড়া', type: 'পাড়া' },
    { id: 101012, nameBn: 'কুতুবদিয়া পাড়া', type: 'পাড়া' },
    { id: 101013, nameBn: 'মুস্তাক পাড়া', type: 'পাড়া' },
    { id: 101014, nameBn: 'সৈকত এলাকা', type: 'লোকাল এলাকা' },
  ],
  10102: [
    { id: 101021, nameBn: 'মাঝির পাড়া', type: 'পাড়া' },
    { id: 101022, nameBn: 'উত্তর রুমালিয়ারছড়া', type: 'মহল্লা' },
    { id: 101023, nameBn: 'নুনিয়াছটা', type: 'মহল্লা' },
  ],
  10103: [
    { id: 101031, nameBn: 'মাছূয়া পাড়া', type: 'পাড়া' },
    { id: 101032, nameBn: 'উত্তর তারাবনিয়ারছড়া', type: 'মহল্লা' },
  ],
  10104: [
    { id: 101041, nameBn: 'তারাবনিয়ারছড়া', type: 'মহল্লা' },
    { id: 101042, nameBn: 'বার্মিজ মার্কেট এলাকা', type: 'বাজার' },
    { id: 101043, nameBn: 'মডেল হাই স্কুল এলাকা', type: 'লোকাল এলাকা' },
  ],
  10105: [
    { id: 101051, nameBn: 'টেকপাড়া', type: 'মহল্লা' },
    { id: 101052, nameBn: 'গোলদিঘীর পাড়', type: 'আবাসিক এলাকা' },
    { id: 101053, nameBn: 'আলীর জাহান', type: 'মহল্লা' },
  ],
  10106: [
    { id: 101061, nameBn: 'রুমালিয়ারছড়া', type: 'মহল্লা' },
    { id: 101062, nameBn: 'হাসেমিয়া মাদ্রাসা এলাকা', type: 'লোকাল এলাকা' },
    { id: 101063, nameBn: 'কায়ুকখালীয়া পাড়া', type: 'পাড়া' },
  ],
  10107: [
    { id: 101071, nameBn: 'পাহাড়তলী', type: 'মহল্লা' },
    { id: 101072, nameBn: 'ইসলামপুর এলাকা', type: 'মহল্লা' },
  ],
  10108: [
    { id: 101081, nameBn: 'বৈদ্যঘোনা', type: 'মহল্লা' },
    { id: 101082, nameBn: 'ডিসি অফিস ও কোর্ট হিল এলাকা', type: 'প্রশাসনিক এলাকা' },
  ],
  10109: [
    { id: 101091, nameBn: 'ঘোনারপাড়া', type: 'মহল্লা' },
    { id: 101092, nameBn: 'লামা বাজার', type: 'বাজার' },
  ],
  10110: [
    { id: 101101, nameBn: 'ঝাউতলা', type: 'মহল্লা' },
    { id: 101102, nameBn: 'বিজিবি ক্যাম্প এলাকা', type: 'লোকাল এলাকা' },
    { id: 101103, nameBn: 'হোটেল মোটেল জোন উত্তর', type: 'পর্যটন জোন' },
    { id: 101104, nameBn: 'সার্কিট হাউস এলাকা', type: 'প্রশাসনিক এলাকা' },
  ],
  10111: [
    { id: 101111, nameBn: 'সুগন্ধা পয়েন্ট', type: 'পর্যটন পয়েন্ট' },
    { id: 101112, nameBn: 'লাবণী পয়েন্ট', type: 'পর্যটন পয়েন্ট' },
    { id: 101113, nameBn: 'সায়মন রোড এলাকা', type: 'লোকাল এলাকা' },
    { id: 101114, nameBn: 'সী ইন পয়েন্ট', type: 'পর্যটন পয়েন্ট' },
    { id: 101115, nameBn: 'ডলফিন মোড়', type: 'মোড়/পয়েন্ট' },
  ],
  10112: [
    { id: 101121, nameBn: 'কলাতলী', type: 'আবাসিক/পর্যটন' },
    { id: 101122, nameBn: 'কলাতলী লাইট হাউস এলাকা', type: 'লোকাল এলাকা' },
    { id: 101123, nameBn: 'মেরিন ড্রাইভ প্রবেশমুখ', type: 'হাইওয়ে এলাকা' },
    { id: 101124, nameBn: 'দক্ষিণ কলাতলী', type: 'পাড়া' },
  ],
  // ঝিলংঝা ইউনিয়ন Wards 1-9
  10201: [
    { id: 102011, nameBn: 'খরুলিয়া', type: 'গ্রাম' },
    { id: 102012, nameBn: 'খরুলিয়া বাজার', type: 'বাজার' },
  ],
  10202: [
    { id: 102021, nameBn: 'পশ্চিম খরুলিয়া', type: 'গ্রাম' },
    { id: 102022, nameBn: 'ঘাটপাড়া', type: 'পাড়া' },
  ],
  10203: [
    { id: 102031, nameBn: 'বাংলাবাজার', type: 'বাজার' },
    { id: 102032, nameBn: 'সিকদারপাড়া', type: 'পাড়া' },
  ],
  10204: [
    { id: 102041, nameBn: 'লিংকরোড', type: 'মোড়/লোকাল এলাকা' },
    { id: 102042, nameBn: 'লিংকরোড বাজার মোড়', type: 'বাজার' },
  ],
  10205: [
    { id: 102051, nameBn: 'লারপাড়া', type: 'গ্রাম' },
    { id: 102052, nameBn: 'বাস টার্মিনাল এলাকা', type: 'টার্মিনাল এলাকা' },
  ],
  10206: [
    { id: 102061, nameBn: 'মুহুরীপাড়া', type: 'পাড়া' },
    { id: 102062, nameBn: 'চান্দেরপাড়া', type: 'পাড়া' },
  ],
  10207: [
    { id: 102071, nameBn: 'দক্ষিণ মুহুরীপাড়া', type: 'পাড়া' },
    { id: 102082, nameBn: 'ডিককুল', type: 'গ্রাম' },
  ],
  10208: [
    { id: 102081, nameBn: 'পূর্ব খরুলিয়া', type: 'গ্রাম' },
    { id: 102082, nameBn: 'তালতলী', type: 'পাড়া' },
  ],
  10209: [
    { id: 102091, nameBn: 'উত্তর ঝিলংঝা', type: 'গ্রাম' },
    { id: 102092, nameBn: 'হাজীপাড়া', type: 'পাড়া' },
  ],
  // পিএমখালী ইউনিয়ন Wards 1-9
  10301: [
    { id: 103011, nameBn: 'ঘাটকুলিয়া', type: 'গ্রাম' },
    { id: 103012, nameBn: 'ঘাটকুলিয়া বাজার', type: 'বাজার' },
  ],
  10302: [
    { id: 103021, nameBn: 'তোতকখালী', type: 'গ্রাম' },
    { id: 103022, nameBn: 'পশ্চিম তোতকখালী', type: 'পাড়া' },
  ],
  10303: [
    { id: 103031, nameBn: 'জুমছড়ি', type: 'গ্রাম' },
    { id: 103032, nameBn: 'জুমছড়ি দক্ষিণপাড়া', type: 'পাড়া' },
  ],
  10304: [
    { id: 103041, nameBn: 'ছনখোলা', type: 'গ্রাম' },
    { id: 103042, nameBn: 'ছনখোলা বাজার', type: 'বাজার' },
  ],
  10305: [
    { id: 103051, nameBn: 'রাজঘাট', type: 'লোকাল এলাকা' },
    { id: 103052, nameBn: 'রাজঘাট সেতু এলাকা', type: 'সেতু পয়েন্ট' },
  ],
  10306: [
    { id: 103061, nameBn: 'ডিকপাড়া', type: 'পাড়া' },
    { id: 103062, nameBn: 'খুইশাতলী', type: 'গ্রাম' },
  ],
  10307: [
    { id: 103071, nameBn: 'নয়াপাড়া', type: 'পাড়া' },
    { id: 103072, nameBn: 'সিকদারপাড়া', type: 'পাড়া' },
  ],
  10308: [
    { id: 103081, nameBn: 'মুহুরীঘোনা', type: 'গ্রাম' },
    { id: 103082, nameBn: 'পূর্ব মুহুরীঘোনা', type: 'পাড়া' },
  ],
  10309: [
    { id: 103091, nameBn: 'বাংলাবাজার সংলগ্ন', type: 'লোকাল এলাকা' },
    { id: 103092, nameBn: 'মাছুয়াখালী', type: 'গ্রাম' },
  ],
  // খুরুশকুল ইউনিয়ন Wards 1-9 (Official Government Source: Khurushkul Union Parishad Portal V2)
  10401: [
    { id: 104011, nameBn: 'তেতৈয়া সওদাগর পাড়া ও মিয়াজি পাড়া', type: 'পাড়া' },
    { id: 104012, nameBn: 'তেতৈয়া ইউছুপ ফকির পাড়া', type: 'পাড়া' },
    { id: 104013, nameBn: 'তেতৈয়া জলিয়া বাপের পাড়া', type: 'পাড়া' },
    { id: 104014, nameBn: 'তেতৈয়া সিকদার পাড়া', type: 'পাড়া' },
    { id: 104015, nameBn: 'তেতৈয়া গুইল্যা বাপের পাড়া', type: 'পাড়া' },
  ],
  10402: [
    { id: 104021, nameBn: 'তেতৈয়া নতুন ঘোনার পাড়া', type: 'পাড়া' },
    { id: 104022, nameBn: 'ডেইল পাড়া', type: 'পাড়া' },
  ],
  10403: [
    { id: 104031, nameBn: 'পেচাঁর ঘোনা', type: 'পাড়া' },
    { id: 104032, nameBn: 'রাস্তার পাড়া', type: 'পাড়া' },
    { id: 104033, nameBn: 'জালিয়া পাড়া(রাখাইন পাড়া)', type: 'পাড়া' },
  ],
  10404: [
    { id: 104041, nameBn: 'কাউয়ার পাড়া', type: 'পাড়া' },
    { id: 104042, nameBn: 'ফকির পাড়া', type: 'পাড়া' },
    { id: 104043, nameBn: 'আদর্শ গ্রাম(ফকির পাড়া)', type: 'পাড়া' },
  ],
  10405: [
    { id: 104051, nameBn: 'মামুন পাড়া', type: 'পাড়া' },
    { id: 104052, nameBn: 'হাট খোলা পাড়া', type: 'পাড়া' },
    { id: 104053, nameBn: 'জানা পাড়া', type: 'পাড়া' },
  ],
  10406: [
    { id: 104061, nameBn: 'হামজার ডেইল', type: 'পাড়া' },
    { id: 104062, nameBn: 'ঘোনার পাড়া', type: 'পাড়া' },
    { id: 104063, nameBn: 'আদর্শ গ্রাম পাহাড়তলী', type: 'পাড়া' },
    { id: 104064, nameBn: 'পূর্ব হিন্দু পাড়া', type: 'পাড়া' },
    { id: 104065, nameBn: 'পাল পাড়া', type: 'পাড়া' },
  ],
  10407: [
    { id: 104071, nameBn: 'রুদ্র পাড়া', type: 'পাড়া' },
    { id: 104072, nameBn: 'উত্তর হিন্দু পাড়া', type: 'পাড়া' },
    { id: 104073, nameBn: 'গাজীর ডেইল', type: 'পাড়া' },
    { id: 104074, nameBn: 'পঞ্চায়েত পাড়া', type: 'পাড়া' },
  ],
  10408: [
    { id: 104081, nameBn: 'মনু পাড়া', type: 'পাড়া' },
    { id: 104082, nameBn: 'লমাজি পাড়া', type: 'পাড়া' },
    { id: 104083, nameBn: 'মেহেদী পাড়া', type: 'পাড়া' },
    { id: 104084, nameBn: 'কোনার পাড়া', type: 'পাড়া' },
  ],
  10409: [
    { id: 104091, nameBn: 'দক্ষিণ হিন্দু পাড়া', type: 'পাড়া' },
    { id: 104092, nameBn: 'সাম্পান ঘাট পাড়া', type: 'পাড়া' },
    { id: 104093, nameBn: 'কুলিয়া পাড়া', type: 'পাড়া' },
    { id: 104094, nameBn: 'রুহুল্লার ডেইল', type: 'পাড়া' },
  ],
  // চৌফলদণ্ডী ইউনিয়ন Wards 1-9
  10501: [
    { id: 105011, nameBn: 'নতুন মহাল', type: 'গ্রাম' },
    { id: 105012, nameBn: 'নতুন মহাল বাজার', type: 'বাজার' },
  ],
  10502: [
    { id: 105021, nameBn: 'মাইয়াপাড়া', type: 'পাড়া' },
    { id: 105022, nameBn: 'উত্তর মাইয়াপাড়া', type: 'পাড়া' },
  ],
  10503: [
    { id: 105031, nameBn: 'উত্তরপাড়া', type: 'পাড়া' },
    { id: 105032, nameBn: 'ঘোনাপাড়া', type: 'পাড়া' },
  ],
  10504: [
    { id: 105041, nameBn: 'দক্ষিণপাড়া', type: 'পাড়া' },
    { id: 105042, nameBn: 'খালের মুখ', type: 'লোকাল এলাকা' },
  ],
  10505: [
    { id: 105051, nameBn: 'সিকদারপাড়া', type: 'পাড়া' },
    { id: 105052, nameBn: 'মধ্যম চৌফলদণ্ডী', type: 'গ্রাম' },
  ],
  10506: [
    { id: 105061, nameBn: 'কালু ফকিরপাড়া', type: 'পাড়া' },
    { id: 105062, nameBn: 'জলদাশপাড়া', type: 'পাড়া' },
  ],
  10507: [
    { id: 105071, nameBn: 'পূর্বপাড়া', type: 'পাড়া' },
    { id: 105072, nameBn: 'পাহাড়তলী', type: 'পাড়া' },
  ],
  10508: [
    { id: 105081, nameBn: 'পশ্চিমপাড়া', type: 'পাড়া' },
    { id: 105082, nameBn: 'বেড়িবাঁধ এলাকা', type: 'লোকাল এলাকা' },
  ],
  10509: [
    { id: 105091, nameBn: 'চৌফলদণ্ডী ব্রিজ ঘাট', type: 'ঘাট/পয়েন্ট' },
    { id: 105092, nameBn: 'লবণ মাঠ এলাকা', type: 'লবণ মাঠ' },
  ],
  // ভারুয়াখালী ইউনিয়ন Wards 1-9
  10601: [
    { id: 106011, nameBn: 'উল্টাপাড়া', type: 'গ্রাম' },
    { id: 106012, nameBn: 'উল্টাপাড়া বাজার', type: 'বাজার' },
  ],
  10602: [
    { id: 106021, nameBn: 'বানিয়ারপাড়া', type: 'পাড়া' },
    { id: 106022, nameBn: 'সিকদারপাড়া', type: 'পাড়া' },
  ],
  10603: [
    { id: 106031, nameBn: 'চৌধুরীপাড়া', type: 'পাড়া' },
    { id: 106032, nameBn: 'মিয়াজীপাড়া', type: 'পাড়া' },
  ],
  10604: [
    { id: 106041, nameBn: 'কোনারপাড়া', type: 'পাড়া' },
    { id: 106042, nameBn: 'পশ্চিমপাড়া', type: 'পাড়া' },
  ],
  10605: [
    { id: 106051, nameBn: 'দক্ষিণপাড়া', type: 'পাড়া' },
    { id: 106052, nameBn: 'ঘাটপাড়া', type: 'পাড়া' },
  ],
  10606: [
    { id: 106061, nameBn: 'মাতব্বরপাড়া', type: 'পাড়া' },
    { id: 106062, nameBn: 'মধ্যম ভারুয়াখালী', type: 'গ্রাম' },
  ],
  10607: [
    { id: 106071, nameBn: 'মুন্সীরপাড়া', type: 'পাড়া' },
    { id: 106072, nameBn: 'পূর্বপাড়া', type: 'পাড়া' },
  ],
  10608: [
    { id: 106081, nameBn: 'নয়াপাড়া', type: 'পাড়া' },
    { id: 106082, nameBn: 'বাজার এলাকা', type: 'বাজার' },
  ],
  10609: [
    { id: 106091, nameBn: 'ভারুয়াখালী মোহনা', type: 'মোহনা এলাকা' },
    { id: 106092, nameBn: 'ঘোনাপাড়া', type: 'পাড়া' },
  ],
};
