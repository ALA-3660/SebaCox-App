import 'package:flutter/material.dart';
import '../../../core/constants/app_brand.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../repositories/auth_repository.dart';
import '../widgets/phone_input_field.dart';
import 'otp_screen.dart';

enum AuthMode { login, register }

class AuthScreen extends StatefulWidget {
  final AuthRepository authRepository;

  const AuthScreen({
    super.key,
    required this.authRepository,
  });

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  final _phoneController = TextEditingController();
  AuthMode _mode = AuthMode.login;
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _phoneController.dispose();
    super.dispose();
  }

  Future<void> _handleRequestOtp() async {
    final rawPhone = _phoneController.text.trim();
    if (rawPhone.isEmpty) {
      setState(() => _errorMessage = 'মোবাইল নম্বর লিখুন।');
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = _mode == AuthMode.login
          ? await widget.authRepository.requestLoginOtp(rawPhone)
          : await widget.authRepository.requestRegisterOtp(rawPhone);

      if (!mounted) return;

      setState(() => _isLoading = false);

      if (response.isSuccess && response.data != null) {
        final canonicalNumber = response.data!['mobile_number'] as String? ?? rawPhone;
        final devOtp = response.data!['dev_otp'] as String?;

        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (_) => OtpScreen(
              authRepository: widget.authRepository,
              mobileNumber: canonicalNumber,
              isRegistration: _mode == AuthMode.register,
              devOtp: devOtp,
            ),
          ),
        );
      } else {
        setState(() {
          _errorMessage = response.message.isNotEmpty
              ? response.message
              : 'ওটিপি পাঠাতে সমস্যা হয়েছে। আবার চেষ্টা করুন।';
        });
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _isLoading = false;
        _errorMessage = 'নেটওয়ার্ক ত্রুটি: অনুগ্রহ করে সংযোগ পরীক্ষা করুন।';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final isLogin = _mode == AuthMode.login;

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('সেবাকক্স একাউন্ট'),
        centerTitle: true,
        elevation: 0,
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF0F172A),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 12),
              // Brand logo/tagline
              Container(
                alignment: Alignment.center,
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 18),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppColors.primary.withOpacity(0.15)),
                ),
                child: Column(
                  children: [
                    Text(
                      '${AppBrand.appNameEn} (${AppBrand.appNameBn})',
                      style: AppTypography.largeHeading2.copyWith(
                        color: AppColors.primary,
                        fontSize: 24,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      AppBrand.sloganWithQuotes,
                      textAlign: TextAlign.center,
                      style: AppTypography.mediumHeading2.copyWith(
                        color: AppColors.primaryDark,
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      AppBrand.shortDescriptionWithQuotes,
                      textAlign: TextAlign.center,
                      style: AppTypography.bodySmall.copyWith(
                        color: AppColors.textSecondary,
                        fontSize: 12,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 28),

              // Mode toggle (Login vs Register)
              Container(
                decoration: BoxDecoration(
                  color: const Color(0xFFE2E8F0),
                  borderRadius: BorderRadius.circular(12),
                ),
                padding: const EdgeInsets.all(4),
                child: Row(
                  children: [
                    Expanded(
                      child: GestureDetector(
                        onTap: () => setState(() {
                          _mode = AuthMode.login;
                          _errorMessage = null;
                        }),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          decoration: BoxDecoration(
                            color: isLogin ? Colors.white : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                            boxShadow: isLogin
                                ? [
                                    BoxShadow(
                                      color: Colors.black.withOpacity(0.05),
                                      blurRadius: 4,
                                      offset: const Offset(0, 2),
                                    )
                                  ]
                                : null,
                          ),
                          alignment: Alignment.center,
                          child: Text(
                            'লগইন',
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.bold,
                              color: isLogin ? const Color(0xFF0F766E) : const Color(0xFF64748B),
                            ),
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      child: GestureDetector(
                        onTap: () => setState(() {
                          _mode = AuthMode.register;
                          _errorMessage = null;
                        }),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          decoration: BoxDecoration(
                            color: !isLogin ? Colors.white : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                            boxShadow: !isLogin
                                ? [
                                    BoxShadow(
                                      color: Colors.black.withOpacity(0.05),
                                      blurRadius: 4,
                                      offset: const Offset(0, 2),
                                    )
                                  ]
                                : null,
                          ),
                          alignment: Alignment.center,
                          child: Text(
                            'নতুন নিবন্ধন',
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.bold,
                              color: !isLogin ? const Color(0xFF0F766E) : const Color(0xFF64748B),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Title guidance
              Text(
                isLogin ? 'আপনার অ্যাকাউন্টে লগইন করুন' : 'নতুন সেবাকক্স অ্যাকাউন্ট তৈরি করুন',
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF0F172A),
                ),
              ),
              const SizedBox(height: 6),
              const Text(
                'যাচাইকরণের জন্য আপনার মোবাইল নম্বরে একটি ৬ অঙ্কের ওটিপি পাঠানো হবে।',
                style: TextStyle(
                  fontSize: 13,
                  color: Color(0xFF64748B),
                ),
              ),
              const SizedBox(height: 20),

              // Mobile number input
              PhoneInputField(
                controller: _phoneController,
                enabled: !_isLoading,
                errorText: _errorMessage,
              ),
              const SizedBox(height: 24),

              // Action button
              ElevatedButton(
                onPressed: _isLoading ? null : _handleRequestOtp,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF0F766E),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  elevation: 0,
                ),
                child: _isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Text(
                        'ওটিপি পাঠান',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
