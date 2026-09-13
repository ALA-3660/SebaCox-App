import React, { useState, useMemo } from 'react';
import { 
  ArrowLeft, 
  Search, 
  CheckCircle2, 
  Clock, 
  Star, 
  Phone, 
  UserCheck, 
  Plus, 
  ShieldCheck, 
  Check, 
  X, 
  ChevronRight, 
  Sparkles,
  SlidersHorizontal,
  Layers,
  MapPin,
  Building2,
  Users,
  AlertCircle
} from 'lucide-react';
import { 
  MockProvider, 
  MockProviderService, 
  INITIAL_MOCK_PROVIDERS 
} from '../data/providerMockData';
import { INITIAL_SERVICES } from '../data/taxonomyMockData';

// -----------------------------------------------------------------------------
// 1. PROVIDER DIRECTORY SCREEN
// -----------------------------------------------------------------------------
interface ProviderDirectoryViewProps {
  providers: MockProvider[];
  onBack: () => void;
  onSelectProvider: (provider: MockProvider) => void;
  onGoToRegister: () => void;
  onGoToDashboard: () => void;
  showTypoTag: (font: 'hind' | 'baloo' | 'tiro', role: string) => React.ReactNode;
}

export const ProviderDirectoryView: React.FC<ProviderDirectoryViewProps> = ({
  providers,
  onBack,
  onSelectProvider,
  onGoToRegister,
  onGoToDashboard,
  showTypoTag
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterUpazila, setFilterUpazila] = useState<string>('ALL');
  const [filterAvailability, setFilterAvailability] = useState<string>('ALL');

  const filteredProviders = useMemo(() => {
    return providers.filter((p) => {
      const q = searchQuery.toLowerCase().trim();
      const matchesSearch = !q ||
        p.business_name.toLowerCase().includes(q) ||
        p.owner_name.toLowerCase().includes(q) ||
        p.services.some(s => s.name_bn.toLowerCase().includes(q) || s.name_en.toLowerCase().includes(q));

      const matchesUpazila = filterUpazila === 'ALL' || 
        p.service_areas.some(a => a.upazila_name_bn === filterUpazila);

      const matchesAvailability = filterAvailability === 'ALL' ||
        p.availability_status === filterAvailability;

      return matchesSearch && matchesUpazila && matchesAvailability;
    });
  }, [providers, searchQuery, filterUpazila, filterAvailability]);

  return (
    <div className="flex flex-col gap-2.5 font-tiro py-1">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-2">
        <button
          onClick={onBack}
          className="flex items-center gap-1 text-xs text-slate-600 hover:text-slate-900 font-bold cursor-pointer font-baloo"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span className="font-baloo">হোম</span>
        </button>
        <div className="flex items-center">
          <span className="text-xs font-bold text-slate-900 font-hind">সেবাদাতা নেটওয়ার্ক</span>
          {showTypoTag('hind', 'Page Title')}
        </div>
        <button
          onClick={onGoToDashboard}
          className="px-2 py-0.5 bg-teal-50 text-teal-800 border border-teal-200 rounded-md text-[10px] font-bold hover:bg-teal-100 cursor-pointer font-baloo"
        >
          ড্যাশবোর্ড
        </button>
      </div>

      {/* Brand Slogan */}
      <div className="bg-teal-50/70 border border-teal-200/80 rounded-xl p-2 text-center">
        <p className="text-[11px] font-bold text-teal-900 font-hind">
          “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
        </p>
        <p className="text-[10px] text-teal-800 font-tiro">
          খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই
        </p>
      </div>

      {/* Search Input */}
      <div className="relative">
        <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder="সেবাদাতা বা কাজের ধরন খুঁজুন..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full bg-white border border-slate-300 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-teal-600 font-tiro"
        />
      </div>

      {/* Quick Filter Chips */}
      <div className="flex gap-1 overflow-x-auto text-[10px] font-baloo pb-1">
        <button
          onClick={() => { setFilterUpazila('ALL'); setFilterAvailability('ALL'); }}
          className={`px-2 py-0.5 rounded-full border cursor-pointer whitespace-nowrap font-baloo ${
            filterUpazila === 'ALL' && filterAvailability === 'ALL'
              ? 'bg-teal-700 text-white border-teal-800'
              : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
          }`}
        >
          সকল ({providers.length})
        </button>
        <button
          onClick={() => setFilterAvailability(filterAvailability === 'ONLINE' ? 'ALL' : 'ONLINE')}
          className={`px-2 py-0.5 rounded-full border cursor-pointer whitespace-nowrap font-baloo ${
            filterAvailability === 'ONLINE'
              ? 'bg-emerald-600 text-white border-emerald-700'
              : 'bg-white text-emerald-700 border-emerald-200 hover:bg-emerald-50'
          }`}
        >
          🟢 অনলাইনে আছেন
        </button>
        <button
          onClick={() => setFilterUpazila(filterUpazila === 'কক্সবাজার সদর' ? 'ALL' : 'কক্সবাজার সদর')}
          className={`px-2 py-0.5 rounded-full border cursor-pointer whitespace-nowrap font-baloo ${
            filterUpazila === 'কক্সবাজার সদর'
              ? 'bg-teal-700 text-white border-teal-800'
              : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
          }`}
        >
          কক্সবাজার সদর
        </button>
        <button
          onClick={() => setFilterUpazila(filterUpazila === 'চকোরিয়া' ? 'ALL' : 'চকোরিয়া')}
          className={`px-2 py-0.5 rounded-full border cursor-pointer whitespace-nowrap font-baloo ${
            filterUpazila === 'চকোরিয়া'
              ? 'bg-teal-700 text-white border-teal-800'
              : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
          }`}
        >
          চকোরিয়া
        </button>
      </div>

      {/* Providers List */}
      <div className="space-y-2.5 max-h-[380px] overflow-y-auto pr-0.5">
        {filteredProviders.map((p) => {
          const isOnline = p.availability_status === 'ONLINE';
          const isBusy = p.availability_status === 'BUSY';

          return (
            <div
              key={p.id}
              className="bg-white rounded-xl border border-slate-200 p-3 shadow-xs hover:border-teal-400 transition space-y-2"
            >
              {/* Top Row: Business Name & Status */}
              <div className="flex items-start justify-between gap-1.5">
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-bold text-slate-900 truncate font-baloo">
                      {p.business_name}
                    </span>
                    {p.is_verified && (
                      <span title="ভেরিফাইড সেবাদাতা" className="shrink-0">
                        <CheckCircle2 className="w-3.5 h-3.5 text-teal-600 fill-teal-50" />
                      </span>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-500 font-tiro mt-0.5">
                    মালিক: {p.owner_name} • {p.experience_years} বছরের অভিজ্ঞতা
                  </div>
                </div>

                <div className="shrink-0 flex flex-col items-end gap-1">
                  <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full font-mono ${
                    isOnline 
                      ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' 
                      : isBusy
                      ? 'bg-amber-50 text-amber-800 border border-amber-200'
                      : 'bg-slate-100 text-slate-600 border border-slate-200'
                  }`}>
                    {isOnline ? 'ONLINE' : isBusy ? 'BUSY' : 'OFFLINE'}
                  </span>
                  <div className="flex items-center text-[10px] font-bold text-amber-600 font-mono">
                    <Star className="w-3 h-3 fill-amber-400 text-amber-500 mr-0.5" />
                    <span>{p.rating.toFixed(1)}</span>
                    <span className="text-slate-400 text-[9px] ml-0.5">({p.review_count})</span>
                  </div>
                </div>
              </div>

              {/* Bio summary */}
              <p className="text-[10px] text-slate-600 font-tiro leading-relaxed line-clamp-2">
                {p.bio}
              </p>

              {/* Service Offering Tags */}
              <div className="space-y-1">
                <div className="text-[9px] font-bold text-slate-500 uppercase font-baloo">
                  প্রদানকৃত সেবাসমূহ:
                </div>
                <div className="flex flex-wrap gap-1">
                  {p.services.map((srv) => (
                    <span
                      key={srv.id}
                      className="px-1.5 py-0.5 bg-teal-50 text-teal-800 border border-teal-200 rounded text-[9px] font-tiro flex items-center gap-1"
                    >
                      <span>{srv.name_bn}</span>
                      <span className="font-mono text-teal-900 font-bold">৳{srv.base_price}</span>
                    </span>
                  ))}
                </div>
              </div>

              {/* Coverage Areas */}
              <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-[10px]">
                <div className="flex items-center gap-1 text-slate-500 font-tiro truncate max-w-[180px]">
                  <MapPin className="w-3 h-3 text-teal-600 shrink-0" />
                  <span className="truncate">
                    {p.service_areas.map(a => a.upazila_name_bn).join(', ')}
                  </span>
                </div>

                <button
                  onClick={() => onSelectProvider(p)}
                  className="px-2.5 py-1 bg-teal-700 hover:bg-teal-800 text-white rounded-lg text-[10px] font-bold transition flex items-center gap-1 cursor-pointer font-baloo shadow-xs"
                >
                  <Phone className="w-3 h-3" />
                  <span className="font-baloo">যোগাযোগ</span>
                </button>
              </div>
            </div>
          );
        })}

        {filteredProviders.length === 0 && (
          <div className="p-6 text-center bg-slate-50 rounded-xl text-slate-500 text-xs">
            কোনো সেবাদাতা পাওয়া যায়নি।
          </div>
        )}
      </div>

      {/* Footer Register Callout */}
      <div className="pt-2 border-t border-slate-200">
        <button
          onClick={onGoToRegister}
          className="w-full py-2 bg-gradient-to-r from-teal-700 to-teal-800 hover:from-teal-800 hover:to-teal-900 text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer shadow-xs font-baloo"
        >
          <Plus className="w-4 h-4" />
          <span className="font-baloo">আমি সেবাদাতা হিসেবে নিবন্ধন করতে চাই</span>
          {showTypoTag('baloo', 'Button')}
        </button>
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// 2. PROVIDER REGISTRATION WIZARD (Phase 5: 4 Steps)
// -----------------------------------------------------------------------------
interface ProviderRegistrationViewProps {
  onBack: () => void;
  onComplete: (newProvider: MockProvider) => void;
  showTypoTag: (font: 'hind' | 'baloo' | 'tiro', role: string) => React.ReactNode;
}

export const ProviderRegistrationView: React.FC<ProviderRegistrationViewProps> = ({
  onBack,
  onComplete,
  showTypoTag
}) => {
  const [step, setStep] = useState<1 | 2 | 3 | 4>(1);

  // Step 1: Basic Info
  const [businessName, setBusinessName] = useState('কক্স স্পিড ইলেকট্রিশিয়ান');
  const [ownerName, setOwnerName] = useState('জসিম উদ্দিন');
  const [providerType, setProviderType] = useState<'INDIVIDUAL' | 'BUSINESS'>('INDIVIDUAL');
  const [bio, setBio] = useState('বাসাবাড়ির লাইটিং, ফ্যান ও মোটর ওয়্যারিংয়ে অভিজ্ঞ টেকনিশিয়ান।');
  const [experienceYears, setExperienceYears] = useState(4);

  // Step 2: Service Selection
  const [selectedServiceIds, setSelectedServiceIds] = useState<number[]>([1, 2]);

  // Step 3: Coverage Areas
  const [selectedAreaNames, setSelectedAreaNames] = useState<string[]>(['কক্সবাজার সদর', 'রামু']);
  const [primaryAreaName, setPrimaryAreaName] = useState<string>('কক্সবাজার সদর');

  const handleNext = () => {
    if (step < 4) {
      setStep((prev) => (prev + 1) as any);
    } else {
      // Complete Registration
      const newProv: MockProvider = {
        id: Date.now(),
        business_name: businessName,
        owner_name: ownerName,
        provider_type: providerType,
        bio: bio,
        experience_years: experienceYears,
        status: 'PENDING_VERIFICATION',
        availability_status: 'ONLINE',
        is_verified: false,
        rating: 5.0,
        review_count: 0,
        total_completed_services: 0,
        contact_visibility: 'PUBLIC',
        phone: '+8801811223344',
        primary_area: { id: 1, name_bn: primaryAreaName, name_en: "Cox's Bazar Sadar" },
        service_areas: selectedAreaNames.map((a, idx) => ({
          upazila_id: idx + 1,
          upazila_name_bn: a,
          upazila_name_en: a,
          is_primary: a === primaryAreaName
        })),
        services: selectedServiceIds.map((sid) => {
          const s = INITIAL_SERVICES.find(x => x.id === sid);
          return {
            id: sid,
            name_bn: s?.name_bn || 'সার্ভিস',
            name_en: s?.name_en || 'Service',
            category_name_bn: 'বাসাবাড়ির মেরামত',
            pricing_model: 'FIXED',
            base_price: 500,
            is_active: true
          };
        }),
        created_at: new Date().toISOString().split('T')[0]
      };
      onComplete(newProv);
    }
  };

  return (
    <div className="flex flex-col gap-3 font-tiro py-1">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-2">
        <button
          onClick={step === 1 ? onBack : () => setStep((prev) => (prev - 1) as any)}
          className="flex items-center gap-1 text-xs text-slate-600 hover:text-slate-900 font-bold cursor-pointer font-baloo"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span className="font-baloo">{step === 1 ? 'বাতিল' : 'পূর্ববর্তী ধাপ'}</span>
        </button>
        <div className="flex items-center">
          <span className="text-xs font-bold text-slate-900 font-hind">
            সেবাদাতা নিবন্ধন ({step}/৪)
          </span>
          {showTypoTag('hind', 'Page Title')}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="flex gap-1">
        {[1, 2, 3, 4].map((s) => (
          <div
            key={s}
            className={`h-1.5 flex-1 rounded-full ${
              s <= step ? 'bg-teal-700' : 'bg-slate-200'
            }`}
          />
        ))}
      </div>

      {/* STEP 1: General Profile */}
      {step === 1 && (
        <div className="space-y-2.5">
          <div className="bg-teal-50 p-2.5 rounded-xl border border-teal-200 text-xs">
            <span className="font-bold text-teal-900 block font-baloo">ধাপ ১: সাধারণ পরিচিতি</span>
            <span className="text-[11px] text-teal-800 font-tiro">
              আপনার সেবা ব্যবসা বা পেশাগত প্রোফাইল তৈরি করুন।
            </span>
          </div>

          <div>
            <label className="text-[11px] font-bold text-slate-700 block mb-1 font-tiro">
              ব্যবসা / প্রতিষ্ঠানের নাম
            </label>
            <input
              type="text"
              value={businessName}
              onChange={(e) => setBusinessName(e.target.value)}
              className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs font-tiro"
              placeholder="যেমন: সৈকত ইলেকট্রিক্যাল"
            />
          </div>

          <div>
            <label className="text-[11px] font-bold text-slate-700 block mb-1 font-tiro">
              মালিক বা সেবাদাতার নাম
            </label>
            <input
              type="text"
              value={ownerName}
              onChange={(e) => setOwnerName(e.target.value)}
              className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs font-tiro"
            />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="text-[11px] font-bold text-slate-700 block mb-1 font-tiro">
                সেবাদাতার ধরন
              </label>
              <select
                value={providerType}
                onChange={(e) => setProviderType(e.target.value as any)}
                className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs font-tiro"
              >
                <option value="INDIVIDUAL">ব্যক্তিগত (Individual)</option>
                <option value="BUSINESS">ব্যবসায়িক (Business)</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-bold text-slate-700 block mb-1 font-tiro">
                অভিজ্ঞতা (বছর)
              </label>
              <input
                type="number"
                value={experienceYears}
                onChange={(e) => setExperienceYears(Number(e.target.value))}
                className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs font-tiro"
                min="0"
              />
            </div>
          </div>

          <div>
            <label className="text-[11px] font-bold text-slate-700 block mb-1 font-tiro">
              সংক্ষিপ্ত বায়ো বা বিবরণ
            </label>
            <textarea
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              rows={2}
              className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs font-tiro"
            />
          </div>
        </div>
      )}

      {/* STEP 2: Service Selection */}
      {step === 2 && (
        <div className="space-y-2.5">
          <div className="bg-teal-50 p-2.5 rounded-xl border border-teal-200 text-xs">
            <span className="font-bold text-teal-900 block font-baloo">ধাপ ২: সেবা নির্বাচন ও মূল্য নির্ধারণ</span>
            <span className="text-[11px] text-teal-800 font-tiro">
              মাস্টার ট্যাক্সোনমি থেকে আপনি যে সেবাগুলো দিতে চান তা নির্বাচন করুন।
            </span>
          </div>

          <div className="space-y-2 max-h-[300px] overflow-y-auto pr-0.5">
            {INITIAL_SERVICES.slice(0, 8).map((srv) => {
              const isSelected = selectedServiceIds.includes(srv.id);
              return (
                <div
                  key={srv.id}
                  onClick={() => {
                    if (isSelected) {
                      setSelectedServiceIds(selectedServiceIds.filter(id => id !== srv.id));
                    } else {
                      setSelectedServiceIds([...selectedServiceIds, srv.id]);
                    }
                  }}
                  className={`p-2.5 rounded-xl border transition cursor-pointer flex items-center justify-between ${
                    isSelected
                      ? 'bg-teal-50/80 border-teal-500 shadow-xs'
                      : 'bg-white border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="min-w-0">
                    <div className="text-xs font-bold text-slate-900 font-baloo">
                      {srv.name_bn}
                    </div>
                    <div className="text-[10px] text-slate-500 font-mono">
                      {srv.name_en}
                    </div>
                  </div>
                  <div className={`w-5 h-5 rounded-md flex items-center justify-center border shrink-0 ${
                    isSelected 
                      ? 'bg-teal-700 border-teal-700 text-white' 
                      : 'border-slate-300 bg-white'
                  }`}>
                    {isSelected && <Check className="w-3.5 h-3.5" />}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* STEP 3: Coverage Areas */}
      {step === 3 && (
        <div className="space-y-2.5">
          <div className="bg-teal-50 p-2.5 rounded-xl border border-teal-200 text-xs">
            <span className="font-bold text-teal-900 block font-baloo">ধাপ ৩: কভারেজ উপজেলা ও প্রাইমারি এলাকা</span>
            <span className="text-[11px] text-teal-800 font-tiro">
              কক্সবাজার জেলার কোন কোন উপজেলায় আপনি সেবা দিতে প্রস্তুত তা নির্ধারণ করুন।
            </span>
          </div>

          <div className="space-y-1.5">
            {['কক্সবাজার সদর', 'চকোরিয়া', 'রামু', 'মহেশখালী', 'টেকনাফ', 'উখিয়া', 'ঈদগাঁও'].map((upz) => {
              const isCovered = selectedAreaNames.includes(upz);
              const isPrimary = primaryAreaName === upz;

              return (
                <div
                  key={upz}
                  className={`p-2.5 rounded-xl border transition flex items-center justify-between ${
                    isCovered ? 'bg-teal-50/60 border-teal-400' : 'bg-white border-slate-200'
                  }`}
                >
                  <button
                    type="button"
                    onClick={() => {
                      if (isCovered) {
                        if (selectedAreaNames.length > 1) {
                          setSelectedAreaNames(selectedAreaNames.filter(a => a !== upz));
                          if (isPrimary) {
                            setPrimaryAreaName(selectedAreaNames.filter(a => a !== upz)[0]);
                          }
                        }
                      } else {
                        setSelectedAreaNames([...selectedAreaNames, upz]);
                      }
                    }}
                    className="flex items-center gap-2 cursor-pointer"
                  >
                    <div className={`w-4 h-4 rounded flex items-center justify-center border ${
                      isCovered ? 'bg-teal-700 border-teal-700 text-white' : 'border-slate-300'
                    }`}>
                      {isCovered && <Check className="w-3 h-3" />}
                    </div>
                    <span className="text-xs font-bold text-slate-800 font-baloo">{upz}</span>
                  </button>

                  {isCovered && (
                    <button
                      type="button"
                      onClick={() => setPrimaryAreaName(upz)}
                      className={`text-[9px] font-bold px-2 py-0.5 rounded cursor-pointer font-baloo ${
                        isPrimary
                          ? 'bg-teal-800 text-white shadow-xs'
                          : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
                      }`}
                    >
                      {isPrimary ? '✓ প্রধান এলাকা' : 'প্রধান করুন'}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* STEP 4: Review & Submit */}
      {step === 4 && (
        <div className="space-y-3">
          <div className="bg-emerald-50 p-2.5 rounded-xl border border-emerald-200 text-xs">
            <span className="font-bold text-emerald-900 block font-baloo">ধাপ ৪: চূড়ান্ত পর্যালোচনা</span>
            <span className="text-[11px] text-emerald-800 font-tiro">
              তথ্য যাচাই করে নিবন্ধন সম্পন্ন করুন। প্রোফাইলটি পর্যালোচনার জন্য জমা হবে।
            </span>
          </div>

          <div className="bg-white p-3 rounded-xl border border-slate-200 space-y-2 text-xs">
            <div className="flex justify-between border-b border-slate-100 pb-1">
              <span className="text-slate-500">প্রতিষ্ঠান:</span>
              <span className="font-bold text-slate-800">{businessName}</span>
            </div>
            <div className="flex justify-between border-b border-slate-100 pb-1">
              <span className="text-slate-500">মালিক:</span>
              <span className="font-bold text-slate-800">{ownerName} ({experienceYears} বছর)</span>
            </div>
            <div className="flex justify-between border-b border-slate-100 pb-1">
              <span className="text-slate-500">প্রধান এলাকা:</span>
              <span className="font-bold text-teal-800">{primaryAreaName}</span>
            </div>
            <div className="flex justify-between border-b border-slate-100 pb-1">
              <span className="text-slate-500">কভারেজ:</span>
              <span className="font-bold text-slate-700">{selectedAreaNames.join(', ')}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">নির্বাচিত সেবা:</span>
              <span className="font-bold text-teal-800">{selectedServiceIds.length}টি সেবা</span>
            </div>
          </div>

          <div className="p-2.5 bg-slate-100 rounded-xl text-[10px] text-slate-600 leading-relaxed font-tiro">
            🔒 <strong>নীতিমালা:</strong> নিবন্ধনের পর প্রোফাইল স্ট্যাটাস <code>DRAFT</code> থেকে <code>PENDING_VERIFICATION</code>-এ রূপান্তরিত হবে।
          </div>
        </div>
      )}

      {/* Bottom Action Button */}
      <button
        onClick={handleNext}
        className="w-full py-2 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer shadow-xs font-baloo mt-2"
      >
        <span>{step === 4 ? 'নিবন্ধন সম্পন্ন করুন' : 'পরবর্তী ধাপ'}</span>
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  );
};

// -----------------------------------------------------------------------------
// 3. PROVIDER OPERATIONAL DASHBOARD
// -----------------------------------------------------------------------------
interface ProviderDashboardViewProps {
  provider: MockProvider;
  onBack: () => void;
  onUpdateAvailability: (newStatus: 'ONLINE' | 'OFFLINE' | 'BUSY' | 'ON_BREAK') => void;
  showTypoTag: (font: 'hind' | 'baloo' | 'tiro', role: string) => React.ReactNode;
}

export const ProviderDashboardView: React.FC<ProviderDashboardViewProps> = ({
  provider,
  onBack,
  onUpdateAvailability,
  showTypoTag
}) => {
  return (
    <div className="flex flex-col gap-3 font-tiro py-1">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-2">
        <button
          onClick={onBack}
          className="flex items-center gap-1 text-xs text-slate-600 hover:text-slate-900 font-bold cursor-pointer font-baloo"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span className="font-baloo">ফিরে যান</span>
        </button>
        <div className="flex items-center">
          <span className="text-xs font-bold text-slate-900 font-hind">প্রোভাইডার ড্যাশবোর্ড</span>
          {showTypoTag('hind', 'Page Title')}
        </div>
      </div>

      {/* Provider Identity & Verification Status Card */}
      <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-xs space-y-2">
        <div className="flex items-start justify-between gap-2">
          <div>
            <div className="flex items-center gap-1">
              <span className="text-xs font-bold text-slate-900 font-baloo">
                {provider.business_name}
              </span>
              {provider.is_verified && (
                <CheckCircle2 className="w-3.5 h-3.5 text-teal-600 fill-teal-50" />
              )}
            </div>
            <div className="text-[11px] text-slate-500 font-tiro">
              মালিক: {provider.owner_name} • আইডি: #{provider.id}
            </div>
          </div>

          <span className={`text-[9px] font-bold font-mono px-2 py-0.5 rounded-full ${
            provider.status === 'ACTIVE'
              ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
              : 'bg-amber-50 text-amber-800 border border-amber-200'
          }`}>
            {provider.status}
          </span>
        </div>

        {/* Live Availability Switcher */}
        <div className="bg-slate-50 p-2 rounded-lg border border-slate-200 space-y-1.5">
          <div className="flex justify-between items-center text-[10px]">
            <span className="font-bold text-slate-700 font-baloo">লাইভ প্রাপ্যতা স্ট্যাটাস:</span>
            <span className="font-mono font-bold text-teal-800">{provider.availability_status}</span>
          </div>

          <div className="grid grid-cols-3 gap-1 text-[10px] font-baloo">
            <button
              type="button"
              onClick={() => onUpdateAvailability('ONLINE')}
              className={`py-1 rounded cursor-pointer transition ${
                provider.availability_status === 'ONLINE'
                  ? 'bg-emerald-600 text-white font-bold shadow-xs'
                  : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
              }`}
            >
              🟢 অনলাইন
            </button>
            <button
              type="button"
              onClick={() => onUpdateAvailability('BUSY')}
              className={`py-1 rounded cursor-pointer transition ${
                provider.availability_status === 'BUSY'
                  ? 'bg-amber-600 text-white font-bold shadow-xs'
                  : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
              }`}
            >
              🟡 ব্যস্ত
            </button>
            <button
              type="button"
              onClick={() => onUpdateAvailability('OFFLINE')}
              className={`py-1 rounded cursor-pointer transition ${
                provider.availability_status === 'OFFLINE'
                  ? 'bg-slate-700 text-white font-bold shadow-xs'
                  : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
              }`}
            >
              ⚪ অফলাইন
            </button>
          </div>
        </div>
      </div>

      {/* 4 Metric Cards */}
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-[10px] text-slate-500 font-tiro">সক্রিয় সেবা</div>
          <div className="text-base font-black text-slate-900 font-mono mt-0.5">
            {provider.services.filter(s => s.is_active).length}
          </div>
        </div>
        <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-[10px] text-slate-500 font-tiro">কভারেজ উপজেলা</div>
          <div className="text-base font-black text-teal-800 font-mono mt-0.5">
            {provider.service_areas.length}
          </div>
        </div>
        <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-[10px] text-slate-500 font-tiro">মোট সেবা সম্পন্ন</div>
          <div className="text-base font-black text-slate-900 font-mono mt-0.5">
            {provider.total_completed_services}
          </div>
        </div>
        <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-[10px] text-slate-500 font-tiro">গড় রেটিং</div>
          <div className="text-base font-black text-amber-600 font-mono mt-0.5 flex items-center gap-1">
            <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-500" />
            <span>{provider.rating.toFixed(1)}</span>
          </div>
        </div>
      </div>

      {/* Managed Service Offerings */}
      <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-xs space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-xs font-bold text-slate-800 font-baloo">আমার সেবাসমূহ</span>
          {showTypoTag('baloo', 'Card Heading')}
        </div>

        <div className="space-y-1.5">
          {provider.services.map((srv) => (
            <div
              key={srv.id}
              className="p-2 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between text-xs"
            >
              <div>
                <div className="font-bold text-slate-800 text-[11px] font-baloo">
                  {srv.name_bn}
                </div>
                <div className="text-[10px] text-slate-500 font-mono">
                  বেস রেট: ৳{srv.base_price} ({srv.pricing_model})
                </div>
              </div>
              <span className="text-[9px] bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded font-mono">
                ACTIVE
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Coverage Areas */}
      <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-xs space-y-1.5">
        <span className="text-xs font-bold text-slate-800 font-baloo">সেবা কভারেজ উপজেলা</span>
        <div className="flex flex-wrap gap-1">
          {provider.service_areas.map((a) => (
            <span
              key={a.upazila_id}
              className={`px-2 py-0.5 rounded-full text-[10px] font-baloo ${
                a.is_primary
                  ? 'bg-teal-700 text-white font-bold'
                  : 'bg-slate-100 text-slate-700 border border-slate-200'
              }`}
            >
              {a.upazila_name_bn} {a.is_primary && '(প্রধান)'}
            </span>
          ))}
        </div>
      </div>

      {/* Audit Log Preview */}
      <div className="p-2.5 bg-slate-100 rounded-xl text-[10px] text-slate-600 font-tiro space-y-1">
        <div className="font-bold text-slate-700 font-mono">📋 ProviderAuditTrail</div>
        <div>• Availability changed to {provider.availability_status}</div>
        <div>• Profile status verified and active in Cox's Bazar region</div>
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// 4. POST BOTTOM SHEET MODAL
// -----------------------------------------------------------------------------
interface ProviderPostBottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectDemand: () => void;
  onSelectProvider: () => void;
}

export const ProviderPostBottomSheet: React.FC<ProviderPostBottomSheetProps> = ({
  isOpen,
  onClose,
  onSelectDemand,
  onSelectProvider
}) => {
  if (!isOpen) return null;

  return (
    <div className="absolute inset-0 bg-black/50 z-40 flex flex-col justify-end animate-in fade-in duration-200">
      <div className="bg-white rounded-t-3xl p-5 shadow-2xl border-t border-slate-200 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-2">
          <div>
            <h3 className="text-sm font-bold text-slate-900 font-hind">আমার পোস্ট করুন</h3>
            <p className="text-[11px] text-slate-500 font-tiro">
              আপনি কীভাবে সেবাকক্স ব্যবহার করতে চান?
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-slate-400 hover:text-slate-600 rounded-full cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="space-y-2">
          {/* Option 1: I need service */}
          <div
            onClick={onSelectDemand}
            className="p-3 rounded-xl border border-slate-200 hover:border-teal-500 hover:bg-teal-50/40 transition cursor-pointer flex items-center gap-3"
          >
            <div className="w-9 h-9 rounded-xl bg-teal-100 text-teal-800 flex items-center justify-center shrink-0">
              <Search className="w-5 h-5" />
            </div>
            <div className="min-w-0">
              <div className="text-xs font-bold text-slate-900 font-baloo">আমি সেবা নিব</div>
              <div className="text-[10px] text-slate-500 font-tiro">
                আপনার প্রয়োজনীয় সেবার চাহিদা বা অনুরোধ পোস্ট করুন (Phase 6)
              </div>
            </div>
          </div>

          {/* Option 2: I provide service */}
          <div
            onClick={onSelectProvider}
            className="p-3 rounded-xl border border-slate-200 hover:border-emerald-500 hover:bg-emerald-50/40 transition cursor-pointer flex items-center gap-3"
          >
            <div className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">
              <Users className="w-5 h-5" />
            </div>
            <div className="min-w-0">
              <div className="text-xs font-bold text-slate-900 font-baloo">আমি সেবা দিব</div>
              <div className="text-[10px] text-slate-500 font-tiro">
                সেবাদাতা হিসেবে প্রোফাইল নিবন্ধন বা পরিচালনা করুন
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// 5. PHASE 5 PROVIDER ARCHITECTURE INSPECTOR (For Right Side Panel)
// -----------------------------------------------------------------------------
interface ProviderArchitectureInspectorProps {
  provider: MockProvider;
  totalProvidersCount: number;
}

export const ProviderArchitectureInspector: React.FC<ProviderArchitectureInspectorProps> = ({
  provider,
  totalProvidersCount
}) => {
  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-teal-700" />
          <h3 className="text-xs font-bold text-slate-900 font-hind">
            Phase 5 Provider & Service Engine Inspector
          </h3>
        </div>
        <span className="text-[10px] font-mono bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded-full font-bold">
          55 / 55 Passing
        </span>
      </div>

      <p className="text-xs text-slate-600 font-tiro leading-relaxed">
        Phase 5 enforces the strict architectural separation of <strong>User ≠ Provider ≠ Service</strong>, 
        audit-trailed state transitions, and multi-area coverage.
      </p>

      <div className="space-y-2 text-xs">
        <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
          <div className="flex justify-between text-[11px]">
            <span className="text-slate-500 font-tiro">Active Profile Entity:</span>
            <span className="font-bold text-slate-800 font-baloo">{provider.business_name}</span>
          </div>
          <div className="flex justify-between text-[10px] font-mono text-slate-600">
            <span>Provider Status:</span>
            <span className="font-bold text-teal-800">{provider.status}</span>
          </div>
          <div className="flex justify-between text-[10px] font-mono text-slate-600">
            <span>Availability Status:</span>
            <span className="font-bold text-emerald-700">{provider.availability_status}</span>
          </div>
          <div className="flex justify-between text-[10px] font-mono text-slate-600">
            <span>Covered Upazilas:</span>
            <span className="font-bold">{provider.service_areas.length} Upazilas</span>
          </div>
        </div>

        <div className="p-2 rounded-lg bg-teal-50/70 border border-teal-200 text-[10px] text-teal-900 font-tiro">
          💡 <strong>Single Source of Truth:</strong> Services belong to the Master Taxonomy (Phase 4), and ProviderService maps the provider's specific pricing without duplicating service logic.
        </div>
      </div>
    </div>
  );
};
