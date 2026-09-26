/// User Intent Model for SebaCox Category & Demand UX.
/// Phase 4E — Intent-Guided Taxonomy Discovery.
/// Architectural Boundary: Category ≠ Intent (Intent is NOT a master category).
/// Global Bangla Typography Standard compliant.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
/// "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
library;

class UserIntent {
  final String code;
  final String nameBn;
  final String nameEn;
  final String shortHintBn;
  final String icon;
  final List<int> suggestedCategoryIds;
  final String defaultDemandType;
  final List<String> quickPromptChips;

  const UserIntent({
    required this.code,
    required this.nameBn,
    required this.nameEn,
    required this.shortHintBn,
    required this.icon,
    required this.suggestedCategoryIds,
    required this.defaultDemandType,
    required this.quickPromptChips,
  });

  /// Canonical catalog of user intents for Cox's Bazar region
  static const List<UserIntent> standardIntents = [
    UserIntent(
      code: 'SERVICE_REPAIR',
      nameBn: 'সেবা বা মেরামত প্রয়োজন',
      nameEn: 'Service & Repair Need',
      shortHintBn: 'বাসাবাড়ি, ইলেকট্রিক, এসি, ফ্রিজ বা প্লাম্বিং মেরামত',
      icon: 'tool',
      suggestedCategoryIds: [2, 1, 3, 19, 30],
      defaultDemandType: 'SERVICE',
      quickPromptChips: ['ইলেকট্রিশিয়ান', 'ফ্রিজ মেরামত', 'এসি সার্ভিসিং', 'প্লাম্বার', 'কার্পেন্টার'],
    ),
    UserIntent(
      code: 'HIRE_WORKER',
      nameBn: 'মিস্ত্রি বা শ্রমিক দরকার',
      nameEn: 'Skilled Artisan & Labor',
      shortHintBn: 'নির্মাণ শ্রমিক, রাজমিস্ত্রি, টাইলস মিস্ত্রি বা মালামাল খালাস',
      icon: 'users',
      suggestedCategoryIds: [1, 4, 16, 24],
      defaultDemandType: 'SERVICE',
      quickPromptChips: ['রাজমিস্ত্রি', 'মেস্ত্রি', 'রড মিস্ত্রি', 'টাইলস মিস্ত্রি', 'মালামাল লেবার'],
    ),
    UserIntent(
      code: 'BUY_PRODUCT',
      nameBn: 'পণ্য সামগ্রী কিনতে চাই',
      nameEn: 'Buy Products & Materials',
      shortHintBn: 'নির্মাণ সামগ্রী, ফার্নিচার, গ্যাজেট, ইলেকট্রনিক্স বা শুঁটকি ক্রয়',
      icon: 'shopping-cart',
      suggestedCategoryIds: [18, 1, 10, 19],
      defaultDemandType: 'PRODUCT',
      quickPromptChips: ['ইট বালু', 'সিমেন্ট রড', 'পুরাতন ফ্রিজ', 'সিসিটিভি ক্যামেরা', 'নাজিরারটেক শুঁটকি'],
    ),
    UserIntent(
      code: 'SELL_PRODUCT',
      nameBn: 'পণ্য বিক্রি করতে চাই',
      nameEn: 'Sell Goods & Equipment',
      shortHintBn: 'ব্যবহৃত গাড়ি, পুরাতন মোবাইল, আসবাবপত্র বা খুচরা পণ্য বিক্রয়',
      icon: 'dollar-sign',
      suggestedCategoryIds: [18, 17, 10],
      defaultDemandType: 'MARKETPLACE',
      quickPromptChips: ['পুরাতন ফ্রিজ বিক্রি', 'ব্যবহৃত বাইক', 'ফার্নিচার বিক্রি', 'মোবাইল বিক্রি'],
    ),
    UserIntent(
      code: 'RENT_IN',
      nameBn: 'ভাড়া নিতে চাই',
      nameEn: 'Rent Property / Vehicle',
      shortHintBn: 'বাসা, ফ্ল্যাট, দোকান, চাঁন্দের গাড়ি, পিকআপ বা জেনারেটর ভাড়া',
      icon: 'truck',
      suggestedCategoryIds: [17, 6, 4, 30, 25],
      defaultDemandType: 'RENTAL',
      quickPromptChips: ['বাসা ভাড়া', 'পিকআপ ভাড়া', 'চাঁন্দের গাড়ি', 'মাইক্রোবাস ভাড়া', 'জেনারেটর ভাড়া'],
    ),
    UserIntent(
      code: 'BOOKING_RESERVATION',
      nameBn: 'বুকিং ও অ্যাপয়েন্টমেন্ট',
      nameEn: 'Booking & Reservations',
      shortHintBn: 'হোটেল, রিসোর্ট, সেন্টমার্টিন জাহাজ, ট্যুর গাইড বা ডাক্তার',
      icon: 'ticket',
      suggestedCategoryIds: [8, 9, 12, 25, 31],
      defaultDemandType: 'BOOKING',
      quickPromptChips: ['হোটেল বুকিং', 'রিসোর্ট রুম', 'সেন্টমার্টিন জাহাজ', 'ডাক্তার অ্যাপয়েন্টমেন্ট', 'কমিউনিটি সেন্টার'],
    ),
    UserIntent(
      code: 'EMERGENCY_RESCUE',
      nameBn: 'জরুরি সেবা ও উদ্ধার',
      nameEn: 'Emergency & Rescue',
      shortHintBn: 'জরুরি অ্যাম্বুলেন্স, অক্সিজেন সিলিন্ডার, ব্লাড ডোনার ও দুর্যোগ উদ্ধার',
      icon: 'alert-triangle',
      suggestedCategoryIds: [26, 12, 27, 30],
      defaultDemandType: 'SERVICE',
      quickPromptChips: ['জরুরি অ্যাম্বুলেন্স', 'অক্সিজেন সিলিন্ডার', 'জরুরি রক্তদাতা', 'জরুরি electrician'],
    ),
    UserIntent(
      code: 'JOB_EMPLOYMENT',
      nameBn: 'চাকরি ও কর্মসংস্থান',
      nameEn: 'Jobs & Employment',
      shortHintBn: 'হোটেল স্টাফ, ড্রাইভার, সেলস এক্সিকিউটিভ বা অভিজ্ঞ কারিগর খুঁজছি',
      icon: 'user-check',
      suggestedCategoryIds: [16, 28, 24],
      defaultDemandType: 'SERVICE',
      quickPromptChips: ['হোটেল চাকরি', 'ড্রাইভার চাকরি', 'সিকিউরিটি গার্ড', 'বাসার কাজের বুয়া'],
    ),
    UserIntent(
      code: 'LEGAL_CITIZEN',
      nameBn: 'আইন, দলিল ও জনসেবা',
      nameEn: 'Legal, Deed & Public Info',
      shortHintBn: 'দলিল লেখক, জমি রেজিস্ট্রি, ট্রেড লাইসেন্স, পুলিশ ও ফায়ার সার্ভিস',
      icon: 'award',
      suggestedCategoryIds: [21, 22, 27],
      defaultDemandType: 'INFORMATION',
      quickPromptChips: ['দলিল লেখক', 'জমি রেজিস্ট্রি', 'ট্রেড লাইসেন্স', 'থানা হেল্পলাইন', 'ফায়ার সার্ভিস'],
    ),
  ];

  static UserIntent? findByCode(String? code) {
    if (code == null) return null;
    try {
      return standardIntents.firstWhere((i) => i.code == code);
    } catch (_) {
      return null;
    }
  }
}
