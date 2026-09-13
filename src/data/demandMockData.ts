/**
 * Authentic Mock Data for SebaCox Demand Engine / “আমার প্রয়োজন”.
 * "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
 * "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
 */

export interface MockDemand {
  id: number;
  requesterId: number;
  requesterName: string;
  contactPhone: string;
  titleBn: string;
  titleEn: string;
  descriptionBn: string;
  descriptionEn: string;
  demandType: 'SERVICE' | 'PRODUCT' | 'RENTAL' | 'BOOKING' | 'MARKETPLACE' | 'INFORMATION' | 'OTHER';
  status: 'DRAFT' | 'PUBLISHED' | 'PAUSED' | 'FULFILLED' | 'CANCELLED' | 'EXPIRED' | 'CLOSED';
  priority: 'NORMAL' | 'URGENT';
  serviceId?: number;
  serviceNameBn?: string;
  categoryId?: number;
  categoryNameBn?: string;
  quantity?: number;
  unit?: string;
  budgetMin?: number;
  budgetMax?: number;
  currency: string;
  upazilaId: number;
  upazilaNameBn: string;
  locationDisplayBn: string;
  visibility: 'PUBLIC' | 'REGISTERED_USERS' | 'PRIVATE';
  contactPreference: 'IN_APP_ONLY' | 'PHONE' | 'BOTH';
  isOwner: boolean;
  publishedAt?: string;
  expiresAt?: string;
  createdAt: string;
}

export const INITIAL_MOCK_DEMANDS: MockDemand[] = [
  {
    id: 1,
    requesterId: 1,
    requesterName: 'মোহাম্মদ করিম',
    contactPhone: '+8801819234567',
    titleBn: 'কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন',
    titleEn: 'Experienced Electrician needed in Cox\'s Bazar Sadar',
    descriptionBn: 'বাসার মূল ডিবি বক্স সার্কিট ব্রেকার ট্রিপ করছে এবং ২য় তলার ওয়্যারিং চেক করে সমাধান করতে হবে। জরুরি কাজ।',
    descriptionEn: 'Main distribution board circuit breaker tripping, need wiring inspection on 2nd floor.',
    demandType: 'SERVICE',
    status: 'PUBLISHED',
    priority: 'URGENT',
    serviceId: 2,
    serviceNameBn: 'ইলেকট্রিক্যাল ওয়্যারিং ও মেরামত',
    categoryId: 2,
    categoryNameBn: 'ইলেকট্রিশিয়ান ও গৃহ মেরামত',
    budgetMin: 800,
    budgetMax: 1500,
    currency: 'BDT',
    upazilaId: 1,
    upazilaNameBn: 'কক্সবাজার সদর',
    locationDisplayBn: 'কলাতলী রোড, কক্সবাজার সদর',
    visibility: 'PUBLIC',
    contactPreference: 'BOTH',
    isOwner: true,
    publishedAt: '2026-09-12T10:00:00Z',
    expiresAt: '2026-09-20T18:00:00Z',
    createdAt: '2026-09-12T09:30:00Z',
  },
  {
    id: 2,
    requesterId: 2,
    requesterName: 'আহমেদ শফিক',
    contactPhone: '+8801712987654',
    titleBn: 'রামু বাইপাসে ৩০০০ পিস অটো ব্রিকস বা ইট প্রয়োজন',
    titleEn: '3000 Auto Bricks needed at Ramu Bypass',
    descriptionBn: 'নির্মাণাধীন সীমানা প্রাচীরের জন্য উন্নত মানের ১ম শ্রেণির অটো ব্রিকস অন-সাইট ডেলিভারিসহ প্রয়োজন।',
    descriptionEn: 'Need 1st class auto bricks with on-site delivery for boundary wall construction.',
    demandType: 'PRODUCT',
    status: 'PUBLISHED',
    priority: 'NORMAL',
    serviceId: 1,
    serviceNameBn: 'অটো ব্রিকস ও নির্মাণ সামগ্রী সরবরাহ',
    categoryId: 1,
    categoryNameBn: 'নির্মাণ ও বিল্ডিং মেটেরিয়ালস',
    quantity: 3000,
    unit: 'পিস',
    budgetMin: 36000,
    budgetMax: 42000,
    currency: 'BDT',
    upazilaId: 4,
    upazilaNameBn: 'রামু',
    locationDisplayBn: 'রামু বাইপাস সংলগ্ন, রামু',
    visibility: 'PUBLIC',
    contactPreference: 'PHONE',
    isOwner: false,
    publishedAt: '2026-09-11T14:20:00Z',
    expiresAt: '2026-09-18T20:00:00Z',
    createdAt: '2026-09-11T13:45:00Z',
  },
  {
    id: 3,
    requesterId: 1,
    requesterName: 'মোহাম্মদ করিম',
    contactPhone: '+8801819234567',
    titleBn: 'টেকনাফ থেকে কক্সবাজার সদর পর্যন্ত পিকআপ বা মিনি ট্রাক ভাড়া',
    titleEn: 'Pickup or Mini Truck rental from Teknaf to Cox\'s Bazar',
    descriptionBn: 'শনিবার সকালে টেকনাফ বন্দর এলাকা থেকে মালামাল আনার জন্য ১ টন ধারণক্ষমতার পিকআপ প্রয়োজন।',
    descriptionEn: 'Need 1-ton pickup truck to transport goods on Saturday morning from Teknaf.',
    demandType: 'RENTAL',
    status: 'DRAFT',
    priority: 'NORMAL',
    serviceId: 3,
    serviceNameBn: 'পিকআপ ও মিনি ট্রাক ভাড়া',
    categoryId: 3,
    categoryNameBn: 'পরিবহন ও রেন্টাল সেবা',
    quantity: 1,
    unit: 'ট্রিপ',
    budgetMin: 4500,
    budgetMax: 5500,
    currency: 'BDT',
    upazilaId: 5,
    upazilaNameBn: 'টেকনাফ',
    locationDisplayBn: 'টেকনাফ স্থলবন্দর সংলগ্ন',
    visibility: 'PUBLIC',
    contactPreference: 'IN_APP_ONLY',
    isOwner: true,
    expiresAt: '2026-09-25T18:00:00Z',
    createdAt: '2026-09-13T08:15:00Z',
  },
  {
    id: 4,
    requesterId: 3,
    requesterName: 'ফারহানা ইসলাম',
    contactPhone: '+8801911443322',
    titleBn: 'ঈদগাঁও বাজারে দক্ষ প্লাম্বার প্রয়োজন',
    titleEn: 'Skilled Plumber needed at Eidgaon Bazar',
    descriptionBn: 'পানির পাইপলাইন লিকেজ ও কিচেন সিঙ্ক পাইপ রিপ্লেসমেন্ট প্রয়োজন। শুক্রবার সকালে কাজ করতে পারলে ভালো।',
    descriptionEn: 'Water pipeline leakage and kitchen sink repair needed in Eidgaon.',
    demandType: 'SERVICE',
    status: 'FULFILLED',
    priority: 'NORMAL',
    serviceId: 2,
    serviceNameBn: 'প্লাম্বিং ও পাইপলাইন মেরামত',
    categoryId: 2,
    categoryNameBn: 'ইলেকট্রিশিয়ান ও গৃহ মেরামত',
    budgetMin: 600,
    budgetMax: 1000,
    currency: 'BDT',
    upazilaId: 9,
    upazilaNameBn: 'ঈদগাঁও',
    locationDisplayBn: 'ঈদগাঁও বাজার সংলগ্ন রোড',
    visibility: 'PUBLIC',
    contactPreference: 'IN_APP_ONLY',
    isOwner: false,
    publishedAt: '2026-09-08T11:00:00Z',
    expiresAt: '2026-09-15T18:00:00Z',
    createdAt: '2026-09-08T10:30:00Z',
  },
];
