/// Offer Enums for SebaCox Mobile Client.
/// Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
/// “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
library;

enum OfferType {
  initial('INITIAL', 'প্রাথমিক প্রস্তাব'),
  counter('COUNTER', 'পাল্টা প্রস্তাব');

  final String value;
  final String labelBn;

  const OfferType(this.value, this.labelBn);

  static OfferType fromString(String? val) {
    switch (val?.toUpperCase()) {
      case 'COUNTER':
        return OfferType.counter;
      case 'INITIAL':
      default:
        return OfferType.initial;
    }
  }
}

enum OfferStatus {
  draft('DRAFT', 'খসড়া'),
  pending('PENDING', 'অপেক্ষমাণ'),
  accepted('ACCEPTED', 'গ্রহণ করা হয়েছে'),
  rejected('REJECTED', 'প্রত্যাখ্যাত'),
  cancelled('CANCELLED', 'বাতিল'),
  expired('EXPIRED', 'মেয়াদ শেষ'),
  superseded('SUPERSEDED', 'নতুন প্রস্তাবে প্রতিস্থাপিত');

  final String value;
  final String labelBn;

  const OfferStatus(this.value, this.labelBn);

  static OfferStatus fromString(String? val) {
    switch (val?.toUpperCase()) {
      case 'DRAFT':
        return OfferStatus.draft;
      case 'ACCEPTED':
        return OfferStatus.accepted;
      case 'REJECTED':
        return OfferStatus.rejected;
      case 'CANCELLED':
        return OfferStatus.cancelled;
      case 'EXPIRED':
        return OfferStatus.expired;
      case 'SUPERSEDED':
        return OfferStatus.superseded;
      case 'PENDING':
      default:
        return OfferStatus.pending;
    }
  }

  bool get isTerminal =>
      this == OfferStatus.accepted ||
      this == OfferStatus.rejected ||
      this == OfferStatus.cancelled ||
      this == OfferStatus.expired ||
      this == OfferStatus.superseded;
}

enum OfferAuditAction {
  created('CREATED', 'প্রস্তাব তৈরি'),
  countered('COUNTERED', 'পাল্টা প্রস্তাব প্রেরণ'),
  accepted('ACCEPTED', 'প্রস্তাব গৃহীত'),
  rejected('REJECTED', 'প্রস্তাব প্রত্যাখ্যাত'),
  cancelled('CANCELLED', 'প্রস্তাব বাতিলকৃত'),
  expired('EXPIRED', 'মেয়াদ উত্তীর্ণ'),
  superseded('SUPERSEDED', 'প্রতিস্থাপিত');

  final String value;
  final String labelBn;

  const OfferAuditAction(this.value, this.labelBn);

  static OfferAuditAction fromString(String? val) {
    switch (val?.toUpperCase()) {
      case 'COUNTERED':
        return OfferAuditAction.countered;
      case 'ACCEPTED':
        return OfferAuditAction.accepted;
      case 'REJECTED':
        return OfferAuditAction.rejected;
      case 'CANCELLED':
        return OfferAuditAction.cancelled;
      case 'EXPIRED':
        return OfferAuditAction.expired;
      case 'SUPERSEDED':
        return OfferAuditAction.superseded;
      case 'CREATED':
      default:
        return OfferAuditAction.created;
    }
  }
}
