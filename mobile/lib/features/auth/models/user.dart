/// Safe User representation in SebaCox client.
/// Exposes only non-sensitive authentication identity fields.
class User {
  final int id;
  final String mobileNumber;
  final String? email;
  final bool isVerified;
  final DateTime? createdAt;

  const User({
    required this.id,
    required this.mobileNumber,
    this.email,
    required this.isVerified,
    this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] is int ? json['id'] as int : int.tryParse(json['id'].toString()) ?? 0,
      mobileNumber: json['mobile_number'] as String? ?? '',
      email: json['email'] as String?,
      isVerified: json['is_verified'] == true,
      createdAt: json['created_at'] != null ? DateTime.tryParse(json['created_at'].toString()) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'mobile_number': mobileNumber,
      'email': email,
      'is_verified': isVerified,
      'created_at': createdAt?.toIso8601String(),
    };
  }
}
