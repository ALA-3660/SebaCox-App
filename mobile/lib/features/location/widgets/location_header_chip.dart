/// Header badge chip displaying the active selected service location.
/// "মানুষের প্রয়োজন থেকে সেবার সমাধান।"
import 'package:flutter/material.dart';
import '../repositories/location_repository.dart';
import '../state/location_state.dart';
import '../screens/location_selection_screen.dart';

class LocationHeaderChip extends StatelessWidget {
  final LocationRepository locationRepository;

  const LocationHeaderChip({
    super.key,
    required this.locationRepository,
  });

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<LocationState>(
      stream: locationRepository.stateStream,
      initialData: locationRepository.currentState,
      builder: (context, snapshot) {
        final state = snapshot.data ?? LocationState.initial();
        final displayText = state.currentDisplayNameBn;

        return InkWell(
          onTap: () {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (_) => LocationSelectionScreen(
                  locationRepository: locationRepository,
                ),
              ),
            );
          },
          borderRadius: BorderRadius.circular(20),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.92),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: const Color(0xFF006A4E).withOpacity(0.3)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.04),
                  blurRadius: 4,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(
                  Icons.location_on,
                  color: Color(0xFF006A4E),
                  size: 16,
                ),
                const SizedBox(width: 4),
                ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 160),
                  child: Text(
                    displayText,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF1E293B),
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                const SizedBox(width: 2),
                const Icon(
                  Icons.keyboard_arrow_down,
                  color: Color(0xFF64748B),
                  size: 16,
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
