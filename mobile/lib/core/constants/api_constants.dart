/// API endpoint definitions and constant headers for SebaCox.
class ApiConstants {
  // API Versioning
  static const String apiVersion = '/api/v1';

  // Core endpoints
  static const String healthEndpoint = '$apiVersion/health/';

  // Standard Headers
  static const String headerContentType = 'Content-Type';
  static const String headerAccept = 'Accept';
  static const String contentTypeJson = 'application/json';
}
