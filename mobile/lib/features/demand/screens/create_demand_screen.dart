/// Create Demand Screen / “আমার প্রয়োজন তৈরি করুন”
/// 9-Step Guided Production Wizard with Phase 3 Geographic Hierarchy & Phase 4 Service Taxonomy.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
/// "খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
library;

import 'package:flutter/material.dart';
import '../models/demand_enums.dart';

class CreateDemandScreen extends StatefulWidget {
  final Function(Map<String, dynamic> data, bool publishNow) onSubmit;
  final VoidCallback? onCancel;
  final Map<String, dynamic>? initialDraft;

  const CreateDemandScreen({
    super.key,
    required this.onSubmit,
    this.onCancel,
    this.initialDraft,
  });

  @override
  State<CreateDemandScreen> createState() => _CreateDemandScreenState();
}

class _CreateDemandScreenState extends State<CreateDemandScreen> {
  int _currentStep = 1;
  final int _totalSteps = 9;

  // Form Controllers
  final _titleController = TextEditingController();
  final _descController = TextEditingController();
  final _quantityController = TextEditingController();
  final _unitController = TextEditingController();
  final _budgetMinController = TextEditingController();
  final _budgetMaxController = TextEditingController();
  final _detailedAddressController = TextEditingController();

  // Step 2: Service / Category Selection (২টি Dropdown)
  int? _selectedCategoryId;
  String? _selectedCategoryNameBn;
  int? _selectedServiceId;
  String? _selectedServiceNameBn;

  // Step 4: Geographic Hierarchy Selection
  int _selectedDistrictId = 1;
  String _selectedDistrictNameBn = "কক্সবাজার";
  int _selectedUpazilaId = 1;
  String _selectedUpazilaNameBn = "কক্সবাজার সদর";
  int? _selectedUnionId;
  String? _selectedUnionNameBn;
  int? _selectedMunicipalityId;
  String? _selectedMunicipalityNameBn;
  int? _selectedWardId;
  String? _selectedWardNameBn;
  int? _selectedLocalityId;
  String? _selectedLocalityNameBn;

  // Step 5: Schedule / Timing
  String _scheduleType = 'ASAP'; // 'ASAP', 'DATE', 'DATE_TIME'
  DateTime? _selectedDate;
  TimeOfDay? _selectedTime;

  // Step 6: Unit selection
  final List<String> _suggestedUnits = [
    'টি', 'কেজি', 'টন', 'ব্যাগ', 'ঘণ্টা', 'দিন', 'ট্রিপ', 'স্কয়ার ফিট'
  ];

  // Step 7: Contact Preference
  DemandContactPreference _contactPreference = DemandContactPreference.inAppOnly;

  // Step 8: Visibility & Priority
  DemandVisibility _visibility = DemandVisibility.public;
  DemandPriority _priority = DemandPriority.normal;
  DemandType _demandType = DemandType.service;

  // State flags & validation errors
  String? _stepError;
  bool _isSubmitting = false;

  // Static Taxonomy Data for Cox's Bazar Master Taxonomy
  final List<Map<String, dynamic>> _categories = [
    {
      'id': 1,
      'name_bn': 'নির্মাণ ও প্রকৌশল',
      'name_en': 'Construction & Engineering',
      'icon': Icons.construction,
      'services': [
        {'id': 101, 'name_bn': 'ইট ও বালু সরবরাহ', 'name_en': 'Brick & Sand Supply'},
        {'id': 102, 'name_bn': 'রাজমিস্ত্রি', 'name_en': 'Masonry'},
        {'id': 103, 'name_bn': 'রড বাইন্ডিং ও ঢালাই', 'name_en': 'Rod Binding & Casting'},
        {'id': 104, 'name_bn': 'রং ও পুটি মিস্ত্রি', 'name_en': 'Painting & Putty'},
        {'id': 105, 'name_bn': 'টাইলস ও মার্বেল মিস্ত্রি', 'name_en': 'Tiles & Marble'},
      ]
    },
    {
      'id': 2,
      'name_bn': 'বাসাবাড়ি ও অফিস রক্ষণাবেক্ষণ',
      'name_en': 'Home & Office Maintenance',
      'icon': Icons.home_repair_service,
      'services': [
        {'id': 201, 'name_bn': 'ইলেকট্রিশিয়ান ও ওয়্যারিং', 'name_en': 'Electrician & Wiring'},
        {'id': 202, 'name_bn': 'প্লাম্বিং ও পাইপ ফিটিং', 'name_en': 'Plumbing & Pipe Fitting'},
        {'id': 203, 'name_bn': 'এসি ও ফ্রিজ সার্ভিসিং', 'name_en': 'AC & Fridge Servicing'},
        {'id': 204, 'name_bn': 'কাঠমিস্ত্রি ও ফার্নিচার মেরামত', 'name_en': 'Carpentry & Furniture'},
        {'id': 205, 'name_bn': 'বাসা-বাড়ি ও অফিস ক্লিনিং', 'name_en': 'Cleaning Services'},
      ]
    },
    {
      'id': 3,
      'name_bn': 'পরিবহন ও লজিস্টিকস',
      'name_en': 'Transport & Logistics',
      'icon': Icons.local_shipping,
      'services': [
        {'id': 301, 'name_bn': 'ট্রাক ও পিকআপ ভাড়া', 'name_en': 'Truck & Pickup Rental'},
        {'id': 302, 'name_bn': 'বাসা বদল ও মালামাল পরিবহন', 'name_en': 'Home Relocation'},
        {'id': 303, 'name_bn': 'অ্যাম্বুলেন্স সার্ভিস', 'name_en': 'Ambulance Service'},
        {'id': 304, 'name_bn': 'কুরিয়ার ও পার্সেল ডেলিভারি', 'name_en': 'Courier & Parcel Delivery'},
      ]
    },
    {
      'id': 4,
      'name_bn': 'পর্যটন ও আতিথেয়তা',
      'name_en': 'Tourism & Hospitality',
      'icon': Icons.hotel,
      'services': [
        {'id': 401, 'name_bn': 'হোটেল ও রিসোর্ট বুকিং', 'name_en': 'Hotel & Resort Booking'},
        {'id': 402, 'name_bn': 'ট্যুর গাইড ও ট্রাভেল প্ল্যানার', 'name_en': 'Tour Guide & Travel Planner'},
        {'id': 403, 'name_bn': 'কার ও জিপ রেন্টাল', 'name_en': 'Car & Jeep Rental'},
        {'id': 404, 'name_bn': 'বোট ও বিচ অ্যাক্টিভিটি', 'name_en': 'Boat & Beach Activities'},
      ]
    },
    {
      'id': 5,
      'name_bn': 'কৃষি ও মৎস্য সম্পদ',
      'name_en': 'Agriculture & Fisheries',
      'icon': Icons.agriculture,
      'services': [
        {'id': 501, 'name_bn': 'শুটকি ও সামুদ্রিক মাছ পাইকারি', 'name_en': 'Dry Fish Wholesale'},
        {'id': 502, 'name_bn': 'লবণ উৎপাদন সামগ্রী', 'name_en': 'Salt Production Supplies'},
        {'id': 503, 'name_bn': 'পান ও সুপারি সরবরাহ', 'name_en': 'Betel Leaf Supply'},
        {'id': 504, 'name_bn': 'কৃষি যন্ত্রপাতি ও সামগ্রী', 'name_en': 'Agri Machinery & Supplies'},
      ]
    },
    {
      'id': 6,
      'name_bn': 'স্বাস্থ্য ও চিকিৎসা',
      'name_en': 'Healthcare & Medical',
      'icon': Icons.medical_services,
      'services': [
        {'id': 601, 'name_bn': 'ডাক্তার', 'name_en': 'Doctor Consultation'},
        {'id': 602, 'name_bn': 'হোম নার্সিং ও কেয়ারগিভার', 'name_en': 'Home Nursing & Caregiver'},
        {'id': 603, 'name_bn': 'ফিজিওথেরাপি সেবা', 'name_en': 'Physiotherapy'},
        {'id': 604, 'name_bn': 'ডায়াগনস্টিক ও ল্যাব টেস্ট', 'name_en': 'Diagnostic & Lab Test'},
      ]
    },
    {
      'id': 7,
      'name_bn': 'খাবার ও রেস্তোরাঁ',
      'name_en': 'Food & Catering',
      'icon': Icons.restaurant,
      'services': [
        {'id': 701, 'name_bn': 'ক্যাটারিং ও বাবুর্চি', 'name_en': 'Catering & Chef'},
        {'id': 702, 'name_bn': 'হোমমেড ফুড ডেলিভারি', 'name_en': 'Homemade Food Delivery'},
        {'id': 703, 'name_bn': 'ইভেন্ট ফুড সাপ্লাই', 'name_en': 'Event Food Supply'},
      ]
    },
    {
      'id': 8,
      'name_bn': 'শিক্ষা ও প্রশিক্ষণ',
      'name_en': 'Education & Training',
      'icon': Icons.school,
      'services': [
        {'id': 801, 'name_bn': 'হোম টিউটর', 'name_en': 'Home Tutor'},
        {'id': 802, 'name_bn': 'ভাষা ও স্কিল কোর্স', 'name_en': 'Language & Skill Training'},
        {'id': 803, 'name_bn': 'কম্পিউটার ও আইটি প্রশিক্ষণ', 'name_en': 'Computer & IT Training'},
      ]
    },
    {
      'id': 9,
      'name_bn': 'যানবাহন সেবা',
      'name_en': 'Vehicle Services',
      'icon': Icons.directions_car,
      'services': [
        {'id': 901, 'name_bn': 'অটোমোবাইল ও বাইক মেরামত', 'name_en': 'Automobile & Bike Repair'},
        {'id': 902, 'name_bn': 'গাড়ি ওয়াশ ও পলিশিং', 'name_en': 'Car Wash & Detailing'},
        {'id': 903, 'name_bn': 'টায়ার ও ব্যাটারি সার্ভিস', 'name_en': 'Tire & Battery Service'},
      ]
    },
    {
      'id': 10,
      'name_bn': 'অনুষ্ঠান ও বিয়ের সেবা',
      'name_en': 'Events & Wedding Services',
      'icon': Icons.celebration,
      'services': [
        {'id': 1001, 'name_bn': 'ডেকোরেশন ও সাউন্ড সিস্টেম', 'name_en': 'Decoration & Sound'},
        {'id': 1002, 'name_bn': 'ফটোগ্রাফি ও ভিডিওগ্রাফি', 'name_en': 'Photography & Videography'},
        {'id': 1003, 'name_bn': 'কমিউনিটি সেন্টার বুকিং', 'name_en': 'Community Center Booking'},
      ]
    },
  ];

  // Upazila & Hierarchy Static Data for Cox's Bazar
  final List<Map<String, dynamic>> _upazilas = [
    {'id': 1, 'name_bn': 'কক্সবাজার সদর', 'name_en': "Cox's Bazar Sadar"},
    {'id': 2, 'name_bn': 'চকরিয়া', 'name_en': 'Chakaria'},
    {'id': 3, 'name_bn': 'মহেশখালী', 'name_en': 'Maheshkhali'},
    {'id': 4, 'name_bn': 'রামু', 'name_en': 'Ramu'},
    {'id': 5, 'name_bn': 'টেকনাফ', 'name_en': 'Teknaf'},
    {'id': 6, 'name_bn': 'উখিয়া', 'name_en': 'Ukhia'},
    {'id': 7, 'name_bn': 'পেকুয়া', 'name_en': 'Pekua'},
    {'id': 8, 'name_bn': 'কুতুবদিয়া', 'name_en': 'Kutubdia'},
    {'id': 9, 'name_bn': 'ঈদগাঁও', 'name_en': 'Eidgaon'},
  ];

  final Map<int, List<Map<String, dynamic>>> _unions = {
    1: [
      {'id': 101, 'name_bn': 'কক্সবাজার পৌরসভা', 'type': 'MUNICIPALITY'},
      {'id': 102, 'name_bn': 'ঝিলংজা ইউনিয়ন', 'type': 'UNION'},
      {'id': 103, 'name_bn': 'পিএমখালী ইউনিয়ন', 'type': 'UNION'},
      {'id': 104, 'name_bn': 'খুরুশকুল ইউনিয়ন', 'type': 'UNION'},
      {'id': 105, 'name_bn': 'ভারুয়াখালী ইউনিয়ন', 'type': 'UNION'},
      {'id': 106, 'name_bn': 'চৌফলদণ্ডী ইউনিয়ন', 'type': 'UNION'},
    ],
    2: [
      {'id': 201, 'name_bn': 'চকরিয়া পৌরসভা', 'type': 'MUNICIPALITY'},
      {'id': 202, 'name_bn': 'কাকারা ইউনিয়ন', 'type': 'UNION'},
      {'id': 203, 'name_bn': 'ডুলাহাজারা ইউনিয়ন', 'type': 'UNION'},
      {'id': 204, 'name_bn': 'হারবাং ইউনিয়ন', 'type': 'UNION'},
    ],
    4: [
      {'id': 401, 'name_bn': 'ফতেখাঁরকূল ইউনিয়ন', 'type': 'UNION'},
      {'id': 402, 'name_bn': 'জোয়ারিয়ানালা ইউনিয়ন', 'type': 'UNION'},
      {'id': 403, 'name_bn': 'রশিদনগর ইউনিয়ন', 'type': 'UNION'},
    ],
  };

  final Map<int, List<Map<String, dynamic>>> _wards = {
    101: [
      {'id': 1001, 'name_bn': '১ নং ওয়ার্ড (সমিতি পাড়া)'},
      {'id': 1002, 'name_bn': '২ নং ওয়ার্ড (উত্তর রুমালিয়ারছড়া)'},
      {'id': 1003, 'name_bn': '৫ নং ওয়ার্ড (আলীর জাঁহাল)'},
      {'id': 1004, 'name_bn': '১০ নং ওয়ার্ড (দক্ষিণ বাহারছড়া)'},
      {'id': 1005, 'name_bn': '১২ নং ওয়ার্ড (কলাতলী রোড)'},
    ],
    102: [
      {'id': 1021, 'name_bn': '১ নং ওয়ার্ড (লারপাড়া)'},
      {'id': 1022, 'name_bn': '২ নং ওয়ার্ড (চৌকিয়া পাড়া)'},
    ],
  };

  final Map<int, List<Map<String, dynamic>>> _localities = {
    1004: [
      {'id': 10041, 'name_bn': 'টেকপাড়া', 'type': 'মহল্লা'},
      {'id': 10042, 'name_bn': 'গোলদিঘির পাড়', 'type': 'আবাসিক এলাকা'},
    ],
    1005: [
      {'id': 10051, 'name_bn': 'কলাতলী বিচ এলাকা', 'type': 'পর্যটন এলাকা'},
      {'id': 10052, 'name_bn': 'হোটেল মোটেল জোন', 'type': 'বাণিজ্যিক এলাকা'},
      {'id': 10053, 'name_bn': 'সুগন্ধা পয়েন্ট', 'type': 'বাজার/পয়েন্ট'},
    ],
  };

  @override
  void initState() {
    super.initState();
    if (widget.initialDraft != null) {
      _loadDraft(widget.initialDraft!);
    }
  }

  void _loadDraft(Map<String, dynamic> draft) {
    _titleController.text = draft['title_bn'] ?? '';
    _descController.text = draft['description_bn'] ?? '';
    _quantityController.text = draft['quantity']?.toString() ?? '';
    _unitController.text = draft['unit'] ?? '';
    _budgetMinController.text = draft['budget_min']?.toString() ?? '';
    _budgetMaxController.text = draft['budget_max']?.toString() ?? '';
    _detailedAddressController.text = draft['location_display_bn'] ?? '';
    _selectedUpazilaId = draft['upazila_id'] ?? 1;
    _selectedCategoryId = draft['category_id'];
    _selectedServiceId = draft['service_id'];
    if (draft['contact_preference'] != null) {
      _contactPreference = DemandContactPreference.fromString(draft['contact_preference']);
    }
    if (draft['visibility'] != null) {
      _visibility = DemandVisibility.fromString(draft['visibility']);
    }
    if (draft['priority'] != null) {
      _priority = DemandPriority.fromString(draft['priority']);
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _descController.dispose();
    _quantityController.dispose();
    _unitController.dispose();
    _budgetMinController.dispose();
    _budgetMaxController.dispose();
    _detailedAddressController.dispose();
    super.dispose();
  }

  // Step Validation Logic
  bool _validateCurrentStep() {
    setState(() => _stepError = null);

    switch (_currentStep) {
      case 1: // Title
        final title = _titleController.text.trim();
        if (title.isEmpty) {
          setState(() => _stepError = 'প্রয়োজনের শিরোনাম লিখুন।');
          return false;
        }
        if (title.length < 5) {
          setState(() => _stepError = 'শিরোনাম কমপক্ষে ৫ অক্ষরের হতে হবে।');
          return false;
        }
        return true;

      case 2: // Service (২টি Dropdown)
        if (_selectedCategoryId == null) {
          setState(() => _stepError = 'অনুগ্রহ করে প্রধান ক্যাটাগরি নির্বাচন করুন।');
          return false;
        }
        if (_selectedServiceId == null) {
          setState(() => _stepError = 'অনুগ্রহ করে সাব-ক্যাটাগরি নির্বাচন করুন।');
          return false;
        }
        return true;

      case 3: // Description
        final desc = _descController.text.trim();
        if (desc.isEmpty) {
          setState(() => _stepError = 'আপনার প্রয়োজনের বিস্তারিত বিবরণ লিখুন।');
          return false;
        }
        if (desc.length < 10) {
          setState(() => _stepError = 'বিবরণ কমপক্ষে ১০ অক্ষরের হতে হবে।');
          return false;
        }
        return true;

      case 4: // Location
        if (_selectedUpazilaId <= 0) {
          setState(() => _stepError = 'অনুগ্রহ করে প্রয়োজনের উপজেলা নির্বাচন করুন।');
          return false;
        }
        return true;

      case 5: // Schedule
        if (_scheduleType == 'DATE' && _selectedDate == null) {
          setState(() => _stepError = 'অনুগ্রহ করে নির্দিষ্ট তারিখ নির্বাচন করুন।');
          return false;
        }
        if (_scheduleType == 'DATE_TIME' && (_selectedDate == null || _selectedTime == null)) {
          setState(() => _stepError = 'অনুগ্রহ করে তারিখ ও সময় নির্বাচন করুন।');
          return false;
        }
        return true;

      case 6: // Budget & Quantity
        final minStr = _budgetMinController.text.trim();
        final maxStr = _budgetMaxController.text.trim();
        if (minStr.isNotEmpty && maxStr.isNotEmpty) {
          final min = double.tryParse(minStr);
          final max = double.tryParse(maxStr);
          if (min != null && max != null) {
            if (min < 0 || max < 0) {
              setState(() => _stepError = 'বাজেটের মান ঋণাত্মক হতে পারে না।');
              return false;
            }
            if (min > max) {
              setState(() => _stepError = 'সর্বনিম্ন বাজেট সর্বোচ্চ বাজেটের চেয়ে বেশি হতে পারবে না।');
              return false;
            }
          }
        }
        return true;

      case 7: // Contact
        return true;

      case 8: // Visibility
        return true;

      case 9: // Review
        return true;

      default:
        return true;
    }
  }

  void _nextStep() {
    if (_validateCurrentStep()) {
      if (_currentStep < _totalSteps) {
        setState(() => _currentStep++);
      }
    }
  }

  void _prevStep() {
    setState(() => _stepError = null);
    if (_currentStep > 1) {
      setState(() => _currentStep--);
    } else if (widget.onCancel != null) {
      widget.onCancel!();
    }
  }

  void _goToStep(int step) {
    setState(() {
      _stepError = null;
      _currentStep = step;
    });
  }

  Map<String, dynamic> _buildPayload() {
    String fullLocationDisplay = _detailedAddressController.text.trim();
    if (fullLocationDisplay.isEmpty) {
      List<String> locParts = [];
      if (_selectedLocalityNameBn != null) locParts.add(_selectedLocalityNameBn!);
      if (_selectedWardNameBn != null) locParts.add(_selectedWardNameBn!);
      if (_selectedUnionNameBn != null) locParts.add(_selectedUnionNameBn!);
      locParts.add(_selectedUpazilaNameBn);
      locParts.add(_selectedDistrictNameBn);
      fullLocationDisplay = locParts.join(', ');
    }

    DateTime? reqAt;
    if (_scheduleType == 'DATE' && _selectedDate != null) {
      reqAt = _selectedDate;
    } else if (_scheduleType == 'DATE_TIME' && _selectedDate != null && _selectedTime != null) {
      reqAt = DateTime(
        _selectedDate!.year,
        _selectedDate!.month,
        _selectedDate!.day,
        _selectedTime!.hour,
        _selectedTime!.minute,
      );
    }

    final payload = <String, dynamic>{
      'title_bn': _titleController.text.trim(),
      'description_bn': _descController.text.trim(),
      'category_id': _selectedCategoryId,
      'category_name_bn': _selectedCategoryNameBn,
      'service_id': _selectedServiceId,
      'service_name_bn': _selectedServiceNameBn,
      'district_id': _selectedDistrictId,
      'district_name_bn': _selectedDistrictNameBn,
      'upazila_id': _selectedUpazilaId,
      'upazila_name_bn': _selectedUpazilaNameBn,
      'union_id': _selectedUnionId,
      'municipality_id': _selectedMunicipalityId,
      'ward_id': _selectedWardId,
      'locality_id': _selectedLocalityId,
      'location_display_bn': fullLocationDisplay,
      'demand_type': _demandType.value,
      'priority': _priority.value,
      'visibility': _visibility.value,
      'contact_preference': _contactPreference.value,
      'required_at': reqAt?.toIso8601String(),
    };

    if (_quantityController.text.trim().isNotEmpty) {
      payload['quantity'] = double.tryParse(_quantityController.text.trim());
    }
    if (_unitController.text.trim().isNotEmpty) {
      payload['unit'] = _unitController.text.trim();
    }
    if (_budgetMinController.text.trim().isNotEmpty) {
      payload['budget_min'] = double.tryParse(_budgetMinController.text.trim());
    }
    if (_budgetMaxController.text.trim().isNotEmpty) {
      payload['budget_max'] = double.tryParse(_budgetMaxController.text.trim());
    }

    return payload;
  }

  void _handleSaveDraft() {
    final payload = _buildPayload();
    setState(() => _isSubmitting = true);
    widget.onSubmit(payload, false);
  }

  void _handleConfirmPublish() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text(
          'প্রয়োজন প্রকাশ নিশ্চিতকরণ',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 16),
        ),
        content: const Text(
          'আপনি কি এই প্রয়োজনটি সর্বসাধারণ বা নিবন্ধিত সেবাদাতাদের জন্য প্রকাশ করতে চান?',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF334155)),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text(
              'পিছনে',
              style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, color: Color(0xFF64748B)),
            ),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(ctx).pop();
              final payload = _buildPayload();
              setState(() => _isSubmitting = true);
              widget.onSubmit(payload, true);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0D9488),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            ),
            child: const Text(
              'প্রকাশ করুন',
              style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, color: Colors.white),
            ),
          ),
        ],
      ),
    );
  }

  // WIDGET BUILDERS PER STEP

  Widget _buildStep1() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'আপনার কী প্রয়োজন?',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        const SizedBox(height: 6),
        const Text(
          'আপনার চাহিদার একটি সংক্ষিপ্ত ও সুনির্দিষ্ট শিরোনাম লিখুন।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 20),
        const Text(
          'প্রয়োজনের শিরোনাম *',
          style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF334155)),
        ),
        const SizedBox(height: 8),
        TextFormField(
          controller: _titleController,
          autofocus: true,
          decoration: InputDecoration(
            hintText: 'e.g. ১০০০টি ইট প্রয়োজন বা অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন',
            hintStyle: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)),
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
            focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFF0D9488), width: 1.5)),
          ),
        ),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: const Color(0xFFF0FDFA),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: const Color(0xFFCCFBF1)),
          ),
          child: const Row(
            children: [
              Icon(Icons.lightbulb_outline, size: 18, color: Color(0xFF0D9488)),
              SizedBox(width: 8),
              Expanded(
                child: Text(
                  'সহজ উদাহরণ: “চকোরিয়ায় বাসা বদলের জন্য পিকআপ প্রয়োজন” বা “কক্সবাজার সদরে এসি মেরামতের জন্য কারিগর প্রয়োজন”',
                  style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF115E59)),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildStep2() {
    // Find services for selected category
    List<Map<String, dynamic>> availableServices = [];
    if (_selectedCategoryId != null) {
      final selectedCat = _categories.firstWhere(
        (cat) => cat['id'] == _selectedCategoryId,
        orElse: () => {},
      );
      if (selectedCat.containsKey('services')) {
        availableServices = List<Map<String, dynamic>>.from(selectedCat['services'] as List);
      }
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'কোন সেবাটি প্রয়োজন?',
          style: TextStyle(
            fontFamily: 'HindSiliguri',
            fontWeight: FontWeight.bold,
            fontSize: 18,
            color: Color(0xFF0F172A),
          ),
        ),
        const SizedBox(height: 6),
        const Text(
          'মাস্টার ট্যাক্সোনমি থেকে প্রধান ক্যাটাগরি ও সাব-ক্যাটাগরি নির্বাচন করুন।',
          style: TextStyle(
            fontFamily: 'TiroBangla',
            fontSize: 13,
            color: Color(0xFF64748B),
          ),
        ),
        const SizedBox(height: 20),

        // ১ম Dropdown — প্রধান ক্যাটাগরি
        const Text(
          'প্রধান ক্যাটাগরি *',
          style: TextStyle(
            fontFamily: 'TiroBangla',
            fontWeight: FontWeight.bold,
            fontSize: 13,
            color: Color(0xFF334155),
          ),
        ),
        const SizedBox(height: 8),
        DropdownButtonFormField<int>(
          value: _selectedCategoryId,
          hint: const Text(
            '-- প্রধান ক্যাটাগরি নির্বাচন করুন --',
            style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)),
          ),
          decoration: InputDecoration(
            filled: true,
            fillColor: Colors.white,
            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFF0D9488), width: 1.5),
            ),
          ),
          icon: const Icon(Icons.keyboard_arrow_down, color: Color(0xFF64748B)),
          items: _categories.map((cat) {
            return DropdownMenuItem<int>(
              value: cat['id'] as int,
              child: Text(
                cat['name_bn'] as String,
                style: const TextStyle(
                  fontFamily: 'BalooDa2',
                  fontWeight: FontWeight.w600,
                  fontSize: 13,
                  color: Color(0xFF0F172A),
                ),
              ),
            );
          }).toList(),
          onChanged: (val) {
            setState(() {
              _selectedCategoryId = val;
              final found = _categories.firstWhere(
                (cat) => cat['id'] == val,
                orElse: () => {},
              );
              _selectedCategoryNameBn = found['name_bn'] as String?;
              // Reset sub-category on main category change
              _selectedServiceId = null;
              _selectedServiceNameBn = null;
            });
          },
        ),
        const SizedBox(height: 6),
        const Text(
          'প্রথমে আপনার প্রয়োজনীয় প্রধান ক্যাটাগরি বাছাই করুন।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF94A3B8)),
        ),
        const SizedBox(height: 18),

        // ২য় Dropdown — সাব-ক্যাটাগরি
        const Text(
          'সাব-ক্যাটাগরি *',
          style: TextStyle(
            fontFamily: 'TiroBangla',
            fontWeight: FontWeight.bold,
            fontSize: 13,
            color: Color(0xFF334155),
          ),
        ),
        const SizedBox(height: 8),
        DropdownButtonFormField<int>(
          value: _selectedServiceId,
          hint: Text(
            _selectedCategoryId == null
                ? '-- প্রথমে প্রধান ক্যাটাগরি নির্বাচন করুন --'
                : '-- সাব-ক্যাটাগরি নির্বাচন করুন --',
            style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)),
          ),
          decoration: InputDecoration(
            filled: true,
            fillColor: _selectedCategoryId == null ? const Color(0xFFF1F5F9) : Colors.white,
            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: BorderSide(
                color: _selectedCategoryId == null ? const Color(0xFFE2E8F0) : const Color(0xFFCBD5E1),
              ),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFF0D9488), width: 1.5),
            ),
            disabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFFE2E8F0)),
            ),
          ),
          icon: Icon(
            Icons.keyboard_arrow_down,
            color: _selectedCategoryId == null ? const Color(0xFFCBD5E1) : const Color(0xFF64748B),
          ),
          items: _selectedCategoryId == null
              ? null
              : availableServices.map((s) {
                  return DropdownMenuItem<int>(
                    value: s['id'] as int,
                    child: Text(
                      s['name_bn'] as String,
                      style: const TextStyle(
                        fontFamily: 'BalooDa2',
                        fontWeight: FontWeight.w600,
                        fontSize: 13,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                  );
                }).toList(),
          onChanged: _selectedCategoryId == null
              ? null
              : (val) {
                  setState(() {
                    _selectedServiceId = val;
                    final found = availableServices.firstWhere(
                      (s) => s['id'] == val,
                      orElse: () => {},
                    );
                    _selectedServiceNameBn = found['name_bn'] as String?;
                  });
                },
        ),
        const SizedBox(height: 6),
        Text(
          _selectedCategoryId == null
              ? 'সাব-ক্যাটাগরি দেখতে আগে প্রধান ক্যাটাগরি নির্বাচন করুন।'
              : 'নির্বাচিত প্রধান ক্যাটাগরির অন্তর্ভুক্ত সুনির্দিষ্ট সেবা।',
          style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF94A3B8)),
        ),
      ],
    );
  }

  Widget _buildStep3() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'আপনার প্রয়োজনটি বিস্তারিত বলুন',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        const SizedBox(height: 6),
        const Text(
          'সুনির্দিষ্ট গুণগত মান, শর্তাবলী বা কাজের পরিধি বিস্তারিতভাবে লিখুন।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 20),
        const Text(
          'বিস্তারিত বিবরণ *',
          style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF334155)),
        ),
        const SizedBox(height: 8),
        TextFormField(
          controller: _descController,
          maxLines: 5,
          onChanged: (_) => setState(() {}),
          decoration: InputDecoration(
            hintText: 'e.g. নির্মাণ কাজের জন্য ১ নম্বর ইট প্রয়োজন। ভালো মানের ইট হতে হবে এবং নির্দিষ্ট এলাকায় পৌঁছে দিতে হবে...',
            hintStyle: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)),
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
            focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFF0D9488), width: 1.5)),
          ),
        ),
        const SizedBox(height: 6),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'কমপক্ষে ১০ অক্ষর আবশ্যক',
              style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF94A3B8)),
            ),
            Text(
              '${_descController.text.length} অক্ষর',
              style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B), fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildStep4() {
    final availableUnions = _unions[_selectedUpazilaId] ?? [];
    final availableWards = _selectedUnionId != null ? (_wards[_selectedUnionId] ?? []) : [];
    final availableLocalities = _selectedWardId != null ? (_localities[_selectedWardId] ?? []) : [];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'কোথায় প্রয়োজন?',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        const SizedBox(height: 6),
        const Text(
          'কক্সবাজার জেলার প্রশাসনিক স্তর নির্বাচন করুন।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 12),

        // GPS ≠ Demand Notice
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: const Color(0xFFEFF6FF),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: const Color(0xFFBFDBFE)),
          ),
          child: const Row(
            children: [
              Icon(Icons.info_outline, size: 16, color: Color(0xFF1D4ED8)),
              SizedBox(width: 8),
              Expanded(
                child: Text(
                  'Current GPS Location ≠ Demand Location। আপনি যেকোনো এলাকার জন্য প্রয়োজন তৈরি করতে পারেন।',
                  style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF1E40AF)),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),

        // 1. District
        const Text('জেলা', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
        const SizedBox(height: 4),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          decoration: BoxDecoration(
            color: const Color(0xFFF1F5F9),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: const Color(0xFFCBD5E1)),
          ),
          child: const Text('কক্সবাজার (Cox\'s Bazar)', style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF334155))),
        ),
        const SizedBox(height: 12),

        // 2. Upazila
        const Text('উপজেলা *', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
        const SizedBox(height: 4),
        DropdownButtonFormField<int>(
          value: _selectedUpazilaId,
          decoration: InputDecoration(
            filled: true,
            fillColor: Colors.white,
            contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
          ),
          items: _upazilas.map((u) {
            return DropdownMenuItem<int>(
              value: u['id'] as int,
              child: Text(u['name_bn'] as String, style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13)),
            );
          }).toList(),
          onChanged: (val) {
            if (val != null) {
              setState(() {
                _selectedUpazilaId = val;
                _selectedUpazilaNameBn = _upazilas.firstWhere((u) => u['id'] == val)['name_bn'];
                // Reset child cascading selections
                _selectedUnionId = null;
                _selectedUnionNameBn = null;
                _selectedMunicipalityId = null;
                _selectedMunicipalityNameBn = null;
                _selectedWardId = null;
                _selectedWardNameBn = null;
                _selectedLocalityId = null;
                _selectedLocalityNameBn = null;
              });
            }
          },
        ),
        const SizedBox(height: 12),

        // 3. Union / Municipality
        const Text('ইউনিয়ন / পৌরসভা (ঐচ্ছিক)', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
        const SizedBox(height: 4),
        DropdownButtonFormField<int?>(
          value: _selectedUnionId,
          decoration: InputDecoration(
            hintText: 'ইউনিয়ন বা পৌরসভা নির্বাচন করুন...',
            filled: true,
            fillColor: Colors.white,
            contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
          ),
          items: [
            const DropdownMenuItem<int?>(value: null, child: Text('নির্বাচন করুন', style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)))),
            ...availableUnions.map((un) {
              return DropdownMenuItem<int?>(
                value: un['id'] as int,
                child: Text(un['name_bn'] as String, style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13)),
              );
            }),
          ],
          onChanged: (val) {
            setState(() {
              _selectedUnionId = val;
              if (val != null) {
                final un = availableUnions.firstWhere((u) => u['id'] == val);
                _selectedUnionNameBn = un['name_bn'];
              } else {
                _selectedUnionNameBn = null;
              }
              // Reset child selections
              _selectedWardId = null;
              _selectedWardNameBn = null;
              _selectedLocalityId = null;
              _selectedLocalityNameBn = null;
            });
          },
        ),
        const SizedBox(height: 12),

        // 4. Ward
        if (availableWards.isNotEmpty) ...[
          const Text('ওয়ার্ড (ঐচ্ছিক)', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
          const SizedBox(height: 4),
          DropdownButtonFormField<int?>(
            value: _selectedWardId,
            decoration: InputDecoration(
              hintText: 'ওয়ার্ড নির্বাচন করুন...',
              filled: true,
              fillColor: Colors.white,
              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
            ),
            items: [
              const DropdownMenuItem<int?>(value: null, child: Text('নির্বাচন করুন', style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)))),
              ...availableWards.map((w) {
                return DropdownMenuItem<int?>(
                  value: w['id'] as int,
                  child: Text(w['name_bn'] as String, style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13)),
                );
              }),
            ],
            onChanged: (val) {
              setState(() {
                _selectedWardId = val;
                if (val != null) {
                  _selectedWardNameBn = availableWards.firstWhere((w) => w['id'] == val)['name_bn'];
                } else {
                  _selectedWardNameBn = null;
                }
                // Reset locality
                _selectedLocalityId = null;
                _selectedLocalityNameBn = null;
              });
            },
          ),
          const SizedBox(height: 12),
        ],

        // 5. Locality (পাড়া / মহল্লা / গ্রাম / বাজার)
        if (availableLocalities.isNotEmpty) ...[
          const Text('পাড়া / মহল্লা / গ্রাম / লোকালিটি (ঐচ্ছিক)', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
          const SizedBox(height: 4),
          DropdownButtonFormField<int?>(
            value: _selectedLocalityId,
            decoration: InputDecoration(
              hintText: 'লোকালিটি নির্বাচন করুন...',
              filled: true,
              fillColor: Colors.white,
              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
            ),
            items: [
              const DropdownMenuItem<int?>(value: null, child: Text('নির্বাচন করুন', style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)))),
              ...availableLocalities.map((loc) {
                return DropdownMenuItem<int?>(
                  value: loc['id'] as int,
                  child: Text('${loc['name_bn']} (${loc['type']})', style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13)),
                );
              }),
            ],
            onChanged: (val) {
              setState(() {
                _selectedLocalityId = val;
                if (val != null) {
                  _selectedLocalityNameBn = availableLocalities.firstWhere((l) => l['id'] == val)['name_bn'];
                } else {
                  _selectedLocalityNameBn = null;
                }
              });
            },
          ),
          const SizedBox(height: 12),
        ],

        // 6. Detailed Address
        const Text('নির্দিষ্ট ঠিকানা / ল্যান্ডমার্ক (ঐচ্ছিক)', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
        const SizedBox(height: 4),
        TextFormField(
          controller: _detailedAddressController,
          decoration: InputDecoration(
            hintText: 'e.g. কলাতলী রোড, হোটেল সী-গালের বিপরীতে',
            hintStyle: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF94A3B8)),
            filled: true,
            fillColor: Colors.white,
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFCBD5E1))),
          ),
        ),
      ],
    );
  }

  Widget _buildStep5() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'কখন প্রয়োজন?',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        const SizedBox(height: 6),
        const Text(
          'কখন সেবা বা পণ্য প্রয়োজন তা নির্বাচন করুন (Asia/Dhaka সময়)।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 16),

        // Option 1: ASAP
        InkWell(
          onTap: () => setState(() => _scheduleType = 'ASAP'),
          child: Container(
            padding: const EdgeInsets.all(14),
            margin: const EdgeInsets.only(bottom: 10),
            decoration: BoxDecoration(
              color: _scheduleType == 'ASAP' ? const Color(0xFFF0FDFA) : Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: _scheduleType == 'ASAP' ? const Color(0xFF0D9488) : const Color(0xFFCBD5E1)),
            ),
            child: Row(
              children: [
                Icon(
                  _scheduleType == 'ASAP' ? Icons.radio_button_checked : Icons.radio_button_unchecked,
                  color: _scheduleType == 'ASAP' ? const Color(0xFF0D9488) : const Color(0xFF94A3B8),
                ),
                const SizedBox(width: 12),
                const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('যত দ্রুত সম্ভব (ASAP)', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14)),
                    Text('আজকের মধ্যেই দ্রুত সমাধান দরকার', style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B))),
                  ],
                ),
              ],
            ),
          ),
        ),

        // Option 2: Specific Date
        InkWell(
          onTap: () => setState(() => _scheduleType = 'DATE'),
          child: Container(
            padding: const EdgeInsets.all(14),
            margin: const EdgeInsets.only(bottom: 10),
            decoration: BoxDecoration(
              color: _scheduleType == 'DATE' ? const Color(0xFFF0FDFA) : Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: _scheduleType == 'DATE' ? const Color(0xFF0D9488) : const Color(0xFFCBD5E1)),
            ),
            child: Row(
              children: [
                Icon(
                  _scheduleType == 'DATE' ? Icons.radio_button_checked : Icons.radio_button_unchecked,
                  color: _scheduleType == 'DATE' ? const Color(0xFF0D9488) : const Color(0xFF94A3B8),
                ),
                const SizedBox(width: 12),
                const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('নির্দিষ্ট তারিখ', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14)),
                    Text('ভবিষ্যতের কোনো নির্দিষ্ট দিনে প্রয়োজন', style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B))),
                  ],
                ),
              ],
            ),
          ),
        ),

        // Option 3: Date & Time
        InkWell(
          onTap: () => setState(() => _scheduleType = 'DATE_TIME'),
          child: Container(
            padding: const EdgeInsets.all(14),
            margin: const EdgeInsets.only(bottom: 16),
            decoration: BoxDecoration(
              color: _scheduleType == 'DATE_TIME' ? const Color(0xFFF0FDFA) : Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: _scheduleType == 'DATE_TIME' ? const Color(0xFF0D9488) : const Color(0xFFCBD5E1)),
            ),
            child: Row(
              children: [
                Icon(
                  _scheduleType == 'DATE_TIME' ? Icons.radio_button_checked : Icons.radio_button_unchecked,
                  color: _scheduleType == 'DATE_TIME' ? const Color(0xFF0D9488) : const Color(0xFF94A3B8),
                ),
                const SizedBox(width: 12),
                const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('নির্দিষ্ট তারিখ ও সময়', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14)),
                    Text('নির্দিষ্ট দিন ও নির্দিষ্ট ঘণ্টার শিডিউল', style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B))),
                  ],
                ),
              ],
            ),
          ),
        ),

        // Pickers for Date / Time
        if (_scheduleType == 'DATE' || _scheduleType == 'DATE_TIME') ...[
          const Text('তারিখ নির্বাচন করুন', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
          const SizedBox(height: 6),
          OutlinedButton.icon(
            onPressed: () async {
              final now = DateTime.now();
              final picked = await showDatePicker(
                context: context,
                initialDate: _selectedDate ?? now,
                firstDate: now,
                lastDate: now.add(const Duration(days: 90)),
              );
              if (picked != null) {
                setState(() => _selectedDate = picked);
              }
            },
            icon: const Icon(Icons.calendar_today, size: 16, color: Color(0xFF0D9488)),
            label: Text(
              _selectedDate != null
                  ? '${_selectedDate!.day}/${_selectedDate!.month}/${_selectedDate!.year}'
                  : 'তারিখ বাছাই করুন',
              style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF0F172A)),
            ),
          ),
          const SizedBox(height: 12),
        ],

        if (_scheduleType == 'DATE_TIME') ...[
          const Text('সময় নির্বাচন করুন', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
          const SizedBox(height: 6),
          OutlinedButton.icon(
            onPressed: () async {
              final picked = await showTimePicker(
                context: context,
                initialTime: _selectedTime ?? TimeOfDay.now(),
              );
              if (picked != null) {
                setState(() => _selectedTime = picked);
              }
            },
            icon: const Icon(Icons.access_time, size: 16, color: Color(0xFF0D9488)),
            label: Text(
              _selectedTime != null
                  ? _selectedTime!.format(context)
                  : 'সময় বাছাই করুন',
              style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF0F172A)),
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildStep6() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'কত পরিমাণ প্রয়োজন ও বাজেট',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        const SizedBox(height: 6),
        const Text(
          'পরিমাণ, পরিমাপের একক এবং আনুমানিক বাজেট পরিসীমা লিখুন (৳ BDT)।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 16),

        // Quantity & Unit
        Row(
          children: [
            Expanded(
              flex: 2,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('পরিমাণ (ঐচ্ছিক)', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
                  const SizedBox(height: 4),
                  TextFormField(
                    controller: _quantityController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      hintText: 'e.g. ১০০০',
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              flex: 2,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('একক (Unit)', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF475569))),
                  const SizedBox(height: 4),
                  TextFormField(
                    controller: _unitController,
                    decoration: InputDecoration(
                      hintText: 'e.g. টি / ব্যাগ',
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        const SizedBox(height: 10),

        // Unit Choice Chips
        Wrap(
          spacing: 6,
          runSpacing: 4,
          children: _suggestedUnits.map((u) {
            final isSelected = _unitController.text == u;
            return ActionChip(
              label: Text(u, style: TextStyle(fontFamily: 'BalooDa2', fontSize: 11, color: isSelected ? Colors.white : const Color(0xFF334155))),
              backgroundColor: isSelected ? const Color(0xFF0D9488) : const Color(0xFFF1F5F9),
              onPressed: () {
                setState(() => _unitController.text = u);
              },
            );
          }).toList(),
        ),
        const SizedBox(height: 20),

        // Budget Range
        const Text(
          'বাজেট পরিসীমা (টাকা, ৳)',
          style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF334155)),
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: TextFormField(
                controller: _budgetMinController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'সর্বনিম্ন (৳)',
                  hintText: 'e.g. ৫০০',
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
                  labelText: 'সর্বোচ্চ (৳)',
                  hintText: 'e.g. ১৫০০',
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 6),
        const Text(
          'বাজেট খালি রাখলে “আলোচনা সাপেক্ষে” হিসেবে প্রদর্শিত হবে।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF94A3B8)),
        ),
      ],
    );
  }

  Widget _buildStep7() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'কীভাবে যোগাযোগ করতে চান?',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        const SizedBox(height: 6),
        const Text(
          'সেবাদাতা ও সংশ্লিষ্ট ব্যক্তিগণ কীভাবে আপনার সাথে যোগাযোগ করতে পারবেন তা নির্ধারণ করুন।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 16),

        _buildRadioOption(
          title: 'শুধু অ্যাপের মাধ্যমে',
          subtitle: 'ইন-অ্যাপ চ্যাট ও মেসেজিং দিয়ে যোগাযোগ হবে (ফোন নম্বর গোপন থাকবে)',
          icon: Icons.chat_bubble_outline,
          isSelected: _contactPreference == DemandContactPreference.inAppOnly,
          onTap: () => setState(() => _contactPreference = DemandContactPreference.inAppOnly),
        ),
        const SizedBox(height: 10),

        _buildRadioOption(
          title: 'ফোনে সরাসরি',
          subtitle: 'ভেরিফায়েড সেবাদাতারা সরাসরি ফোনে যোগাযোগ করতে পারবেন',
          icon: Icons.phone_outlined,
          isSelected: _contactPreference == DemandContactPreference.phone,
          onTap: () => setState(() => _contactPreference = DemandContactPreference.phone),
        ),
        const SizedBox(height: 10),

        _buildRadioOption(
          title: 'অ্যাপ + ফোন উভয় মাধ্যমে',
          subtitle: 'চ্যাট এবং ফোন কল উভয় পদ্ধতি উন্মুক্ত থাকবে',
          icon: Icons.contact_phone_outlined,
          isSelected: _contactPreference == DemandContactPreference.both,
          onTap: () => setState(() => _contactPreference = DemandContactPreference.both),
        ),
        const SizedBox(height: 16),

        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: const Color(0xFFF8FAFC),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: const Color(0xFFE2E8F0)),
          ),
          child: const Row(
            children: [
              Icon(Icons.shield_outlined, size: 18, color: Color(0xFF0D9488)),
              SizedBox(width: 8),
              Expanded(
                child: Text(
                  'গোপনীয়তা সুরক্ষা: আপনার ব্যক্তিগত ফোন নম্বর স্প্যাম থেকে সুরক্ষিত রাখা হবে।',
                  style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF475569)),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildStep8() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'কারা এই প্রয়োজন দেখতে পারবেন?',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        const SizedBox(height: 6),
        const Text(
          'প্রয়োজনের দৃশ্যমানতা এবং জরুরিতা সেটিংস নির্ধারণ করুন।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 16),

        _buildRadioOption(
          title: 'সবার জন্য উন্মুক্ত (Public)',
          subtitle: 'সকল ভিজিটর ও সেবাদাতা এই প্রয়োজন দেখতে পারবেন',
          icon: Icons.public,
          isSelected: _visibility == DemandVisibility.public,
          onTap: () => setState(() => _visibility = DemandVisibility.public),
        ),
        const SizedBox(height: 10),

        _buildRadioOption(
          title: 'শুধু নিবন্ধিত ব্যবহারকারী (Registered Users)',
          subtitle: 'শুধুমাত্র সেবাকক্সে লগইনকৃত ভেরিফায়েড ব্যবহারকারীরা দেখতে পাবেন',
          icon: Icons.lock_open,
          isSelected: _visibility == DemandVisibility.registeredUsers,
          onTap: () => setState(() => _visibility = DemandVisibility.registeredUsers),
        ),
        const SizedBox(height: 10),

        _buildRadioOption(
          title: 'ব্যক্তিগত (Private)',
          subtitle: 'শুধুমাত্র আপনার নির্ধারিত সেবাদাতাদের সাথে সরাসরি শেয়ার হবে',
          icon: Icons.lock_outline,
          isSelected: _visibility == DemandVisibility.private,
          onTap: () => setState(() => _visibility = DemandVisibility.private),
        ),
        const SizedBox(height: 20),

        // Priority Switch
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            color: _priority == DemandPriority.urgent ? const Color(0xFFFEF2F2) : Colors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: _priority == DemandPriority.urgent ? const Color(0xFFFECACA) : const Color(0xFFE2E8F0)),
          ),
          child: Row(
            children: [
              const Icon(Icons.flash_on, color: Color(0xFFDC2626)),
              const SizedBox(width: 10),
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('জরুরি প্রয়োজন? (Urgent)', style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF991B1B))),
                    Text('জরুরি ট্যাগ যোগ হবে এবং উপযুক্ত সেবাদাতাদের কাছে অগ্রাধিকার পাবে', style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF7F1D1D))),
                  ],
                ),
              ),
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
        ),
      ],
    );
  }

  Widget _buildStep9() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'আপনার প্রয়োজন পর্যালোচনা করুন',
          style: TextStyle(fontFamily: 'HindSiliguri', fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        const SizedBox(height: 6),
        const Text(
          'প্রকাশ করার আগে সমস্ত তথ্য যাচাই করে নিন। যেকোনো সেকশন পরিবর্তন করতে পারেন।',
          style: TextStyle(fontFamily: 'TiroBangla', fontSize: 13, color: Color(0xFF64748B)),
        ),
        const SizedBox(height: 16),

        // Section 1: Title & Service
        _buildReviewCard(
          title: '১. শিরোনাম ও সেবা',
          stepIndex: 1,
          content: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                _titleController.text.trim(),
                style: const TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 15, color: Color(0xFF0F172A)),
              ),
              const SizedBox(height: 4),
              Text(
                'সেবা: ${_selectedServiceNameBn ?? _selectedCategoryNameBn ?? "সাধারণ"}',
                style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 12, color: Color(0xFF0D9488), fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ),

        // Section 2: Description
        _buildReviewCard(
          title: '২. বিস্তারিত বিবরণ',
          stepIndex: 3,
          content: Text(
            _descController.text.trim(),
            style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 12, color: Color(0xFF334155), height: 1.4),
          ),
        ),

        // Section 3: Location
        _buildReviewCard(
          title: '৩. ভৌগোলিক অবস্থান',
          stepIndex: 4,
          content: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'উপজেলা: $_selectedUpazilaNameBn, জেলা: $_selectedDistrictNameBn',
                style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
              ),
              if (_selectedUnionNameBn != null)
                Text('ইউনিয়ন/পৌরসভা: $_selectedUnionNameBn', style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B))),
              if (_selectedWardNameBn != null)
                Text('ওয়ার্ড: $_selectedWardNameBn', style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B))),
              if (_selectedLocalityNameBn != null)
                Text('লোকালিটি: $_selectedLocalityNameBn', style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B))),
              if (_detailedAddressController.text.trim().isNotEmpty)
                Text('ঠিকানা: ${_detailedAddressController.text.trim()}', style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF0F172A))),
            ],
          ),
        ),

        // Section 4: Schedule & Budget
        _buildReviewCard(
          title: '৪. সময়সূচি ও বাজেট',
          stepIndex: 5,
          content: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'সময়: ${_scheduleType == "ASAP" ? "যত দ্রুত সম্ভব" : (_selectedDate != null ? "${_selectedDate!.day}/${_selectedDate!.month}/${_selectedDate!.year}" : "নির্ধারিত নেই")}',
                style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 12, color: Color(0xFF334155)),
              ),
              const SizedBox(height: 4),
              if (_quantityController.text.trim().isNotEmpty)
                Text(
                  'পরিমাণ: ${_quantityController.text.trim()} ${_unitController.text.trim()}',
                  style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 12, color: Color(0xFF334155)),
                ),
              const SizedBox(height: 4),
              Text(
                'বাজেট: ${_budgetMinController.text.isNotEmpty && _budgetMaxController.text.isNotEmpty ? "৳${_budgetMinController.text} – ৳${_budgetMaxController.text}" : (_budgetMinController.text.isNotEmpty ? "৳${_budgetMinController.text}+" : "আলোচনা সাপেক্ষে")}',
                style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF047857)),
              ),
            ],
          ),
        ),

        // Section 5: Settings
        _buildReviewCard(
          title: '৫. দৃশ্যমানতা ও যোগাযোগ',
          stepIndex: 7,
          content: Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(6)),
                child: Text(_visibility.labelBn, style: const TextStyle(fontFamily: 'BalooDa2', fontSize: 11, color: Color(0xFF475569))),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(6)),
                child: Text(_contactPreference.labelBn, style: const TextStyle(fontFamily: 'BalooDa2', fontSize: 11, color: Color(0xFF475569))),
              ),
              if (_priority == DemandPriority.urgent) ...[
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(color: const Color(0xFFFEE2E2), borderRadius: BorderRadius.circular(6)),
                  child: const Text('জরুরি', style: TextStyle(fontFamily: 'BalooDa2', fontSize: 11, color: Color(0xFFDC2626), fontWeight: FontWeight.bold)),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildReviewCard({required String title, required int stepIndex, required Widget content}) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: const TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF475569))),
              InkWell(
                onTap: () => _goToStep(stepIndex),
                child: const Text('পরিবর্তন করুন', style: TextStyle(fontFamily: 'BalooDa2', color: Color(0xFF0D9488), fontSize: 11, fontWeight: FontWeight.bold)),
              ),
            ],
          ),
          const Divider(height: 16, color: Color(0xFFF1F5F9)),
          content,
        ],
      ),
    );
  }

  Widget _buildRadioOption({
    required String title,
    required String subtitle,
    required IconData icon,
    required bool isSelected,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFFF0FDFA) : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: isSelected ? const Color(0xFF0D9488) : const Color(0xFFCBD5E1)),
        ),
        child: Row(
          children: [
            Icon(
              isSelected ? Icons.radio_button_checked : Icons.radio_button_unchecked,
              color: isSelected ? const Color(0xFF0D9488) : const Color(0xFF94A3B8),
            ),
            const SizedBox(width: 12),
            Icon(icon, size: 20, color: isSelected ? const Color(0xFF0D9488) : const Color(0xFF64748B)),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF0F172A))),
                  Text(subtitle, style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B))),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStepBody() {
    switch (_currentStep) {
      case 1:
        return _buildStep1();
      case 2:
        return _buildStep2();
      case 3:
        return _buildStep3();
      case 4:
        return _buildStep4();
      case 5:
        return _buildStep5();
      case 6:
        return _buildStep6();
      case 7:
        return _buildStep7();
      case 8:
        return _buildStep8();
      case 9:
        return _buildStep9();
      default:
        return _buildStep1();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text(
          'নতুন প্রয়োজন তৈরি করুন',
          style: TextStyle(
            fontFamily: 'HindSiliguri',
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF0F172A),
        elevation: 0.5,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: _prevStep,
        ),
        actions: [
          TextButton(
            onPressed: _isSubmitting ? null : _handleSaveDraft,
            child: const Text(
              'খসড়া সংরক্ষণ',
              style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, color: Color(0xFF0D9488)),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // Step Header & Progress Bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            color: Colors.white,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'ধাপ $_currentStep / $_totalSteps',
                      style: const TextStyle(
                        fontFamily: 'BalooDa2',
                        fontWeight: FontWeight.bold,
                        fontSize: 13,
                        color: Color(0xFF0D9488),
                      ),
                    ),
                    const Text(
                      'প্রয়োজনীয় তথ্যগুলো ধাপে ধাপে পূরণ করুন।',
                      style: TextStyle(fontFamily: 'TiroBangla', fontSize: 11, color: Color(0xFF64748B)),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: _currentStep / _totalSteps,
                    backgroundColor: const Color(0xFFE2E8F0),
                    valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF0D9488)),
                    minHeight: 6,
                  ),
                ),
              ],
            ),
          ),

          // Validation Error Banner
          if (_stepError != null)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              color: const Color(0xFFFEF2F2),
              child: Row(
                children: [
                  const Icon(Icons.error_outline, size: 16, color: Color(0xFFDC2626)),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      _stepError!,
                      style: const TextStyle(fontFamily: 'TiroBangla', fontSize: 12, color: Color(0xFFB91C1C), fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
            ),

          // Scrollable Body
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _buildStepBody(),
                const SizedBox(height: 24),
              ],
            ),
          ),

          // Bottom Navigation Bar
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border(top: BorderSide(color: Colors.grey.shade200)),
            ),
            child: Row(
              children: [
                if (_currentStep > 1)
                  Expanded(
                    child: OutlinedButton(
                      onPressed: _prevStep,
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        side: const BorderSide(color: Color(0xFF94A3B8)),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      ),
                      child: const Text(
                        'পিছনে',
                        style: TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, color: Color(0xFF475569)),
                      ),
                    ),
                  ),
                if (_currentStep > 1) const SizedBox(width: 12),

                Expanded(
                  flex: 2,
                  child: ElevatedButton(
                    onPressed: _isSubmitting
                        ? null
                        : (_currentStep == _totalSteps ? _handleConfirmPublish : _nextStep),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      backgroundColor: const Color(0xFF0D9488),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    child: Text(
                      _currentStep == _totalSteps ? 'প্রয়োজন প্রকাশ করুন' : 'পরবর্তী',
                      style: const TextStyle(fontFamily: 'BalooDa2', fontWeight: FontWeight.bold, color: Colors.white, fontSize: 14),
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
}
