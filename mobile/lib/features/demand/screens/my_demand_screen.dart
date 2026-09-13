/// My Demands / “আমার প্রয়োজন” Screen in Flutter client.
/// Tabs: সক্রিয় (Active), খসড়া (Draft), সম্পন্ন (Fulfilled), ইতিহাস (History)
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

import 'package:flutter/material.dart';
import '../models/demand_model.dart';
import '../models/demand_enums.dart';
import '../widgets/demand_card.dart';

class MyDemandScreen extends StatefulWidget {
  final List<DemandModel> demands;
  final VoidCallback onAddNew;
  final Function(DemandModel) onSelectDemand;

  const MyDemandScreen({
    super.key,
    required this.demands,
    required this.onAddNew,
    required this.onSelectDemand,
  });

  @override
  State<MyDemandScreen> createState() => _MyDemandScreenState();
}

class _MyDemandScreenState extends State<MyDemandScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  List<DemandModel> get activeDemands =>
      widget.demands.where((d) => d.status == DemandStatus.published || d.status == DemandStatus.paused).toList();

  List<DemandModel> get draftDemands =>
      widget.demands.where((d) => d.status == DemandStatus.draft).toList();

  List<DemandModel> get fulfilledDemands =>
      widget.demands.where((d) => d.status == DemandStatus.fulfilled).toList();

  List<DemandModel> get historyDemands =>
      widget.demands.where((d) => d.status == DemandStatus.cancelled || d.status == DemandStatus.expired || d.status == DemandStatus.closed).toList();

  Widget _buildEmptyState(String message) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.inbox_outlined, size: 48, color: Color(0xFF94A3B8)),
            const SizedBox(height: 12),
            Text(
              message,
              style: const TextStyle(
                fontFamily: 'TiroBangla',
                fontSize: 14,
                color: Color(0xFF64748B),
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildList(List<DemandModel> list, String emptyMessage) {
    if (list.isEmpty) {
      return _buildEmptyState(emptyMessage);
    }
    return ListView.builder(
      padding: const EdgeInsets.symmetric(vertical: 8),
      itemCount: list.length,
      itemBuilder: (ctx, i) => DemandCard(
        demand: list[i],
        onTap: () => widget.onSelectDemand(list[i]),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text(
          'আমার প্রয়োজন',
          style: TextStyle(
            fontFamily: 'HindSiliguri',
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF0F172A),
        elevation: 0.5,
        bottom: TabBar(
          controller: _tabController,
          labelColor: const Color(0xFF0D9488),
          unselectedLabelColor: const Color(0xFF64748B),
          indicatorColor: const Color(0xFF0D9488),
          labelStyle: const TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 13),
          tabs: [
            Tab(text: 'সক্রিয় (${activeDemands.length})'),
            Tab(text: 'খসড়া (${draftDemands.length})'),
            Tab(text: 'সম্পন্ন (${fulfilledDemands.length})'),
            Tab(text: 'ইতিহাস (${historyDemands.length})'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildList(activeDemands, 'আপনার কোনো সক্রিয় প্রয়োজন নেই।'),
          _buildList(draftDemands, 'কোনো খসড়া প্রয়োজন সংরক্ষিত নেই।'),
          _buildList(fulfilledDemands, 'এখনো কোনো প্রয়োজন পূরণ হিসেবে চিহ্নিত হয়নি।'),
          _buildList(historyDemands, 'পূর্বে বাতিল বা মেয়াদোত্তীর্ণ প্রয়োজনের ইতিহাস এখানে থাকবে।'),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: widget.onAddNew,
        backgroundColor: const Color(0xFF0D9488),
        icon: const Icon(Icons.add, color: Colors.white),
        label: const Text(
          'নতুন প্রয়োজন',
          style: TextStyle(
            fontFamily: 'BalooDa2',
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
    );
  }
}
