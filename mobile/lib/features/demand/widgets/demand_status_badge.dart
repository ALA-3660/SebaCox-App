/// Demand Status Badge for Flutter UI.
/// Strict Bengali Labels & Brand Color Palette.
library;

import 'package:flutter/material.dart';
import '../models/demand_enums.dart';

class DemandStatusBadge extends StatelessWidget {
  final DemandStatus status;
  final bool isCompact;

  const DemandStatusBadge({
    super.key,
    required this.status,
    this.isCompact = false,
  });

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color fg;
    Color border;
    IconData icon;

    switch (status) {
      case DemandStatus.draft:
        bg = const Color(0xFFF1F5F9);
        fg = const Color(0xFF475569);
        border = const Color(0xFFCBD5E1);
        icon = Icons.edit_note_outlined;
        break;
      case DemandStatus.published:
        bg = const Color(0xFFF0FDF4);
        fg = const Color(0xFF15803D);
        border = const Color(0xFFBBF7D0);
        icon = Icons.check_circle_outline;
        break;
      case DemandStatus.paused:
        bg = const Color(0xFFFEFCE8);
        fg = const Color(0xFFA16207);
        border = const Color(0xFFFEF08A);
        icon = Icons.pause_circle_outline;
        break;
      case DemandStatus.fulfilled:
        bg = const Color(0xFFEFF6FF);
        fg = const Color(0xFF1D4ED8);
        border = const Color(0xFFBFDBFE);
        icon = Icons.task_alt;
        break;
      case DemandStatus.cancelled:
        bg = const Color(0xFFFEF2F2);
        fg = const Color(0xFFB91C1C);
        border = const Color(0xFFFECACA);
        icon = Icons.cancel_outlined;
        break;
      case DemandStatus.expired:
        bg = const Color(0xFFFFF7ED);
        fg = const Color(0xFFC2410C);
        border = const Color(0xFFFFEDD5);
        icon = Icons.timer_off_outlined;
        break;
      case DemandStatus.closed:
        bg = const Color(0xFFF8FAFC);
        fg = const Color(0xFF64748B);
        border = const Color(0xFFE2E8F0);
        icon = Icons.lock_outline;
        break;
    }

    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: isCompact ? 6.0 : 8.0,
        vertical: isCompact ? 2.0 : 4.0,
      ),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: border, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: isCompact ? 11 : 13, color: fg),
          const SizedBox(width: 4),
          Text(
            status.labelBn,
            style: TextStyle(
              fontFamily: 'BalooDa2',
              fontSize: isCompact ? 10.0 : 11.5,
              fontWeight: FontWeight.w600,
              color: fg,
            ),
          ),
        ],
      ),
    );
  }
}
