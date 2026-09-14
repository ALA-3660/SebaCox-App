/// Reusable Cascading Location Selector Widget for SebaCox.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
import 'package:flutter/material.dart';
import '../models/location_models.dart';
import '../services/location_api_service.dart';

class CascadingLocationSelectionResult {
  final GeographicItem? division;
  final GeographicItem? district;
  final GeographicItem? upazila;
  final GeographicItem? municipality;
  final GeographicItem? union;
  final GeographicItem? ward;
  final GeographicItem? locality;
  final String fullHierarchyTextBn;
  final String fullHierarchyTextEn;

  const CascadingLocationSelectionResult({
    this.division,
    this.district,
    this.upazila,
    this.municipality,
    this.union,
    this.ward,
    this.locality,
    required this.fullHierarchyTextBn,
    required this.fullHierarchyTextEn,
  });
}

class CascadingLocationSelector extends StatefulWidget {
  final LocationApiService apiService;
  final ValueChanged<CascadingLocationSelectionResult> onSelectionChanged;
  final int? initialDivisionId;
  final int? initialDistrictId;
  final int? initialUpazilaId;
  final bool showLocalityLevel;
  final bool showWardLevel;
  final bool isRequired;

  const CascadingLocationSelector({
    super.key,
    required this.apiService,
    required this.onSelectionChanged,
    this.initialDivisionId,
    this.initialDistrictId,
    this.initialUpazilaId,
    this.showLocalityLevel = true,
    this.showWardLevel = true,
    this.isRequired = true,
  });

  @override
  State<CascadingLocationSelector> createState() => _CascadingLocationSelectorState();
}

class _CascadingLocationSelectorState extends State<CascadingLocationSelector> {
  // Lists
  List<GeographicItem> _divisions = [];
  List<GeographicItem> _districts = [];
  List<GeographicItem> _upazilas = [];
  List<GeographicItem> _municipalities = [];
  List<GeographicItem> _unions = [];
  List<GeographicItem> _wards = [];
  List<GeographicItem> _localities = [];

  // Selections
  GeographicItem? _selectedDivision;
  GeographicItem? _selectedDistrict;
  GeographicItem? _selectedUpazila;
  String _subUpazilaType = 'NONE'; // 'UNION', 'MUNICIPALITY'
  GeographicItem? _selectedMunicipality;
  GeographicItem? _selectedUnion;
  GeographicItem? _selectedWard;
  GeographicItem? _selectedLocality;

  // Loading flags
  bool _loadingDivisions = false;
  bool _loadingDistricts = false;
  bool _loadingUpazilas = false;
  bool _loadingSubUnits = false;
  bool _loadingWards = false;
  bool _loadingLocalities = false;

  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadDivisions();
  }

  Future<void> _loadDivisions() async {
    setState(() {
      _loadingDivisions = true;
      _errorMessage = null;
    });

    try {
      final items = await widget.apiService.fetchDivisions();
      setState(() {
        _divisions = items;
        _loadingDivisions = false;
      });

      // Handle auto-select if initial provided
      if (widget.initialDivisionId != null) {
        final match = items.firstWhere(
          (d) => d.id == widget.initialDivisionId,
          orElse: () => items.first,
        );
        _onDivisionSelected(match);
      } else if (items.isNotEmpty) {
        // Default to Chittagong / first division
        final ctg = items.firstWhere(
          (d) => d.nameEn.toLowerCase().contains('chattogram') || d.nameEn.toLowerCase().contains('chittagong'),
          orElse: () => items.first,
        );
        _onDivisionSelected(ctg);
      }
    } catch (e) {
      setState(() {
        _loadingDivisions = false;
        _errorMessage = 'বিভাগ তালিকা লোড করা যায়নি।';
      });
    }
  }

  Future<void> _onDivisionSelected(GeographicItem? division) async {
    if (division == null) return;
    setState(() {
      _selectedDivision = division;
      _selectedDistrict = null;
      _selectedUpazila = null;
      _selectedMunicipality = null;
      _selectedUnion = null;
      _selectedWard = null;
      _selectedLocality = null;
      _districts = [];
      _upazilas = [];
      _municipalities = [];
      _unions = [];
      _wards = [];
      _localities = [];
      _loadingDistricts = true;
    });

    _notifyResult();

    try {
      final list = await widget.apiService.fetchDistricts(divisionId: division.id);
      setState(() {
        _districts = list;
        _loadingDistricts = false;
      });

      if (widget.initialDistrictId != null) {
        final match = list.firstWhere(
          (d) => d.id == widget.initialDistrictId,
          orElse: () => list.first,
        );
        _onDistrictSelected(match);
      } else if (list.isNotEmpty) {
        // Default to Cox's Bazar if present
        final cxb = list.firstWhere(
          (d) => d.nameEn.toLowerCase().contains('cox'),
          orElse: () => list.first,
        );
        _onDistrictSelected(cxb);
      }
    } catch (_) {
      setState(() => _loadingDistricts = false);
    }
  }

  Future<void> _onDistrictSelected(GeographicItem? district) async {
    if (district == null) return;
    setState(() {
      _selectedDistrict = district;
      _selectedUpazila = null;
      _selectedMunicipality = null;
      _selectedUnion = null;
      _selectedWard = null;
      _selectedLocality = null;
      _upazilas = [];
      _municipalities = [];
      _unions = [];
      _wards = [];
      _localities = [];
      _loadingUpazilas = true;
    });

    _notifyResult();

    try {
      final list = await widget.apiService.fetchUpazilas(districtId: district.id);
      setState(() {
        _upazilas = list;
        _loadingUpazilas = false;
      });

      if (widget.initialUpazilaId != null) {
        final match = list.firstWhere(
          (u) => u.id == widget.initialUpazilaId,
          orElse: () => list.first,
        );
        _onUpazilaSelected(match);
      }
    } catch (_) {
      setState(() => _loadingUpazilas = false);
    }
  }

  Future<void> _onUpazilaSelected(GeographicItem? upazila) async {
    if (upazila == null) return;
    setState(() {
      _selectedUpazila = upazila;
      _selectedMunicipality = null;
      _selectedUnion = null;
      _selectedWard = null;
      _selectedLocality = null;
      _municipalities = [];
      _unions = [];
      _wards = [];
      _localities = [];
      _loadingSubUnits = true;
    });

    _notifyResult();

    try {
      // Fetch both unions and municipalities for this upazila concurrently
      final unionsFuture = widget.apiService.fetchUnions(upazilaId: upazila.id);
      final munFuture = widget.apiService.fetchMunicipalities(upazilaId: upazila.id);
      final results = await Future.wait([unionsFuture, munFuture]);

      final fetchedUnions = results[0];
      final fetchedMun = results[1];

      setState(() {
        _unions = fetchedUnions;
        _municipalities = fetchedMun;
        _loadingSubUnits = false;
        if (fetchedMun.isNotEmpty && fetchedUnions.isEmpty) {
          _subUpazilaType = 'MUNICIPALITY';
        } else {
          _subUpazilaType = 'UNION';
        }
      });
    } catch (_) {
      setState(() => _loadingSubUnits = false);
    }
  }

  Future<void> _onUnionSelected(GeographicItem? union) async {
    if (union == null) return;
    setState(() {
      _selectedUnion = union;
      _selectedMunicipality = null;
      _selectedWard = null;
      _selectedLocality = null;
      _wards = [];
      _localities = [];
      _loadingWards = true;
    });

    _notifyResult();

    try {
      final wards = await widget.apiService.fetchWards(unionId: union.id);
      setState(() {
        _wards = wards;
        _loadingWards = false;
      });
    } catch (_) {
      setState(() => _loadingWards = false);
    }
  }

  Future<void> _onMunicipalitySelected(GeographicItem? municipality) async {
    if (municipality == null) return;
    setState(() {
      _selectedMunicipality = municipality;
      _selectedUnion = null;
      _selectedWard = null;
      _selectedLocality = null;
      _wards = [];
      _localities = [];
      _loadingWards = true;
    });

    _notifyResult();

    try {
      final wards = await widget.apiService.fetchWards(municipalityId: municipality.id);
      setState(() {
        _wards = wards;
        _loadingWards = false;
      });
    } catch (_) {
      setState(() => _loadingWards = false);
    }
  }

  Future<void> _onWardSelected(GeographicItem? ward) async {
    if (ward == null) return;
    setState(() {
      _selectedWard = ward;
      _selectedLocality = null;
      _localities = [];
      _loadingLocalities = true;
    });

    _notifyResult();

    if (widget.showLocalityLevel) {
      try {
        final locs = await widget.apiService.fetchLocalities(
          upazilaId: _selectedUpazila?.id,
          wardId: ward.id,
          unionId: _selectedUnion?.id,
          municipalityId: _selectedMunicipality?.id,
        );
        setState(() {
          _localities = locs;
          _loadingLocalities = false;
        });
      } catch (_) {
        setState(() => _loadingLocalities = false);
      }
    } else {
      setState(() => _loadingLocalities = false);
    }
  }

  void _onLocalitySelected(GeographicItem? locality) {
    setState(() {
      _selectedLocality = locality;
    });
    _notifyResult();
  }

  void _notifyResult() {
    final bnParts = <String>[];
    final enParts = <String>[];

    if (_selectedLocality != null) {
      bnParts.add(_selectedLocality!.nameBn);
      enParts.add(_selectedLocality!.nameEn);
    }
    if (_selectedWard != null) {
      bnParts.add('ওয়ার্ড ${_selectedWard!.nameBn}');
      enParts.add('Ward ${_selectedWard!.nameEn}');
    }
    if (_selectedUnion != null) {
      bnParts.add('${_selectedUnion!.nameBn} ইউপি');
      enParts.add('${_selectedUnion!.nameEn} Union');
    }
    if (_selectedMunicipality != null) {
      bnParts.add('${_selectedMunicipality!.nameBn} পৌরসভা');
      enParts.add('${_selectedMunicipality!.nameEn} Municipality');
    }
    if (_selectedUpazila != null) {
      bnParts.add(_selectedUpazila!.nameBn);
      enParts.add(_selectedUpazila!.nameEn);
    }
    if (_selectedDistrict != null) {
      bnParts.add(_selectedDistrict!.nameBn);
      enParts.add(_selectedDistrict!.nameEn);
    }

    widget.onSelectionChanged(CascadingLocationSelectionResult(
      division: _selectedDivision,
      district: _selectedDistrict,
      upazila: _selectedUpazila,
      municipality: _selectedMunicipality,
      union: _selectedUnion,
      ward: _selectedWard,
      locality: _selectedLocality,
      fullHierarchyTextBn: bnParts.join(', '),
      fullHierarchyTextEn: enParts.join(', '),
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (_errorMessage != null)
          Container(
            padding: const EdgeInsets.all(8),
            margin: const EdgeInsets.only(bottom: 8),
            decoration: BoxDecoration(
              color: Colors.red.shade50,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.red.shade200),
            ),
            child: Row(
              children: [
                const Icon(Icons.error_outline, color: Colors.red, size: 16),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _errorMessage!,
                    style: const TextStyle(color: Colors.red, fontSize: 12),
                  ),
                ),
                TextButton(
                  onPressed: _loadDivisions,
                  child: const Text('পুনরায় চেষ্টা', style: TextStyle(fontSize: 12)),
                )
              ],
            ),
          ),

        // 1. Division Dropdown
        _buildDropdownRow(
          title: '১. বিভাগ (Division)',
          hint: _loadingDivisions ? 'বিভাগ লোড হচ্ছে...' : 'বিভাগ বাছাই করুন',
          value: _selectedDivision,
          items: _divisions,
          isLoading: _loadingDivisions,
          enabled: true,
          onChanged: _onDivisionSelected,
        ),
        const SizedBox(height: 10),

        // 2. District Dropdown
        _buildDropdownRow(
          title: '২. জেলা (District)',
          hint: _loadingDistricts ? 'জেলা লোড হচ্ছে...' : 'জেলা বাছাই করুন',
          value: _selectedDistrict,
          items: _districts,
          isLoading: _loadingDistricts,
          enabled: _selectedDivision != null,
          onChanged: _onDistrictSelected,
        ),
        const SizedBox(height: 10),

        // 3. Upazila Dropdown
        _buildDropdownRow(
          title: '৩. উপজেলা / থানা (Upazila)',
          hint: _loadingUpazilas ? 'উপজেলা লোড হচ্ছে...' : 'উপজেলা বাছাই করুন',
          value: _selectedUpazila,
          items: _upazilas,
          isLoading: _loadingUpazilas,
          enabled: _selectedDistrict != null,
          onChanged: _onUpazilaSelected,
        ),
        const SizedBox(height: 10),

        // 4. Union / Municipality Selector (if Upazila is selected)
        if (_selectedUpazila != null) ...[
          if (_municipalities.isNotEmpty && _unions.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(
                children: [
                  ChoiceChip(
                    label: const Text('ইউনিয়ন সমূহ'),
                    selected: _subUpazilaType == 'UNION',
                    onSelected: (val) {
                      if (val) {
                        setState(() {
                          _subUpazilaType = 'UNION';
                          _selectedMunicipality = null;
                        });
                      }
                    },
                  ),
                  const SizedBox(width: 8),
                  ChoiceChip(
                    label: const Text('পৌরসভা এলাকা'),
                    selected: _subUpazilaType == 'MUNICIPALITY',
                    onSelected: (val) {
                      if (val) {
                        setState(() {
                          _subUpazilaType = 'MUNICIPALITY';
                          _selectedUnion = null;
                        });
                      }
                    },
                  ),
                ],
              ),
            ),

          if (_subUpazilaType == 'UNION' && _unions.isNotEmpty)
            _buildDropdownRow(
              title: '৪. ইউনিয়ন পরিষদ (Union)',
              hint: _loadingSubUnits ? 'ইউনিয়ন লোড হচ্ছে...' : 'ইউনিয়ন বাছাই করুন (ঐচ্ছিক)',
              value: _selectedUnion,
              items: _unions,
              isLoading: _loadingSubUnits,
              enabled: true,
              onChanged: _onUnionSelected,
            ),

          if (_subUpazilaType == 'MUNICIPALITY' || (_municipalities.isNotEmpty && _unions.isEmpty))
            _buildDropdownRow(
              title: '৪. পৌরসভা (Municipality)',
              hint: _loadingSubUnits ? 'পৌরসভা লোড হচ্ছে...' : 'পৌরসভা বাছাই করুন (ঐচ্ছিক)',
              value: _selectedMunicipality,
              items: _municipalities,
              isLoading: _loadingSubUnits,
              enabled: true,
              onChanged: _onMunicipalitySelected,
            ),

          const SizedBox(height: 10),
        ],

        // 5. Ward Dropdown (if Union or Municipality is selected and showWardLevel is true)
        if (widget.showWardLevel && (_selectedUnion != null || _selectedMunicipality != null)) ...[
          _buildDropdownRow(
            title: '৫. ওয়ার্ড নম্বর (Ward)',
            hint: _loadingWards ? 'ওয়ার্ড লোড হচ্ছে...' : 'ওয়ার্ড বাছাই করুন (ঐচ্ছিক)',
            value: _selectedWard,
            items: _wards,
            isLoading: _loadingWards,
            enabled: _wards.isNotEmpty,
            onChanged: _onWardSelected,
          ),
          const SizedBox(height: 10),
        ],

        // 6. Locality Dropdown (পাড়া, মহল্লা, গ্রাম, বাজার, আবাসিক এলাকা)
        if (widget.showLocalityLevel && (_selectedWard != null || _selectedUnion != null || _selectedMunicipality != null)) ...[
          _buildDropdownRow(
            title: '৬. লোকালিটি / পাড়া / মহল্লা / গ্রাম / বাজার',
            hint: _loadingLocalities ? 'এলাকা লোড হচ্ছে...' : 'পাড়া, মহল্লা বা বাজার নির্বাচন করুন (ঐচ্ছিক)',
            value: _selectedLocality,
            items: _localities,
            isLoading: _loadingLocalities,
            enabled: _localities.isNotEmpty,
            onChanged: _onLocalitySelected,
          ),
        ],
      ],
    );
  }

  Widget _buildDropdownRow({
    required String title,
    required String hint,
    required GeographicItem? value,
    required List<GeographicItem> items,
    required bool isLoading,
    required bool enabled,
    required ValueChanged<GeographicItem?> onChanged,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: enabled ? Colors.white : const Color(0xFFF8FAFC),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: enabled ? const Color(0xFFCBD5E1) : const Color(0xFFE2E8F0)),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: enabled ? const Color(0xFF334155) : const Color(0xFF94A3B8),
                ),
              ),
              if (isLoading)
                const SizedBox(
                  width: 14,
                  height: 14,
                  child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFF006A4E)),
                ),
            ],
          ),
          DropdownButtonHideUnderline(
            child: DropdownButton<GeographicItem>(
              value: value,
              isExpanded: true,
              disabledHint: Text(
                hint,
                style: const TextStyle(fontSize: 13, color: Color(0xFFCBD5E1)),
              ),
              hint: Text(
                hint,
                style: const TextStyle(fontSize: 13, color: Color(0xFF94A3B8)),
              ),
              items: enabled
                  ? items.map((item) {
                      return DropdownMenuItem<GeographicItem>(
                        value: item,
                        child: Text(
                          '${item.nameBn} (${item.nameEn})',
                          style: const TextStyle(fontSize: 13, color: Color(0xFF0F172A)),
                          overflow: TextOverflow.ellipsis,
                        ),
                      );
                    }).toList()
                  : null,
              onChanged: enabled ? onChanged : null,
            ),
          ),
        ],
      ),
    );
  }
}
