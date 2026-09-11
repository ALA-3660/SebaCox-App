/// Health Check Model for SebaCox API GET /api/v1/health/
class HealthStatus {
  final String status;

  const HealthStatus({required this.status});

  factory HealthStatus.fromJson(Map<String, dynamic> json) {
    return HealthStatus(
      status: json['status'] as String? ?? 'unknown',
    );
  }

  Map<String, dynamic> toJson() => {'status': status};

  bool get isHealthy => status.toLowerCase() == 'healthy';
}
