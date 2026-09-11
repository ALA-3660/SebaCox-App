/// API endpoint definitions and constant headers for SebaCox.
class ApiConstants {
  // API Versioning
  static const String apiVersion = '/api/v1';

  // Core endpoints
  static const String healthEndpoint = '$apiVersion/health/';

  // Phase 2 Authentication Endpoints
  static const String registerRequestOtp = '$apiVersion/auth/register/request-otp/';
  static const String registerVerifyOtp = '$apiVersion/auth/register/verify-otp/';
  static const String loginRequestOtp = '$apiVersion/auth/login/request-otp/';
  static const String loginVerifyOtp = '$apiVersion/auth/login/verify-otp/';
  static const String tokenRefresh = '$apiVersion/auth/token/refresh/';
  static const String logout = '$apiVersion/auth/logout/';
  static const String currentUser = '$apiVersion/auth/me/';

  // Standard Headers
  static const String headerContentType = 'Content-Type';
  static const String headerAccept = 'Accept';
  static const String headerAuthorization = 'Authorization';
  static const String contentTypeJson = 'application/json';
  static const String bearerPrefix = 'Bearer ';
}
