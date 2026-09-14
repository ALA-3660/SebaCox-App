import 'package:flutter/material.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/constants/app_colors.dart';
import '../services/offer_service.dart';

class CreateOfferScreen extends StatefulWidget {
  final int demandId;
  final int providerId;
  final String demandTitleBn;
  final double? suggestedBudget;
  final int? matchCandidateId;

  const CreateOfferScreen({
    super.key,
    required this.demandId,
    required this.providerId,
    required this.demandTitleBn,
    this.suggestedBudget,
    this.matchCandidateId,
  });

  @override
  State<CreateOfferScreen> createState() => _CreateOfferScreenState();
}

class _CreateOfferScreenState extends State<CreateOfferScreen> {
  final _formKey = GlobalKey<FormState>();
  final OfferService _offerService = OfferService();

  late TextEditingController _titleController;
  late TextEditingController _priceController;
  final TextEditingController _deliveryFeeController = TextEditingController(text: '0.00');
  final TextEditingController _serviceFeeController = TextEditingController(text: '0.00');
  final TextEditingController _descController = TextEditingController();
  final TextEditingController _durationController = TextEditingController();
  final TextEditingController _termsController = TextEditingController();

  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController(text: 'প্রস্তাব: ${widget.demandTitleBn}');
    _priceController = TextEditingController(
      text: widget.suggestedBudget != null ? widget.suggestedBudget!.toStringAsFixed(2) : '',
    );
  }

  @override
  void dispose() {
    _titleController.dispose();
    _priceController.dispose();
    _deliveryFeeController.dispose();
    _serviceFeeController.dispose();
    _descController.dispose();
    _durationController.dispose();
    _termsController.dispose();
    super.dispose();
  }

  double get _calculatedTotal {
    final p = double.tryParse(_priceController.text) ?? 0.0;
    final d = double.tryParse(_deliveryFeeController.text) ?? 0.0;
    final s = double.tryParse(_serviceFeeController.text) ?? 0.0;
    return p + d + s;
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isSubmitting = true);

    try {
      final price = double.parse(_priceController.text);
      final deliveryFee = double.tryParse(_deliveryFeeController.text) ?? 0.0;
      final serviceFee = double.tryParse(_serviceFeeController.text) ?? 0.0;

      final offer = await _offerService.createInitialOffer(
        demandId: widget.demandId,
        providerId: widget.providerId,
        titleBn: _titleController.text,
        price: price,
        deliveryFee: deliveryFee,
        serviceFee: serviceFee,
        descriptionBn: _descController.text,
        estimatedDeliveryDuration: _durationController.text,
        termsBn: _termsController.text,
        matchCandidateId: widget.matchCandidateId,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('প্রস্তাব সফলভাবে প্রেরণ করা হয়েছে!')),
        );
        Navigator.pop(context, offer);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('ত্রুটি: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('নতুন প্রস্তাব তৈরি', style: AppTypography.appBarTitle),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'প্রয়োজন: ${widget.demandTitleBn}',
                style: const TextStyle(
                  fontFamily: AppTypography.fontHindSiliguri,
                  fontSize: 16,
                  fontWeight: FontWeight.w700,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(
                  labelText: 'প্রস্তাবের শিরোনাম *',
                  border: OutlineInputBorder(),
                ),
                validator: (v) => (v == null || v.trim().isEmpty) ? 'শিরোনাম আবশ্যক' : null,
              ),
              const SizedBox(height: 16),

              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _priceController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: const InputDecoration(
                        labelText: 'মূল মূল্য (৳) *',
                        border: OutlineInputBorder(),
                        prefixText: '৳ ',
                      ),
                      onChanged: (_) => setState(() {}),
                      validator: (v) {
                        if (v == null || v.isEmpty) return 'মূল্য আবশ্যক';
                        final val = double.tryParse(v);
                        if (val == null || val <= 0) return 'সঠিক মূল্য দিন';
                        return null;
                      },
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextFormField(
                      controller: _deliveryFeeController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: const InputDecoration(
                        labelText: 'ডেলিভারি ফি (৳)',
                        border: OutlineInputBorder(),
                        prefixText: '৳ ',
                      ),
                      onChanged: (_) => setState(() {}),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              TextFormField(
                controller: _serviceFeeController,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                decoration: const InputDecoration(
                  labelText: 'সার্ভিস চার্জ / অতিরিক্ত ফি (৳)',
                  border: OutlineInputBorder(),
                  prefixText: '৳ ',
                ),
                onChanged: (_) => setState(() {}),
              ),
              const SizedBox(height: 16),

              // Total Calculation Preview
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.primaryLight.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(8),
                  border: BorderSide(color: AppColors.primary.withOpacity(0.3)),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'সর্বমোট প্রস্তাবিত মূল্য:',
                      style: TextStyle(
                        fontFamily: AppTypography.fontBalooDa2,
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    Text(
                      '৳${_calculatedTotal.toStringAsFixed(2)}',
                      style: const TextStyle(
                        fontFamily: AppTypography.fontBalooDa2,
                        fontSize: 18,
                        fontWeight: FontWeight.w700,
                        color: AppColors.primary,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _durationController,
                decoration: const InputDecoration(
                  labelText: 'আনুমানিক সময়কাল (যেমন: ২ দিন, ২৪ ঘণ্টা)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _descController,
                maxLines: 3,
                decoration: const InputDecoration(
                  labelText: 'কাজের প্রস্তাবনার বিস্তারিত বিবরণ',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _termsController,
                maxLines: 2,
                decoration: const InputDecoration(
                  labelText: 'শর্তাবলী (যদি থাকে)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isSubmitting ? null : _submit,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                  child: _isSubmitting
                      ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Text(
                          'প্রস্তাব প্রেরণ করুন',
                          style: TextStyle(
                            fontFamily: AppTypography.fontBalooDa2,
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
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
