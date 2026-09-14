/// Offer Service for SebaCox Mobile Client.
/// Phase 8: Offer & Counter-Offer Foundation (“ম্যাচ থেকে প্রস্তাব”).
/// “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
library;

import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../../core/network/api_client.dart';
import '../models/offer_model.dart';

class OfferService {
  final ApiClient _apiClient;

  OfferService({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  /// Fetches offers visible to the user
  Future<List<OfferModel>> fetchUserOffers({String? status, int? demandId, String? role}) async {
    final queryParams = <String, String>{};
    if (status != null) queryParams['status'] = status;
    if (demandId != null) queryParams['demand_id'] = demandId.toString();
    if (role != null) queryParams['role'] = role;

    final uri = Uri.parse('/api/v1/offers/').replace(queryParameters: queryParams.isEmpty ? null : queryParams);
    final response = await _apiClient.get(uri.toString());

    if (response.success && response.data != null) {
      final results = response.data['results'] as List<dynamic>? ?? [];
      return results.map((item) => OfferModel.fromJson(item as Map<String, dynamic>)).toList();
    }
    return [];
  }

  /// Fetches offers belonging to a specific Demand
  Future<List<OfferModel>> fetchDemandOffers(int demandId) async {
    final response = await _apiClient.get('/api/v1/offers/demand/$demandId/');

    if (response.success && response.data != null) {
      final results = response.data['offers'] as List<dynamic>? ?? [];
      return results.map((item) => OfferModel.fromJson(item as Map<String, dynamic>)).toList();
    }
    return [];
  }

  /// Fetches single offer detail
  Future<OfferModel?> fetchOfferDetail(int offerId) async {
    final response = await _apiClient.get('/api/v1/offers/$offerId/');

    if (response.success && response.data != null) {
      return OfferModel.fromJson(response.data['offer'] as Map<String, dynamic>);
    }
    return null;
  }

  /// Fetches chain history and audit trail
  Future<Map<String, dynamic>> fetchOfferHistory(int offerId) async {
    final response = await _apiClient.get('/api/v1/offers/$offerId/history/');

    if (response.success && response.data != null) {
      final chainList = (response.data['chain'] as List<dynamic>? ?? [])
          .map((i) => OfferModel.fromJson(i as Map<String, dynamic>))
          .toList();
      final auditList = (response.data['audit_trail'] as List<dynamic>? ?? [])
          .map((i) => OfferAuditLogModel.fromJson(i as Map<String, dynamic>))
          .toList();
      return {
        'chain': chainList,
        'audit_trail': auditList,
      };
    }
    return {'chain': <OfferModel>[], 'audit_trail': <OfferAuditLogModel>[]};
  }

  /// Creates initial offer (Provider only)
  Future<OfferModel> createInitialOffer({
    required int demandId,
    required int providerId,
    required String titleBn,
    required double price,
    double deliveryFee = 0.0,
    double serviceFee = 0.0,
    String? descriptionBn,
    double? quantity,
    String? unit,
    String? termsBn,
    String? estimatedDeliveryDuration,
    DateTime? expiresAt,
    int? matchCandidateId,
  }) async {
    final payload = {
      'demand_id': demandId,
      'provider_id': providerId,
      'title_bn': titleBn,
      'price': price,
      'delivery_fee': deliveryFee,
      'service_fee': serviceFee,
      'description_bn': descriptionBn ?? '',
      'quantity': quantity,
      'unit': unit ?? '',
      'terms_bn': termsBn ?? '',
      'estimated_delivery_duration': estimatedDeliveryDuration ?? '',
      if (expiresAt != null) 'expires_at': expiresAt.toIso8601String(),
      if (matchCandidateId != null) 'match_candidate_id': matchCandidateId,
    };

    final response = await _apiClient.post('/api/v1/offers/', body: payload);

    if (response.success && response.data != null) {
      return OfferModel.fromJson(response.data['offer'] as Map<String, dynamic>);
    }
    throw Exception(response.error?.message ?? 'প্রস্তাব পাঠাতে ব্যর্থ হয়েছে।');
  }

  /// Creates a counter offer against an existing pending offer
  Future<OfferModel> createCounterOffer({
    required int parentOfferId,
    required double price,
    String? titleBn,
    double deliveryFee = 0.0,
    double serviceFee = 0.0,
    String? descriptionBn,
    double? quantity,
    String? unit,
    String? termsBn,
    String? estimatedDeliveryDuration,
    DateTime? expiresAt,
  }) async {
    final payload = {
      'price': price,
      if (titleBn != null) 'title_bn': titleBn,
      'delivery_fee': deliveryFee,
      'service_fee': serviceFee,
      if (descriptionBn != null) 'description_bn': descriptionBn,
      if (quantity != null) 'quantity': quantity,
      if (unit != null) 'unit': unit,
      if (termsBn != null) 'terms_bn': termsBn,
      if (estimatedDeliveryDuration != null) 'estimated_delivery_duration': estimatedDeliveryDuration,
      if (expiresAt != null) 'expires_at': expiresAt.toIso8601String(),
    };

    final response = await _apiClient.post('/api/v1/offers/$parentOfferId/counter/', body: payload);

    if (response.success && response.data != null) {
      return OfferModel.fromJson(response.data['counter_offer'] as Map<String, dynamic>);
    }
    throw Exception(response.error?.message ?? 'পাল্টা প্রস্তাব পাঠাতে ব্যর্থ হয়েছে।');
  }

  /// Accepts a pending offer
  Future<OfferModel> acceptOffer(int offerId) async {
    final response = await _apiClient.post('/api/v1/offers/$offerId/accept/');

    if (response.success && response.data != null) {
      return OfferModel.fromJson(response.data['offer'] as Map<String, dynamic>);
    }
    throw Exception(response.error?.message ?? 'প্রস্তাব গ্রহণে ত্রুটি ঘটেছে।');
  }

  /// Rejects a pending offer
  Future<OfferModel> rejectOffer(int offerId, {String? reasonBn}) async {
    final response = await _apiClient.post(
      '/api/v1/offers/$offerId/reject/',
      body: {'rejection_reason_bn': reasonBn ?? ''},
    );

    if (response.success && response.data != null) {
      return OfferModel.fromJson(response.data['offer'] as Map<String, dynamic>);
    }
    throw Exception(response.error?.message ?? 'প্রস্তাব প্রত্যাখ্যান করতে ত্রুটি ঘটেছে।');
  }

  /// Cancels a pending offer
  Future<OfferModel> cancelOffer(int offerId, {String? reasonBn}) async {
    final response = await _apiClient.post(
      '/api/v1/offers/$offerId/cancel/',
      body: {'cancellation_reason_bn': reasonBn ?? ''},
    );

    if (response.success && response.data != null) {
      return OfferModel.fromJson(response.data['offer'] as Map<String, dynamic>);
    }
    throw Exception(response.error?.message ?? 'প্রস্তাব বাতিল করতে ত্রুটি ঘটেছে।');
  }
}
