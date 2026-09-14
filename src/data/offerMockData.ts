/**
 * Authentic Mock Data for SebaCox Offer & Counter-Offer Engine (Phase 8).
 * "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
 * "ম্যাচ থেকে প্রস্তাব"
 */

export interface MockOffer {
  id: number;
  demandId: number;
  demandTitleBn: string;
  providerId: number;
  providerNameBn: string;
  proposerId: number;
  proposerName: string;
  proposerRole: 'PROVIDER' | 'REQUESTER';
  recipientId: number;
  recipientName: string;
  recipientRole: 'PROVIDER' | 'REQUESTER';
  offeredPrice: number;
  deliveryFee: number;
  serviceFee: number;
  totalAmount: number;
  currency: string;
  status: 'DRAFT' | 'PENDING' | 'ACCEPTED' | 'REJECTED' | 'CANCELLED' | 'EXPIRED' | 'SUPERSEDED';
  version: number;
  parentOfferId: number | null;
  rootOfferId: number;
  termsConditions: string;
  estimatedDuration: string;
  rejectionReason?: string;
  expiresAt: string;
  createdAt: string;
  isProposer: boolean;
  isRecipient: boolean;
}

export const INITIAL_MOCK_OFFERS: MockOffer[] = [
  {
    id: 101,
    demandId: 1,
    demandTitleBn: 'কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন',
    providerId: 1,
    providerNameBn: 'সৈকত ইলেকট্রিক্যাল সল্যুশন',
    proposerId: 10,
    proposerName: 'কামাল উদ্দিন (কারিগর)',
    proposerRole: 'PROVIDER',
    recipientId: 1,
    recipientName: 'মোহাম্মদ করিম',
    recipientRole: 'REQUESTER',
    offeredPrice: 1200,
    deliveryFee: 100,
    serviceFee: 50,
    totalAmount: 1350,
    currency: 'BDT',
    status: 'SUPERSEDED',
    version: 1,
    parentOfferId: null,
    rootOfferId: 101,
    termsConditions: 'সার্কিট ব্রেকার চেক ও ওয়্যারিং মেরামত করা হবে। নতুন পার্টস লাগলে তার মূল্য আলাদা হবে।',
    estimatedDuration: '২ ঘণ্টা',
    expiresAt: '2026-09-18T18:00:00Z',
    createdAt: '2026-09-12T11:00:00Z',
    isProposer: false,
    isRecipient: true,
  },
  {
    id: 102,
    demandId: 1,
    demandTitleBn: 'কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন',
    providerId: 1,
    providerNameBn: 'সৈকত ইলেকট্রিক্যাল সল্যুশন',
    proposerId: 1,
    proposerName: 'মোহাম্মদ করিম (অনুরোধকারী)',
    proposerRole: 'REQUESTER',
    recipientId: 10,
    recipientName: 'কামাল উদ্দিন (কারিগর)',
    recipientRole: 'PROVIDER',
    offeredPrice: 1000,
    deliveryFee: 50,
    serviceFee: 50,
    totalAmount: 1100,
    currency: 'BDT',
    status: 'PENDING',
    version: 2,
    parentOfferId: 101,
    rootOfferId: 101,
    termsConditions: 'পাল্টা প্রস্তাব: সর্বোচ্চ ১০০০ টাকা সার্ভিস চার্জ ও ৫০ টাকা যাতায়াত ব্যয় দিতে পারব।',
    estimatedDuration: '২ ঘণ্টা',
    expiresAt: '2026-09-19T20:00:00Z',
    createdAt: '2026-09-12T14:30:00Z',
    isProposer: true,
    isRecipient: false,
  },
  {
    id: 103,
    demandId: 2,
    demandTitleBn: 'রামু বাইপাসে ৩০০০ পিস অটো ব্রিকস বা ইট প্রয়োজন',
    providerId: 2,
    providerNameBn: 'কক্স অটো ব্রিকস লিমিটেড',
    proposerId: 20,
    proposerName: 'রহিম উল্লাহ (ম্যানেজার)',
    proposerRole: 'PROVIDER',
    recipientId: 2,
    recipientName: 'আহমেদ শফিক',
    recipientRole: 'REQUESTER',
    offeredPrice: 37500,
    deliveryFee: 1500,
    serviceFee: 0,
    totalAmount: 39000,
    currency: 'BDT',
    status: 'PENDING',
    version: 1,
    parentOfferId: null,
    rootOfferId: 103,
    termsConditions: '১ম শ্রেণির ৩০০০ পিস গ্যাস পোড়ানো অটো ব্রিকস সাইটে সরাসরি আনলোডসহ প্রদান করা হবে।',
    estimatedDuration: '১ দিন',
    expiresAt: '2026-09-20T22:00:00Z',
    createdAt: '2026-09-12T15:10:00Z',
    isProposer: false,
    isRecipient: true,
  }
];
