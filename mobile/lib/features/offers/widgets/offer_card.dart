import 'package:flutter/material.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/constants/app_colors.dart';
import '../models/offer_model.dart';
import '../models/offer_enums.dart';
import 'offer_status_badge.dart';

class OfferCard extends StatelessWidget {
  final OfferModel offer;
  final VoidCallback? onTap;
  final VoidCallback? onAccept;
  final VoidCallback? onCounter;
  final VoidCallback? onReject;
  final VoidCallback? onCancel;
  final bool isProposer;

  const OfferCard({
    super.key,
    required this.offer,
    this.onTap,
    this.onAccept,
    this.onCounter,
    this.onReject,
    this.onCancel,
    this.isProposer = false,
  });

  @override
  Widget build(BuildContext context) {
    final bool canInteract = offer.status == OfferStatus.pending && !offer.isExpired;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: offer.status == OfferStatus.accepted
              ? Colors.green.shade400
              : Colors.grey.shade300,
          width: offer.status == OfferStatus.accepted ? 1.5 : 1.0,
        ),
      ),
      elevation: 1.5,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header: Version & Type & Status
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: AppColors.primaryLight.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          'v${offer.version} ${offer.offerType.labelBn}',
                          style: const TextStyle(
                            fontFamily: AppTypography.fontBalooDa2,
                            fontSize: 12,
                            fontWeight: FontWeight.w700,
                            color: AppColors.primary,
                          ),
                        ),
                      ),
                      if (offer.isProviderVerified) ...[
                        const SizedBox(width: 6),
                        const Icon(Icons.verified, size: 16, color: Colors.blue),
                      ],
                    ],
                  ),
                  OfferStatusBadge(status: offer.status),
                ],
              ),
              const SizedBox(height: 10),

              // Title
              Text(
                offer.titleBn,
                style: const TextStyle(
                  fontFamily: AppTypography.fontHindSiliguri,
                  fontSize: 17,
                  fontWeight: FontWeight.w700,
                  color: AppColors.textPrimary,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),

              const SizedBox(height: 4),

              // Provider & Demand context
              Text(
                'সেবাদাতা: ${offer.providerBusinessNameBn} | প্রয়োজন: ${offer.demandTitleBn}',
                style: TextStyle(
                  fontFamily: AppTypography.fontTiroBangla,
                  fontSize: 13,
                  color: Colors.grey.shade700,
                ),
              ),

              const SizedBox(height: 12),

              // Pricing Box
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Colors.grey.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: BorderSide(color: Colors.grey.shade200),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'মূল দর: ৳${offer.price.toStringAsFixed(2)}',
                          style: TextStyle(
                            fontFamily: AppTypography.fontTiroBangla,
                            fontSize: 12,
                            color: Colors.grey.shade600,
                          ),
                        ),
                        if (offer.deliveryFee > 0 || offer.serviceFee > 0)
                          Text(
                            '+ ফি: ৳${(offer.deliveryFee + offer.serviceFee).toStringAsFixed(2)}',
                            style: TextStyle(
                              fontFamily: AppTypography.fontTiroBangla,
                              fontSize: 11,
                              color: Colors.grey.shade500,
                            ),
                          ),
                      ],
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          'সর্বমোট',
                          style: TextStyle(
                            fontFamily: AppTypography.fontTiroBangla,
                            fontSize: 11,
                            color: Colors.grey.shade600,
                          ),
                        ),
                        Text(
                          '৳${offer.totalAmount.toStringAsFixed(2)}',
                          style: const TextStyle(
                            fontFamily: AppTypography.fontBalooDa2,
                            fontSize: 18,
                            fontWeight: FontWeight.w700,
                            color: AppColors.primary,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              if (offer.estimatedDeliveryDuration.isNotEmpty) ...[
                const SizedBox(height: 8),
                Row(
                  children: [
                    Icon(Icons.timer_outlined, size: 14, color: Colors.grey.shade600),
                    const SizedBox(width: 4),
                    Text(
                      'আনুমানিক সময়: ${offer.estimatedDeliveryDuration}',
                      style: TextStyle(
                        fontFamily: AppTypography.fontTiroBangla,
                        fontSize: 12,
                        color: Colors.grey.shade700,
                      ),
                    ),
                  ],
                ),
              ],

              // Action Buttons
              if (canInteract) ...[
                const Divider(height: 24),
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    if (isProposer) ...[
                      OutlinedButton.icon(
                        onPressed: onCancel,
                        icon: const Icon(Icons.close, size: 16, color: Colors.red),
                        label: const Text(
                          'বাতিল করুন',
                          style: TextStyle(
                            fontFamily: AppTypography.fontBalooDa2,
                            color: Colors.red,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: Colors.red),
                        ),
                      ),
                    ] else ...[
                      TextButton(
                        onPressed: onReject,
                        child: const Text(
                          'প্রত্যাখ্যান',
                          style: TextStyle(
                            fontFamily: AppTypography.fontBalooDa2,
                            color: Colors.red,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      OutlinedButton(
                        onPressed: onCounter,
                        child: const Text(
                          'পাল্টা প্রস্তাব',
                          style: TextStyle(
                            fontFamily: AppTypography.fontBalooDa2,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      ElevatedButton(
                        onPressed: onAccept,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green.shade700,
                          foregroundColor: Colors.white,
                        ),
                        child: const Text(
                          'গ্রহণ করুন',
                          style: TextStyle(
                            fontFamily: AppTypography.fontBalooDa2,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
