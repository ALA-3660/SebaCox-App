/// Provider Registration Flow Screen ("আমি সেবা দিব")
/// Multi-step onboarding workflow for new service providers.
/// Global Bangla Typography Standard compliant.
library;

import 'package:flutter/material.dart';
import '../../../core/constants/app_colors.dart';
import '../../../core/theme/app_typography.dart';
import '../../../core/network/api_client.dart';
import '../../categories/models/category_model.dart';
import '../../categories/repositories/category_repository.dart';
import '../../categories/services/category_api_service.dart';
import '../../categories/widgets/category_selector_card.dart';
import '../../categories/widgets/category_cascading_picker.dart';
import '../models/provider_enums.dart';
import '../repositories/provider_repository.dart';

class ProviderRegistrationFlowScreen extends StatefulWidget {
  const ProviderRegistrationFlowScreen({super.key});

  @override
  State<ProviderRegistrationFlowScreen> createState() => _ProviderRegistrationFlowScreenState();
}

class _ProviderRegistrationFlowScreenState extends State<ProviderRegistrationFlowScreen> {
  final _repository = ProviderRepository();
  final _categoryRepo = CategoryRepository(CategoryApiService(ApiClient()));
  int _currentStep = 0;
  bool _isLoading = false;

  // Dynamic Category & Sub-category State (Phase 4C.7)
  List<CategoryItem> _categories = [];
  List<SubCategoryItem> _subcategories = [];
  int? _selectedCategoryId;
  String? _selectedCategoryNameBn;
  int? _selectedSubcategoryId;
  String? _selectedSubcategoryNameBn;
  bool _isLoadingCategories = false;
  bool _isLoadingSubcategories = false;
  String? _categoriesError;
  String? _subcategoriesError;

  // Step 1: Provider Type
  ProviderType _selectedType = ProviderType.individual;

  // Step 2: Basic Info
  final _nameBnController = TextEditingController();
  final _nameEnController = TextEditingController();
  final _bioBnController = TextEditingController();
  final _phoneController = TextEditingController();
  ContactVisibility _contactVisibility = ContactVisibility.registeredOnly;

  // Step 3: Service Selection (Cascading taxonomy)
  final Set<int> _selectedServices = {};

  // Step 4: Service Areas (Upazilas)
  final Set<int> _selectedUpazilas = {1}; // default Cox's Bazar Sadar

  final List<Map<String, dynamic>> _availableUpazilas = [
    {'id': 1, 'name_bn': 'কক্সবাজার সদর'},
    {'id': 2, 'name_bn': 'রামু'},
    {'id': 3, 'name_bn': 'উখিয়া'},
    {'id': 4, 'name_bn': 'টেকনাফ'},
    {'id': 5, 'name_bn': 'চকোরিয়া'},
    {'id': 6, 'name_bn': 'পেকুয়া'},
    {'id': 7, 'name_bn': 'মহেশখালী'},
    {'id': 8, 'name_bn': 'কুতুবদিয়া'},
  ];

  @override
  void initState() {
    super.initState();
    _fetchCategories();
  }

  Future<void> _fetchCategories() async {
    setState(() {
      _isLoadingCategories = true;
      _categoriesError = null;
    });
    try {
      final cats = await _categoryRepo.getMainCategories();
      if (mounted) {
        setState(() {
          _categories = cats;
          _isLoadingCategories = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoadingCategories = false;
          _categoriesError = 'ক্যাটাগরি লোড করা যায়নি।';
        });
      }
    }
  }

  Future<void> _fetchSubcategories(int categoryId) async {
    setState(() {
      _isLoadingSubcategories = true;
      _subcategoriesError = null;
    });
    try {
      final subs = await _categoryRepo.getSubcategories(categoryId);
      if (mounted) {
        setState(() {
          _subcategories = subs;
          _isLoadingSubcategories = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoadingSubcategories = false;
          _subcategoriesError = 'সাব-ক্যাটাগরি লোড করা যায়নি।';
        });
      }
    }
  }

  @override
  void dispose() {
    _nameBnController.dispose();
    _nameEnController.dispose();
    _bioBnController.dispose();
    _phoneController.dispose();
    super.dispose();
  }

  Future<void> _submitRegistration() async {
    if (_nameBnController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('অনুগ্রহ করে বাংলায় নাম লিখুন')),
      );
      setState(() => _currentStep = 1);
      return;
    }

    setState(() => _isLoading = true);

    try {
      final res = await _repository.createProviderProfile({
        'provider_type': _selectedType.value,
        'display_name_bn': _nameBnController.text.trim(),
        'display_name_en': _nameEnController.text.trim().isNotEmpty
            ? _nameEnController.text.trim()
            : _nameBnController.text.trim(),
        'short_description_bn': _bioBnController.text.trim(),
        'contact_phone': _phoneController.text.trim(),
        'contact_visibility': _contactVisibility.value,
      });

      setState(() => _isLoading = false);

      if (res.isSuccess && mounted) {
        // Link initial services and areas if any
        if (res.data != null) {
          final providerId = res.data!.id;
          for (final sId in _selectedServices) {
            await _repository.addProviderService(providerId, {'service_id': sId});
          }
          for (final uId in _selectedUpazilas) {
            await _repository.addProviderServiceArea(providerId, {'upazila_id': uId});
          }
        }

        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (ctx) => AlertDialog(
            title: Text(
              'অভিনন্দন!',
              style: AppTypography.largeHeading2.copyWith(
                color: AppColors.primary,
                fontWeight: FontWeight.bold,
              ),
            ),
            content: Text(
              'আপনার সেবাদাতা প্রোফাইল সফলভাবে তৈরি হয়েছে। আপনার সেবা তালিকা এবং প্রোফাইল সেবাকক্স প্ল্যাটফর্মে পর্যালোচনার জন্য প্রস্তুত।',
              style: AppTypography.bodyRegular,
            ),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(ctx).pop();
                  Navigator.of(context).pop(true);
                },
                child: Text(
                  'ড্যাশবোর্ডে যান',
                  style: AppTypography.mediumHeading2.copyWith(
                    color: AppColors.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        );
      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(res.message ?? 'প্রোফাইল তৈরিতে সমস্যা হয়েছে')),
        );
      }
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('ত্রুটি: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(
          'আমি সেবা দিব (নিবন্ধন)',
          style: AppTypography.mediumHeading2.copyWith(
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        backgroundColor: AppColors.primary,
        elevation: 0,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                // Step Progress Indicator
                Container(
                  color: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  child: Row(
                    children: [
                      _buildStepChip(0, 'ধরন'),
                      _buildStepDivider(),
                      _buildStepChip(1, 'তথ্য'),
                      _buildStepDivider(),
                      _buildStepChip(2, 'সেবা'),
                      _buildStepDivider(),
                      _buildStepChip(3, 'এলাকা'),
                    ],
                  ),
                ),

                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(16),
                    child: _buildStepContent(),
                  ),
                ),

                // Navigation Controls
                Container(
                  padding: const EdgeInsets.all(16),
                  color: Colors.white,
                  child: Row(
                    children: [
                      if (_currentStep > 0)
                        Expanded(
                          child: OutlinedButton(
                            onPressed: () => setState(() => _currentStep--),
                            style: OutlinedButton.styleFrom(
                              side: const BorderSide(color: AppColors.border),
                              padding: const EdgeInsets.symmetric(vertical: 14),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(12),
                              ),
                            ),
                            child: Text(
                              'পূর্ববর্তী',
                              style: AppTypography.mediumHeading2.copyWith(
                                color: AppColors.textSecondary,
                              ),
                            ),
                          ),
                        ),
                      if (_currentStep > 0) const SizedBox(width: 12),
                      Expanded(
                        child: ElevatedButton(
                          onPressed: () {
                            if (_currentStep == 1) {
                              if (_nameBnController.text.trim().isEmpty) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('অনুগ্রহ করে বাংলায় আপনার নাম লিখুন।')),
                                );
                                return;
                              }
                            } else if (_currentStep == 2) {
                              if (_selectedCategoryId == null) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('অনুগ্রহ করে প্রধান ক্যাটাগরি নির্বাচন করুন।')),
                                );
                                return;
                              }
                              if (_selectedSubcategoryId == null) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('অনুগ্রহ করে সাব-ক্যাটাগরি নির্বাচন করুন।')),
                                );
                                return;
                              }
                            }

                            if (_currentStep < 3) {
                              setState(() => _currentStep++);
                            } else {
                              _submitRegistration();
                            }
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primary,
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          child: Text(
                            _currentStep < 3 ? 'পরবর্তী' : 'নিবন্ধন সম্পন্ন করুন',
                            style: AppTypography.mediumHeading2.copyWith(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
    );
  }

  Widget _buildStepChip(int step, String label) {
    final isActive = _currentStep == step;
    final isDone = _currentStep > step;

    return Row(
      children: [
        CircleAvatar(
          radius: 12,
          backgroundColor: isActive
              ? AppColors.primary
              : (isDone ? const Color(0xFF10B981) : AppColors.border),
          child: isDone
              ? const Icon(Icons.check, size: 14, color: Colors.white)
              : Text(
                  '${step + 1}',
                  style: TextStyle(
                    fontSize: 11,
                    color: isActive ? Colors.white : AppColors.textSecondary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
        ),
        const SizedBox(width: 4),
        Text(
          label,
          style: AppTypography.mediumHeading3.copyWith(
            fontSize: 12,
            color: isActive ? AppColors.primary : AppColors.textSecondary,
            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
          ),
        ),
      ],
    );
  }

  Widget _buildStepDivider() {
    return Expanded(
      child: Container(
        height: 1,
        color: AppColors.border,
        margin: const EdgeInsets.symmetric(horizontal: 4),
      ),
    );
  }

  Widget _buildStepContent() {
    switch (_currentStep) {
      case 0:
        return _buildStep1Type();
      case 1:
        return _buildStep2Info();
      case 2:
        return _buildStep3Services();
      case 3:
        return _buildStep4Areas();
      default:
        return const SizedBox.shrink();
    }
  }

  Widget _buildStep1Type() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'আপনার সেবাদাতার ধরন নির্বাচন করুন',
          style: AppTypography.largeHeading2.copyWith(
            fontWeight: FontWeight.bold,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 6),
        Text(
          'আপনি কীভাবে সেবাকক্সে সেবা প্রদান করতে চান তা নির্ধারণ করুন।',
          style: AppTypography.bodyRegular.copyWith(
            color: AppColors.textSecondary,
          ),
        ),
        const SizedBox(height: 20),

        ...ProviderType.values.map((type) {
          final isSelected = _selectedType == type;
          return Container(
            margin: const EdgeInsets.only(bottom: 12),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.Border.all(
                color: isSelected ? AppColors.primary : AppColors.border,
                width: isSelected ? 2.0 : 1.0,
              ),
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.all(12),
              leading: Icon(
                type == ProviderType.individual
                    ? Icons.person_outline
                    : (type == ProviderType.business ? Icons.store_outlined : Icons.corporate_fare),
                color: isSelected ? AppColors.primary : AppColors.textSecondary,
                size: 32,
              ),
              title: Text(
                type.labelBn,
                style: AppTypography.mediumHeading2.copyWith(
                  fontWeight: FontWeight.bold,
                  color: isSelected ? AppColors.primary : AppColors.textPrimary,
                ),
              ),
              subtitle: Text(
                type.labelEn,
                style: AppTypography.bodySmall.copyWith(
                  color: AppColors.textSecondary,
                ),
              ),
              trailing: Radio<ProviderType>(
                value: type,
                groupValue: _selectedType,
                onChanged: (val) {
                  if (val != null) setState(() => _selectedType = val);
                },
                activeColor: AppColors.primary,
              ),
              onTap: () => setState(() => _selectedType = type),
            ),
          );
        }),
      ],
    );
  }

  Widget _buildStep2Info() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'মৌলিক তথ্য ও পরিচিতি',
          style: AppTypography.largeHeading2.copyWith(
            fontWeight: FontWeight.bold,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 16),

        TextField(
          controller: _nameBnController,
          decoration: InputDecoration(
            labelText: 'প্রদর্শনী নাম (বাংলায়) *',
            hintText: 'e.g. কক্স ইলেকট্রিক কেয়ার / মো: রফিকুল ইসলাম',
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
        ),
        const SizedBox(height: 12),

        TextField(
          controller: _nameEnController,
          decoration: InputDecoration(
            labelText: 'Display Name (English)',
            hintText: 'e.g. Cox Electric Care',
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
        ),
        const SizedBox(height: 12),

        TextField(
          controller: _bioBnController,
          maxLines: 3,
          decoration: InputDecoration(
            labelText: 'সংক্ষিপ্ত পরিচিতি বা কাজের বিবরণ',
            hintText: 'আপনার অভিজ্ঞতা বা সেবার বিশেষত্ব লিখুন...',
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
        ),
        const SizedBox(height: 12),

        TextField(
          controller: _phoneController,
          keyboardType: TextInputType.phone,
          decoration: InputDecoration(
            labelText: 'যোগাযোগের মোবাইল নম্বর',
            hintText: '01XXXXXXXXX',
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
          ),
        ),
      ],
    );
  }

  Widget _buildStep3Services() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'আপনার সেবাসমূহ বেছে নিন',
          style: AppTypography.largeHeading2.copyWith(
            fontWeight: FontWeight.bold,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 6),
        Text(
          'সেন্ট্রালাইজড মাস্টার ট্যাক্সোনমি থেকে সহজে সার্চ করে অথবা ড্রপডাউন থেকে আপনার প্রধান ক্যাটাগরি ও সাব-ক্যাটাগরি নির্বাচন করুন।',
          style: AppTypography.bodyRegular.copyWith(
            color: AppColors.textSecondary,
          ),
        ),
        const SizedBox(height: 16),

        // Quick Searchable Modal Selector Card
        CategorySelectorCard(
          repository: _categoryRepo,
          selectedCategoryId: _selectedCategoryId,
          selectedCategoryNameBn: _selectedCategoryNameBn,
          selectedSubcategoryId: _selectedSubcategoryId,
          selectedSubcategoryNameBn: _selectedSubcategoryNameBn,
          label: 'সার্চ ও নির্বাচন করুন *',
          hint: '🔍 ট্রেড বা কাজের ক্ষেত্র খুঁজুন...',
          onSelected: (result) {
            setState(() {
              _selectedCategoryId = result.category.id;
              _selectedCategoryNameBn = result.category.nameBn;
              _selectedSubcategoryId = result.subcategory.id;
              _selectedSubcategoryNameBn = result.subcategory.nameBn;
              _selectedServices = [result.subcategory.id];
            });
            _fetchSubcategories(result.category.id);
          },
          onReset: () {
            setState(() {
              _selectedCategoryId = null;
              _selectedCategoryNameBn = null;
              _selectedSubcategoryId = null;
              _selectedSubcategoryNameBn = null;
              _selectedServices.clear();
              _subcategories = [];
            });
          },
        ),

        const SizedBox(height: 18),
        Row(
          children: [
            const Expanded(child: Divider(color: Color(0xFFE2E8F0))),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: Text(
                'অথবা সরাসরি ড্রপডাউন বাছাই করুন',
                style: AppTypography.bodySmall.copyWith(
                  fontSize: 11,
                  color: const Color(0xFF94A3B8),
                ),
              ),
            ),
            const Expanded(child: Divider(color: Color(0xFFE2E8F0))),
          ],
        ),
        const SizedBox(height: 16),

        if (_categoriesError != null)
          Container(
            padding: const EdgeInsets.all(12),
            margin: const EdgeInsets.only(bottom: 14),
            decoration: BoxDecoration(
              color: const Color(0xFFFEF2F2),
              borderRadius: BorderRadius.circular(10),
              border: Border.Border.all(color: const Color(0xFFFCA5A5)),
            ),
            child: Row(
              children: [
                const Icon(Icons.error_outline, color: Color(0xFFDC2626), size: 20),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _categoriesError!,
                    style: AppTypography.bodySmall.copyWith(color: const Color(0xFFB91C1C)),
                  ),
                ),
                TextButton(
                  onPressed: _fetchCategories,
                  child: Text(
                    'পুনরায় চেষ্টা',
                    style: AppTypography.mediumHeading3.copyWith(
                      color: const Color(0xFFDC2626),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),

        // ১. প্রধান ক্যাটাগরি Dropdown
        Row(
          children: [
            Text(
              'প্রধান ক্যাটাগরি *',
              style: AppTypography.mediumHeading2.copyWith(
                fontWeight: FontWeight.bold,
                fontSize: 13,
                color: AppColors.textPrimary,
              ),
            ),
            if (_isLoadingCategories) ...[
              const SizedBox(width: 8),
              const SizedBox(
                width: 14,
                height: 14,
                child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.primary),
              ),
            ],
          ],
        ),
        const SizedBox(height: 8),
        DropdownButtonFormField<int>(
          value: _selectedCategoryId,
          hint: Text(
            _isLoadingCategories ? 'ক্যাটাগরি লোড হচ্ছে...' : '-- প্রধান ক্যাটাগরি নির্বাচন করুন --',
            style: AppTypography.bodyRegular.copyWith(color: AppColors.textSecondary),
          ),
          decoration: InputDecoration(
            filled: true,
            fillColor: Colors.white,
            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.border),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.border),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
            ),
          ),
          icon: const Icon(Icons.keyboard_arrow_down, color: AppColors.textSecondary),
          items: _categories.map((cat) {
            return DropdownMenuItem<int>(
              value: cat.id,
              child: Text(
                cat.nameBn,
                style: AppTypography.mediumHeading2.copyWith(
                  fontWeight: FontWeight.w600,
                  fontSize: 13,
                  color: AppColors.textPrimary,
                ),
              ),
            );
          }).toList(),
          onChanged: (val) {
            if (val == null) return;
            setState(() {
              _selectedCategoryId = val;
              try {
                final found = _categories.firstWhere((cat) => cat.id == val);
                _selectedCategoryNameBn = found.nameBn;
              } catch (_) {
                _selectedCategoryNameBn = null;
              }
              // Reset subcategory selection
              _selectedSubcategoryId = null;
              _selectedSubcategoryNameBn = null;
              _selectedServices.clear();
              _subcategories = [];
            });
            _fetchSubcategories(val);
          },
        ),
        const SizedBox(height: 6),
        Text(
          'আপনার ব্যবসার মূল কাজের ক্ষেত্র বা প্রধান ট্রেড সিলেক্ট করুন।',
          style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary, fontSize: 11),
        ),
        const SizedBox(height: 18),

        // ২. সাব-ক্যাটাগরি Dropdown (Cascading)
        Row(
          children: [
            Text(
              'সাব-ক্যাটাগরি *',
              style: AppTypography.mediumHeading2.copyWith(
                fontWeight: FontWeight.bold,
                fontSize: 13,
                color: AppColors.textPrimary,
              ),
            ),
            if (_isLoadingSubcategories) ...[
              const SizedBox(width: 8),
              const SizedBox(
                width: 14,
                height: 14,
                child: CircularProgressIndicator(strokeWidth: 2, color: AppColors.primary),
              ),
            ],
          ],
        ),
        const SizedBox(height: 8),

        if (_subcategoriesError != null && _selectedCategoryId != null)
          Container(
            padding: const EdgeInsets.all(10),
            margin: const EdgeInsets.only(bottom: 8),
            decoration: BoxDecoration(
              color: const Color(0xFFFEF2F2),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    _subcategoriesError!,
                    style: AppTypography.bodySmall.copyWith(color: const Color(0xFFDC2626), fontSize: 11),
                  ),
                ),
                TextButton(
                  onPressed: () => _fetchSubcategories(_selectedCategoryId!),
                  child: Text(
                    'পুনরায় চেষ্টা',
                    style: AppTypography.mediumHeading3.copyWith(
                      color: const Color(0xFFDC2626),
                      fontWeight: FontWeight.bold,
                      fontSize: 11,
                    ),
                  ),
                ),
              ],
            ),
          ),

        DropdownButtonFormField<int>(
          value: _selectedSubcategoryId,
          hint: Text(
            _selectedCategoryId == null
                ? '-- প্রথমে প্রধান ক্যাটাগরি নির্বাচন করুন --'
                : (_isLoadingSubcategories
                    ? 'সাব-ক্যাটাগরি লোড হচ্ছে...'
                    : (_subcategories.isEmpty
                        ? '-- কোনো সাব-ক্যাটাগরি পাওয়া যায়নি --'
                        : '-- সাব-ক্যাটাগরি নির্বাচন করুন --')),
            style: AppTypography.bodyRegular.copyWith(color: AppColors.textSecondary),
          ),
          decoration: InputDecoration(
            filled: true,
            fillColor: (_selectedCategoryId == null || _isLoadingSubcategories) ? const Color(0xFFF1F5F9) : Colors.white,
            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.border),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: BorderSide(
                color: _selectedCategoryId == null ? const Color(0xFFE2E8F0) : AppColors.border,
              ),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: AppColors.primary, width: 1.5),
            ),
            disabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
            ),
          ),
          icon: Icon(
            Icons.keyboard_arrow_down,
            color: _selectedCategoryId == null ? const Color(0xFFCBD5E1) : AppColors.textSecondary,
          ),
          items: (_selectedCategoryId == null || _subcategories.isEmpty)
              ? null
              : _subcategories.map((s) {
                  return DropdownMenuItem<int>(
                    value: s.id,
                    child: Text(
                      s.nameBn,
                      style: AppTypography.mediumHeading2.copyWith(
                        fontWeight: FontWeight.w600,
                        fontSize: 13,
                        color: AppColors.textPrimary,
                      ),
                    ),
                  );
                }).toList(),
          onChanged: (_selectedCategoryId == null || _subcategories.isEmpty)
              ? null
              : (val) {
                  if (val == null) return;
                  setState(() {
                    _selectedSubcategoryId = val;
                    try {
                      final found = _subcategories.firstWhere((s) => s.id == val);
                      _selectedSubcategoryNameBn = found.nameBn;
                    } catch (_) {
                      _selectedSubcategoryNameBn = null;
                    }
                    _selectedServices.clear();
                    _selectedServices.add(val);
                  });
                },
        ),
        const SizedBox(height: 6),
        Text(
          _selectedCategoryId == null
              ? 'সাব-ক্যাটাগরি দেখতে আগে উপরে প্রধান ক্যাটাগরি নির্বাচন করুন।'
              : 'নির্বাচিত প্রধান ক্যাটাগরির অন্তর্ভুক্ত সুনির্দিষ্ট সেবা।',
          style: AppTypography.bodySmall.copyWith(color: AppColors.textSecondary, fontSize: 11),
        ),

        // ৩. নির্বাচিত সারাংশ কার্ড (Summary Card)
        if (_selectedCategoryId != null && _selectedSubcategoryId != null) ...[
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFFF0FDFA),
              borderRadius: BorderRadius.circular(12),
              border: Border.Border.all(color: const Color(0xFF99F6E4)),
            ),
            child: Row(
              children: [
                const Icon(Icons.check_circle_outline, color: Color(0xFF0D9488), size: 20),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'নির্বাচিত সেবা:',
                        style: AppTypography.bodySmall.copyWith(
                          color: const Color(0xFF115E59),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        '${_selectedCategoryNameBn ?? ''} ➔ ${_selectedSubcategoryNameBn ?? ''}',
                        style: AppTypography.mediumHeading2.copyWith(
                          fontSize: 13,
                          fontWeight: FontWeight.bold,
                          color: const Color(0xFF134E4A),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildStep4Areas() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'সেবা প্রদানের এলাকা (কভারেজ)',
          style: AppTypography.largeHeading2.copyWith(
            fontWeight: FontWeight.bold,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 6),
        Text(
          'কোন কোন উপজেলায় আপনি সেবা পৌঁছাতে প্রস্তুত?',
          style: AppTypography.bodyRegular.copyWith(
            color: AppColors.textSecondary,
          ),
        ),
        const SizedBox(height: 16),

        Wrap(
          spacing: 8,
          runSpacing: 10,
          children: _availableUpazilas.map((upz) {
            final isSelected = _selectedUpazilas.contains(upz['id']);
            return FilterChip(
              label: Text(
                upz['name_bn'],
                style: AppTypography.mediumHeading3.copyWith(
                  color: isSelected ? Colors.white : AppColors.textPrimary,
                  fontSize: 12,
                ),
              ),
              selected: isSelected,
              selectedColor: AppColors.primary,
              checkmarkColor: Colors.white,
              backgroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
                side: BorderSide(
                  color: isSelected ? AppColors.primary : AppColors.border,
                ),
              ),
              onSelected: (val) {
                setState(() {
                  if (val) {
                    _selectedUpazilas.add(upz['id'] as int);
                  } else {
                    _selectedUpazilas.remove(upz['id'] as int);
                  }
                });
              },
            );
          }).toList(),
        ),
      ],
    );
  }
}
