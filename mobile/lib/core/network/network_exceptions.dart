/// Unified Network Exceptions for SebaCox Mobile App.
class NetworkException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic errorDetails;

  const NetworkException({
    required this.message,
    this.statusCode,
    this.errorDetails,
  });

  @override
  String toString() => 'NetworkException: $message (code: $statusCode)';
}

class TimeoutNetworkException extends NetworkException {
  const TimeoutNetworkException([String message = 'অনুরোধের সময়সীমা শেষ হয়েছে (Timeout)'])
      : super(message: message, statusCode: 408);
}

class NoInternetNetworkException extends NetworkException {
  const NoInternetNetworkException([String message = 'ইন্টারনেট সংযোগ নেই। অনুগ্রহ করে সংযোগ পরীক্ষা করুন।'])
      : super(message: message);
}

class ServerNetworkException extends NetworkException {
  const ServerNetworkException([String message = 'সার্ভারের সাথে যোগাযোগে সমস্যা হয়েছে।'])
      : super(message: message, statusCode: 500);
}
