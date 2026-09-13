/// Demand Detail Screen / “প্রয়োজনের বিস্তারিত”
/// Displays complete requirements, location, budget, requester profile,
/// and contextual lifecycle controls.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

import 'package:flutter/material.dart';
import '../models/demand_model.dart';
import '../models/demand_enums.dart';
import '../widgets/demand_status_badge.dart';

class DemandDetailScreen extends StatelessWidget {
  final DemandModel demand;
  final Function(String action, Map<String, dynamic>? body)? onAction;

  const DemandDetailScreen({
    super.key,
    required this.demand,
    this.onAction,
  });

  Widget _buildSection({required String title, required Widget child}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontFamily: 'BalooDa2',
              fontWeight: FontWeight.bold,
              fontSize: 14,
              color: Color(0xFF334155),
            ),
          ),
          const SizedBox(height: 8),
          child,
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text(
          'প্রয়োজনের বিস্তারিত',
          style: TextStyle(
            fontFamily: 'HindSiliguri',
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF0F172A),
        elevation: 0.5,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Header Card
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: const Color(0xFFE2E8F0)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    DemandStatusBadge(status: demand.status),
                    if (demand.priority == DemandPriority.urgent)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFEE2E2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Text(
                          'জরুরি প্রয়োজন',
                          style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 11, color: Color(0xFFDC2626)),
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 12),
                Text(
                  demand.titleBn,
                  style: const TextStyle(
                    fontFamily: 'BalooDa2',
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                    color: Color(0xFF0F172A),
                    height: 1.3,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Description Section
          _buildSection(
            title: 'বিবরণ',
            child: Text(
              demand.descriptionBn,
              style: const TextStyle(
                fontFamily: 'TiroBangla',
                fontSize: 14,
                color: Color(0xFF334155),
                height: 1.5,
              ),
            ),
          ),

          // Location & Budget Section
          _buildSection(
            title: 'স্থান ও বাজেট',
            child: Column(
              children: [
                Row(
                  children: [
                    const Icon(Icons.location_on_outlined, size: 16, color: Color(0xFF0D9488)),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        demand.locationDisplayBn ?? demand.upazilaNameBn ?? 'কক্সবাজার',
                        style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF1E293B)),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Row(
                  children: [
                    const Icon(Icons.payments_outlined, size: 16, color: Color(0xFF047857)),
                    const SizedBox(width: 8),
                    Text(
                      demand.budgetDisplay,
                      style: const TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF047857)),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Requester & Contact Section
          _buildSection(
            title: 'অনুরোধকারীর তথ্য',
            child: Row(
              children: [
                const CircleAvatar(
                  backgroundColor: Color(0xFFCCFBF1),
                  child: Icon(Icons.person, color: Color(0xFF0D9488)),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        demand.requesterName,
                        style: const TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14),
                      ),
                      if (demand.contactPhone != null && demand.contactPhone!.isNotEmpty)
                        Text(
                          demand.contactPhone!,
                          style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 12, color: Color(0xFF64748B)),
                        ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Owner Lifecycle Controls
          if (demand.isOwner && onAction != null) ...[
            const SizedBox(height: 8),
            if (demand.status == DemandStatus.draft)
              ElevatedButton.icon(
                onPressed: () => onAction!('publish', null),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF0D9488),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                icon: const Icon(Icons.publish, color: Colors.white),
                label: const Text(
                  'এখনই প্রকাশ করুন',
                  style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14, color: Colors.white),
                ),
              ),
            if (demand.status == DemandStatus.published) ...[
              ElevatedButton.icon(
                onPressed: () => onAction!('fulfill', null),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF1D4ED8),
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                icon: const Icon(Icons.task_alt, color: Colors.white),
                label: const Text(
                  'প্রয়োজন পূরণ হয়েছে চিহ্নিত করুন',
                  style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 13, color: Colors.white),
                ),
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () => onAction!('pause', null),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      child: const Text('সাময়িক স্থগিত', style: TextStyle(fontFamily: 'BalooDa2', color: Color(0xFFA16207))),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () => onAction!('cancel', null),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      child: const Text('বাতিল করুন', style: TextStyle(fontFamily: 'BalooDa2', color: Color(0xFFDC2626))),
                    ),
                  ),
                ],
              ),
            ],
            if (demand.status == DemandStatus.paused)
              ElevatedButton.icon(
                onPressed: () => onAction!('resume', null),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF0D9488),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                icon: const Icon(Icons.play_arrow, color: Colors.white),
                label: const Text(
                  'পুনরায় প্রকাশ করুন',
                  style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14, color: Colors.white),
                ),
              ),
          ],
        ],
      ),
    );
  }
}
