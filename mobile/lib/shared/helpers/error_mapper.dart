import '../../core/network/network_exceptions.dart';

/// Maps raw exceptions into clean localized user-facing messages.
class ErrorMapper {
  static String map(dynamic error) {
    if (error is TimeoutNetworkException) {
      return 'অনুরোধের সময়সীমা অতিক্রম করেছে। অনুগ্রহ করে আপনার ইন্টারনেট সংযোগ যাচাই করুন।';
    } else if (error is NoInternetNetworkException) {
      return 'ইন্টারনেট সংযোগ পাওয়া যায়নি। অনুগ্রহ করে নেটওয়ার্ক চেক করুন।';
    } else if (error is NetworkException) {
      return error.message;
    }
    return 'সার্ভারের সাথে সংযোগ ব্যর্থ হয়েছে।';
  }
}
