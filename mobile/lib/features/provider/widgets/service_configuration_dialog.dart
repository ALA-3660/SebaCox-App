/// Advanced Service Configuration Dialog for SebaCox.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
/// Global Bangla Typography Standard compliant.
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../models/provider_enums.dart';
import '../models/provider_service_model.dart';
import '../../category/models/category_model.dart';
import '../../category/models/subcategory_model.dart';
import '../../category/models/service_model.dart';
import '../../category/repositories/category_repository.dart';

class ServiceConfigurationDialog extends StatefulWidget {
  final int providerId;
  final ProviderServiceItem? existingService;
  final Function(Map<String, dynamic> data) onSave;

  const ServiceConfigurationDialog({
    super.key,
    required this.providerId,
    this.existingService,
    required this.onSave,
  });

  @override
  State<ServiceConfigurationDialog> createState() => _ServiceConfigurationDialogState();
}

class _ServiceConfigurationDialogState extends State<ServiceConfigurationDialog> {
  final _categoryRepo = CategoryRepository();

  List<CategoryModel> _categories = [];
  List<SubCategoryModel> _subcategories = [];
  List<ServiceModel> _services = [];

  CategoryModel? _selectedCategory;
  SubCategoryModel? _selectedSubcategory;
  ServiceModel? _selectedService;

  bool _isLoadingTaxonomy = true;
  bool _isLoadingSubcategories = false;
  bool _isLoadingServices = false;

  // Form Controllers
  final _titleController = TextEditingController();
  final _descController = TextEditingController();
  final _priceController = TextEditingController();
  final _maxPriceController = TextEditingController();
  final _unitController = TextEditingController();
  final _expController = TextEditingController();
  final _emergencyFeeController = TextEditingController();
  final _warrantyController = TextEditingController();
  final _skillInputController = TextEditingController();

  PriceType _selectedPriceType = PriceType.startingFrom;
  bool _isEmergencyAvailable = false;
  bool _isAvailable = true;
  final List<String> _skills = [];

  @override
  void initState() {
    super.initState();
    _initExistingData();
    _loadMasterCategories();
  }

  void _initExistingData() {
    if (widget.existingService != null) {
      final s = widget.existingService!;
      _titleController.text = s.titleBn;
      _descController.text = s.descriptionBn;
      if (s.startingPrice != null) _priceController.text = s.startingPrice!.toStringAsFixed(0);
      if (s.maxPrice != null) _maxPriceController.text = s.maxPrice!.toStringAsFixed(0);
      _unitController.text = s.unitBn;
      if (s.experienceYears != null) _expController.text = s.experienceYears.toString();
      _selectedPriceType = s.priceType;
      _isEmergencyAvailable = s.isEmergencyAvailable;
      if (s.emergencyFee != null) _emergencyFeeController.text = s.emergencyFee!.toStringAsFixed(0);
      _warrantyController.text = s.warrantyTextBn;
      _skills.addAll(s.skills);
      _isAvailable = s.isAvailable;
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descController.dispose();
    _priceController.dispose();
    _maxPriceController.dispose();
    _unitController.dispose();
    _expController.dispose();
    _emergencyFeeController.dispose();
    _warrantyController.dispose();
    _skillInputController.dispose();
    super.dispose();
  }

  Future<void> _loadMasterCategories() async {
    setState(() => _isLoadingTaxonomy = true);
    final res = await _categoryRepo.getCategories();
    if (res.isSuccess && res.data != null) {
      setState(() {
        _categories = res.data!;
        _isLoadingTaxonomy = false;
      });
    } else {
      setState(() => _isLoadingTaxonomy = false);
    }
  }

  Future<void> _loadSubcategories(int categoryId) async {
    setState(() {
      _isLoadingSubcategories = true;
      _subcategories = [];
      _services = [];
      _selectedSubcategory = null;
      _selectedService = null;
    });

    final res = await _categoryRepo.getSubcategories(categoryId: categoryId);
    if (res.isSuccess && res.data != null) {
      setState(() {
        _subcategories = res.data!;
        _isLoadingSubcategories = false;
      });
    } else {
      setState(() => _isLoadingSubcategories = false);
    }
  }

  Future<void> _loadServices(int subcategoryId) async {
    setState(() {
      _isLoadingServices = true;
      _services = [];
      _selectedService = null;
    });

    final res = await _categoryRepo.getServices(subcategoryId: subcategoryId);
    if (res.isSuccess && res.data != null) {
      setState(() {
        _services = res.data!;
        _isLoadingServices = false;
      });
    } else {
      setState(() => _isLoadingServices = false);
    }
  }

  void _addSkillTag() {
    final text = _skillInputController.text.trim();
    if (text.isNotEmpty && !_skills.contains(text)) {
      setState(() {
        _skills.add(text);
        _skillInputController.clear();
      });
    }
  }

  void _handleSubmit() {
    if (widget.existingService == null && _selectedService == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('অনুগ্রহ করে সেবা (Service) নির্বাচন করুন')),
      );
      return;
    }

    final double? startingPrice = _priceController.text.isNotEmpty
        ? double.tryParse(_priceController.text.trim())
        : null;

    final double? maxPrice = _maxPriceController.text.isNotEmpty
        ? double.tryParse(_maxPriceController.text.trim())
        : null;

    final int? expYears = _expController.text.isNotEmpty
        ? int.tryParse(_expController.text.trim())
        : null;

    final double? emergencyFee = _emergencyFeeController.text.isNotEmpty
        ? double.tryParse(_emergencyFeeController.text.trim())
        : null;

    final payload = <String, dynamic>{
      'service_id': widget.existingService?.serviceId ?? _selectedService!.id,
      'title_bn': _titleController.text.trim(),
      'description_bn': _descController.text.trim(),
      'starting_price': startingPrice,
      'max_price': maxPrice,
      'price_type': _selectedPriceType.value,
      'unit_bn': _unitController.text.trim(),
      'experience_years': expYears,
      'is_emergency_available': _isEmergencyAvailable,
      'emergency_fee': emergencyFee,
      'warranty_text_bn': _warrantyController.text.trim(),
      'skills': _skills,
      'is_available': _isAvailable,
      'is_active': true,
    };

    widget.onSave(payload);
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    final isEditing = widget.existingService != null;

    return Dialog(
      backgroundColor: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      insetPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 24),
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * 0.88,
          maxWidth: 600,
        ),
        child: Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              decoration: const BoxDecoration(
                color: AppColors.primary,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(16),
                  topRight: Radius.circular(16),
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    isEditing ? Icons.edit_note_outlined : Icons.add_circle_outline,
                    color: Colors.white,
                    size: 24,
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      isEditing ? 'সেবা কনফিগারেশন পরিবর্তন' : 'নতুন সেবা নির্বাচন ও কনফিগারেশন',
                      style: AppTypography.mediumHeading2.copyWith(
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close, color: Colors.white),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ],
              ),
            ),

            // Form Content
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (!isEditing) ...[
                      // Taxonomy cascading selectors
                      Text(
                        '১. মাস্টার ক্যাটাগরি ও সেবা নির্বাচন',
                        style: AppTypography.mediumHeading2.copyWith(
                          fontWeight: FontWeight.bold,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 12),

                      // Category Selector
                      _buildDropdown<CategoryModel>(
                        label: 'মূল ক্যাটাগরি *',
                        hint: 'ক্যাটাগরি বেছে নিন',
                        value: _selectedCategory,
                        items: _categories,
                        isLoading: _isLoadingTaxonomy,
                        itemLabel: (c) => c.nameBn,
                        onChanged: (cat) {
                          if (cat != null) {
                            setState(() => _selectedCategory = cat);
                            _loadSubcategories(cat.id);
                          }
                        },
                      ),
                      const SizedBox(height: 12),

                      // Subcategory Selector
                      if (_selectedCategory != null)
                        _buildDropdown<SubCategoryModel>(
                          label: 'সাব-ক্যাটাগরি *',
                          hint: 'সাব-ক্যাটাগরি বেছে নিন',
                          value: _selectedSubcategory,
                          items: _subcategories,
                          isLoading: _isLoadingSubcategories,
                          itemLabel: (sc) => sc.nameBn,
                          onChanged: (sub) {
                            if (sub != null) {
                              setState(() => _selectedSubcategory = sub);
                              _loadServices(sub.id);
                            }
                          },
                        ),
                      if (_selectedCategory != null) const SizedBox(height: 12),

                      // Service Selector
                      if (_selectedSubcategory != null)
                        _buildDropdown<ServiceModel>(
                          label: 'নির্দিষ্ট সেবা বা দক্ষতা *',
                          hint: 'সেবা বেছে নিন',
                          value: _selectedService,
                          items: _services,
                          isLoading: _isLoadingServices,
                          itemLabel: (s) => s.nameBn,
                          onChanged: (srv) {
                            if (srv != null) {
                              setState(() {
                                _selectedService = srv;
                                if (_titleController.text.isEmpty) {
                                  _titleController.text = srv.nameBn;
                                }
                              });
                            }
                          },
                        ),
                      const Divider(height: 32),
                    ] else ...[
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: AppColors.primary.withValues(alpha: 0.08),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: AppColors.primary.withValues(alpha: 0.2)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.miscellaneous_services, color: AppColors.primary),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Text(
                                widget.existingService!.effectiveTitleBn,
                                style: AppTypography.mediumHeading2.copyWith(
                                  fontWeight: FontWeight.bold,
                                  color: AppColors.primary,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 16),
                    ],

                    // Advanced Service Details
                    Text(
                      '২. সেবার শিরোনাম ও বিবরণ',
                      style: AppTypography.mediumHeading2.copyWith(
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Custom Title
                    TextField(
                      controller: _titleController,
                      style: AppTypography.bodyRegular,
                      decoration: InputDecoration(
                        labelText: 'কাস্টম সেবার শিরোনাম (ঐচ্ছিক)',
                        hintText: 'যেমন: ইনভার্টার এসি গ্যাস চার্জ ও মেরামত',
                        labelStyle: AppTypography.bodySmall,
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Custom Description
                    TextField(
                      controller: _descController,
                      maxLines: 3,
                      style: AppTypography.bodyRegular,
                      decoration: InputDecoration(
                        labelText: 'কাজের বিস্তারিত বিবরণ ও সেবার শর্তাবলী',
                        hintText: 'আপনার সেবার বিশেষত্ব, কাজের পরিধি ও অভিজ্ঞতা উল্লেখ করুন...',
                        labelStyle: AppTypography.bodySmall,
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        contentPadding: const EdgeInsets.all(14),
                      ),
                    ),
                    const Divider(height: 32),

                    // Pricing Configuration
                    Text(
                      '৩. মূল্য নির্ধারণ ও প্রাইসিং মডেল',
                      style: AppTypography.mediumHeading2.copyWith(
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Price Type Chips
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: PriceType.values.map((type) {
                        final isSelected = _selectedPriceType == type;
                        return ChoiceChip(
                          label: Text(
                            type.labelBn,
                            style: AppTypography.mediumHeading3.copyWith(
                              fontSize: 12,
                              fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                              color: isSelected ? Colors.white : AppColors.textPrimary,
                            ),
                          ),
                          selected: isSelected,
                          selectedColor: AppColors.primary,
                          backgroundColor: AppColors.background,
                          onSelected: (val) {
                            if (val) setState(() => _selectedPriceType = type);
                          },
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 14),

                    // Price Input Row
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _priceController,
                            keyboardType: TextInputType.number,
                            style: AppTypography.bodyRegular,
                            decoration: InputDecoration(
                              labelText: 'শুরু / মূল রেট (৳) *',
                              hintText: 'যেমন: ৫০০',
                              prefixText: '৳ ',
                              labelStyle: AppTypography.bodySmall,
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                            ),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: TextField(
                            controller: _maxPriceController,
                            keyboardType: TextInputType.number,
                            style: AppTypography.bodyRegular,
                            decoration: InputDecoration(
                              labelText: 'সর্বোচ্চ রেট (ঐচ্ছিক)',
                              hintText: 'যেমন: ১৫০০',
                              prefixText: '৳ ',
                              labelStyle: AppTypography.bodySmall,
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),

                    // Unit & Experience Row
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _unitController,
                            style: AppTypography.bodyRegular,
                            decoration: InputDecoration(
                              labelText: 'মূল্য ইউনিট',
                              hintText: 'যেমন: ঘণ্টা / পয়েন্ট / স্কয়ার ফিট',
                              labelStyle: AppTypography.bodySmall,
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                            ),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: TextField(
                            controller: _expController,
                            keyboardType: TextInputType.number,
                            style: AppTypography.bodyRegular,
                            decoration: InputDecoration(
                              labelText: 'অভিজ্ঞতা (বছর)',
                              hintText: 'যেমন: ৫',
                              suffixText: 'বছর',
                              labelStyle: AppTypography.bodySmall,
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const Divider(height: 32),

                    // Emergency & Warranty
                    Text(
                      '৪. জরুরি সেবা ও কাজের নিশ্চয়তা',
                      style: AppTypography.mediumHeading2.copyWith(
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Emergency Toggle
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: _isEmergencyAvailable ? const Color(0xFFFEF2F2) : AppColors.background,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: _isEmergencyAvailable ? const Color(0xFFFCA5A5) : AppColors.border,
                        ),
                      ),
                      child: Column(
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Row(
                                children: [
                                  const Icon(Icons.flash_on, color: Color(0xFFEF4444)),
                                  const SizedBox(width: 8),
                                  Text(
                                    '২৪/৭ জরুরি ভিত্তিতে সেবা প্রদান',
                                    style: AppTypography.mediumHeading3.copyWith(
                                      fontWeight: FontWeight.bold,
                                      color: _isEmergencyAvailable ? const Color(0xFF991B1B) : AppColors.textPrimary,
                                    ),
                                  ),
                                ],
                              ),
                              Switch(
                                value: _isEmergencyAvailable,
                                activeColor: const Color(0xFFEF4444),
                                onChanged: (val) => setState(() => _isEmergencyAvailable = val),
                              ),
                            ],
                          ),
                          if (_isEmergencyAvailable) ...[
                            const SizedBox(height: 10),
                            TextField(
                              controller: _emergencyFeeController,
                              keyboardType: TextInputType.number,
                              style: AppTypography.bodyRegular,
                              decoration: InputDecoration(
                                labelText: 'জরুরি সেবার অতিরিক্ত ফি (৳)',
                                hintText: 'যেমন: ৩০০',
                                prefixText: '৳ ',
                                labelStyle: AppTypography.bodySmall,
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                                contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                                filled: true,
                                fillColor: Colors.white,
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Warranty Note
                    TextField(
                      controller: _warrantyController,
                      style: AppTypography.bodyRegular,
                      decoration: InputDecoration(
                        labelText: 'কাজের ওয়ারেন্টি বা গ্যারান্টি (ঐচ্ছিক)',
                        hintText: 'যেমন: ৩০ দিনের ফ্রি সার্ভিসিং ওয়ারেন্টি',
                        prefixIcon: const Icon(Icons.verified_user_outlined, color: Color(0xFF10B981)),
                        labelStyle: AppTypography.bodySmall,
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                      ),
                    ),
                    const Divider(height: 32),

                    // Skills Tags
                    Text(
                      '৫. বিশেষ দক্ষতা ও কিওয়ার্ড',
                      style: AppTypography.mediumHeading2.copyWith(
                        fontWeight: FontWeight.bold,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: _skillInputController,
                            style: AppTypography.bodyRegular,
                            onSubmitted: (_) => _addSkillTag(),
                            decoration: InputDecoration(
                              hintText: 'যেমন: গ্যাস রিফিল, সার্কিট রিপেয়ার...',
                              hintStyle: AppTypography.bodySmall,
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton.icon(
                          onPressed: _addSkillTag,
                          icon: const Icon(Icons.add, size: 18),
                          label: const Text('যোগ করুন'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primary,
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                          ),
                        ),
                      ],
                    ),
                    if (_skills.isNotEmpty) ...[
                      const SizedBox(height: 10),
                      Wrap(
                        spacing: 6,
                        runSpacing: 6,
                        children: _skills.map((skill) {
                          return Chip(
                            label: Text(
                              skill,
                              style: AppTypography.bodySmall.copyWith(fontWeight: FontWeight.bold),
                            ),
                            deleteIcon: const Icon(Icons.cancel, size: 16),
                            onDeleted: () => setState(() => _skills.remove(skill)),
                            backgroundColor: AppColors.primary.withValues(alpha: 0.1),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                          );
                        }).toList(),
                      ),
                    ],
                  ],
                ),
              ),
            ),

            // Footer / Actions
            Container(
              padding: const EdgeInsets.all(16),
              decoration: const BoxDecoration(
                border: Border(top: BorderSide(color: AppColors.border)),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () => Navigator.of(context).pop(),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      child: Text('বাতিল', style: AppTypography.mediumHeading3),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    flex: 2,
                    child: ElevatedButton(
                      onPressed: _handleSubmit,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      child: Text(
                        isEditing ? 'সংরক্ষণ করুন' : 'সেবা নিশ্চিত করুন',
                        style: AppTypography.mediumHeading3.copyWith(
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDropdown<T>({
    required String label,
    required String hint,
    required T? value,
    required List<T> items,
    required bool isLoading,
    required String Function(T) itemLabel,
    required void Function(T?) onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: AppTypography.bodySmall.copyWith(
            fontWeight: FontWeight.bold,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 6),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 14),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: AppColors.border),
          ),
          child: isLoading
              ? const SizedBox(
                  height: 48,
                  child: Center(child: SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))),
                )
              : DropdownButtonHideUnderline(
                  child: DropdownButton<T>(
                    isExpanded: true,
                    value: value,
                    hint: Text(hint, style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary)),
                    items: items.map((item) {
                      return DropdownMenuItem<T>(
                        value: item,
                        child: Text(
                          itemLabel(item),
                          style: AppTypography.bodyRegular,
                        ),
                      );
                    }).toList(),
                    onChanged: onChanged,
                  ),
                ),
        ),
      ],
    );
  }
}
