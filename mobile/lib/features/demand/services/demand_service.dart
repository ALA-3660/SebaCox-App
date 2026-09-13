/// Network Service for SebaCox Demand Engine.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
/// "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
library;

import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/demand_model.dart';
import '../models/demand_enums.dart';

class DemandApiService {
  final String baseUrl;
  final http.Client _client;

  DemandApiService({
    required this.baseUrl,
    http.Client? client,
  }) : _client = client ?? http.Client();

  Map<String, String> _headers([String? token]) {
    final map = {
      'Content-Type': 'application/json; charset=UTF-8',
      'Accept': 'application/json',
    };
    if (token != null && token.isNotEmpty) {
      map['Authorization'] = 'Bearer $token';
    }
    return map;
  }

  /// Get public or filtered demands
  Future<List<DemandModel>> getDemands({
    String? query,
    int? serviceId,
    int? categoryId,
    int? upazilaId,
    String? token,
  }) async {
    final queryParams = <String, String>{};
    if (query != null && query.isNotEmpty) queryParams['q'] = query;
    if (serviceId != null) queryParams['service_id'] = serviceId.toString();
    if (categoryId != null) queryParams['category_id'] = categoryId.toString();
    if (upazilaId != null) queryParams['upazila_id'] = upazilaId.toString();

    final uri = Uri.parse('$baseUrl/api/v1/demands/').replace(queryParameters: queryParams);
    final response = await _client.get(uri, headers: _headers(token));

    if (response.statusCode == 200) {
      final json = jsonDecode(utf8.decode(response.bodyBytes));
      final List list = json['data'] as List? ?? [];
      return list.map((item) => DemandModel.fromJson(item)).toList();
    }
    throw Exception('প্রয়োজনের তালিকা লোড করা সম্ভব হয়নি');
  }

  /// Get current user's demands
  Future<List<DemandModel>> getMyDemands({required String token}) async {
    final uri = Uri.parse('$baseUrl/api/v1/demands/me/');
    final response = await _client.get(uri, headers: _headers(token));

    if (response.statusCode == 200) {
      final json = jsonDecode(utf8.decode(response.bodyBytes));
      final List list = json['data'] as List? ?? [];
      return list.map((item) => DemandModel.fromJson(item)).toList();
    }
    throw Exception('আপনার প্রয়োজন তালিকা লোড করা সম্ভব হয়নি');
  }

  /// Create demand (Draft or Published)
  Future<DemandModel> createDemand({
    required String token,
    required Map<String, dynamic> data,
    bool publishNow = false,
  }) async {
    final uri = Uri.parse('$baseUrl/api/v1/demands/');
    final payload = Map<String, dynamic>.from(data);
    payload['publish_now'] = publishNow;

    final response = await _client.post(
      uri,
      headers: _headers(token),
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201 || response.statusCode == 200) {
      final json = jsonDecode(utf8.decode(response.bodyBytes));
      return DemandModel.fromJson(json['data']);
    }
    final errJson = jsonDecode(utf8.decode(response.bodyBytes));
    throw Exception(errJson['message'] ?? 'প্রয়োজন তৈরি ব্যর্থ হয়েছে');
  }

  /// Trigger lifecycle actions (publish, pause, resume, cancel, fulfill, close)
  Future<DemandModel> performLifecycleAction({
    required String token,
    required int demandId,
    required String action, // publish, pause, resume, cancel, fulfill, close
    Map<String, dynamic>? body,
  }) async {
    final uri = Uri.parse('$baseUrl/api/v1/demands/$demandId/$action/');
    final response = await _client.post(
      uri,
      headers: _headers(token),
      body: jsonEncode(body ?? {}),
    );

    if (response.statusCode == 200) {
      final json = jsonDecode(utf8.decode(response.bodyBytes));
      return DemandModel.fromJson(json['data']);
    }
    final errJson = jsonDecode(utf8.decode(response.bodyBytes));
    throw Exception(errJson['message'] ?? 'অ্যাকশন সম্পন্ন করা যায়নি');
  }
}
