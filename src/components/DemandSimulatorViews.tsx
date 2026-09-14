import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Search, 
  MapPin, 
  Tag, 
  Clock, 
  CheckCircle2, 
  PauseCircle, 
  PlayCircle, 
  XCircle, 
  Lock, 
  AlertCircle, 
  DollarSign, 
  Calendar, 
  User, 
  Phone, 
  ShieldCheck, 
  ExternalLink, 
  ChevronRight, 
  ChevronDown,
  Filter, 
  Check, 
  X, 
  ArrowLeft,
  HandCoins,
  ArrowRightLeft,
  History,
  FileText,
  Building2,
  Layers,
  Sparkles,
  HelpCircle,
  AlertTriangle,
  Info
} from 'lucide-react';
import { MockDemand, INITIAL_MOCK_DEMANDS } from '../data/demandMockData';
import { MockOffer, INITIAL_MOCK_OFFERS } from '../data/offerMockData';
import { APP_BRAND } from '../constants/brand';
import { MasterCategory, SEBACOX_MASTER_CATEGORIES } from '../data/categoryMasterData';
import { 
  COX_UPAZILAS, 
  COX_POSTAL_LOCATIONS, 
  COX_UNIONS, 
  COX_WARDS, 
  COX_LOCALITIES 
} from '../data/coxSadarAddressMasterData';

interface DemandSimulatorProps {
  demands?: MockDemand[];
  onAddDemand?: (newDemand: Partial<MockDemand>, publishNow: boolean) => void;
  onStatusChange?: (demandId: number, newStatus: MockDemand['status']) => void;
  onBack?: () => void;
  showTypoTag?: (font: 'hind' | 'baloo' | 'tiro', role: string) => React.ReactNode;
}

export const DemandStatusBadge: React.FC<{ status: MockDemand['status']; compact?: boolean }> = ({ status, compact = false }) => {
  const configs = {
    DRAFT: { label: 'খসড়া', bg: 'bg-slate-100', text: 'text-slate-700', border: 'border-slate-300' },
    PUBLISHED: { label: 'প্রকাশিত', bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
    PAUSED: { label: 'সাময়িক বন্ধ', bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
    FULFILLED: { label: 'পূরণ হয়েছে', bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
    CANCELLED: { label: 'বাতিল', bg: 'bg-rose-50', text: 'text-rose-700', border: 'border-rose-200' },
    EXPIRED: { label: 'মেয়াদ শেষ', bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-200' },
    CLOSED: { label: 'স্থায়ী বন্ধ', bg: 'bg-slate-100', text: 'text-slate-500', border: 'border-slate-200' },
  };

  const c = configs[status] || configs.DRAFT;
  return (
    <span className={`inline-flex items-center gap-1 font-semibold rounded-full border ${c.bg} ${c.text} ${c.border} ${compact ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs'}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current opacity-80" />
      <span>{c.label}</span>
    </span>
  );
};

export const OfferStatusBadge: React.FC<{ status: MockOffer['status']; version?: number; compact?: boolean }> = ({ status, version, compact = false }) => {
  const configs = {
    DRAFT: { label: 'খসড়া', bg: 'bg-slate-100', text: 'text-slate-700', border: 'border-slate-300' },
    PENDING: { label: 'বিবেচনাধীন', bg: 'bg-amber-50', text: 'text-amber-800', border: 'border-amber-300' },
    ACCEPTED: { label: 'গৃহীত', bg: 'bg-emerald-50', text: 'text-emerald-800', border: 'border-emerald-300' },
    REJECTED: { label: 'প্রত্যাখ্যাত', bg: 'bg-rose-50', text: 'text-rose-800', border: 'border-rose-300' },
    CANCELLED: { label: 'বাতিল', bg: 'bg-slate-100', text: 'text-slate-600', border: 'border-slate-300' },
    EXPIRED: { label: 'মেয়াদোত্তীর্ণ', bg: 'bg-orange-50', text: 'text-orange-800', border: 'border-orange-300' },
    SUPERSEDED: { label: 'পাল্টা প্রস্তাবকৃত (সুপারসিডেড)', bg: 'bg-purple-50', text: 'text-purple-800', border: 'border-purple-300' },
  };

  const c = configs[status] || configs.PENDING;
  return (
    <div className="flex items-center gap-1">
      <span className={`inline-flex items-center gap-1 font-semibold rounded-full border ${c.bg} ${c.text} ${c.border} ${compact ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs'}`}>
        <span className="w-1.5 h-1.5 rounded-full bg-current opacity-80" />
        <span>{c.label}</span>
      </span>
      {version && version > 1 && (
        <span className="px-1.5 py-0.5 rounded text-[9px] font-bold font-mono bg-purple-100 text-purple-800 border border-purple-200">
          v{version}
        </span>
      )}
    </div>
  );
};

export const DemandSimulatorViews: React.FC<DemandSimulatorProps> = ({ 
  demands: externalDemands, 
  onAddDemand, 
  onStatusChange,
  onBack,
  showTypoTag
}) => {
  const [internalDemands, setInternalDemands] = useState<MockDemand[]>(INITIAL_MOCK_DEMANDS);
  const demands = (externalDemands && Array.isArray(externalDemands) && externalDemands.length > 0)
    ? externalDemands
    : internalDemands;

  const [offers, setOffers] = useState<MockOffer[]>(INITIAL_MOCK_OFFERS);
  const [activeTab, setActiveTab] = useState<'feed' | 'my_demands' | 'offers'>('feed');
  const [selectedDemand, setSelectedDemand] = useState<MockDemand | null>(null);
  const [selectedOffer, setSelectedOffer] = useState<MockOffer | null>(null);

  // Modals
  const [isWizardOpen, setIsWizardOpen] = useState<boolean>(false);
  const [isPublishConfirmOpen, setIsPublishConfirmOpen] = useState<boolean>(false);
  const [isCreateOfferOpen, setIsCreateOfferOpen] = useState<boolean>(false);
  const [isCounterOfferOpen, setIsCounterOfferOpen] = useState<boolean>(false);
  const [isRejectModalOpen, setIsRejectModalOpen] = useState<boolean>(false);

  // Search & Filter
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedUpazila, setSelectedUpazila] = useState<string>('all');
  const [urgencyFilter, setUrgencyFilter] = useState<'all' | 'urgent'>('all');

  // WIZARD FORM STATE (10-Step Architecture)
  const [wizardStep, setWizardStep] = useState<number>(1);
  const [wizardError, setWizardError] = useState<string | null>(null);

  // Step 1: Title
  const [wizTitle, setWizTitle] = useState('');
  
  // Step 2: Service Selection (২টি Dropdown)
  const [categoriesList, setCategoriesList] = useState<MasterCategory[]>(SEBACOX_MASTER_CATEGORIES);
  const [isLoadingCategories, setIsLoadingCategories] = useState<boolean>(false);
  const [wizCategoryId, setWizCategoryId] = useState<number | null>(null);
  const [wizCategoryNameBn, setWizCategoryNameBn] = useState<string | null>(null);
  const [wizServiceId, setWizServiceId] = useState<number | null>(null);
  const [wizServiceNameBn, setWizServiceNameBn] = useState<string | null>(null);

  // Step 3: Description
  const [wizDescription, setWizDescription] = useState('');

  // Step 4: Geographic Hierarchy & Address Master
  const [wizDistrictId, setWizDistrictId] = useState(1);
  const [wizDistrictNameBn, setWizDistrictNameBn] = useState('কক্সবাজার');
  const [wizUpazilaId, setWizUpazilaId] = useState(1);
  const [wizUpazilaNameBn, setWizUpazilaNameBn] = useState('কক্সবাজার সদর');
  const [wizUnionId, setWizUnionId] = useState<number | null>(null);
  const [wizUnionNameBn, setWizUnionNameBn] = useState<string | null>(null);
  const [wizWardId, setWizWardId] = useState<number | null>(null);
  const [wizWardNameBn, setWizWardNameBn] = useState<string | null>(null);
  const [wizLocalityId, setWizLocalityId] = useState<number | null>(null);
  const [wizLocalityNameBn, setWizLocalityNameBn] = useState<string | null>(null);
  const [availableLocalities, setAvailableLocalities] = useState<Array<{ id: number; nameBn: string; type: string }>>([]);
  const [isLoadingLocalities, setIsLoadingLocalities] = useState<boolean>(false);
  const [wizPostalLocationId, setWizPostalLocationId] = useState<number | null>(null);
  const [wizPostalLocationNameBn, setWizPostalLocationNameBn] = useState<string | null>(null);
  const [wizPostCode, setWizPostCode] = useState<string>('4700');
  const [wizDetailedAddress, setWizDetailedAddress] = useState('');

  // Step 5: Schedule / Timing
  const [wizScheduleType, setWizScheduleType] = useState<'ASAP' | 'DATE' | 'DATE_TIME'>('ASAP');
  const [wizDate, setWizDate] = useState('');
  const [wizTime, setWizTime] = useState('');

  // Step 6: Quantity & Budget
  const [wizQuantity, setWizQuantity] = useState('');
  const [wizUnit, setWizUnit] = useState('টি');
  const [wizBudgetMin, setWizBudgetMin] = useState('800');
  const [wizBudgetMax, setWizBudgetMax] = useState('1500');

  // Step 7: Contact Preference
  const [wizContactPref, setWizContactPref] = useState<MockDemand['contactPreference']>('IN_APP_ONLY');

  // Step 8: Visibility & Priority
  const [wizVisibility, setWizVisibility] = useState<MockDemand['visibility']>('PUBLIC');
  const [wizPriority, setWizPriority] = useState<MockDemand['priority']>('NORMAL');
  const [wizDemandType, setWizDemandType] = useState<MockDemand['demandType']>('SERVICE');

  // Offer Creation State
  const [offerPrice, setOfferPrice] = useState<string>('1200');
  const [offerDeliveryFee, setOfferDeliveryFee] = useState<string>('100');
  const [offerServiceFee, setOfferServiceFee] = useState<string>('50');
  const [offerTerms, setOfferTerms] = useState<string>('সব প্রয়োজনীয় সরঞ্জামসহ সময়মতো সমাধান প্রদান করা হবে।');
  const [offerDuration, setOfferDuration] = useState<string>('২ ঘণ্টা');
  const [offerExpiryDays, setOfferExpiryDays] = useState<number>(3);

  // Counter Offer State
  const [counterTargetOffer, setCounterTargetOffer] = useState<MockOffer | null>(null);
  const [counterPrice, setCounterPrice] = useState<string>('');
  const [counterDeliveryFee, setCounterDeliveryFee] = useState<string>('');
  const [counterServiceFee, setCounterServiceFee] = useState<string>('');
  const [counterTerms, setCounterTerms] = useState<string>('');
  const [counterDuration, setCounterDuration] = useState<string>('');

  // Rejection State
  const [rejectReason, setRejectReason] = useState<string>('');

  // Fetch Master Categories & Subcategories dynamically
  useEffect(() => {
    let isMounted = true;
    setIsLoadingCategories(true);
    fetch('/api/v1/categories?include_inactive=false')
      .then((res) => res.json())
      .then((json) => {
        if (!isMounted) return;
        if (json && json.success && Array.isArray(json.data) && json.data.length > 0) {
          setCategoriesList(json.data);
        }
      })
      .catch(() => {
        // Fallback already preloaded with SEBACOX_MASTER_CATEGORIES
      })
      .finally(() => {
        if (isMounted) setIsLoadingCategories(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  // Dynamic Locality Fetching with fallback
  useEffect(() => {
    let isMounted = true;
    if (!wizWardId) {
      setAvailableLocalities([]);
      return;
    }

    setIsLoadingLocalities(true);
    const fetchUrl = `/api/v1/locations/localities?ward_id=${wizWardId}${wizUnionId ? `&union_id=${wizUnionId}` : ''}`;
    
    fetch(fetchUrl)
      .then(res => res.json())
      .then(json => {
        if (!isMounted) return;
        if (json && json.success && Array.isArray(json.data) && json.data.length > 0) {
          const mapped = json.data
            .filter((l: any) => l.is_active !== false && l.verification_status !== 'NEEDS_REVIEW')
            .map((l: any) => {
              const rawType = l.locality_type || l.source_type || 'PARA';
              const typeMap: Record<string, string> = {
                'PARA': 'পাড়া',
                'MOHOLLA': 'মহল্লা',
                'VILLAGE': 'গ্রাম',
                'BAZAR': 'বাজার',
                'RESIDENTIAL': 'আবাসিক এলাকা',
                'LOCAL_AREA': 'লোকাল এলাকা',
              };
              return {
                id: l.id,
                nameBn: l.name_bn,
                type: typeMap[rawType] || 'এলাকা'
              };
            });
          setAvailableLocalities(mapped);
        } else {
          // Fallback to verified local constant
          const fallback = COX_LOCALITIES[wizWardId] || [];
          setAvailableLocalities(fallback);
        }
      })
      .catch(() => {
        if (!isMounted) return;
        const fallback = COX_LOCALITIES[wizWardId] || [];
        setAvailableLocalities(fallback);
      })
      .finally(() => {
        if (isMounted) setIsLoadingLocalities(false);
      });

    return () => {
      isMounted = false;
    };
  }, [wizWardId, wizUnionId]);

  const handleStatusChange = (demandId: number, newStatus: MockDemand['status']) => {
    if (onStatusChange) {
      onStatusChange(demandId, newStatus);
    } else {
      setInternalDemands(prev => prev.map(d => d.id === demandId ? { ...d, status: newStatus } : d));
    }
    if (selectedDemand && selectedDemand.id === demandId) {
      setSelectedDemand({ ...selectedDemand, status: newStatus });
    }
  };

  // WIZARD STEP VALIDATION
  const validateStep = (step: number): boolean => {
    setWizardError(null);
    if (step === 1) {
      if (!wizTitle.trim()) {
        setWizardError('প্রয়োজনের শিরোনাম লিখুন।');
        return false;
      }
      if (wizTitle.trim().length < 5) {
        setWizardError('শিরোনাম কমপক্ষে ৫ অক্ষরের হতে হবে।');
        return false;
      }
      return true;
    }
    if (step === 2) {
      if (!wizCategoryId) {
        setWizardError('অনুগ্রহ করে প্রধান ক্যাটাগরি নির্বাচন করুন।');
        return false;
      }
      if (!wizServiceId) {
        setWizardError('অনুগ্রহ করে সাব-ক্যাটাগরি নির্বাচন করুন।');
        return false;
      }
      return true;
    }
    if (step === 3) {
      if (!wizDescription.trim()) {
        setWizardError('আপনার প্রয়োজনের বিস্তারিত বিবরণ লিখুন।');
        return false;
      }
      if (wizDescription.trim().length < 10) {
        setWizardError('বিবরণ কমপক্ষে ১০ অক্ষরের হতে হবে।');
        return false;
      }
      return true;
    }
    if (step === 4) {
      if (!wizUpazilaId) {
        setWizardError('উপজেলা নির্বাচন করা আবশ্যক।');
        return false;
      }
      return true;
    }
    if (step === 5) {
      if (wizScheduleType === 'DATE' && !wizDate) {
        setWizardError('অনুগ্রহ করে নির্দিষ্ট তারিখ নির্বাচন করুন।');
        return false;
      }
      if (wizScheduleType === 'DATE_TIME' && (!wizDate || !wizTime)) {
        setWizardError('অনুগ্রহ করে নির্দিষ্ট তারিখ ও সময় লিখুন।');
        return false;
      }
      return true;
    }
    if (step === 6) {
      if (wizBudgetMin && wizBudgetMax) {
        const min = Number(wizBudgetMin);
        const max = Number(wizBudgetMax);
        if (min < 0 || max < 0) {
          setWizardError('বাজেটের মান ঋণাত্মক হতে পারে না।');
          return false;
        }
        if (min > max) {
          setWizardError('সর্বনিম্ন বাজেট সর্বোচ্চ বাজেটের চেয়ে বেশি হতে পারবে না।');
          return false;
        }
      }
      return true;
    }
    return true;
  };

  const nextWizardStep = () => {
    if (validateStep(wizardStep)) {
      if (wizardStep < 9) {
        setWizardStep(prev => prev + 1);
      }
    }
  };

  const prevWizardStep = () => {
    setWizardError(null);
    if (wizardStep > 1) {
      setWizardStep(prev => prev - 1);
    } else {
      setIsWizardOpen(false);
    }
  };

  const handleFinalSubmit = (publishNow: boolean) => {
    const locParts = [];
    if (wizLocalityNameBn) locParts.push(wizLocalityNameBn);
    if (wizWardNameBn) locParts.push(wizWardNameBn);
    if (wizUnionNameBn) locParts.push(wizUnionNameBn);
    locParts.push(wizUpazilaNameBn);
    locParts.push(wizDistrictNameBn);
    const generatedLoc = locParts.join(', ');

    const newDemand: Partial<MockDemand> = {
      id: Date.now(),
      requesterId: 1,
      requesterName: 'মোহাম্মদ করিম (বর্তমান ব্যবহারকারী)',
      contactPhone: '+8801819234567',
      titleBn: wizTitle.trim(),
      titleEn: wizTitle.trim(),
      descriptionBn: wizDescription.trim(),
      descriptionEn: wizDescription.trim(),
      demandType: wizDemandType,
      priority: wizPriority,
      status: publishNow ? 'PUBLISHED' : 'DRAFT',
      serviceId: wizServiceId || undefined,
      serviceNameBn: wizServiceNameBn || undefined,
      categoryId: wizCategoryId || undefined,
      categoryNameBn: wizCategoryNameBn || undefined,
      quantity: wizQuantity ? Number(wizQuantity) : undefined,
      unit: wizUnit || undefined,
      budgetMin: wizBudgetMin ? Number(wizBudgetMin) : undefined,
      budgetMax: wizBudgetMax ? Number(wizBudgetMax) : undefined,
      currency: 'BDT',
      upazilaId: wizUpazilaId,
      upazilaNameBn: wizUpazilaNameBn,
      locationDisplayBn: wizDetailedAddress.trim() || generatedLoc,
      visibility: wizVisibility,
      contactPreference: wizContactPref,
      isOwner: true,
      publishedAt: publishNow ? new Date().toISOString() : undefined,
      createdAt: new Date().toISOString(),
    };

    if (onAddDemand) {
      onAddDemand(newDemand, publishNow);
    } else {
      setInternalDemands(prev => [newDemand as MockDemand, ...prev]);
    }

    setIsPublishConfirmOpen(false);
    setIsWizardOpen(false);
    // Reset form
    setWizardStep(1);
    setWizTitle('');
    setWizDescription('');
    setWizServiceId(null);
    setWizServiceNameBn(null);
  };

  // ACCEPT OFFER HANDLER
  const handleAcceptOffer = (offerId: number) => {
    setOffers(prev => prev.map(o => {
      if (o.id === offerId) {
        return { ...o, status: 'ACCEPTED' as const };
      }
      if (selectedDemand && o.demandId === selectedDemand.id && o.id !== offerId) {
        return { ...o, status: 'REJECTED' as const, rejectionReason: 'অন্য একটি প্রস্তাব গৃহীত হয়েছে।' };
      }
      return o;
    }));

    if (selectedDemand) {
      handleStatusChange(selectedDemand.id, 'FULFILLED');
    }
  };

  // REJECT OFFER HANDLER
  const handleRejectOffer = (offerId: number) => {
    setOffers(prev => prev.map(o => {
      if (o.id === offerId) {
        return {
          ...o,
          status: 'REJECTED' as const,
          rejectionReason: rejectReason || 'মূল্য বা শর্তাবলী চাহিদার সাথে সঙ্গতিপূর্ণ নয়।'
        };
      }
      return o;
    }));
    setIsRejectModalOpen(false);
    setRejectReason('');
  };

  // CANCEL OFFER HANDLER
  const handleCancelOffer = (offerId: number) => {
    setOffers(prev => prev.map(o => o.id === offerId ? { ...o, status: 'CANCELLED' as const } : o));
  };

  // COUNTER OFFER SUBMIT HANDLER
  const handleCounterOfferSubmit = () => {
    if (!counterTargetOffer) return;
    const p = Number(counterPrice) || counterTargetOffer.offeredPrice;
    const d = Number(counterDeliveryFee) || counterTargetOffer.deliveryFee;
    const s = Number(counterServiceFee) || counterTargetOffer.serviceFee;

    setOffers(prev => prev.map(o => {
      if (o.id === counterTargetOffer.id) {
        return { ...o, status: 'SUPERSEDED' as const };
      }
      return o;
    }));

    const newOffer: MockOffer = {
      id: Date.now(),
      demandId: counterTargetOffer.demandId,
      demandTitleBn: counterTargetOffer.demandTitleBn,
      providerId: counterTargetOffer.providerId,
      providerNameBn: counterTargetOffer.providerNameBn,
      proposerId: 1,
      proposerName: 'মোহাম্মদ করিম (চাহিদা প্রদানকারী)',
      proposerRole: 'REQUESTER',
      recipientId: counterTargetOffer.proposerId,
      recipientName: counterTargetOffer.proposerName,
      recipientRole: counterTargetOffer.proposerRole,
      offeredPrice: p,
      deliveryFee: d,
      serviceFee: s,
      totalAmount: p + d + s,
      currency: 'BDT',
      termsConditions: counterTerms || 'পাল্টা প্রস্তাবিত শর্তাবলী',
      estimatedDuration: counterDuration || counterTargetOffer.estimatedDuration,
      status: 'PENDING',
      version: (counterTargetOffer.version || 1) + 1,
      parentOfferId: counterTargetOffer.id,
      rootOfferId: counterTargetOffer.rootOfferId || counterTargetOffer.id,
      expiresAt: new Date(Date.now() + 3 * 86400000).toISOString(),
      createdAt: new Date().toISOString(),
      isProposer: true,
      isRecipient: false,
    };

    setOffers(prev => [newOffer, ...prev]);
    setIsCounterOfferOpen(false);
    setCounterTargetOffer(null);
  };

  // CREATE NEW OFFER HANDLER
  const handleCreateOfferSubmit = () => {
    if (!selectedDemand) return;
    const p = Number(offerPrice) || 1200;
    const d = Number(offerDeliveryFee) || 100;
    const s = Number(offerServiceFee) || 50;

    const newOffer: MockOffer = {
      id: Date.now(),
      demandId: selectedDemand.id,
      demandTitleBn: selectedDemand.titleBn,
      providerId: 101,
      providerNameBn: 'কক্স সার্ভিস টেকনিশিয়ান ও ইলেকট্রিক্যালস',
      proposerId: 101,
      proposerName: 'আব্দুল করিম (টেকনিশিয়ান)',
      proposerRole: 'PROVIDER',
      recipientId: selectedDemand.requesterId || 1,
      recipientName: selectedDemand.requesterName,
      recipientRole: 'REQUESTER',
      offeredPrice: p,
      deliveryFee: d,
      serviceFee: s,
      totalAmount: p + d + s,
      currency: 'BDT',
      termsConditions: offerTerms,
      estimatedDuration: offerDuration,
      status: 'PENDING',
      version: 1,
      parentOfferId: null,
      rootOfferId: Date.now(),
      expiresAt: new Date(Date.now() + offerExpiryDays * 86400000).toISOString(),
      createdAt: new Date().toISOString(),
      isProposer: true,
      isRecipient: false,
    };

    setOffers(prev => [newOffer, ...prev]);
    setIsCreateOfferOpen(false);
  };

  // Filtered demands
  const filteredDemands = demands.filter(d => {
    if (activeTab === 'my_demands' && !d.isOwner) return false;
    if (selectedUpazila !== 'all' && d.upazilaId !== Number(selectedUpazila)) return false;
    if (urgencyFilter === 'urgent' && d.priority !== 'URGENT') return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchTitle = d.titleBn.toLowerCase().includes(q) || (d.titleEn && d.titleEn.toLowerCase().includes(q));
      const matchDesc = d.descriptionBn.toLowerCase().includes(q);
      const matchLoc = d.locationDisplayBn.toLowerCase().includes(q);
      if (!matchTitle && !matchDesc && !matchLoc) return false;
    }
    return true;
  });

  const demandOffers = selectedDemand ? offers.filter(o => o.demandId === selectedDemand.id) : [];

  return (
    <div className="flex flex-col gap-3 py-1 font-tiro">
      {/* HEADER / NAVIGATION BAR */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-2">
        <div className="flex items-center gap-1.5">
          {onBack && (
            <button
              onClick={onBack}
              className="p-1 hover:bg-slate-100 rounded-lg text-slate-600 transition cursor-pointer"
              title="পিছনে যান"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
          )}
          <div>
            <div className="flex items-center gap-1.5">
              <h1 className="text-sm font-black text-slate-900 font-hind">আমার প্রয়োজন (Demand)</h1>
              {showTypoTag && showTypoTag('hind', 'App Title')}
            </div>
            <p className="text-[10px] text-teal-800 font-baloo">Phase 6 Demand Engine • SebaCox</p>
          </div>
        </div>

        {/* User Flow: আমার পোস্ট → আমি সেবা নিব → আমার প্রয়োজন → + নতুন প্রয়োজন */}
        <button
          onClick={() => {
            setWizardStep(1);
            setWizardError(null);
            setIsWizardOpen(true);
          }}
          className="flex items-center gap-1 bg-teal-700 hover:bg-teal-800 text-white px-3 py-1.5 rounded-xl text-xs font-bold font-baloo shadow-xs transition cursor-pointer"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>+ নতুন প্রয়োজন</span>
        </button>
      </div>

      {/* TABS NAVIGATION */}
      <div className="flex bg-slate-100 p-1 rounded-xl gap-1 text-xs font-baloo font-bold">
        <button
          onClick={() => setActiveTab('feed')}
          className={`flex-1 py-1.5 rounded-lg transition text-center cursor-pointer ${
            activeTab === 'feed' ? 'bg-white text-teal-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          প্রয়োজন ফিড ({demands.filter(d => d.status === 'PUBLISHED').length})
        </button>
        <button
          onClick={() => setActiveTab('my_demands')}
          className={`flex-1 py-1.5 rounded-lg transition text-center cursor-pointer ${
            activeTab === 'my_demands' ? 'bg-white text-teal-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          আমার তালিকা ({demands.filter(d => d.isOwner).length})
        </button>
        <button
          onClick={() => setActiveTab('offers')}
          className={`flex-1 py-1.5 rounded-lg transition text-center cursor-pointer flex items-center justify-center gap-1 ${
            activeTab === 'offers' ? 'bg-white text-teal-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          <span>প্রস্তাবসমূহ</span>
          <span className="px-1.5 py-0.2 rounded-full bg-teal-100 text-teal-800 text-[10px]">
            {offers.length}
          </span>
        </button>
      </div>

      {/* SEARCH & FILTERS BAR */}
      {activeTab !== 'offers' && (
        <div className="space-y-2">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="প্রয়োজন খুঁজুন (যেমন: ইট, ইলেকট্রিশিয়ান, বাসা বদল)..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 text-xs bg-white border border-slate-200 rounded-xl focus:outline-none focus:border-teal-600 font-tiro"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-2 text-slate-400 hover:text-slate-600"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          <div className="flex gap-1.5 overflow-x-auto pb-1 text-xs font-tiro scrollbar-none">
            <select
              value={selectedUpazila}
              onChange={e => setSelectedUpazila(e.target.value)}
              className="px-2.5 py-1 bg-white border border-slate-200 rounded-lg text-slate-700 text-[11px] font-medium cursor-pointer"
            >
              <option value="all">সকল উপজেলা ({COX_UPAZILAS.length})</option>
              {COX_UPAZILAS.map(u => (
                <option key={u.id} value={u.id}>{u.nameBn}</option>
              ))}
            </select>

            <button
              onClick={() => setUrgencyFilter(urgencyFilter === 'all' ? 'urgent' : 'all')}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-bold font-baloo border transition cursor-pointer flex items-center gap-1 ${
                urgencyFilter === 'urgent'
                  ? 'bg-rose-50 border-rose-300 text-rose-700'
                  : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
              <span>জরুরি মাত্র</span>
            </button>
          </div>
        </div>
      )}

      {/* DEMAND LIST VIEW (Feed & My Demands) */}
      {activeTab !== 'offers' && (
        <div className="space-y-2.5">
          {filteredDemands.length === 0 ? (
            <div className="p-8 text-center bg-white rounded-2xl border border-slate-200 space-y-2">
              <div className="text-3xl">📭</div>
              <div className="text-xs font-bold text-slate-700 font-baloo">কোনো প্রয়োজন পাওয়া যায়নি</div>
              <p className="text-[11px] text-slate-500 font-tiro">
                {activeTab === 'my_demands' 
                  ? 'আপনি এখনও কোনো প্রয়োজন তৈরি করেননি। উপরের “+ নতুন প্রয়োজন” বোতামে চাপুন।'
                  : 'বর্তমান ফিল্টারের সাথে মিলে এমন কোনো প্রকাশিত প্রয়োজন নেই।'}
              </p>
            </div>
          ) : (
            filteredDemands.map(demand => (
              <div
                key={demand.id}
                onClick={() => setSelectedDemand(demand)}
                className="p-3 bg-white border border-slate-200 hover:border-teal-400 rounded-2xl shadow-xs transition cursor-pointer space-y-2"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-1.5">
                    <DemandStatusBadge status={demand.status} compact />
                    {demand.priority === 'URGENT' && (
                      <span className="bg-rose-50 text-rose-700 border border-rose-200 px-1.5 py-0.2 rounded-full text-[9px] font-bold">
                        জরুরি
                      </span>
                    )}
                    <span className="text-[10px] text-slate-400 font-mono">#{demand.id}</span>
                  </div>
                  <div className="text-[10px] font-bold text-teal-800 font-mono">
                    {demand.budgetMin && demand.budgetMax ? `৳${demand.budgetMin} - ৳${demand.budgetMax}` : (demand.budgetMin ? `৳${demand.budgetMin}+` : 'আলোচনা সাপেক্ষে')}
                  </div>
                </div>

                <h3 className="text-xs font-bold text-slate-900 font-baloo line-clamp-1">
                  {demand.titleBn}
                </h3>

                <p className="text-[11px] text-slate-600 font-tiro line-clamp-2 leading-relaxed">
                  {demand.descriptionBn}
                </p>

                <div className="flex items-center justify-between pt-1 border-t border-slate-100 text-[10px] text-slate-500 font-tiro">
                  <div className="flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-teal-600" />
                    <span>{demand.locationDisplayBn}</span>
                  </div>
                  <div className="flex items-center gap-1 text-teal-700 font-bold font-baloo">
                    <span>বিস্তারিত দেখুন</span>
                    <ChevronRight className="w-3 h-3" />
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* OFFERS TAB VIEW */}
      {activeTab === 'offers' && (
        <div className="space-y-2.5">
          {offers.length === 0 ? (
            <div className="p-8 text-center bg-white rounded-2xl border border-slate-200 space-y-2">
              <div className="text-3xl">🤝</div>
              <div className="text-xs font-bold text-slate-700 font-baloo">কোনো প্রস্তাব নেই</div>
              <p className="text-[11px] text-slate-500 font-tiro">
                সেবাদাতারা আপনার চাহিদায় প্রস্তাব দিলে এখানে দেখতে পারবেন।
              </p>
            </div>
          ) : (
            offers.map(offer => (
              <div
                key={offer.id}
                className="p-3 bg-white border border-slate-200 rounded-2xl shadow-xs space-y-2.5 text-xs font-tiro"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-slate-900 font-baloo">{offer.demandTitleBn}</h4>
                    <p className="text-[10px] text-slate-500 font-mono">Offer #{offer.id} • {new Date(offer.createdAt).toLocaleDateString('bn-BD')}</p>
                  </div>
                  <OfferStatusBadge status={offer.status} version={offer.version} compact />
                </div>

                <div className="bg-slate-50 p-2.5 rounded-xl space-y-1">
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-500">প্রস্তাবকারী:</span>
                    <span className="font-bold text-slate-800">{offer.proposerName}</span>
                  </div>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-500">মূল্য:</span>
                    <span className="font-bold text-emerald-700 font-mono">৳{offer.offeredPrice}</span>
                  </div>
                  <div className="text-[11px] text-slate-700 pt-1 border-t border-slate-200">
                    <strong>শর্তাবলী:</strong> {offer.termsConditions}
                  </div>
                </div>

                {offer.status === 'PENDING' && (
                  <div className="flex gap-1.5 pt-1">
                    <button
                      onClick={() => handleAcceptOffer(offer.id)}
                      className="flex-1 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold font-baloo transition flex items-center justify-center gap-1 cursor-pointer"
                    >
                      <Check className="w-3.5 h-3.5" />
                      <span>গ্রহণ করুন</span>
                    </button>
                    <button
                      onClick={() => handleCancelOffer(offer.id)}
                      className="py-1.5 px-3 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-lg text-xs font-bold font-baloo transition cursor-pointer"
                    >
                      বাতিল
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* DEMAND DETAIL MODAL */}
      {selectedDemand && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-in fade-in duration-150 font-tiro">
          <div className="bg-white rounded-3xl max-w-lg w-full max-h-[90vh] overflow-y-auto p-5 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <DemandStatusBadge status={selectedDemand.status} />
                {selectedDemand.priority === 'URGENT' && (
                  <span className="bg-rose-50 text-rose-700 border border-rose-200 px-2 py-0.5 rounded-full text-[10px] font-bold">
                    জরুরি
                  </span>
                )}
              </div>
              <button
                onClick={() => setSelectedDemand(null)}
                className="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center transition cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div>
              <h2 className="text-base font-black text-slate-900 font-hind leading-snug">
                {selectedDemand.titleBn}
              </h2>
              <p className="text-[10px] text-slate-400 font-mono mt-0.5">
                Demand #{selectedDemand.id} • প্রকাশিত: {selectedDemand.publishedAt ? new Date(selectedDemand.publishedAt).toLocaleDateString('bn-BD') : 'খসড়া'}
              </p>
            </div>

            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 space-y-1">
              <div className="text-[10px] font-bold text-slate-500 font-baloo">প্রয়োজনের বিবরণ</div>
              <p className="text-xs text-slate-700 leading-relaxed font-medium">
                {selectedDemand.descriptionBn}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="border border-slate-100 bg-white p-2.5 rounded-xl shadow-2xs">
                <p className="text-[10px] text-slate-400 font-bold uppercase">স্থান / উপজেলা</p>
                <p className="font-bold text-slate-800 mt-0.5 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-teal-600" />
                  <span>{selectedDemand.locationDisplayBn}</span>
                </p>
              </div>

              <div className="border border-slate-100 bg-white p-2.5 rounded-xl shadow-2xs">
                <p className="text-[10px] text-slate-400 font-bold uppercase">বাজেট পরিসীমা</p>
                <p className="font-bold text-teal-800 mt-0.5 font-mono">
                  {selectedDemand.budgetMin && selectedDemand.budgetMax ? `৳${selectedDemand.budgetMin} - ৳${selectedDemand.budgetMax}` : (selectedDemand.budgetMin ? `৳${selectedDemand.budgetMin}+` : 'আলোচনা সাপেক্ষে')}
                </p>
              </div>
            </div>

            {/* Owner Actions */}
            {selectedDemand.isOwner && (
              <div className="pt-2 border-t border-slate-100 flex gap-2">
                {selectedDemand.status === 'PUBLISHED' && (
                  <button
                    onClick={() => handleStatusChange(selectedDemand.id, 'PAUSED')}
                    className="flex-1 py-1.5 bg-amber-50 text-amber-800 border border-amber-200 rounded-xl text-xs font-bold font-baloo cursor-pointer"
                  >
                    সাময়িক বন্ধ করুন
                  </button>
                )}
                {selectedDemand.status === 'PAUSED' && (
                  <button
                    onClick={() => handleStatusChange(selectedDemand.id, 'PUBLISHED')}
                    className="flex-1 py-1.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-xl text-xs font-bold font-baloo cursor-pointer"
                  >
                    পুনরায় চালু করুন
                  </button>
                )}
                {(selectedDemand.status === 'PUBLISHED' || selectedDemand.status === 'PAUSED') && (
                  <button
                    onClick={() => handleStatusChange(selectedDemand.id, 'CANCELLED')}
                    className="flex-1 py-1.5 bg-rose-50 text-rose-800 border border-rose-200 rounded-xl text-xs font-bold font-baloo cursor-pointer"
                  >
                    বাতিল করুন
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* 10-STEP DEMAND CREATION WIZARD MODAL */}
      {isWizardOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 font-tiro">
          <div className="bg-white rounded-3xl max-w-lg w-full max-h-[92vh] overflow-y-auto p-5 shadow-2xl border border-slate-200 flex flex-col">
            
            {/* Top Wizard Header & Breadcrumb */}
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <div>
                <div className="text-[10px] text-teal-700 font-bold font-baloo">আমার পোস্ট &gt; আমি সেবা নিব &gt; আমার প্রয়োজন</div>
                <h2 className="text-base font-black text-slate-900 font-hind">নতুন প্রয়োজন তৈরি করুন</h2>
              </div>
              <button
                onClick={() => setIsWizardOpen(false)}
                className="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center transition cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Step Indicator & Linear Progress Bar */}
            <div className="py-2.5">
              <div className="flex items-center justify-between text-xs mb-1.5 font-baloo">
                <span className="font-bold text-teal-800">ধাপ {wizardStep} / ৯</span>
                <span className="text-[11px] text-slate-500 font-tiro">প্রয়োজনীয় তথ্যগুলো ধাপে ধাপে পূরণ করুন।</span>
              </div>
              <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                <div 
                  className="bg-teal-700 h-full rounded-full transition-all duration-300"
                  style={{ width: `${(wizardStep / 9) * 100}%` }}
                />
              </div>
            </div>

            {/* Validation Error Banner */}
            {wizardError && (
              <div className="mb-3 p-2.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-semibold flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 shrink-0 text-rose-600" />
                <span>{wizardError}</span>
              </div>
            )}

            {/* STEP BODY */}
            <div className="flex-1 py-2 text-xs space-y-3">
              
              {/* STEP 1: কী প্রয়োজন? */}
              {wizardStep === 1 && (
                <div className="space-y-3">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">আপনার কী প্রয়োজন?</h3>
                    <p className="text-[11px] text-slate-500">আপনার চাহিদার একটি সংক্ষিপ্ত ও পরিষ্কার শিরোনাম লিখুন।</p>
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">প্রয়োজনের শিরোনাম *</label>
                    <input
                      type="text"
                      autoFocus
                      placeholder="e.g. ১০০০টি ইট প্রয়োজন বা অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন"
                      value={wizTitle}
                      onChange={e => setWizTitle(e.target.value)}
                      className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-teal-600 font-medium text-xs"
                    />
                  </div>

                  <div className="p-3 bg-teal-50/70 border border-teal-200 rounded-xl space-y-1">
                    <div className="flex items-center gap-1 text-teal-900 font-bold font-baloo text-xs">
                      <Sparkles className="w-3.5 h-3.5 text-teal-700" />
                      <span>টিপস ও সহজ উদাহরণ</span>
                    </div>
                    <ul className="text-[11px] text-teal-800 space-y-0.5 list-disc list-inside">
                      <li>“চকোরিয়ায় বাসা বদলের জন্য পিকআপ প্রয়োজন”</li>
                      <li>“কক্সবাজার সদরে এসি মেরামতের জন্য কারিগর প্রয়োজন”</li>
                      <li>“১০০০টি ভালো মানের প্রথম শ্রেণির ইট সরবরাহ”</li>
                    </ul>
                  </div>
                </div>
              )}

              {/* STEP 2: সেবা নির্বাচন (২টি Dropdown) */}
              {wizardStep === 2 && (
                <div className="space-y-4 font-tiro">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">কোন সেবাটি প্রয়োজন?</h3>
                    <p className="text-[11px] text-slate-500 font-tiro">
                      মাস্টার ট্যাক্সোনমি থেকে প্রধান ক্যাটাগরি ও সাব-ক্যাটাগরি নির্বাচন করুন।
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
                    {/* ১ম Dropdown — প্রধান ক্যাটাগরি */}
                    <div className="space-y-1.5">
                      <div className="flex items-center justify-between">
                        <label className="block text-xs font-bold text-slate-700 font-tiro">
                          প্রধান ক্যাটাগরি *
                        </label>
                        {isLoadingCategories && (
                          <span className="text-[10px] text-teal-600 font-medium">লোড হচ্ছে...</span>
                        )}
                        {!isLoadingCategories && categoriesList.length > 0 && (
                          <span className="text-[10px] text-slate-400 font-medium font-tiro">
                            {categoriesList.length}টি ক্যাটাগরি
                          </span>
                        )}
                      </div>
                      <div className="relative">
                        <select
                          id="demand-wizard-main-category"
                          value={wizCategoryId || ''}
                          onChange={(e) => {
                            const catId = e.target.value ? Number(e.target.value) : null;
                            setWizCategoryId(catId);
                            const found = categoriesList.find((c) => c.id === catId);
                            setWizCategoryNameBn(found ? found.nameBn : null);
                            // প্রধান ক্যাটাগরি পরিবর্তন করলে সাব-ক্যাটাগরি অবশ্যই reset হবে
                            setWizServiceId(null);
                            setWizServiceNameBn(null);
                          }}
                          className="w-full px-3 py-2.5 bg-white border border-slate-300 hover:border-teal-500 focus:border-teal-600 focus:ring-1 focus:ring-teal-600 rounded-xl text-xs font-baloo font-bold text-slate-800 shadow-xs appearance-none transition pr-8 cursor-pointer"
                        >
                          <option value="" className="text-slate-400 font-tiro font-normal">
                            -- প্রধান ক্যাটাগরি নির্বাচন করুন --
                          </option>
                          {categoriesList.map((cat) => {
                            const subCount = cat.subCategories?.length ?? (cat as any).services?.length ?? 0;
                            return (
                              <option key={cat.id} value={cat.id} className="text-slate-800 font-baloo">
                                {cat.nameBn} {subCount > 0 ? `(${subCount}টি সেবা)` : ''}
                              </option>
                            );
                          })}
                        </select>
                        <div className="absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500">
                          <ChevronDown className="w-4 h-4" />
                        </div>
                      </div>
                      <p className="text-[10px] text-slate-400 font-tiro">
                        প্রথমে আপনার প্রয়োজনীয় প্রধান ক্যাটাগরি বাছাই করুন।
                      </p>
                    </div>

                    {/* ২য় Dropdown — সাব-ক্যাটাগরি */}
                    <div className="space-y-1.5">
                      <label className="block text-xs font-bold text-slate-700 font-tiro">
                        সাব-ক্যাটাগরি *
                      </label>
                      <div className="relative">
                        <select
                          id="demand-wizard-sub-category"
                          disabled={!wizCategoryId}
                          value={wizServiceId || ''}
                          onChange={(e) => {
                            const sId = e.target.value ? Number(e.target.value) : null;
                            setWizServiceId(sId);
                            const activeCat = categoriesList.find((c) => c.id === wizCategoryId);
                            const subList = activeCat?.subCategories || (activeCat as any)?.services || [];
                            const foundSvc = subList.find((s: any) => s.id === sId);
                            setWizServiceNameBn(foundSvc ? (foundSvc.nameBn || foundSvc.name_bn) : null);
                          }}
                          className={`w-full px-3 py-2.5 border rounded-xl text-xs font-baloo font-bold shadow-xs appearance-none transition pr-8 ${
                            !wizCategoryId
                              ? 'bg-slate-100 border-slate-200 text-slate-400 cursor-not-allowed'
                              : 'bg-white border-slate-300 hover:border-teal-500 focus:border-teal-600 focus:ring-1 focus:ring-teal-600 text-slate-800 cursor-pointer'
                          }`}
                        >
                          <option value="" className="text-slate-400 font-tiro font-normal">
                            {!wizCategoryId
                              ? '-- প্রথমে প্রধান ক্যাটাগরি নির্বাচন করুন --'
                              : '-- সাব-ক্যাটাগরি নির্বাচন করুন --'}
                          </option>
                          {wizCategoryId &&
                            (categoriesList.find((c) => c.id === wizCategoryId)?.subCategories || (categoriesList.find((c) => c.id === wizCategoryId) as any)?.services || []).map((svc: any) => (
                              <option key={svc.id} value={svc.id} className="text-slate-800 font-baloo">
                                {svc.nameBn || svc.name_bn}
                              </option>
                            ))}
                        </select>
                        <div className="absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500">
                          <ChevronDown className="w-4 h-4" />
                        </div>
                      </div>
                      <p className="text-[10px] text-slate-400 font-tiro">
                        {!wizCategoryId 
                          ? 'সাব-ক্যাটাগরি দেখতে আগে প্রধান ক্যাটাগরি নির্বাচন করুন।' 
                          : 'নির্বাচিত প্রধান ক্যাটাগরির অন্তর্ভুক্ত সুনির্দিষ্ট সেবা।'}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 3: বিস্তারিত প্রয়োজন */}
              {wizardStep === 3 && (
                <div className="space-y-3">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">আপনার প্রয়োজনটি বিস্তারিত বলুন</h3>
                    <p className="text-[11px] text-slate-500">কাজের পরিধি, প্রয়োজনীয় সরঞ্জাম বা শর্তাবলী পরিষ্কারভাবে লিখুন।</p>
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 mb-1">বিস্তারিত বিবরণ *</label>
                    <textarea
                      rows={4}
                      placeholder="e.g. নির্মাণ কাজের জন্য ১০০০টি প্রথম শ্রেণির ইট প্রয়োজন। আগামীকাল দুপুরের মধ্যে সাইটে পৌঁছে দিতে হবে..."
                      value={wizDescription}
                      onChange={e => setWizDescription(e.target.value)}
                      className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-teal-600 text-xs"
                    />
                    <div className="flex justify-between items-center text-[10px] text-slate-400 mt-1">
                      <span>কমপক্ষে ১০ অক্ষর আবশ্যক</span>
                      <span>{wizDescription.length} অক্ষর</span>
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 4: কোথায় প্রয়োজন? (Cox's Bazar Sadar Address Master v1) */}
              {wizardStep === 4 && (
                <div className="space-y-3 font-tiro">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">কোথায় প্রয়োজন?</h3>
                    <p className="text-[11px] text-slate-500">কক্সবাজার সদর অ্যাড্রেস মাস্টার v1 অনুযায়ী সঠিক প্রশাসনিক ও ডাক অবস্থান নির্বাচন করুন।</p>
                  </div>

                  {/* GPS notice */}
                  <div className="p-2.5 bg-teal-50/70 border border-teal-200 rounded-xl text-teal-900 text-[11px] flex items-center gap-1.5 font-medium">
                    <Info className="w-4 h-4 text-teal-700 shrink-0" />
                    <span>Current GPS Location ≠ Demand Location। আপনি কক্সবাজারের যেকোনো এলাকার জন্য চাহিদা প্রকাশ করতে পারেন।</span>
                  </div>

                  {/* Country / Division / District */}
                  <div className="grid grid-cols-3 gap-2">
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">দেশ</label>
                      <div className="px-2.5 py-1.5 bg-slate-100 border border-slate-200 rounded-lg text-slate-700 text-xs font-baloo">
                        বাংলাদেশ
                      </div>
                    </div>
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">বিভাগ</label>
                      <div className="px-2.5 py-1.5 bg-slate-100 border border-slate-200 rounded-lg text-slate-700 text-xs font-baloo">
                        চট্টগ্রাম
                      </div>
                    </div>
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">জেলা *</label>
                      <div className="px-2.5 py-1.5 bg-slate-100 border border-slate-200 rounded-lg text-slate-800 text-xs font-baloo font-bold">
                        কক্সবাজার
                      </div>
                    </div>
                  </div>

                  {/* Upazila & Union/Municipality */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">উপজেলা *</label>
                      <select
                        value={wizUpazilaId}
                        onChange={e => {
                          const id = Number(e.target.value);
                          setWizUpazilaId(id);
                          setWizUpazilaNameBn(COX_UPAZILAS.find(u => u.id === id)?.nameBn || 'কক্সবাজার সদর');
                          setWizUnionId(null);
                          setWizUnionNameBn(null);
                          setWizWardId(null);
                          setWizWardNameBn(null);
                          setWizLocalityId(null);
                          setWizLocalityNameBn(null);
                          setWizPostalLocationId(null);
                          setWizPostalLocationNameBn(null);
                        }}
                        className="w-full px-2.5 py-2 bg-white border border-slate-300 rounded-xl text-xs font-baloo font-bold text-slate-800 focus:border-teal-600 focus:ring-1 focus:ring-teal-600 shadow-2xs cursor-pointer"
                      >
                        {COX_UPAZILAS.map(u => (
                          <option key={u.id} value={u.id}>{u.nameBn}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">ইউনিয়ন / পৌরসভা (ঐচ্ছিক)</label>
                      <select
                        value={wizUnionId || ''}
                        onChange={e => {
                          const id = e.target.value ? Number(e.target.value) : null;
                          setWizUnionId(id);
                          const list = COX_UNIONS[wizUpazilaId] || [];
                          const foundUnion = list.find(un => un.id === id);
                          setWizUnionNameBn(foundUnion?.nameBn || null);
                          if (foundUnion?.defaultPostCode) {
                            setWizPostCode(foundUnion.defaultPostCode);
                          }
                          setWizWardId(null);
                          setWizWardNameBn(null);
                          setWizLocalityId(null);
                          setWizLocalityNameBn(null);
                        }}
                        className="w-full px-2.5 py-2 bg-white border border-slate-300 rounded-xl text-xs font-baloo font-bold text-slate-800 focus:border-teal-600 focus:ring-1 focus:ring-teal-600 shadow-2xs cursor-pointer"
                      >
                        <option value="">-- ইউনিয়ন / পৌরসভা নির্বাচন করুন --</option>
                        {(COX_UNIONS[wizUpazilaId] || []).map(un => (
                          <option key={un.id} value={un.id}>{un.nameBn}</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* Ward & Locality / Para */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">ওয়ার্ড (ঐচ্ছিক)</label>
                      <select
                        disabled={!wizUnionId || !(COX_WARDS[wizUnionId] && COX_WARDS[wizUnionId].length > 0)}
                        value={wizWardId || ''}
                        onChange={e => {
                          const id = e.target.value ? Number(e.target.value) : null;
                          setWizWardId(id);
                          const list = wizUnionId ? COX_WARDS[wizUnionId] || [] : [];
                          setWizWardNameBn(list.find(w => w.id === id)?.nameBn || null);
                          setWizLocalityId(null);
                          setWizLocalityNameBn(null);
                        }}
                        className={`w-full px-2.5 py-2 rounded-xl text-xs font-baloo font-bold shadow-2xs ${
                          !wizUnionId 
                            ? 'bg-slate-100 border-slate-200 text-slate-400 cursor-not-allowed'
                            : 'bg-white border-slate-300 text-slate-800 focus:border-teal-600 focus:ring-1 focus:ring-teal-600 cursor-pointer'
                        }`}
                      >
                        <option value="">-- ওয়ার্ড নির্বাচন করুন --</option>
                        {wizUnionId && COX_WARDS[wizUnionId]?.map(w => (
                          <option key={w.id} value={w.id}>{w.nameBn}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">
                        পাড়া / মহল্লা / গ্রাম / লোকালিটি (ঐচ্ছিক)
                        {isLoadingLocalities && <span className="ml-1 text-teal-600 font-normal animate-pulse">(লোড হচ্ছে...)</span>}
                      </label>
                      <select
                        disabled={!wizWardId || (!isLoadingLocalities && availableLocalities.length === 0)}
                        value={wizLocalityId || ''}
                        onChange={e => {
                          const id = e.target.value ? Number(e.target.value) : null;
                          setWizLocalityId(id);
                          setWizLocalityNameBn(availableLocalities.find(l => l.id === id)?.nameBn || null);
                        }}
                        className={`w-full px-2.5 py-2 rounded-xl text-xs font-baloo font-bold shadow-2xs ${
                          !wizWardId || (!isLoadingLocalities && availableLocalities.length === 0)
                            ? 'bg-slate-100 border-slate-200 text-slate-400 cursor-not-allowed'
                            : 'bg-white border-slate-300 text-slate-800 focus:border-teal-600 focus:ring-1 focus:ring-teal-600 cursor-pointer'
                        }`}
                      >
                        <option value="">
                          {!wizWardId 
                            ? '-- প্রথমে ওয়ার্ড নির্বাচন করুন --' 
                            : isLoadingLocalities
                              ? '-- তথ্য লোড হচ্ছে... --'
                              : availableLocalities.length > 0
                                ? '-- পাড়া / মহল্লা নির্বাচন করুন --'
                                : '-- কোনো তালিকাভুক্ত পাড়া নেই (ঐচ্ছিক) --'
                          }
                        </option>
                        {wizWardId && availableLocalities.map(l => (
                          <option key={l.id} value={l.id}>{l.nameBn} ({l.type})</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* Postal Location & Auto Post Code */}
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
                    <div className="sm:col-span-2">
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">ডাকঘর / পোস্ট অফিস (ঐচ্ছিক)</label>
                      <select
                        value={wizPostalLocationId || ''}
                        onChange={e => {
                          const id = e.target.value ? Number(e.target.value) : null;
                          setWizPostalLocationId(id);
                          const foundPost = COX_POSTAL_LOCATIONS.find(p => p.id === id);
                          setWizPostalLocationNameBn(foundPost?.nameBn || null);
                          if (foundPost?.postCode) {
                            setWizPostCode(foundPost.postCode);
                          }
                        }}
                        className="w-full px-2.5 py-2 bg-white border border-slate-300 rounded-xl text-xs font-baloo font-bold text-slate-800 focus:border-teal-600 focus:ring-1 focus:ring-teal-600 shadow-2xs cursor-pointer"
                      >
                        <option value="">-- ডাকঘর নির্বাচন করুন --</option>
                        {COX_POSTAL_LOCATIONS.filter(p => p.upazilaId === wizUpazilaId).map(p => (
                          <option key={p.id} value={p.id}>{p.nameBn} ({p.postCode})</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">পোস্ট কোড (Auto)</label>
                      <input
                        type="text"
                        readOnly
                        value={wizPostCode}
                        className="w-full px-2.5 py-2 bg-slate-100 border border-slate-200 rounded-xl text-xs font-mono font-bold text-teal-800 text-center"
                      />
                    </div>
                  </div>

                  {/* Specific Street Address */}
                  <div>
                    <label className="block font-bold text-slate-700 mb-1 text-[11px]">নির্দিষ্ট ঠিকানা / রোড নম্বর (ঐচ্ছিক)</label>
                    <input
                      type="text"
                      placeholder="e.g. কলাতলী রোড, হোটেল সী-গালের বিপরীতে"
                      value={wizDetailedAddress}
                      onChange={e => setWizDetailedAddress(e.target.value)}
                      className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium focus:outline-none focus:border-teal-600"
                    />
                  </div>
                </div>
              )}

              {/* STEP 5: কখন প্রয়োজন? */}
              {wizardStep === 5 && (
                <div className="space-y-3">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">কখন প্রয়োজন?</h3>
                    <p className="text-[11px] text-slate-500">কখন সেবা বা মালামাল প্রয়োজন তা নির্ধারণ করুন (Asia/Dhaka টাইমজোন)।</p>
                  </div>

                  <div className="space-y-2">
                    <div 
                      onClick={() => setWizScheduleType('ASAP')}
                      className={`p-3 rounded-xl border cursor-pointer flex items-center gap-2.5 ${
                        wizScheduleType === 'ASAP' ? 'bg-teal-50 border-teal-600 text-teal-900' : 'bg-white border-slate-200'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${wizScheduleType === 'ASAP' ? 'border-teal-700 bg-teal-700 text-white' : 'border-slate-300'}`}>
                        {wizScheduleType === 'ASAP' && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                      </div>
                      <div>
                        <p className="font-bold text-xs font-baloo">যত দ্রুত সম্ভব (ASAP)</p>
                        <p className="text-[10px] text-slate-500">আজকের মধ্যে দ্রুত সমাধান প্রয়োজন</p>
                      </div>
                    </div>

                    <div 
                      onClick={() => setWizScheduleType('DATE')}
                      className={`p-3 rounded-xl border cursor-pointer flex items-center gap-2.5 ${
                        wizScheduleType === 'DATE' ? 'bg-teal-50 border-teal-600 text-teal-900' : 'bg-white border-slate-200'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${wizScheduleType === 'DATE' ? 'border-teal-700 bg-teal-700 text-white' : 'border-slate-300'}`}>
                        {wizScheduleType === 'DATE' && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                      </div>
                      <div>
                        <p className="font-bold text-xs font-baloo">নির্দিষ্ট তারিখে</p>
                        <p className="text-[10px] text-slate-500">ভবিষ্যতের একটি নির্দিষ্ট দিনে</p>
                      </div>
                    </div>

                    <div 
                      onClick={() => setWizScheduleType('DATE_TIME')}
                      className={`p-3 rounded-xl border cursor-pointer flex items-center gap-2.5 ${
                        wizScheduleType === 'DATE_TIME' ? 'bg-teal-50 border-teal-600 text-teal-900' : 'bg-white border-slate-200'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${wizScheduleType === 'DATE_TIME' ? 'border-teal-700 bg-teal-700 text-white' : 'border-slate-300'}`}>
                        {wizScheduleType === 'DATE_TIME' && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                      </div>
                      <div>
                        <p className="font-bold text-xs font-baloo">নির্দিষ্ট তারিখ ও সময়ে</p>
                        <p className="text-[10px] text-slate-500">নির্দিষ্ট দিন এবং নির্দিষ্ট ঘণ্টায়</p>
                      </div>
                    </div>
                  </div>

                  {(wizScheduleType === 'DATE' || wizScheduleType === 'DATE_TIME') && (
                    <div className="grid grid-cols-2 gap-2 pt-2">
                      <div>
                        <label className="block font-bold text-slate-700 mb-1 text-[11px]">তারিখ</label>
                        <input
                          type="date"
                          value={wizDate}
                          onChange={e => setWizDate(e.target.value)}
                          className="w-full px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                        />
                      </div>
                      {wizScheduleType === 'DATE_TIME' && (
                        <div>
                          <label className="block font-bold text-slate-700 mb-1 text-[11px]">সময়</label>
                          <input
                            type="time"
                            value={wizTime}
                            onChange={e => setWizTime(e.target.value)}
                            className="w-full px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                          />
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}

              {/* STEP 6: পরিমাণ ও বাজেট */}
              {wizardStep === 6 && (
                <div className="space-y-3">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">পরিমাণ ও বাজেট পরিসীমা</h3>
                    <p className="text-[11px] text-slate-500">পরিমাণ ও পরিমাপের একক এবং আনুমানিক বাজেট (৳ BDT) লিখুন।</p>
                  </div>

                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">পরিমাণ (ঐচ্ছিক)</label>
                      <input
                        type="number"
                        placeholder="e.g. ১০০০"
                        value={wizQuantity}
                        onChange={e => setWizQuantity(e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-mono"
                      />
                    </div>
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">একক (Unit)</label>
                      <input
                        type="text"
                        placeholder="e.g. টি"
                        value={wizUnit}
                        onChange={e => setWizUnit(e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                      />
                    </div>
                  </div>

                  {/* Unit chips */}
                  <div className="flex flex-wrap gap-1">
                    {['টি', 'কেজি', 'টন', 'ব্যাগ', 'ঘণ্টা', 'দিন', 'ট্রিপ', 'স্কয়ার ফিট'].map(u => (
                      <button
                        key={u}
                        type="button"
                        onClick={() => setWizUnit(u)}
                        className={`px-2 py-0.5 rounded text-[10px] font-bold font-baloo border ${
                          wizUnit === u ? 'bg-teal-700 text-white border-teal-700' : 'bg-slate-100 text-slate-600 border-slate-200'
                        }`}
                      >
                        {u}
                      </button>
                    ))}
                  </div>

                  <div className="grid grid-cols-2 gap-2 pt-2">
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">সর্বনিম্ন বাজেট (৳)</label>
                      <input
                        type="number"
                        placeholder="৫০০"
                        value={wizBudgetMin}
                        onChange={e => setWizBudgetMin(e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-mono"
                      />
                    </div>
                    <div>
                      <label className="block font-bold text-slate-700 mb-1 text-[11px]">সর্বোচ্চ বাজেট (৳)</label>
                      <input
                        type="number"
                        placeholder="১৫০০"
                        value={wizBudgetMax}
                        onChange={e => setWizBudgetMax(e.target.value)}
                        className="w-full px-2.5 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-mono"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 7: যোগাযোগের পছন্দ */}
              {wizardStep === 7 && (
                <div className="space-y-3">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">যোগাযোগের পছন্দ</h3>
                    <p className="text-[11px] text-slate-500">সেবাদাতা কীভাবে যোগাযোগ করবেন তা নির্ধারণ করুন।</p>
                  </div>

                  <div className="space-y-2">
                    <div 
                      onClick={() => setWizContactPref('IN_APP_ONLY')}
                      className={`p-3 rounded-xl border cursor-pointer flex items-center gap-2.5 ${
                        wizContactPref === 'IN_APP_ONLY' ? 'bg-teal-50 border-teal-600 text-teal-900' : 'bg-white border-slate-200'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${wizContactPref === 'IN_APP_ONLY' ? 'border-teal-700 bg-teal-700 text-white' : 'border-slate-300'}`}>
                        {wizContactPref === 'IN_APP_ONLY' && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                      </div>
                      <div>
                        <p className="font-bold text-xs font-baloo">শুধু অ্যাপের মাধ্যমে (ইন-অ্যাপ বার্তা)</p>
                        <p className="text-[10px] text-slate-500">ফোন নম্বর সম্পূর্ণ গোপন থাকবে</p>
                      </div>
                    </div>

                    <div 
                      onClick={() => setWizContactPref('PHONE')}
                      className={`p-3 rounded-xl border cursor-pointer flex items-center gap-2.5 ${
                        wizContactPref === 'PHONE' ? 'bg-teal-50 border-teal-600 text-teal-900' : 'bg-white border-slate-200'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${wizContactPref === 'PHONE' ? 'border-teal-700 bg-teal-700 text-white' : 'border-slate-300'}`}>
                        {wizContactPref === 'PHONE' && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                      </div>
                      <div>
                        <p className="font-bold text-xs font-baloo">সরাসরি ফোনে</p>
                        <p className="text-[10px] text-slate-500">যাচাইকৃত সেবাদাতারা সরাসরি ফোন করতে পারবেন</p>
                      </div>
                    </div>

                    <div 
                      onClick={() => setWizContactPref('BOTH')}
                      className={`p-3 rounded-xl border cursor-pointer flex items-center gap-2.5 ${
                        wizContactPref === 'BOTH' ? 'bg-teal-50 border-teal-600 text-teal-900' : 'bg-white border-slate-200'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${wizContactPref === 'BOTH' ? 'border-teal-700 bg-teal-700 text-white' : 'border-slate-300'}`}>
                        {wizContactPref === 'BOTH' && <div className="w-1.5 h-1.5 bg-white rounded-full" />}
                      </div>
                      <div>
                        <p className="font-bold text-xs font-baloo">অ্যাপ + ফোন উভয় মাধ্যমে</p>
                        <p className="text-[10px] text-slate-500">চ্যাট এবং ফোন কল উভয় পদ্ধতি চালু থাকবে</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 8: প্রকাশের সেটিংস */}
              {wizardStep === 8 && (
                <div className="space-y-3">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">প্রকাশের সেটিংস ও জরুরিতা</h3>
                    <p className="text-[11px] text-slate-500">কারা দেখতে পারবেন এবং জরুরি ট্যাগ প্রযোজ্য কি না তা নির্ধারণ করুন।</p>
                  </div>

                  <div className="space-y-2">
                    <div 
                      onClick={() => setWizVisibility('PUBLIC')}
                      className={`p-2.5 rounded-xl border cursor-pointer flex items-center justify-between ${
                        wizVisibility === 'PUBLIC' ? 'bg-teal-50 border-teal-600 text-teal-900' : 'bg-white border-slate-200'
                      }`}
                    >
                      <span className="font-bold text-xs font-baloo">সবার জন্য উন্মুক্ত (Public)</span>
                      <span className="text-[10px] text-slate-500">সকল ভিজিটর দেখতে পাবেন</span>
                    </div>

                    <div 
                      onClick={() => setWizVisibility('REGISTERED_USERS')}
                      className={`p-2.5 rounded-xl border cursor-pointer flex items-center justify-between ${
                        wizVisibility === 'REGISTERED_USERS' ? 'bg-teal-50 border-teal-600 text-teal-900' : 'bg-white border-slate-200'
                      }`}
                    >
                      <span className="font-bold text-xs font-baloo">নিবন্ধিত ব্যবহারকারী (Registered Users)</span>
                      <span className="text-[10px] text-slate-500">লগইনকৃত সেবাদাতারা দেখবেন</span>
                    </div>
                  </div>

                  <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between pt-2">
                    <div>
                      <p className="font-bold text-slate-800 text-xs font-baloo">জরুরি প্রয়োজন? (Urgent)</p>
                      <p className="text-[10px] text-slate-500">জরুরি ট্যাগ যোগ হবে</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={wizPriority === 'URGENT'}
                      onChange={e => setWizPriority(e.target.checked ? 'URGENT' : 'NORMAL')}
                      className="w-4 h-4 text-teal-600 rounded cursor-pointer"
                    />
                  </div>
                </div>
              )}

              {/* STEP 9: পর্যালোচনা (Review) */}
              {wizardStep === 9 && (
                <div className="space-y-2.5">
                  <div className="space-y-1">
                    <h3 className="text-sm font-bold text-slate-900 font-hind">আপনার প্রয়োজন পর্যালোচনা করুন</h3>
                    <p className="text-[11px] text-slate-500">প্রকাশ করার আগে নিচের তথ্যগুলো যাচাই করে নিন।</p>
                  </div>

                  {/* Section 1 */}
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-[11px] font-bold text-slate-500 font-baloo">১. শিরোনাম ও সেবা</span>
                      <button onClick={() => setWizardStep(1)} className="text-[10px] text-teal-700 font-bold font-baloo hover:underline">
                        পরিবর্তন করুন
                      </button>
                    </div>
                    <p className="font-bold text-slate-900 text-xs font-baloo">{wizTitle}</p>
                    <p className="text-[11px] text-teal-800 font-medium">সেবা: {wizServiceNameBn || wizCategoryNameBn || 'সাধারণ'}</p>
                  </div>

                  {/* Section 2 */}
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-[11px] font-bold text-slate-500 font-baloo">২. বিস্তারিত বিবরণ</span>
                      <button onClick={() => setWizardStep(3)} className="text-[10px] text-teal-700 font-bold font-baloo hover:underline">
                        পরিবর্তন করুন
                      </button>
                    </div>
                    <p className="text-[11px] text-slate-700">{wizDescription}</p>
                  </div>

                  {/* Section 3 */}
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1 font-tiro">
                    <div className="flex justify-between items-center">
                      <span className="text-[11px] font-bold text-slate-500 font-baloo">৩. ভৌগোলিক অবস্থান ও ঠিকানা</span>
                      <button onClick={() => setWizardStep(4)} className="text-[10px] text-teal-700 font-bold font-baloo hover:underline">
                        পরিবর্তন করুন
                      </button>
                    </div>
                    <p className="text-[11px] text-slate-800 font-bold">
                      {wizUnionNameBn ? `${wizUnionNameBn}, ` : ''}{wizUpazilaNameBn}, {wizDistrictNameBn} {wizPostCode ? `(পোস্ট কোড: ${wizPostCode})` : ''}
                    </p>
                    {(wizWardNameBn || wizLocalityNameBn) && (
                      <p className="text-[10px] text-slate-600 font-medium">
                        {wizWardNameBn ? `${wizWardNameBn}` : ''}{wizLocalityNameBn ? ` • ${wizLocalityNameBn}` : ''}
                      </p>
                    )}
                    {wizPostalLocationNameBn && (
                      <p className="text-[10px] text-teal-800">
                        ডাকঘর: {wizPostalLocationNameBn}
                      </p>
                    )}
                    {wizDetailedAddress && <p className="text-[10px] text-slate-600">নির্দিষ্ট ঠিকানা: {wizDetailedAddress}</p>}
                  </div>

                  {/* Section 4 */}
                  <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-[11px] font-bold text-slate-500 font-baloo">৪. বাজেট ও সময়</span>
                      <button onClick={() => setWizardStep(6)} className="text-[10px] text-teal-700 font-bold font-baloo hover:underline">
                        পরিবর্তন করুন
                      </button>
                    </div>
                    <p className="text-[11px] text-slate-700">
                      বাজেট: {wizBudgetMin && wizBudgetMax ? `৳${wizBudgetMin} - ৳${wizBudgetMax}` : (wizBudgetMin ? `৳${wizBudgetMin}+` : 'আলোচনা সাপেক্ষে')}
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* WIZARD BOTTOM ACTIONS */}
            <div className="flex gap-2 pt-3 border-t border-slate-100 font-baloo mt-auto">
              {wizardStep > 1 && (
                <button
                  onClick={prevWizardStep}
                  className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition cursor-pointer"
                >
                  পিছনে
                </button>
              )}

              <button
                onClick={() => handleFinalSubmit(false)}
                className="px-3 py-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 rounded-xl text-xs font-bold transition cursor-pointer"
              >
                খসড়া সংরক্ষণ
              </button>

              {wizardStep < 9 ? (
                <button
                  onClick={nextWizardStep}
                  className="flex-1 bg-teal-700 hover:bg-teal-800 text-white py-2 rounded-xl text-xs font-bold shadow-xs transition cursor-pointer"
                >
                  পরবর্তী
                </button>
              ) : (
                <button
                  onClick={() => setIsPublishConfirmOpen(true)}
                  className="flex-1 bg-teal-700 hover:bg-teal-800 text-white py-2 rounded-xl text-xs font-bold shadow-xs transition cursor-pointer"
                >
                  প্রয়োজন প্রকাশ করুন
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* CONFIRMATION DIALOG MODAL */}
      {isPublishConfirmOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-60 font-tiro">
          <div className="bg-white rounded-2xl max-w-sm w-full p-4 shadow-2xl border border-slate-200 space-y-3">
            <h3 className="text-sm font-bold text-slate-900 font-hind">প্রয়োজন প্রকাশ নিশ্চিতকরণ</h3>
            <p className="text-xs text-slate-600">
              আপনি কি এই প্রয়োজনটি সর্বসাধারণ ও সংশ্লিষ্ট সেবাদাতাদের জন্য প্রকাশ করতে চান?
            </p>
            <div className="flex gap-2 pt-2 font-baloo">
              <button
                onClick={() => setIsPublishConfirmOpen(false)}
                className="flex-1 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold cursor-pointer"
              >
                ফিরে যান
              </button>
              <button
                onClick={() => handleFinalSubmit(true)}
                className="flex-1 py-1.5 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold shadow-xs cursor-pointer"
              >
                প্রকাশ করুন
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
