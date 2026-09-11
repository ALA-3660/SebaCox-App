import '../../../core/constants/api_constants.dart';
import '../../../core/network/api_client.dart';
import '../../../shared/models/api_response.dart';
import '../models/auth_tokens.dart';
import '../models/user.dart';

/// Network service for SebaCox Authentication API.
class AuthService {
  final ApiClient _apiClient;

  AuthService(this._apiClient);

  /// Request OTP for registration
  Future<ApiResponse<Map<String, dynamic>>> requestRegisterOtp(String mobileNumber) async {
    return _apiClient.post<Map<String, dynamic>>(
      ApiConstants.registerRequestOtp,
      body: {'mobile_number': mobileNumber},
      fromJson: (data) => data as Map<String, dynamic>,
    );
  }

  /// Verify OTP and complete registration
  Future<ApiResponse<Map<String, dynamic>>> verifyRegisterOtp({
    required String mobileNumber,
    required String otpCode,
  }) async {
    return _apiClient.post<Map<String, dynamic>>(
      ApiConstants.registerVerifyOtp,
      body: {
        'mobile_number': mobileNumber,
        'otp_code': otpCode,
      },
      fromJson: (data) => data as Map<String, dynamic>,
    );
  }

  /// Request OTP for login
  Future<ApiResponse<Map<String, dynamic>>> requestLoginOtp(String mobileNumber) async {
    return _apiClient.post<Map<String, dynamic>>(
      ApiConstants.loginRequestOtp,
      body: {'mobile_number': mobileNumber},
      fromJson: (data) => data as Map<String, dynamic>,
    );
  }

  /// Verify OTP and complete login
  Future<ApiResponse<Map<String, dynamic>>> verifyLoginOtp({
    required String mobileNumber,
    required String otpCode,
  }) async {
    return _apiClient.post<Map<String, dynamic>>(
      ApiConstants.loginVerifyOtp,
      body: {
        'mobile_number': mobileNumber,
        'otp_code': otpCode,
      },
      fromJson: (data) => data as Map<String, dynamic>,
    );
  }

  /// Refresh expired access token
  Future<ApiResponse<Map<String, dynamic>>> refreshAccessToken(String refreshToken) async {
    return _apiClient.post<Map<String, dynamic>>(
      ApiConstants.tokenRefresh,
      body: {'refresh_token': refreshToken},
      fromJson: (data) => data as Map<String, dynamic>,
      retryOnAuthFailure: false,
    );
  }

  /// Invalidate refresh token and logout
  Future<ApiResponse<void>> logout({String? refreshToken}) async {
    return _apiClient.post<void>(
      ApiConstants.logout,
      body: refreshToken != null ? {'refresh_token': refreshToken} : null,
      retryOnAuthFailure: false,
    );
  }

  /// Fetch authenticated user identity
  Future<ApiResponse<User>> getCurrentUser() async {
    return _apiClient.get<User>(
      ApiConstants.currentUser,
      fromJson: (data) => User.fromJson(data as Map<String, dynamic>),
    );
  }
}
