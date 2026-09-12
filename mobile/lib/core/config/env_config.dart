/// Environment and runtime configuration for SebaCox Mobile App.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
enum AppEnvironment { development, staging, production }

class EnvConfig {
  static AppEnvironment _environment = AppEnvironment.development;
  static String? _customBaseUrl;

  /// Configure active environment
  static void setEnvironment(AppEnvironment env, {String? customBaseUrl}) {
    _environment = env;
    _customBaseUrl = customBaseUrl;
  }

  static AppEnvironment get environment => _environment;

  /// Dynamic base URL - easily configured for local emulators, LAN, or production
  static String get apiBaseUrl {
    if (_customBaseUrl != null && _customBaseUrl!.isNotEmpty) {
      return _customBaseUrl!;
    }
    switch (_environment) {
      case AppEnvironment.production:
        return 'https://api.sebacox.com';
      case AppEnvironment.staging:
        return 'https://staging-api.sebacox.com';
      case AppEnvironment.development:
      default:
        // Default dev host for web / local testing
        return 'http://127.0.0.1:8000';
    }
  }

  static const Duration connectTimeout = Duration(seconds: 10);
  static const Duration receiveTimeout = Duration(seconds: 15);
}
