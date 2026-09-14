import 'package:flutter/material.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/constants/app_colors.dart';
import '../models/offer_model.dart';
import '../models/offer_enums.dart';
import '../services/offer_service.dart';
import '../widgets/offer_status_badge.dart';
import 'counter_offer_screen.dart';
import 'offer_history_screen.dart';

class OfferDetailScreen extends StatefulWidget {
  final int offerId;

  const OfferDetailScreen({super.key, required this.offerId});

  @override
  State<OfferDetailScreen> createState() => _OfferDetailScreenState();
}

class _OfferDetailScreenState extends State<OfferDetailScreen> {
  final OfferService _offerService = OfferService();
  OfferModel? _offer;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadDetail();
  }

  Future<void> _loadDetail() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final offer = await _offerService.fetchOfferDetail(widget.offerId);
      setState(() {
        _offer = offer;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'প্রস্তাবের বিবরণ আনতে ব্যর্থ: $e';
        _isLoading = false;
      });
    }
  }

  Future<void> _accept() async {
    if (_offer == null) return;
    try {
      await _offerService.acceptOffer(_offer!.id);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('প্রস্তাব সফলভাবে গৃহীত হয়েছে!')),
      );
      _loadDetail();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('ত্রুটি: $e'), backgroundColor: Colors.red),
      );
    }
  }

  Future<void> _reject() async {
    if (_offer == null) return;
    final controller = TextEditingController();
    final confirm = await showDialog<bool>(
      context: context,
      builder: (c) => AlertDialog(
        title: const Text('প্রস্তাব প্রত্যাখ্যান', style: AppTypography.largeHeading3),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            hintText: 'প্রত্যাখ্যানের কারণ লিখুন',
            border: OutlineInputBorder(),
          ),
          maxLines: 2,
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(c, false), child: const Text('বাতিল')),
          ElevatedButton(
            onPressed: () => Navigator.pop(c, true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('প্রত্যাখ্যান করুন'),
          ),
        ],
      ),
    );

    if (confirm == true) {
      try {
        await _offerService.rejectOffer(_offer!.id, reasonBn: controller.text);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('প্রস্তাব প্রত্যাখ্যাত হয়েছে।')),
        );
        _loadDetail();
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('ত্রুটি: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: const Text('প্রস্তাবের বিবরণ', style: AppTypography.appBarTitle)),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_errorMessage != null || _offer == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('প্রস্তাবের বিবরণ', style: AppTypography.appBarTitle)),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(_errorMessage ?? 'প্রস্তাব পাওয়া যায়নি', style: const TextStyle(fontFamily: AppTypography.fontTiroBangla)),
              const SizedBox(height: 12),
              ElevatedButton(onPressed: _loadDetail, child: const Text('পুনরায় চেষ্টা করুন')),
            ],
          ),
        ),
      );
    }

    final offer = _offer!;
    final canAct = offer.status == OfferStatus.pending && !offer.isExpired;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'প্রস্তাব #${offer.id} (v${offer.version})',
          style: AppTypography.appBarTitle,
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            tooltip: 'সংস্করণ ইতিহাস ও অডিট',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (c) => OfferHistoryScreen(offerId: offer.id),
                ),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Status row
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.primaryLight.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    'সংস্করণ ${offer.version} • ${offer.offerType.labelBn}',
                    style: const TextStyle(
                      fontFamily: AppTypography.fontBalooDa2,
                      fontWeight: FontWeight.w700,
                      color: AppColors.primary,
                    ),
                  ),
                ),
                OfferStatusBadge(status: offer.status),
              ],
            ),
            const SizedBox(height: 16),

            // Title
            Text(
              offer.titleBn,
              style: AppTypography.largeHeading2,
            ),
            const SizedBox(height: 8),

            // Description
            if (offer.descriptionBn.isNotEmpty) ...[
              Text(
                offer.descriptionBn,
                style: const TextStyle(
                  fontFamily: AppTypography.fontTiroBangla,
                  fontSize: 15,
                  height: 1.5,
                ),
              ),
              const SizedBox(height: 16),
            ],

            // Pricing Breakdown Card
            Card(
              elevation: 1,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              color: Colors.grey.shade50,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'মূল্য ও খরচের হিসাব (সার্ভার-সাইড নির্ধারিত)',
                      style: TextStyle(
                        fontFamily: AppTypography.fontBalooDa2,
                        fontSize: 15,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const Divider(height: 20),
                    _buildPriceRow('কাজের মূল্য (Price):', '৳${offer.price.toStringAsFixed(2)}'),
                    if (offer.deliveryFee > 0)
                      _buildPriceRow('ডেলিভারি / পরিবহন ফি:', '৳${offer.deliveryFee.toStringAsFixed(2)}'),
                    if (offer.serviceFee > 0)
                      _buildPriceRow('সার্ভিস ফি:', '৳${offer.serviceFee.toStringAsFixed(2)}'),
                    const Divider(height: 20),
                    _buildPriceRow(
                      'সর্বমোট প্রদেয় মূল্য:',
                      '৳${offer.totalAmount.toStringAsFixed(2)}',
                      isBold: true,
                      color: AppColors.primary,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Meta Info
            _buildInfoTile(Icons.store, 'সেবাদাতা', offer.providerBusinessNameBn),
            _buildInfoTile(Icons.assignment, 'সংশ্লিষ্ট প্রয়োজন', offer.demandTitleBn),
            if (offer.quantity != null && offer.quantity! > 0)
              _buildInfoTile(Icons.format_list_numbered, 'পরিমাণ', '${offer.quantity} ${offer.unit ?? ""}'),
            if (offer.estimatedDeliveryDuration.isNotEmpty)
              _buildInfoTile(Icons.schedule, 'আনুমানিক সময়কাল', offer.estimatedDeliveryDuration),
            _buildInfoTile(Icons.event_available, 'প্রস্তাবের মেয়াদ শেষ', offer.expiresAt.toLocal().toString().split('.')[0]),

            if (offer.termsBn.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Text('শর্তাবলী:', style: AppTypography.largeHeading3),
              const SizedBox(height: 4),
              Text(
                offer.termsBn,
                style: const TextStyle(fontFamily: AppTypography.fontTiroBangla, fontSize: 14),
              ),
            ],

            if (offer.rejectionReasonBn.isNotEmpty) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.red.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: BorderSide(color: Colors.red.shade200),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('প্রত্যাখ্যানের কারণ:', style: TextStyle(fontFamily: AppTypography.fontBalooDa2, fontWeight: FontWeight.w700, color: Colors.red)),
                    const SizedBox(height: 4),
                    Text(offer.rejectionReasonBn, style: const TextStyle(fontFamily: AppTypography.fontTiroBangla)),
                  ],
                ),
              ),
            ],
            const SizedBox(height: 32),

            // Slogans
            Center(
              child: Text(
                '“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”\n“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontFamily: AppTypography.fontTiroBangla,
                  fontSize: 12,
                  color: Colors.grey.shade500,
                  fontStyle: FontStyle.italic,
                ),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: canAct
          ? Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 8, offset: const Offset(0, -2))
                ],
              ),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: _reject,
                      style: OutlinedButton.styleFrom(
                        side: const BorderSide(color: Colors.red),
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                      child: const Text('প্রত্যাখ্যান', style: TextStyle(fontFamily: AppTypography.fontBalooDa2, color: Colors.red)),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (c) => CounterOfferScreen(parentOffer: offer),
                          ),
                        ).then((_) => _loadDetail());
                      },
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                      child: const Text('পাল্টা প্রস্তাব', style: TextStyle(fontFamily: AppTypography.fontBalooDa2)),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: _accept,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green.shade700,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                      child: const Text('গ্রহণ করুন', style: TextStyle(fontFamily: AppTypography.fontBalooDa2, fontWeight: FontWeight.w700)),
                    ),
                  ),
                ],
              ),
            )
          : null,
    );
  }

  Widget _buildPriceRow(String label, String value, {bool isBold = false, Color? color}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: TextStyle(
              fontFamily: AppTypography.fontTiroBangla,
              fontSize: isBold ? 15 : 13,
              fontWeight: isBold ? FontWeight.w700 : FontWeight.normal,
            ),
          ),
          Text(
            value,
            style: TextStyle(
              fontFamily: AppTypography.fontBalooDa2,
              fontSize: isBold ? 17 : 14,
              fontWeight: isBold ? FontWeight.w700 : FontWeight.w600,
              color: color ?? AppColors.textPrimary,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoTile(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        children: [
          Icon(icon, size: 20, color: Colors.grey.shade600),
          const SizedBox(width: 10),
          Text(
            '$label: ',
            style: TextStyle(
              fontFamily: AppTypography.fontBalooDa2,
              fontWeight: FontWeight.w600,
              fontSize: 14,
              color: Colors.grey.shade700,
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(
                fontFamily: AppTypography.fontTiroBangla,
                fontSize: 14,
                color: AppColors.textPrimary,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
