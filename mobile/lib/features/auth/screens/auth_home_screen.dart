import 'package:flutter/material.dart';
import '../models/user.dart';
import '../repositories/auth_repository.dart';
import '../../location/repositories/location_repository.dart';
import '../../location/state/location_state.dart';
import '../../location/widgets/location_header_chip.dart';
import '../../location/screens/location_selection_screen.dart';

/// Basic authenticated screen with user identity and location foundation.
class AuthHomeScreen extends StatefulWidget {
  final AuthRepository authRepository;
  final LocationRepository locationRepository;
  final User user;

  const AuthHomeScreen({
    super.key,
    required this.authRepository,
    required this.locationRepository,
    required this.user,
  });

  @override
  State<AuthHomeScreen> createState() => _AuthHomeScreenState();
}

class _AuthHomeScreenState extends State<AuthHomeScreen> {
  bool _isLoggingOut = false;

  @override
  void initState() {
    super.initState();
    widget.locationRepository.initialize();
  }

  Future<void> _handleLogout() async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('লগআউট নিশ্চিতকরণ'),
        content: const Text('আপনি কি নিশ্চিত যে আপনি আপনার অ্যাকাউন্ট থেকে লগআউট করতে চান?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('না'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(ctx, true),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFDC2626),
              foregroundColor: Colors.white,
            ),
            child: const Text('লগআউট'),
          ),
        ],
      ),
    );

    if (confirm != true) return;

    setState(() => _isLoggingOut = true);
    await widget.authRepository.logout();
  }

  @override
  Widget build(BuildContext context) {
    final user = widget.user;

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('সেবাকক্স প্রোফাইল'),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF0F172A),
        elevation: 0,
        actions: [
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: LocationHeaderChip(locationRepository: widget.locationRepository),
          ),
          const SizedBox(width: 8),
          IconButton(
            icon: _isLoggingOut
                ? const SizedBox(
                    width: 18,
                    height: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.logout, color: Color(0xFFDC2626)),
            tooltip: 'লগআউট',
            onPressed: _isLoggingOut ? null : _handleLogout,
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Location Card (Phase 3 Foundation)
              StreamBuilder<LocationState>(
                stream: widget.locationRepository.stateStream,
                initialData: widget.locationRepository.currentState,
                builder: (context, snapshot) {
                  final locState = snapshot.data ?? LocationState.initial();
                  final selectedLoc = locState.selectedLocation;
                  final gpsLoc = locState.currentGpsLocation;

                  return Card(
                    elevation: 0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                      side: const BorderSide(color: Color(0xFF006A4E), width: 1.2),
                    ),
                    color: const Color(0xFFF0FDF4),
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              const Row(
                                children: [
                                  Icon(Icons.location_on, color: Color(0xFF006A4E), size: 20),
                                  SizedBox(width: 6),
                                  Text(
                                    'নির্বাচিত সেবা এলাকা',
                                    style: TextStyle(
                                      fontSize: 15,
                                      fontWeight: FontWeight.bold,
                                      color: Color(0xFF006A4E),
                                    ),
                                  ),
                                ],
                              ),
                              TextButton(
                                onPressed: () {
                                  Navigator.of(context).push(
                                    MaterialPageRoute(
                                      builder: (_) => LocationSelectionScreen(
                                        locationRepository: widget.locationRepository,
                                      ),
                                    ),
                                  );
                                },
                                style: TextButton.styleFrom(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                  minimumSize: Size.zero,
                                  tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                                ),
                                child: const Text(
                                  'পরিবর্তন করুন',
                                  style: TextStyle(
                                    fontSize: 13,
                                    fontWeight: FontWeight.w600,
                                    color: Color(0xFF006A4E),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          Text(
                            selectedLoc != null && selectedLoc.displayAddressBn.isNotEmpty
                                ? selectedLoc.displayAddressBn
                                : 'কোনো সেবা এলাকা নির্বাচন করা হয়নি',
                            style: const TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF0F172A),
                            ),
                          ),
                          if (gpsLoc != null) ...[
                            const SizedBox(height: 8),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(6),
                                border: Border.all(color: const Color(0xFFD1D5DB)),
                              ),
                              child: Row(
                                children: [
                                  const Icon(Icons.gps_fixed, size: 14, color: Color(0xFF0284C7)),
                                  const SizedBox(width: 6),
                                  Expanded(
                                    child: Text(
                                      'বর্তমান জিপিএস: ${gpsLoc.addressText}',
                                      style: const TextStyle(fontSize: 11, color: Color(0xFF475569)),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  );
                },
              ),
              const SizedBox(height: 16),
              // Success badge
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFECFDF5),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFFA7F3D0)),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.verified, color: Color(0xFF059669), size: 28),
                    SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'লগইন সফল হয়েছে',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF065F46),
                            ),
                          ),
                          Text(
                            'সেশন সক্রিয় এবং সুরক্ষিত রয়েছে।',
                            style: TextStyle(
                              fontSize: 13,
                              color: Color(0xFF047857),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // User Info Card
              Card(
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                  side: const BorderSide(color: Color(0xFFE2E8F0)),
                ),
                color: Colors.white,
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'ব্যবহারকারীর বিবরণ',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF0F172A),
                        ),
                      ),
                      const Divider(height: 24),
                      _buildInfoRow('ব্যবহারকারী আইডি', '#${user.id}'),
                      _buildInfoRow('মোবাইল নম্বর', user.mobileNumber),
                      if (user.email != null && user.email!.isNotEmpty)
                        _buildInfoRow('ইমেইল', user.email!),
                      _buildInfoRow(
                        'যাচাইকরণ অবস্থা',
                        user.isVerified ? 'যাচাইকৃত (Verified)' : 'অযাচাইকৃত',
                        textColor: user.isVerified ? const Color(0xFF059669) : const Color(0xFFDC2626),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 24),

              // Security info
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFF1F5F9),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.shield_outlined, size: 18, color: Color(0xFF475569)),
                        SizedBox(width: 8),
                        Text(
                          'নিরাপত্তা ও গোপনীয়তা',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF334155),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 6),
                    Text(
                      '• JWT অ্যাক্সেস ও রিফ্রেশ টোকেন FlutterSecureStorage-এ এনক্রিপ্ট অবস্থায় সংরক্ষিত।\n• ওটিপি কোড ও পাসওয়ার্ড কখনোই অ্যাপ লগ অথবা অনিরাপদ স্টোরেজে উন্মুক্ত করা হয় না।\n• ৪০১ অননুমোদিত ত্রুটিতে স্বয়ংক্রিয় টোকেন রিফ্রেশ কার্যকর।',
                      style: TextStyle(
                        fontSize: 12,
                        color: Color(0xFF64748B),
                        height: 1.5,
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 32),

              // Logout button
              OutlinedButton.icon(
                onPressed: _isLoggingOut ? null : _handleLogout,
                icon: const Icon(Icons.logout, color: Color(0xFFDC2626)),
                label: const Text(
                  'লগআউট',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFFDC2626),
                  ),
                ),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  side: const BorderSide(color: Color(0xFFFCA5A5)),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value, {Color? textColor}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(
              fontSize: 14,
              color: Color(0xFF64748B),
            ),
          ),
          Text(
            value,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: textColor ?? const Color(0xFF0F172A),
            ),
          ),
        ],
      ),
    );
  }
}
