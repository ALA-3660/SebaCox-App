/// Availability Badge Widget for SebaCox.
/// Global Bangla Typography Standard: Baloo Da 2 for tags & badges.
library;

import 'package:flutter/material.dart';
import '../../../core/theme/app_typography.dart';
import '../models/provider_enums.dart';

class AvailabilityBadge extends StatelessWidget {
  final AvailabilityStatus status;
  final bool showDot;

  const AvailabilityBadge({
    super.key,
    required this.status,
    this.showDot = true,
  });

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color fg;
    Color dot;

    switch (status) {
      case AvailabilityStatus.available:
        bg = const Color(0xFFE8F5E9);
        fg = const Color(0xFF2E7D32);
        dot = const Color(0xFF4CAF50);
        break;
      case AvailabilityStatus.busy:
        bg = const Color(0xFFFFF3E0);
        fg = const Color(0xFFE65100);
        dot = const Color(0xFFFF9800);
        break;
      case AvailabilityStatus.temporarilyUnavailable:
        bg = const Color(0xFFFFEBEE);
        fg = const Color(0xFFC62828);
        dot = const Color(0xFFEF5350);
        break;
      case AvailabilityStatus.offline:
        bg = const Color(0xFFECEFF1);
        fg = const Color(0xFF546E7A);
        dot = const Color(0xFF90A4AE);
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (showDot) ...[
            Container(
              width: 6,
              height: 6,
              decoration: BoxDecoration(
                color: dot,
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 5),
          ],
          Text(
            status.labelBn,
            style: AppTypography.mediumHeading3.copyWith(
              color: fg,
              fontSize: 11,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
