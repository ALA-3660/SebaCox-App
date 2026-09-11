import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../config/env_config.dart';
import '../constants/api_constants.dart';
import '../utils/logger.dart';
import 'network_exceptions.dart';
import '../../shared/models/api_response.dart';

/// Reusable HTTP API Client for SebaCox Mobile App.
/// Handles standard request lifecycles, authentication headers, timeouts, token refresh, and error contracts.
class ApiClient {
  final http.Client _client;
  String? _accessToken;
  Future<String?> Function()? _refreshTokenCallback;

  ApiClient({
    http.Client? client,
    String? accessToken,
    Future<String?> Function()? onRefreshToken,
  })  : _client = client ?? http.Client(),
        _accessToken = accessToken,
        _refreshTokenCallback = onRefreshToken;

  void setAccessToken(String? token) {
    _accessToken = token;
  }

  void setRefreshTokenCallback(Future<String?> Function()? callback) {
    _refreshTokenCallback = callback;
  }

  Map<String, String> _buildHeaders(Map<String, String>? customHeaders) {
    final headers = {
      ApiConstants.headerContentType: ApiConstants.contentTypeJson,
      ApiConstants.headerAccept: ApiConstants.contentTypeJson,
    };

    if (_accessToken != null && _accessToken!.isNotEmpty) {
      headers[ApiConstants.headerAuthorization] = '${ApiConstants.bearerPrefix}$_accessToken';
    }

    if (customHeaders != null) {
      headers.addAll(customHeaders);
    }
    return headers;
  }

  /// Perform a GET request to the SebaCox backend API
  Future<ApiResponse<T>> get<T>(
    String endpoint, {
    Map<String, String>? headers,
    T Function(dynamic json)? fromJson,
    bool retryOnAuthFailure = true,
  }) async {
    final uri = Uri.parse('${EnvConfig.apiBaseUrl}$endpoint');
    AppLogger.d('GET Request: $uri');

    final requestHeaders = _buildHeaders(headers);

    try {
      final response = await _client
          .get(uri, headers: requestHeaders)
          .timeout(EnvConfig.connectTimeout);

      if (response.statusCode == 401 && retryOnAuthFailure && _refreshTokenCallback != null) {
        final refreshed = await _refreshTokenCallback!();
        if (refreshed != null) {
          _accessToken = refreshed;
          return get<T>(endpoint, headers: headers, fromJson: fromJson, retryOnAuthFailure: false);
        }
      }

      return _processResponse<T>(response, fromJson);
    } on TimeoutException {
      AppLogger.e('Network request timed out: $endpoint');
      throw const TimeoutNetworkException();
    } on SocketException {
      AppLogger.e('Socket error / no internet reaching: $endpoint');
      throw const NoInternetNetworkException();
    } catch (e) {
      if (e is NetworkException) rethrow;
      AppLogger.e('Unexpected network exception: $e');
      throw ServerNetworkException('সার্ভারের সাথে সংযোগ ব্যর্থ: ${e.toString()}');
    }
  }

  /// Perform a POST request to the SebaCox backend API
  Future<ApiResponse<T>> post<T>(
    String endpoint, {
    Map<String, dynamic>? body,
    Map<String, String>? headers,
    T Function(dynamic json)? fromJson,
    bool retryOnAuthFailure = true,
  }) async {
    final uri = Uri.parse('${EnvConfig.apiBaseUrl}$endpoint');
    AppLogger.d('POST Request: $uri');

    final requestHeaders = _buildHeaders(headers);

    try {
      final response = await _client
          .post(
            uri,
            headers: requestHeaders,
            body: body != null ? jsonEncode(body) : null,
          )
          .timeout(EnvConfig.connectTimeout);

      if (response.statusCode == 401 && retryOnAuthFailure && _refreshTokenCallback != null) {
        final refreshed = await _refreshTokenCallback!();
        if (refreshed != null) {
          _accessToken = refreshed;
          return post<T>(endpoint, body: body, headers: headers, fromJson: fromJson, retryOnAuthFailure: false);
        }
      }

      return _processResponse<T>(response, fromJson);
    } on TimeoutException {
      AppLogger.e('Network request timed out: $endpoint');
      throw const TimeoutNetworkException();
    } on SocketException {
      AppLogger.e('Socket error / no internet reaching: $endpoint');
      throw const NoInternetNetworkException();
    } catch (e) {
      if (e is NetworkException) rethrow;
      AppLogger.e('Unexpected network exception: $e');
      throw ServerNetworkException('সার্ভারের সাথে সংযোগ ব্যর্থ: ${e.toString()}');
    }
  }

  /// Process standard response contract
  ApiResponse<T> _processResponse<T>(
    http.Response response,
    T Function(dynamic json)? fromJson,
  ) {
    AppLogger.d('HTTP Response [${response.statusCode}] from server');

    try {
      final decoded = jsonDecode(utf8.decode(response.bodyBytes));
      if (decoded is Map<String, dynamic>) {
        final success = decoded['success'] == true;
        final message = decoded['message'] as String? ?? '';
        final errors = decoded['errors'];

        T? data;
        if (decoded['data'] != null) {
          if (fromJson != null) {
            data = fromJson(decoded['data']);
          } else {
            data = decoded['data'] as T?;
          }
        }

        if (response.statusCode >= 200 && response.statusCode < 300 && success) {
          return ApiResponse<T>.success(
            data: data,
            message: message,
            statusCode: response.statusCode,
          );
        } else {
          return ApiResponse<T>.error(
            message: message.isNotEmpty ? message : 'অনুরোধটি সম্পন্ন করা যায়নি',
            statusCode: response.statusCode,
            errors: errors,
          );
        }
      }
    } catch (e) {
      AppLogger.e('Error decoding API response: $e');
    }

    if (response.statusCode >= 400) {
      throw NetworkException(
        message: 'সার্ভার ত্রুটি (${response.statusCode})',
        statusCode: response.statusCode,
      );
    }

    throw const ServerNetworkException();
  }
}
