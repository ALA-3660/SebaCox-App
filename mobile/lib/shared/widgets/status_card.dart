import 'package:flutter/material.dart';
import '../../core/constants/app_colors.dart';

enum ConnectionStateStatus { loading, success, failure }

/// Reusable status presentation card for connection checks.
class StatusCard extends StatelessWidget {
  final ConnectionStateStatus status;
  final String message;
  final String? details;

  const StatusCard({
    super.key,
    required this.status,
    required this.message,
    this.details,
  });

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color border;
    Color iconColor;
    IconData icon;

    switch (status) {
      case ConnectionStateStatus.loading:
        bg = Colors.blue.shade50;
        border = Colors.blue.shade200;
        iconColor = Colors.blue.shade700;
        icon = Icons.sync_rounded;
        break;
      case ConnectionStateStatus.success:
        bg = AppColors.successLight;
        border = AppColors.success;
        iconColor = AppColors.success;
        icon = Icons.check_circle_rounded;
        break;
      case ConnectionStateStatus.failure:
        bg = AppColors.errorLight;
        border = AppColors.error;
        iconColor = AppColors.error;
        icon = Icons.error_rounded;
        break;
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: border, width: 1.5),
      ),
      child: Column(
        children: [
          status == ConnectionStateStatus.loading
              ? const SizedBox(
                  width: 36,
                  height: 36,
                  child: CircularProgressIndicator(strokeWidth: 3),
                )
              : Icon(icon, color: iconColor, size: 42),
          const SizedBox(height: 16),
          Text(
            message,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w700,
              color: AppColors.textPrimary,
            ),
          ),
          if (details != null && details!.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(
              details!,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 13,
                color: AppColors.textSecondary,
              ),
            ),
          ],
        ],
      ),
    );
  }
}
