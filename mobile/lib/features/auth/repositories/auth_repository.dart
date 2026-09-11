import 'dart:async';
import '../../../core/storage/secure_storage.dart';
import '../../../core/network/api_client.dart';
import '../../../shared/models/api_response.dart';
import '../models/auth_state.dart';
import '../models/auth_tokens.dart';
import '../models/user.dart';
import '../services/auth_service.dart';

/// Centralized Authentication Repository.
/// Coordinates secure token storage, authentication state stream, and API client auth hooks.
class AuthRepository {
  static const String _keyAccessToken = 'sebacox_auth_access_token';
  static const String _keyRefreshToken = 'sebacox_auth_refresh_token';

  final AuthService _authService;
  final ApiClient _apiClient;
  final _stateController = StreamController<AuthState>.broadcast();

  AuthState _currentState = AuthState.unknown();
  AuthState get currentState => _currentState;
  Stream<AuthState> get stateStream => _stateController.stream;

  AuthRepository({
    required AuthService authService,
    required ApiClient apiClient,
  })  : _authService = authService,
        _apiClient = apiClient {
    // Configure automatic token refresh callback in ApiClient
    _apiClient.setRefreshTokenCallback(_handleTokenRefresh);
  }

  void _emit(AuthState newState) {
    _currentState = newState;
    _stateController.add(newState);
  }

  /// Check whether an existing valid secure token session exists.
  /// UNKNOWN -> CHECKING_SESSION -> AUTHENTICATED or UNAUTHENTICATED
  Future<AuthState> checkExistingSession() async {
    _emit(AuthState.checkingSession());

    try {
      final accessToken = await LocalStorage.readSecure(_keyAccessToken);
      final refreshToken = await LocalStorage.readSecure(_keyRefreshToken);

      if (accessToken == null && refreshToken == null) {
        final state = AuthState.unauthenticated();
        _emit(state);
        return state;
      }

      if (accessToken != null) {
        _apiClient.setAccessToken(accessToken);
        final userResponse = await _authService.getCurrentUser();

        if (userResponse.isSuccess && userResponse.data != null) {
          final state = AuthState.authenticated(userResponse.data!);
          _emit(state);
          return state;
        }
      }

      // If access token failed but refresh token exists, try refreshing
      if (refreshToken != null) {
        final newAccess = await _handleTokenRefresh();
        if (newAccess != null) {
          final userResponse = await _authService.getCurrentUser();
          if (userResponse.isSuccess && userResponse.data != null) {
            final state = AuthState.authenticated(userResponse.data!);
            _emit(state);
            return state;
          }
        }
      }

      // If both failed, clean up invalid tokens
      await _clearTokens();
      final state = AuthState.unauthenticated();
      _emit(state);
      return state;
    } catch (e) {
      await _clearTokens();
      final state = AuthState.unauthenticated(error: e.toString());
      _emit(state);
      return state;
    }
  }

  /// Request OTP for registration
  Future<ApiResponse<Map<String, dynamic>>> requestRegisterOtp(String mobileNumber) {
    return _authService.requestRegisterOtp(mobileNumber);
  }

  /// Verify OTP and store tokens upon successful registration
  Future<ApiResponse<Map<String, dynamic>>> verifyRegisterOtp({
    required String mobileNumber,
    required String otpCode,
  }) async {
    final response = await _authService.verifyRegisterOtp(
      mobileNumber: mobileNumber,
      otpCode: otpCode,
    );

    if (response.isSuccess && response.data != null) {
      await _persistAuthSession(response.data!);
    }

    return response;
  }

  /// Request OTP for login
  Future<ApiResponse<Map<String, dynamic>>> requestLoginOtp(String mobileNumber) {
    return _authService.requestLoginOtp(mobileNumber);
  }

  /// Verify OTP and store tokens upon successful login
  Future<ApiResponse<Map<String, dynamic>>> verifyLoginOtp({
    required String mobileNumber,
    required String otpCode,
  }) async {
    final response = await _authService.verifyLoginOtp(
      mobileNumber: mobileNumber,
      otpCode: otpCode,
    );

    if (response.isSuccess && response.data != null) {
      await _persistAuthSession(response.data!);
    }

    return response;
  }

  Future<void> _persistAuthSession(Map<String, dynamic> data) async {
    final userJson = data['user'] as Map<String, dynamic>?;
    final tokensJson = data['tokens'] as Map<String, dynamic>?;

    if (tokensJson != null) {
      final tokens = AuthTokens.fromJson(tokensJson);
      await LocalStorage.writeSecure(_keyAccessToken, tokens.accessToken);
      await LocalStorage.writeSecure(_keyRefreshToken, tokens.refreshToken);
      _apiClient.setAccessToken(tokens.accessToken);
    }

    if (userJson != null) {
      final user = User.fromJson(userJson);
      _emit(AuthState.authenticated(user));
    }
  }

  /// Automatic token refresh hook
  Future<String?> _handleTokenRefresh() async {
    try {
      final refreshToken = await LocalStorage.readSecure(_keyRefreshToken);
      if (refreshToken == null) return null;

      final response = await _authService.refreshAccessToken(refreshToken);
      if (response.isSuccess && response.data != null) {
        final newAccessToken = response.data!['access_token'] as String?;
        if (newAccessToken != null) {
          await LocalStorage.writeSecure(_keyAccessToken, newAccessToken);
          _apiClient.setAccessToken(newAccessToken);
          return newAccessToken;
        }
      }
    } catch (_) {
      // Refresh failed or token revoked
    }

    await logout();
    return null;
  }

  /// Secure logout: Revokes refresh token and clears secure storage
  Future<void> logout() async {
    try {
      final refreshToken = await LocalStorage.readSecure(_keyRefreshToken);
      await _authService.logout(refreshToken: refreshToken);
    } catch (_) {
      // Ignore network errors during logout
    } finally {
      await _clearTokens();
      _emit(AuthState.unauthenticated());
    }
  }

  Future<void> _clearTokens() async {
    await LocalStorage.deleteSecure(_keyAccessToken);
    await LocalStorage.deleteSecure(_keyRefreshToken);
    _apiClient.setAccessToken(null);
  }

  void dispose() {
    _stateController.close();
  }
}
