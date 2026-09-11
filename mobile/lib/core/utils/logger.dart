import 'package:flutter/foundation.dart';

/// Secure application logger that masks sensitive strings and only prints in debug mode.
class AppLogger {
  static void d(String message) {
    if (kDebugMode) {
      debugPrint('[DEBUG] ${_sanitize(message)}');
    }
  }

  static void i(String message) {
    debugPrint('[INFO] ${_sanitize(message)}');
  }

  static void w(String message) {
    debugPrint('[WARNING] ${_sanitize(message)}');
  }

  static void e(String message, [dynamic error, StackTrace? stackTrace]) {
    debugPrint('[ERROR] ${_sanitize(message)}');
    if (error != null && kDebugMode) {
      debugPrint('Error Details: $error');
    }
    if (stackTrace != null && kDebugMode) {
      debugPrint('StackTrace: $stackTrace');
    }
  }

  /// Masks tokens, passwords, OTPs from client-side console logs
  static String _sanitize(String input) {
    return input
        .replaceAll(RegExp(r'(password|passwd)=([^\s&]+)', caseSensitive: false), r'$1=********')
        .replaceAll(RegExp(r'(otp|pin)=([^\s&]+)', caseSensitive: false), r'$1=******')
        .replaceAll(RegExp(r'Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*', caseSensitive: false), 'Bearer ********');
  }
}
