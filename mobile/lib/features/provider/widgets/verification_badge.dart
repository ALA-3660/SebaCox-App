/// Verification Badge Widget for SebaCox.
/// Global Bangla Typography Standard: Baloo Da 2 for tags & badges.
library;

import 'package:flutter/material.dart';
import '../../../core/theme/app_typography.dart';
import '../models/provider_enums.dart';

class VerificationBadge extends StatelessWidget {
  final VerificationStatus status;
  final bool isVerified;

  const VerificationBadge({
    super.key,
    required this.status,
    required this.isVerified,
  });

  @override
  Widget build(BuildContext context) {
    if (!isVerified && status == VerificationStatus.unverified) {
      return const SizedBox.shrink();
    }

    Color bg;
    Color fg;
    IconData icon;
    String label = status.labelBn;

    if (isVerified || status == VerificationStatus.verified) {
      bg = const Color(0xFFE0F2FE);
      fg = const Color(0xFF0369A1);
      icon = Icons.verified_rounded;
      label = 'যাচাইকৃত';
    } else if (status == VerificationStatus.pending) {
      bg = const Color(0xFFFEF3C7);
      fg = const Color(0xFFB45309);
      icon = Icons.pending_outlined;
    } else {
      bg = const Color(0xFFF1F5F9);
      fg = const Color(0xFF64748B);
      icon = Icons.info_outline_rounded;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 12, color: fg),
          const SizedBox(width: 4),
          Text(
            label,
            style: AppTypography.mediumHeading3.copyWith(
              color: fg,
              fontSize: 10,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
