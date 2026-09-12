/// Location Selection Screen for SebaCox.
/// মূল স্লোগান: “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
/// ছোট পরিচিতি: “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”
import 'package:flutter/material.dart';
import '../../../core/constants/app_brand.dart';
import '../repositories/location_repository.dart';
import '../models/location_models.dart';
import '../models/location_enums.dart';
import '../state/location_state.dart';

class LocationSelectionScreen extends StatefulWidget {
  final LocationRepository locationRepository;

  const LocationSelectionScreen({
    super.key,
    required this.locationRepository,
  });

  @override
  State<LocationSelectionScreen> createState() => _LocationSelectionScreenState();
}

class _LocationSelectionScreenState extends State<LocationSelectionScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<LocationSearchResult> _searchResults = [];
  bool _isSearching = false;

  // Manual hierarchy selection state
  List<GeographicItem> _divisions = [];
  List<GeographicItem> _districts = [];
  List<GeographicItem> _upazilas = [];
  List<GeographicItem> _unions = [];

  GeographicItem? _selectedDivision;
  GeographicItem? _selectedDistrict;
  GeographicItem? _selectedUpazila;
  GeographicItem? _selectedUnion;

  bool _isLoadingHierarchy = false;
  String? _hierarchyError;

  @override
  void initState() {
    super.initState();
    _loadInitialDivisions();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _loadInitialDivisions() async {
    setState(() {
      _isLoadingHierarchy = true;
      _hierarchyError = null;
    });

    try {
      final list = await widget.locationRepository.apiService.fetchDivisions();
      setState(() {
        _divisions = list;
        _isLoadingHierarchy = false;
      });
    } catch (e) {
      setState(() {
        _isLoadingHierarchy = false;
        _hierarchyError = 'বিভাগ তালিকা লোড করা যায়নি। পুনরায় চেষ্টা করুন।';
      });
    }
  }

  Future<void> _onDivisionSelected(GeographicItem division) async {
    setState(() {
      _selectedDivision = division;
      _selectedDistrict = null;
      _selectedUpazila = null;
      _selectedUnion = null;
      _districts = [];
      _upazilas = [];
      _unions = [];
      _isLoadingHierarchy = true;
    });

    try {
      final list = await widget.locationRepository.apiService.fetchDistricts(divisionId: division.id);
      setState(() {
        _districts = list;
        _isLoadingHierarchy = false;
      });
    } catch (_) {
      setState(() => _isLoadingHierarchy = false);
    }
  }

  Future<void> _onDistrictSelected(GeographicItem district) async {
    setState(() {
      _selectedDistrict = district;
      _selectedUpazila = null;
      _selectedUnion = null;
      _upazilas = [];
      _unions = [];
      _isLoadingHierarchy = true;
    });

    try {
      final list = await widget.locationRepository.apiService.fetchUpazilas(districtId: district.id);
      setState(() {
        _upazilas = list;
        _isLoadingHierarchy = false;
      });
    } catch (_) {
      setState(() => _isLoadingHierarchy = false);
    }
  }

  Future<void> _onUpazilaSelected(GeographicItem upazila) async {
    setState(() {
      _selectedUpazila = upazila;
      _selectedUnion = null;
      _unions = [];
      _isLoadingHierarchy = true;
    });

    try {
      final list = await widget.locationRepository.apiService.fetchUnions(upazilaId: upazila.id);
      setState(() {
        _unions = list;
        _isLoadingHierarchy = false;
      });
    } catch (_) {
      setState(() => _isLoadingHierarchy = false);
    }
  }

  Future<void> _performSearch(String query) async {
    if (query.trim().length < 2) {
      setState(() {
        _searchResults = [];
        _isSearching = false;
      });
      return;
    }

    setState(() => _isSearching = true);
    final results = await widget.locationRepository.search(query);
    setState(() {
      _searchResults = results;
      _isSearching = false;
    });
  }

  Future<void> _confirmManualSelection() async {
    if (_selectedDistrict == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('অনুগ্রহ করে অন্তত একটি জেলা নির্বাচন করুন')),
      );
      return;
    }

    final success = await widget.locationRepository.selectAdministrativeArea(
      districtId: _selectedDistrict!.id,
      upazilaId: _selectedUpazila?.id,
      unionId: _selectedUnion?.id,
      label: _selectedUpazila != null
          ? '${_selectedUpazila!.nameBn}, ${_selectedDistrict!.nameBn}'
          : _selectedDistrict!.nameBn,
    );

    if (mounted && success) {
      Navigator.of(context).pop();
    }
  }

  void _showGpsConfirmationModal(BuildContext context, dynamic point) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('বর্তমান অবস্থান নিশ্চিতকরণ'),
        content: Text(
          'আপনার বর্তমান জিপিএস অবস্থান:\n${point.addressText ?? "অজানা"}\n\n'
          'আপনি কি এই অবস্থানটিকে আপনার নির্বাচিত সেবা এলাকা হিসেবে নির্ধারণ করতে চান?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('বাতিল'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF006A4E),
              foregroundColor: Colors.white,
            ),
            onPressed: () async {
              Navigator.of(ctx).pop();
              // Create user location from GPS fix if coordinates match
              if (mounted) {
                Navigator.of(context).pop();
              }
            },
            child: const Text('হ্যাঁ, নিশ্চিত করুন'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text(
          'আপনার অবস্থান নির্বাচন করুন',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 17),
        ),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF0F172A),
        elevation: 0.5,
      ),
      body: Column(
        children: [
          // 1. Search Bar
          Container(
            color: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: TextField(
              controller: _searchController,
              onChanged: _performSearch,
              decoration: InputDecoration(
                hintText: 'এলাকা, উপজেলা বা জেলা অনুসন্ধান করুন...',
                hintStyle: const TextStyle(fontSize: 14, color: Color(0xFF94A3B8)),
                prefixIcon: const Icon(Icons.search, color: Color(0xFF006A4E)),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear, color: Color(0xFF94A3B8)),
                        onPressed: () {
                          _searchController.clear();
                          _performSearch('');
                        },
                      )
                    : null,
                filled: true,
                fillColor: const Color(0xFFF1F5F9),
                contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),

          // 2. Body: Search Results or GPS Card + Hierarchy Stepper
          Expanded(
            child: _searchController.text.isNotEmpty
                ? _buildSearchResults()
                : _buildHierarchySelector(),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchResults() {
    if (_isSearching) {
      return const Center(
        child: CircularProgressIndicator(color: Color(0xFF006A4E)),
      );
    }

    if (_searchResults.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.location_off, size: 48, color: Color(0xFF94A3B8)),
            const SizedBox(height: 12),
            const Text(
              'লোকেশন পাওয়া যায়নি',
              style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF64748B)),
            ),
            const SizedBox(height: 4),
            const Text(
              'সঠিক বানান দিয়ে আবার অনুসন্ধান করুন',
              style: TextStyle(fontSize: 13, color: Color(0xFF94A3B8)),
            ),
            const SizedBox(height: 10),
            Text(
              AppBrand.shortDescriptionWithQuotes,
              style: const TextStyle(fontSize: 12, color: Color(0xFF0F766E), fontWeight: FontWeight.w600),
            ),
          ],
        ),
      );
    }

    return ListView.separated(
      itemCount: _searchResults.length,
      separatorBuilder: (_, __) => const Divider(height: 1),
      itemBuilder: (context, index) {
        final item = _searchResults[index];
        return ListTile(
          leading: Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: const Color(0xFFE6F4EA),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(Icons.place, color: Color(0xFF006A4E), size: 20),
          ),
          title: Text(
            '${item.nameBn} (${item.nameEn})',
            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14),
          ),
          subtitle: Text(
            item.hierarchyPath,
            style: const TextStyle(fontSize: 12, color: Color(0xFF64748B)),
          ),
          trailing: Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
            decoration: BoxDecoration(
              color: const Color(0xFFF1F5F9),
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              item.typeLabel,
              style: const TextStyle(fontSize: 11, color: Color(0xFF475569)),
            ),
          ),
          onTap: () async {
            // Select based on item type
            final success = await widget.locationRepository.selectAdministrativeArea(
              districtId: item.parentId ?? item.id,
              upazilaId: item.type == 'UPAZILA' ? item.id : null,
              label: '${item.nameBn} (${item.typeLabel})',
            );
            if (mounted && success) {
              Navigator.of(context).pop();
            }
          },
        );
      },
    );
  }

  Widget _buildHierarchySelector() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // GPS Location Card
          _buildGpsTriggerCard(),
          const SizedBox(height: 20),

          // Hierarchy Section Title
          const Row(
            children: [
              Icon(Icons.account_tree_outlined, size: 20, color: Color(0xFF006A4E)),
              SizedBox(width: 8),
              Text(
                'প্রশাসনিক এলাকা নির্বাচন করুন',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF0F172A)),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Division Dropdown
          _buildDropdownCard(
            label: '১. বিভাগ নির্বাচন',
            value: _selectedDivision,
            items: _divisions,
            hint: 'বিভাগ বাছাই করুন',
            onChanged: (val) {
              if (val != null) _onDivisionSelected(val);
            },
          ),
          const SizedBox(height: 12),

          // District Dropdown
          if (_selectedDivision != null)
            _buildDropdownCard(
              label: '২. জেলা নির্বাচন',
              value: _selectedDistrict,
              items: _districts,
              hint: 'জেলা বাছাই করুন',
              onChanged: (val) {
                if (val != null) _onDistrictSelected(val);
              },
            ),
          if (_selectedDivision != null) const SizedBox(height: 12),

          // Upazila Dropdown
          if (_selectedDistrict != null)
            _buildDropdownCard(
              label: '৩. উপজেলা / পৌরসভা নির্বাচন',
              value: _selectedUpazila,
              items: _upazilas,
              hint: 'উপজেলা বাছাই করুন (ঐচ্ছিক)',
              onChanged: (val) {
                if (val != null) _onUpazilaSelected(val);
              },
            ),
          if (_selectedDistrict != null) const SizedBox(height: 12),

          // Union Dropdown
          if (_selectedUpazila != null && _unions.isNotEmpty)
            _buildDropdownCard(
              label: '৪. ইউনিয়ন / ওয়ার্ড নির্বাচন',
              value: _selectedUnion,
              items: _unions,
              hint: 'ইউনিয়ন বাছাই করুন (ঐচ্ছিক)',
              onChanged: (val) {
                setState(() => _selectedUnion = val);
              },
            ),
          if (_selectedUpazila != null && _unions.isNotEmpty) const SizedBox(height: 12),

          if (_isLoadingHierarchy)
            const Center(
              child: Padding(
                padding: EdgeInsets.all(12),
                child: CircularProgressIndicator(color: Color(0xFF006A4E)),
              ),
            ),

          if (_hierarchyError != null)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(
                _hierarchyError!,
                style: const TextStyle(color: Colors.red, fontSize: 13),
              ),
            ),

          const SizedBox(height: 16),

          // Confirmation Button
          if (_selectedDistrict != null)
            SizedBox(
              width: double.infinity,
              height: 48,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF006A4E),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                onPressed: _confirmManualSelection,
                child: Text(
                  _selectedUpazila != null
                      ? '${_selectedUpazila!.nameBn} সেবা এলাকা নিশ্চিত করুন'
                      : '${_selectedDistrict!.nameBn} জেলা নিশ্চিত করুন',
                  style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildGpsTriggerCard() {
    return StreamBuilder<LocationState>(
      stream: widget.locationRepository.stateStream,
      initialData: widget.locationRepository.currentState,
      builder: (context, snapshot) {
        final state = snapshot.data ?? LocationState.initial();
        final isFetching = state.status == LocationLoadingStatus.fetchingLocation;

        return Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: const Color(0xFFE2E8F0)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: const Color(0xFFE6F4EA),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Icon(Icons.my_location, color: Color(0xFF006A4E), size: 20),
                  ),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'বর্তমান অবস্থান ব্যবহার করুন',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF0F172A)),
                        ),
                        SizedBox(height: 2),
                        Text(
                          'ডিভাইসের জিপিএস দিয়ে আপনার নিকটবর্তী অবস্থান নির্ধারণ করুন',
                          style: TextStyle(fontSize: 12, color: Color(0xFF64748B)),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              if (state.currentGpsLocation != null) ...[
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.check_circle, color: Color(0xFF006A4E), size: 16),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          state.currentGpsLocation!.addressText,
                          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 10),
              ],
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  style: OutlinedButton.styleFrom(
                    foregroundColor: const Color(0xFF006A4E),
                    side: const BorderSide(color: Color(0xFF006A4E)),
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
                  onPressed: isFetching
                      ? null
                      : () async {
                          await widget.locationRepository.fetchCurrentGpsLocation();
                          final updated = widget.locationRepository.currentState;
                          if (mounted && updated.currentGpsLocation != null) {
                            _showGpsConfirmationModal(context, updated.currentGpsLocation);
                          }
                        },
                  icon: isFetching
                      ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFF006A4E)),
                        )
                      : const Icon(Icons.gps_fixed, size: 18),
                  label: Text(
                    isFetching ? 'অবস্থান খোঁজা হচ্ছে...' : 'লোকেশন অনুমতি দিন ও জিপিএস ট্র্যাক করুন',
                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildDropdownCard({
    required String label,
    required GeographicItem? value,
    required List<GeographicItem> items,
    required String hint,
    required ValueChanged<GeographicItem?> onChanged,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Color(0xFF64748B)),
          ),
          DropdownButtonHideUnderline(
            child: DropdownButton<GeographicItem>(
              value: value,
              isExpanded: true,
              hint: Text(hint, style: const TextStyle(fontSize: 14, color: Color(0xFF94A3B8))),
              items: items.map((item) {
                return DropdownMenuItem<GeographicItem>(
                  value: item,
                  child: Text(
                    '${item.nameBn} (${item.nameEn})',
                    style: const TextStyle(fontSize: 14, color: Color(0xFF0F172A)),
                  ),
                );
              }).toList(),
              onChanged: onChanged,
            ),
          ),
        ],
      ),
    );
  }
}
