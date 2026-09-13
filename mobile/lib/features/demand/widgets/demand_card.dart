/// Card widget representing a single Demand in Flutter lists.
/// Enforces Bengali typography: Baloo Da 2 for headings, Tiro Bangla for details.
library;

import 'package:flutter/material.dart';
import '../models/demand_model.dart';
import '../models/demand_enums.dart';
import 'demand_status_badge.dart';

class DemandCard extends StatelessWidget {
  final DemandModel demand;
  final VoidCallback onTap;

  const DemandCard({
    super.key,
    required this.demand,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final isUrgent = demand.priority == DemandPriority.urgent;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      elevation: 0.5,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(
          color: isUrgent ? const Color(0xFFFCA5A5) : const Color(0xFFE2E8F0),
          width: isUrgent ? 1.5 : 1.0,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(14),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header row: Status & Priority
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  DemandStatusBadge(status: demand.status, isCompact: true),
                  if (isUrgent)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: const Color(0xFFFEE2E2),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: const Row(
                        children: [
                          Icon(Icons.bolt, size: 12, color: Color(0xFFDC2626)),
                          SizedBox(width: 2),
                          Text(
                            'জরুরি',
                            style: TextStyle(
                              fontFamily: 'BalooDa2',
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFFDC2626),
                            ),
                          ),
                        ],
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 8),

              // Title in Baloo Da 2
              Text(
                demand.titleBn,
                style: const TextStyle(
                  fontFamily: 'BalooDa2',
                  fontSize: 15,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF0F172A),
                  height: 1.3,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 6),

              // Service & Category chip
              if (demand.serviceNameBn != null || demand.categoryNameBn != null)
                Row(
                  children: [
                    const Icon(Icons.category_outlined, size: 13, color: Color(0xFF64748B)),
                    const SizedBox(width: 4),
                    Text(
                      demand.serviceNameBn ?? demand.categoryNameBn ?? '',
                      style: const TextStyle(
                        fontFamily: 'TiroBangla',
                        fontSize: 12,
                        color: Color(0xFF475569),
                      ),
                    ),
                  ],
                ),
              const SizedBox(height: 8),

              const Divider(height: 1, color: Color(0xFFF1F5F9)),
              const SizedBox(height: 8),

              // Location & Budget Row
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Location
                  Row(
                    children: [
                      const Icon(Icons.location_on_outlined, size: 13, color: Color(0xFF0D9488)),
                      const SizedBox(width: 3),
                      Text(
                        demand.upazilaNameBn ?? demand.locationDisplayBn ?? 'কক্সবাজার',
                        style: const TextStyle(
                          fontFamily: 'TiroBangla',
                          fontSize: 12,
                          color: Color(0xFF334155),
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),

                  // Budget
                  Text(
                    demand.budgetDisplay,
                    style: const TextStyle(
                      fontFamily: 'BalooDa2',
                      fontSize: 13,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF047857),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
