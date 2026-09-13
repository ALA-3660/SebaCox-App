/// Create Demand Screen / “আমার প্রয়োজন প্রকাশ করুন”
/// 6-step guided wizard or single cohesive form.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

import 'package:flutter/material.dart';
import '../models/demand_enums.dart';

class CreateDemandScreen extends StatefulWidget {
  final Function(Map<String, dynamic> data, bool publishNow) onSubmit;

  const CreateDemandScreen({
    super.key,
    required this.onSubmit,
  });

  @override
  State<CreateDemandScreen> createState() => _CreateDemandScreenState();
}

class _CreateDemandScreenState extends State<CreateDemandScreen> {
  final _formKey = GlobalKey<FormState>();

  final _titleController = TextEditingController();
  final _descController = TextEditingController();
  final _locationDisplayController = TextEditingController();
  final _quantityController = TextEditingController();
  final _unitController = TextEditingController();
  final _budgetMinController = TextEditingController();
  final _budgetMaxController = TextEditingController();

  DemandType _demandType = DemandType.service;
  DemandPriority _priority = DemandPriority.normal;
  DemandVisibility _visibility = DemandVisibility.public;
  DemandContactPreference _contactPreference = DemandContactPreference.inAppOnly;

  DateTime? _expiresAt = DateTime.now().add(const Duration(days: 7));
  bool _isSubmitting = false;

  @override
  void dispose() {
    _titleController.dispose();
    _descController.dispose();
    _locationDisplayController.dispose();
    _quantityController.dispose();
    _unitController.dispose();
    _budgetMinController.dispose();
    _budgetMaxController.dispose();
    super.dispose();
  }

  void _handleSave(bool publishNow) {
    if (!_formKey.currentState!.validate()) return;

    final data = <String, dynamic>{
      'title_bn': _titleController.text.trim(),
      'description_bn': _descController.text.trim(),
      'location_display_bn': _locationDisplayController.text.trim(),
      'demand_type': _demandType.value,
      'priority': _priority.value,
      'visibility': _visibility.value,
      'contact_preference': _contactPreference.value,
      'expires_at': _expiresAt?.toIso8601String(),
    };

    if (_quantityController.text.isNotEmpty) {
      data['quantity'] = double.tryParse(_quantityController.text);
    }
    if (_unitController.text.isNotEmpty) {
      data['unit'] = _unitController.text.trim();
    }
    if (_budgetMinController.text.isNotEmpty) {
      data['budget_min'] = double.tryParse(_budgetMinController.text);
    }
    if (_budgetMaxController.text.isNotEmpty) {
      data['budget_max'] = double.tryParse(_budgetMaxController.text);
    }

    setState(() => _isSubmitting = true);
    widget.onSubmit(data, publishNow);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text(
          'নতুন প্রয়োজন যোগ করুন',
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
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Title
            const Text(
              '১. কী প্রয়োজন? (শিরোনাম) *',
              style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 6),
            TextFormField(
              controller: _titleController,
              decoration: InputDecoration(
                hintText: 'e.g. কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন',
                hintStyle: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)),
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
                enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
              ),
              validator: (v) {
                if (v == null || v.trim().isEmpty) return 'বাংলা শিরোনাম দেওয়া আবশ্যক';
                if (v.trim().length < 5) return 'শিরোনাম কমপক্ষে ৫ অক্ষরের হতে হবে';
                return null;
              },
            ),
            const SizedBox(height: 16),

            // Description
            const Text(
              '২. বিস্তারিত বিবরণ *',
              style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 6),
            TextFormField(
              controller: _descController,
              maxLines: 4,
              decoration: InputDecoration(
                hintText: 'আপনার প্রয়োজনের সুনির্দিষ্ট বিবরণ লিখুন...',
                hintStyle: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)),
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
                enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
              ),
              validator: (v) {
                if (v == null || v.trim().isEmpty) return 'বিস্তারিত বিবরণ দেওয়া আবশ্যক';
                if (v.trim().length < 10) return 'বিবরণ কমপক্ষে ১০ অক্ষরের হতে হবে';
                return null;
              },
            ),
            const SizedBox(height: 16),

            // Location
            const Text(
              '৩. এলাকা / অবস্থান *',
              style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 6),
            TextFormField(
              controller: _locationDisplayController,
              decoration: InputDecoration(
                hintText: 'e.g. কলাতলী রোড, কক্সবাজার সদর',
                hintStyle: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)),
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
                enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
              ),
              validator: (v) {
                if (v == null || v.trim().isEmpty) return 'এলাকার বিবরণ আবশ্যক';
                return null;
              },
            ),
            const SizedBox(height: 16),

            // Budget
            const Text(
              '৪. বাজেট (টাকা, ঐচ্ছিক)',
              style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 6),
            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _budgetMinController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      hintText: 'সর্বনিম্ন (৳)',
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: TextFormField(
                    controller: _budgetMaxController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      hintText: 'সর্বোচ্চ (৳)',
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Priority
            Row(
              children: [
                const Text('জরুরি প্রয়োজন?', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14)),
                const Spacer(),
                Switch(
                  value: _priority == DemandPriority.urgent,
                  activeColor: const Color(0xFFDC2626),
                  onChanged: (val) {
                    setState(() {
                      _priority = val ? DemandPriority.urgent : DemandPriority.normal;
                    });
                  },
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Buttons: Save Draft & Publish Now
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: _isSubmitting ? null : () => _handleSave(false),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      side: const BorderSide(color: Color(0xFF0D9488)),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    child: const Text(
                      'খসড়া সংরক্ষণ',
                      style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, color: Color(0xFF0D9488)),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    onPressed: _isSubmitting ? null : () => _handleSave(true),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      backgroundColor: const Color(0xFF0D9488),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    child: const Text(
                      'প্রকাশ করুন',
                      style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
