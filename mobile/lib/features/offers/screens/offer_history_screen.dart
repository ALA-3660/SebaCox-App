import 'package:flutter/material.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/constants/app_colors.dart';
import '../models/offer_model.dart';
import '../services/offer_service.dart';
import '../widgets/offer_status_badge.dart';

class OfferHistoryScreen extends StatefulWidget {
  final int offerId;

  const OfferHistoryScreen({super.key, required this.offerId});

  @override
  State<OfferHistoryScreen> createState() => _OfferHistoryScreenState();
}

class _OfferHistoryScreenState extends State<OfferHistoryScreen> {
  final OfferService _offerService = OfferService();

  List<OfferModel> _chain = [];
  List<OfferAuditLogModel> _auditLogs = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final res = await _offerService.fetchOfferHistory(widget.offerId);
      setState(() {
        _chain = res['chain'] as List<OfferModel>;
        _auditLogs = res['audit_trail'] as List<OfferAuditLogModel>;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'ইতিহাস লোড করতে ত্রুটি: $e';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('দরকষাকষি ও পরিবর্তন ইতিহাস', style: AppTypography.appBarTitle),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _errorMessage != null
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(_errorMessage!, style: const TextStyle(fontFamily: AppTypography.fontTiroBangla)),
                      const SizedBox(height: 12),
                      ElevatedButton(onPressed: _loadHistory, child: const Text('পুনরায় চেষ্টা করুন')),
                    ],
                  ),
                )
              : ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    const Text(
                      'প্রস্তাবের সংস্করণ ক্রম (Versions)',
                      style: AppTypography.largeHeading3,
                    ),
                    const SizedBox(height: 12),
                    ..._chain.map((offer) => _buildChainItem(offer)),
                    const SizedBox(height: 24),
                    const Text(
                      'অডিট রেকর্ড (Audit Trail)',
                      style: AppTypography.largeHeading3,
                    ),
                    const SizedBox(height: 12),
                    ..._auditLogs.map((log) => _buildAuditItem(log)),
                  ],
                ),
    );
  }

  Widget _buildChainItem(OfferModel offer) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: Padding(
        padding: const EdgeInsets.all(14.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'সংস্করণ v${offer.version} • ${offer.offerType.labelBn}',
                  style: const TextStyle(
                    fontFamily: AppTypography.fontBalooDa2,
                    fontWeight: FontWeight.w700,
                    fontSize: 14,
                    color: AppColors.primary,
                  ),
                ),
                OfferStatusBadge(status: offer.status),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              offer.titleBn,
              style: const TextStyle(
                fontFamily: AppTypography.fontHindSiliguri,
                fontSize: 15,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 4),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'প্রস্তাবক: ${offer.proposerSummary?['name'] ?? 'পক্ষ'}',
                  style: TextStyle(fontFamily: AppTypography.fontTiroBangla, fontSize: 13, color: Colors.grey.shade700),
                ),
                Text(
                  '৳${offer.totalAmount.toStringAsFixed(2)}',
                  style: const TextStyle(
                    fontFamily: AppTypography.fontBalooDa2,
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                    color: AppColors.primary,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAuditItem(OfferAuditLogModel log) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(8),
        border: BorderSide(color: Colors.grey.shade200),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.history_toggle_drop, size: 20, color: Colors.grey.shade600),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${log.actionLabel} (${log.actorName})',
                  style: const TextStyle(
                    fontFamily: AppTypography.fontBalooDa2,
                    fontWeight: FontWeight.w700,
                    fontSize: 13,
                  ),
                ),
                if (log.previousStatus.isNotEmpty || log.newStatus.isNotEmpty)
                  Text(
                    '${log.previousStatus} ➔ ${log.newStatus}',
                    style: TextStyle(fontFamily: AppTypography.fontTiroBangla, fontSize: 12, color: Colors.grey.shade600),
                  ),
                Text(
                  log.createdAt.toLocal().toString().split('.')[0],
                  style: TextStyle(fontFamily: AppTypography.fontTiroBangla, fontSize: 11, color: Colors.grey.shade500),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
