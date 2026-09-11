import 'dart:async';
import 'package:flutter/material.dart';
import '../repositories/auth_repository.dart';
import '../widgets/otp_input_field.dart';

class OtpScreen extends StatefulWidget {
  final AuthRepository authRepository;
  final String mobileNumber;
  final bool isRegistration;
  final String? devOtp;

  const OtpScreen({
    super.key,
    required this.authRepository,
    required this.mobileNumber,
    required this.isRegistration,
    this.devOtp,
  });

  @override
  State<OtpScreen> createState() => _OtpScreenState();
}

class _OtpScreenState extends State<OtpScreen> {
  final _otpController = TextEditingController();
  bool _isLoading = false;
  String? _errorMessage;
  int _countdownSeconds = 60;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _startCountdown();
    if (widget.devOtp != null) {
      _otpController.text = widget.devOtp!;
    }
  }

  void _startCountdown() {
    _timer?.cancel();
    _countdownSeconds = 60;
    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_countdownSeconds <= 1) {
        timer.cancel();
        if (mounted) setState(() => _countdownSeconds = 0);
      } else {
        if (mounted) setState(() => _countdownSeconds--);
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _otpController.dispose();
    super.dispose();
  }

  Future<void> _handleVerifyOtp() async {
    final code = _otpController.text.trim();
    if (code.length != 6) {
      setState(() => _errorMessage = 'সঠিক ৬ অঙ্কের ওটিপি লিখুন।');
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = widget.isRegistration
          ? await widget.authRepository.verifyRegisterOtp(
              mobileNumber: widget.mobileNumber,
              otpCode: code,
            )
          : await widget.authRepository.verifyLoginOtp(
              mobileNumber: widget.mobileNumber,
              otpCode: code,
            );

      if (!mounted) return;
      setState(() => _isLoading = false);

      if (response.isSuccess) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              widget.isRegistration ? 'নিবন্ধন সফল হয়েছে!' : 'লগইন সফল হয়েছে!',
            ),
            backgroundColor: const Color(0xFF0F766E),
          ),
        );
        Navigator.of(context).popUntil((route) => route.isFirst);
      } else {
        setState(() {
          _errorMessage = response.message.isNotEmpty
              ? response.message
              : 'ওটিপি যাচাই করা যায়নি। অনুগ্রহ করে আবার চেষ্টা করুন।';
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

  Future<void> _handleResendOtp() async {
    if (_countdownSeconds > 0) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = widget.isRegistration
          ? await widget.authRepository.requestRegisterOtp(widget.mobileNumber)
          : await widget.authRepository.requestLoginOtp(widget.mobileNumber);

      if (!mounted) return;
      setState(() => _isLoading = false);

      if (response.isSuccess) {
        _startCountdown();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('নতুন ওটিপি পাঠানো হয়েছে'),
            backgroundColor: Color(0xFF0F766E),
          ),
        );
      } else {
        setState(() {
          _errorMessage = response.message;
        });
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _isLoading = false;
        _errorMessage = 'পুনরায় ওটিপি পাঠাতে সমস্যা হয়েছে।';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('ওটিপি যাচাইকরণ'),
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
              // Success feedback banner
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFECFDF5),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFFA7F3D0)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.check_circle_outline, color: Color(0xFF047857), size: 20),
                        SizedBox(width: 8),
                        Text(
                          'ওটিপি পাঠানো হয়েছে',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF065F46),
                            fontSize: 15,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'নম্বর: ${widget.mobileNumber}',
                      style: const TextStyle(
                        fontSize: 14,
                        color: Color(0xFF047857),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),

              if (widget.devOtp != null) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFEF3C7),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: const Color(0xFFFDE68A)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.developer_mode, color: Color(0xFFB45309), size: 18),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'ডেভেলপমেন্ট টেস্ট কোড: ${widget.devOtp}',
                          style: const TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF92400E),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],

              const SizedBox(height: 28),

              // OTP input
              OtpInputField(
                controller: _otpController,
                enabled: !_isLoading,
                errorText: _errorMessage,
              ),

              const SizedBox(height: 24),

              // Verify button
              ElevatedButton(
                onPressed: _isLoading ? null : _handleVerifyOtp,
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
                        'যাচাই করুন',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
              ),

              const SizedBox(height: 20),

              // Resend cooldown
              Center(
                child: _countdownSeconds > 0
                    ? Text(
                        'আবার ওটিপি পাঠাতে অপেক্ষা করুন: $_countdownSeconds সেকেন্ড',
                        style: const TextStyle(
                          fontSize: 13,
                          color: Color(0xFF64748B),
                        ),
                      )
                    : TextButton(
                        onPressed: _isLoading ? null : _handleResendOtp,
                        child: const Text(
                          'আবার ওটিপি পাঠান',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF0F766E),
                          ),
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
