/// Generic API response wrapper matching SebaCox backend response specification.
class ApiResponse<T> {
  final bool success;
  final T? data;
  final String message;
  final dynamic errors;
  final int? statusCode;

  const ApiResponse({
    required this.success,
    this.data,
    required this.message,
    this.errors,
    this.statusCode,
  });

  factory ApiResponse.success({
    T? data,
    String message = 'সফলভাবে সম্পন্ন হয়েছে',
    int? statusCode,
  }) {
    return ApiResponse<T>(
      success: true,
      data: data,
      message: message,
      statusCode: statusCode,
    );
  }

  factory ApiResponse.error({
    String message = 'অনুরোধটি সম্পন্ন করা যায়নি',
    dynamic errors,
    int? statusCode,
  }) {
    return ApiResponse<T>(
      success: false,
      data: null,
      message: message,
      errors: errors,
      statusCode: statusCode,
    );
  }
}
