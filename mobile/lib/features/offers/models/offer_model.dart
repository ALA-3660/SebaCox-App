/// Offer Models for SebaCox Mobile Client.
/// Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
/// “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
library;

import 'offer_enums.dart';

class OfferModel {
  final int id;
  final int demandId;
  final int? matchCandidateId;
  final int providerId;
  final int requesterId;
  final int proposerId;
  final int? parentOfferId;
  final int? rootOfferId;
  final int version;
  final OfferType offerType;
  final OfferStatus status;
  final String titleBn;
  final String descriptionBn;
  final double? quantity;
  final String? unit;
  final double price;
  final String currency;
  final double deliveryFee;
  final double serviceFee;
  final double totalAmount;
  final String termsBn;
  final String estimatedDeliveryDuration;
  final DateTime proposedAt;
  final DateTime expiresAt;
  final DateTime? acceptedAt;
  final DateTime? rejectedAt;
  final DateTime? cancelledAt;
  final String rejectionReasonBn;
  final String cancellationReasonBn;
  final bool isExpired;
  final bool isTerminal;
  final Map<String, dynamic>? providerSummary;
  final Map<String, dynamic>? proposerSummary;
  final Map<String, dynamic>? demandSummary;
  final Map<String, dynamic> snapshot;
  final DateTime createdAt;

  const OfferModel({
    required this.id,
    required this.demandId,
    this.matchCandidateId,
    required this.providerId,
    required this.requesterId,
    required this.proposerId,
    this.parentOfferId,
    this.rootOfferId,
    required this.version,
    required this.offerType,
    required this.status,
    required this.titleBn,
    this.descriptionBn = '',
    this.quantity,
    this.unit,
    required this.price,
    this.currency = 'BDT',
    this.deliveryFee = 0.0,
    this.serviceFee = 0.0,
    required this.totalAmount,
    this.termsBn = '',
    this.estimatedDeliveryDuration = '',
    required this.proposedAt,
    required this.expiresAt,
    this.acceptedAt,
    this.rejectedAt,
    this.cancelledAt,
    this.rejectionReasonBn = '',
    this.cancellationReasonBn = '',
    this.isExpired = false,
    this.isTerminal = false,
    this.providerSummary,
    this.proposerSummary,
    this.demandSummary,
    this.snapshot = const {},
    required this.createdAt,
  });

  factory OfferModel.fromJson(Map<String, dynamic> json) {
    return OfferModel(
      id: json['id'] as int,
      demandId: json['demand'] is int ? json['demand'] as int : (json['demand_summary']?['id'] ?? 0),
      matchCandidateId: json['match_candidate'] as int?,
      providerId: json['provider'] is int ? json['provider'] as int : (json['provider_summary']?['id'] ?? 0),
      requesterId: json['requester'] is int ? json['requester'] as int : 0,
      proposerId: json['proposer'] is int ? json['proposer'] as int : (json['proposer_summary']?['id'] ?? 0),
      parentOfferId: json['parent_offer'] as int?,
      rootOfferId: json['root_offer'] as int?,
      version: json['version'] as int? ?? 1,
      offerType: OfferType.fromString(json['offer_type'] as String?),
      status: OfferStatus.fromString(json['status'] as String?),
      titleBn: json['title_bn'] as String? ?? '',
      descriptionBn: json['description_bn'] as String? ?? '',
      quantity: json['quantity'] != null ? double.tryParse(json['quantity'].toString()) : null,
      unit: json['unit'] as String?,
      price: double.tryParse(json['price']?.toString() ?? '0') ?? 0.0,
      currency: json['currency'] as String? ?? 'BDT',
      deliveryFee: double.tryParse(json['delivery_fee']?.toString() ?? '0') ?? 0.0,
      serviceFee: double.tryParse(json['service_fee']?.toString() ?? '0') ?? 0.0,
      totalAmount: double.tryParse(json['total_amount']?.toString() ?? '0') ?? 0.0,
      termsBn: json['terms_bn'] as String? ?? '',
      estimatedDeliveryDuration: json['estimated_delivery_duration'] as String? ?? '',
      proposedAt: json['proposed_at'] != null ? DateTime.parse(json['proposed_at'] as String) : DateTime.now(),
      expiresAt: json['expires_at'] != null ? DateTime.parse(json['expires_at'] as String) : DateTime.now().add(const Duration(hours: 24)),
      acceptedAt: json['accepted_at'] != null ? DateTime.parse(json['accepted_at'] as String) : null,
      rejectedAt: json['rejected_at'] != null ? DateTime.parse(json['rejected_at'] as String) : null,
      cancelledAt: json['cancelled_at'] != null ? DateTime.parse(json['cancelled_at'] as String) : null,
      rejectionReasonBn: json['rejection_reason_bn'] as String? ?? '',
      cancellationReasonBn: json['cancellation_reason_bn'] as String? ?? '',
      isExpired: json['is_expired'] as bool? ?? false,
      isTerminal: json['is_terminal'] as bool? ?? false,
      providerSummary: json['provider_summary'] as Map<String, dynamic>?,
      proposerSummary: json['proposer_summary'] as Map<String, dynamic>?,
      demandSummary: json['demand_summary'] as Map<String, dynamic>?,
      snapshot: json['snapshot'] as Map<String, dynamic>? ?? {},
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at'] as String) : DateTime.now(),
    );
  }

  String get providerBusinessNameBn =>
      providerSummary?['business_name_bn'] as String? ?? 'সেবাদাতা';

  String get demandTitleBn =>
      demandSummary?['title_bn'] as String? ?? 'প্রয়োজন';

  bool get isProviderVerified =>
      providerSummary?['is_verified'] as bool? ?? false;
}

class OfferAuditLogModel {
  final int id;
  final int offerId;
  final int? actorId;
  final String actorName;
  final OfferAuditAction action;
  final String actionLabel;
  final String previousStatus;
  final String newStatus;
  final Map<String, dynamic> metadata;
  final DateTime createdAt;

  const OfferAuditLogModel({
    required this.id,
    required this.offerId,
    this.actorId,
    required this.actorName,
    required this.action,
    required this.actionLabel,
    this.previousStatus = '',
    this.newStatus = '',
    this.metadata = const {},
    required this.createdAt,
  });

  factory OfferAuditLogModel.fromJson(Map<String, dynamic> json) {
    return OfferAuditLogModel(
      id: json['id'] as int,
      offerId: json['offer'] as int,
      actorId: json['actor'] as int?,
      actorName: json['actor_name'] as String? ?? 'ব্যবহারকারী',
      action: OfferAuditAction.fromString(json['action'] as String?),
      actionLabel: json['action_label'] as String? ?? '',
      previousStatus: json['previous_status'] as String? ?? '',
      newStatus: json['new_status'] as String? ?? '',
      metadata: json['metadata'] as Map<String, dynamic>? ?? {},
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at'] as String) : DateTime.now(),
    );
  }
}
