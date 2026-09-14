import 'package:flutter/material.dart';
import '../../../../core/theme/app_typography.dart';
import '../../../../core/constants/app_colors.dart';
import '../models/offer_model.dart';
import '../services/offer_service.dart';

class CounterOfferScreen extends StatefulWidget {
  final OfferModel parentOffer;

  const CounterOfferScreen({super.key, required this.parentOffer});

  @override
  State<CounterOfferScreen> createState() => _CounterOfferScreenState();
}

class _CounterOfferScreenState extends State<CounterOfferScreen> {
  final _formKey = GlobalKey<FormState>();
  final OfferService _offerService = OfferService();

  late TextEditingController _priceController;
  late TextEditingController _deliveryFeeController;
  late TextEditingController _serviceFeeController;
  late TextEditingController _descController;
  late TextEditingController _durationController;
  late TextEditingController _termsController;

  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _priceController = TextEditingController(text: widget.parentOffer.price.toStringAsFixed(2));
    _deliveryFeeController = TextEditingController(text: widget.parentOffer.deliveryFee.toStringAsFixed(2));
    _serviceFeeController = TextEditingController(text: widget.parentOffer.serviceFee.toStringAsFixed(2));
    _descController = TextEditingController(text: widget.parentOffer.descriptionBn);
    _durationController = TextEditingController(text: widget.parentOffer.estimatedDeliveryDuration);
    _termsController = TextEditingController(text: widget.parentOffer.termsBn);
  }

  @override
  void dispose() {
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

      final counterOffer = await _offerService.createCounterOffer(
        parentOfferId: widget.parentOffer.id,
        price: price,
        deliveryFee: deliveryFee,
        serviceFee: serviceFee,
        descriptionBn: _descController.text,
        estimatedDeliveryDuration: _durationController.text,
        termsBn: _termsController.text,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('পাল্টা প্রস্তাব সফলভাবে পাঠানো হয়েছে!')),
        );
        Navigator.pop(context, counterOffer);
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
        title: Text('পাল্টা প্রস্তাব (v${widget.parentOffer.version + 1})', style: AppTypography.appBarTitle),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Parent Offer Summary Box
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(8),
                  border: BorderSide(color: Colors.grey.shade300),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'বর্তমান প্রস্তাব: ${widget.parentOffer.titleBn}',
                      style: const TextStyle(
                        fontFamily: AppTypography.fontBalooDa2,
                        fontWeight: FontWeight.w700,
                        fontSize: 14,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'বর্তমান সর্বমোট: ৳${widget.parentOffer.totalAmount.toStringAsFixed(2)}',
                      style: const TextStyle(
                        fontFamily: AppTypography.fontTiroBangla,
                        color: Colors.red,
                        fontWeight: FontWeight.w600,
                        fontSize: 13,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              const Text(
                'আপনার প্রস্তাবিত নতুন দর ও শর্ত নির্ধারণ করুন:',
                style: AppTypography.largeHeading3,
              ),
              const SizedBox(height: 12),

              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _priceController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: const InputDecoration(
                        labelText: 'নতুন মূল্য (৳) *',
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
                  labelText: 'সার্ভিস চার্জ (৳)',
                  border: OutlineInputBorder(),
                  prefixText: '৳ ',
                ),
                onChanged: (_) => setState(() {}),
              ),
              const SizedBox(height: 16),

              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.amber.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: BorderSide(color: Colors.amber.shade200),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'নতুন সর্বমোট প্রদেয়:',
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
                        color: Colors.deepOrange,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _durationController,
                decoration: const InputDecoration(
                  labelText: 'প্রস্তাবিত সময়কাল (যেমন: ১ দিন, ১২ ঘণ্টা)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _descController,
                maxLines: 3,
                decoration: const InputDecoration(
                  labelText: 'পাল্টা প্রস্তাবনার কারণ ও মন্তব্য',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),

              TextFormField(
                controller: _termsController,
                maxLines: 2,
                decoration: const InputDecoration(
                  labelText: 'সংশোধিত শর্তাবলী (যদি থাকে)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isSubmitting ? null : _submit,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.amber.shade800,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                  child: _isSubmitting
                      ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Text(
                          'পাল্টা প্রস্তাব প্রেরণ করুন',
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
