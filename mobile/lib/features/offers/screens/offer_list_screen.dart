import 'package:flutter/material.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/constants/app_colors.dart';
import '../models/offer_model.dart';
import '../models/offer_enums.dart';
import '../services/offer_service.dart';
import '../widgets/offer_card.dart';
import 'offer_detail_screen.dart';
import 'counter_offer_screen.dart';

class OfferListScreen extends StatefulWidget {
  final int? demandId;
  final String? role;

  const OfferListScreen({super.key, this.demandId, this.role});

  @override
  State<OfferListScreen> createState() => _OfferListScreenState();
}

class _OfferListScreenState extends State<OfferListScreen> with SingleTickerProviderStateMixin {
  final OfferService _offerService = OfferService();
  late TabController _tabController;

  List<OfferModel> _allOffers = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _loadOffers();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadOffers() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final offers = widget.demandId != null
          ? await _offerService.fetchDemandOffers(widget.demandId!)
          : await _offerService.fetchUserOffers(role: widget.role);

      setState(() {
        _allOffers = offers;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'প্রস্তাব লোড করতে সমস্যা হয়েছে: $e';
        _isLoading = false;
      });
    }
  }

  List<OfferModel> _filterByTab(int tabIndex) {
    switch (tabIndex) {
      case 0: // All
        return _allOffers;
      case 1: // Pending
        return _allOffers.where((o) => o.status == OfferStatus.pending).toList();
      case 2: // Accepted
        return _allOffers.where((o) => o.status == OfferStatus.accepted).toList();
      case 3: // Archived / Completed (rejected, cancelled, expired, superseded)
        return _allOffers.where((o) => o.status != OfferStatus.pending && o.status != OfferStatus.accepted).toList();
      default:
        return _allOffers;
    }
  }

  Future<void> _handleAccept(OfferModel offer) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('প্রস্তাব গ্রহণ করুন', style: AppTypography.largeHeading3),
        content: Text(
          'আপনি কি নিশ্চিতভাবে ৳${offer.totalAmount.toStringAsFixed(2)}-এর প্রস্তাবটি গ্রহণ করতে চান?',
          style: const TextStyle(fontFamily: AppTypography.fontTiroBangla),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('না', style: TextStyle(fontFamily: AppTypography.fontBalooDa2)),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(ctx, true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
            child: const Text('হ্যাঁ, গ্রহণ করুন', style: TextStyle(fontFamily: AppTypography.fontBalooDa2)),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        await _offerService.acceptOffer(offer.id);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('প্রস্তাব সফলভাবে গ্রহণ করা হয়েছে!')),
        );
        _loadOffers();
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('ত্রুটি: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  Future<void> _handleReject(OfferModel offer) async {
    final reasonController = TextEditingController();
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('প্রস্তাব প্রত্যাখ্যান', style: AppTypography.largeHeading3),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'প্রস্তাবটি প্রত্যাখ্যানের কারণ উল্লেখ করুন (ঐচ্ছিক):',
              style: TextStyle(fontFamily: AppTypography.fontTiroBangla),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: reasonController,
              decoration: const InputDecoration(
                hintText: 'যেমন: বাজেট অতিরিক্ত / অন্য সময়ে প্রয়োজন',
                border: OutlineInputBorder(),
              ),
              maxLines: 2,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('ফিরে যান', style: TextStyle(fontFamily: AppTypography.fontBalooDa2)),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(ctx, true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('প্রত্যাখ্যান করুন', style: TextStyle(fontFamily: AppTypography.fontBalooDa2)),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        await _offerService.rejectOffer(offer.id, reasonBn: reasonController.text);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('প্রস্তাব প্রত্যাখ্যান করা হয়েছে।')),
        );
        _loadOffers();
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('ত্রুটি: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  Future<void> _handleCancel(OfferModel offer) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('প্রস্তাব বাতিল করুন', style: AppTypography.largeHeading3),
        content: const Text(
          'আপনি কি নিজের প্রেরিত এই প্রস্তাবটি প্রত্যাহার বা বাতিল করতে চান?',
          style: TextStyle(fontFamily: AppTypography.fontTiroBangla),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('না', style: TextStyle(fontFamily: AppTypography.fontBalooDa2)),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(ctx, true),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('হ্যাঁ, বাতিল করুন', style: TextStyle(fontFamily: AppTypography.fontBalooDa2)),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        await _offerService.cancelOffer(offer.id);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('প্রস্তাব বাতিল করা হয়েছে।')),
        );
        _loadOffers();
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('ত্রুটি: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'প্রস্তাবসমূহ',
          style: AppTypography.appBarTitle,
        ),
        bottom: TabBar(
          controller: _tabController,
          labelStyle: const TextStyle(
            fontFamily: AppTypography.fontBalooDa2,
            fontWeight: FontWeight.w700,
            fontSize: 14,
          ),
          unselectedLabelStyle: const TextStyle(
            fontFamily: AppTypography.fontBalooDa2,
            fontWeight: FontWeight.w500,
            fontSize: 14,
          ),
          tabs: const [
            Tab(text: 'সকল'),
            Tab(text: 'অপেক্ষমাণ'),
            Tab(text: 'গৃহীত'),
            Tab(text: 'অন্যান্য'),
          ],
        ),
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
                      ElevatedButton(onPressed: _loadOffers, child: const Text('পুনরায় চেষ্টা করুন')),
                    ],
                  ),
                )
              : TabBarView(
                  controller: _tabController,
                  children: [
                    _buildOfferList(0),
                    _buildOfferList(1),
                    _buildOfferList(2),
                    _buildOfferList(3),
                  ],
                ),
    );
  }

  Widget _buildOfferList(int tabIndex) {
    final list = _filterByTab(tabIndex);
    if (list.isEmpty) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.inbox_outlined, size: 64, color: Colors.grey.shade400),
              const SizedBox(height: 12),
              const Text(
                'কোনো প্রস্তাব পাওয়া যায়নি',
                style: AppTypography.largeHeading3,
              ),
              const SizedBox(height: 6),
              Text(
                '“প্রয়োজন থেকে সমাধান- এক অ্যাপেই”\n“খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontFamily: AppTypography.fontTiroBangla,
                  fontSize: 13,
                  color: Colors.grey.shade600,
                ),
              ),
            ],
          ),
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _loadOffers,
      child: ListView.builder(
        padding: const EdgeInsets.symmetric(vertical: 8),
        itemCount: list.length,
        itemBuilder: (ctx, idx) {
          final offer = list[idx];
          return OfferCard(
            offer: offer,
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (c) => OfferDetailScreen(offerId: offer.id),
                ),
              ).then((_) => _loadOffers());
            },
            onAccept: () => _handleAccept(offer),
            onReject: () => _handleReject(offer),
            onCancel: () => _handleCancel(offer),
            onCounter: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (c) => CounterOfferScreen(parentOffer: offer),
                ),
              ).then((_) => _loadOffers());
            },
          );
        },
      ),
    );
  }
}
