/// Coordinate point representation.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”

class GeoPoint {
  final double latitude;
  final double longitude;
  final String addressText;
  final int srid;

  const GeoPoint({
    required this.latitude,
    required this.longitude,
    this.addressText = '',
    this.srid = 4326,
  });

  factory GeoPoint.fromJson(Map<String, dynamic> json) {
    return GeoPoint(
      latitude: (json['latitude'] is num)
          ? (json['latitude'] as num).toDouble()
          : double.tryParse(json['latitude'].toString()) ?? 0.0,
      longitude: (json['longitude'] is num)
          ? (json['longitude'] as num).toDouble()
          : double.tryParse(json['longitude'].toString()) ?? 0.0,
      addressText: json['address_text'] as String? ?? '',
      srid: json['srid'] as int? ?? 4326,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'latitude': latitude,
      'longitude': longitude,
      'address_text': addressText,
      'srid': srid,
    };
  }

  @override
  String toString() => 'GeoPoint($latitude, $longitude)';
}
