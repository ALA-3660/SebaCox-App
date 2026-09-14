import 'package:flutter/material.dart';
import '../../../../core/theme/app_typography.dart';
import '../models/offer_enums.dart';

class OfferStatusBadge extends StatelessWidget {
  final OfferStatus status;

  const OfferStatusBadge({super.key, required this.status});

  @override
  Widget build(BuildContext context) {
    Color bgColor;
    Color textColor;

    switch (status) {
      case OfferStatus.draft:
        bgColor = Colors.grey.shade200;
        textColor = Colors.grey.shade800;
        break;
      case OfferStatus.pending:
        bgColor = Colors.amber.shade100;
        textColor = Colors.amber.shade900;
        break;
      case OfferStatus.accepted:
        bgColor = Colors.green.shade100;
        textColor = Colors.green.shade800;
        break;
      case OfferStatus.rejected:
        bgColor = Colors.red.shade100;
        textColor = Colors.red.shade800;
        break;
      case OfferStatus.cancelled:
        bgColor = Colors.blueGrey.shade100;
        textColor = Colors.blueGrey.shade800;
        break;
      case OfferStatus.expired:
        bgColor = Colors.deepOrange.shade100;
        textColor = Colors.deepOrange.shade900;
        break;
      case OfferStatus.superseded:
        bgColor = Colors.purple.shade100;
        textColor = Colors.purple.shade900;
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        status.labelBn,
        style: TextStyle(
          fontFamily: AppTypography.fontBalooDa2,
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: textColor,
          height: 1.2,
        ),
      ),
    );
  }
}
