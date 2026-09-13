import React, { useState } from 'react';
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
  Filter,
  Check,
  X
} from 'lucide-react';
import { MockDemand } from '../data/demandMockData';

interface DemandSimulatorProps {
  demands: MockDemand[];
  onAddDemand: (newDemand: Partial<MockDemand>, publishNow: boolean) => void;
  onStatusChange: (demandId: number, newStatus: MockDemand['status']) => void;
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

export const DemandSimulatorViews: React.FC<DemandSimulatorProps> = ({ demands, onAddDemand, onStatusChange }) => {
  const [activeTab, setActiveTab] = useState<'feed' | 'my_demands'>('feed');
  const [selectedDemand, setSelectedDemand] = useState<MockDemand | null>(null);
  const [isCreateOpen, setIsCreateOpen] = useState<boolean>(false);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedUpazila, setSelectedUpazila] = useState<string>('all');
  const [urgencyFilter, setUrgencyFilter] = useState<'all' | 'urgent'>('all');

  // Form states for creating new demand
  const [formTitle, setFormTitle] = useState('');
  const [formDesc, setFormDesc] = useState('');
  const [formLocation, setFormLocation] = useState('কলাতলী রোড, কক্সবাজার সদর');
  const [formUpazilaId, setFormUpazilaId] = useState(1);
  const [formDemandType, setFormDemandType] = useState<MockDemand['demandType']>('SERVICE');
  const [formPriority, setFormPriority] = useState<MockDemand['priority']>('NORMAL');
  const [formBudgetMin, setFormBudgetMin] = useState('800');
  const [formBudgetMax, setFormBudgetMax] = useState('1500');
  const [formError, setFormError] = useState<string | null>(null);

  const UPAZILAS = [
    { id: 1, name: 'কক্সবাজার সদর' },
    { id: 2, name: 'চকোরিয়া' },
    { id: 3, name: 'মহেশখালী' },
    { id: 4, name: 'রামু' },
    { id: 5, name: 'টেকনাফ' },
    { id: 6, name: 'উখিয়া' },
    { id: 7, name: 'কুতুবদিয়া' },
    { id: 8, name: 'পেকুয়া' },
    { id: 9, name: 'ঈদগাঁও' },
  ];

  const filteredFeed = demands.filter(d => {
    if (d.status !== 'PUBLISHED') return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchTitle = d.titleBn.toLowerCase().includes(q) || d.titleEn.toLowerCase().includes(q);
      const matchDesc = d.descriptionBn.toLowerCase().includes(q);
      if (!matchTitle && !matchDesc) return false;
    }
    if (selectedUpazila !== 'all' && d.upazilaId !== Number(selectedUpazila)) {
      return false;
    }
    if (urgencyFilter === 'urgent' && d.priority !== 'URGENT') {
      return false;
    }
    return true;
  });

  const myDemands = demands.filter(d => d.isOwner);

  const handleCreateSubmit = (publishNow: boolean) => {
    if (!formTitle.trim() || formTitle.trim().length < 5) {
      setFormError('শিরোনাম কমপক্ষে ৫ অক্ষরের হতে হবে।');
      return;
    }
    if (!formDesc.trim() || formDesc.trim().length < 10) {
      setFormError('বিস্তারিত বিবরণ কমপক্ষে ১০ অক্ষরের হতে হবে।');
      return;
    }

    const upz = UPAZILAS.find(u => u.id === formUpazilaId);

    onAddDemand({
      titleBn: formTitle.trim(),
      titleEn: formTitle.trim(),
      descriptionBn: formDesc.trim(),
      descriptionEn: formDesc.trim(),
      demandType: formDemandType,
      priority: formPriority,
      upazilaId: formUpazilaId,
      upazilaNameBn: upz ? upz.name : 'কক্সবাজার সদর',
      locationDisplayBn: formLocation.trim(),
      budgetMin: formBudgetMin ? Number(formBudgetMin) : undefined,
      budgetMax: formBudgetMax ? Number(formBudgetMax) : undefined,
      currency: 'BDT',
      visibility: 'PUBLIC',
      contactPreference: 'IN_APP_ONLY',
    }, publishNow);

    // Reset
    setFormTitle('');
    setFormDesc('');
    setFormError(null);
    setIsCreateOpen(false);
  };

  return (
    <div className="flex flex-col h-full bg-slate-50 text-slate-800">
      {/* Subheader Navigation */}
      <div className="bg-white border-b border-slate-200 px-4 py-2.5 flex items-center justify-between">
        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('feed')}
            className={`px-3 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
              activeTab === 'feed'
                ? 'bg-teal-700 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            প্রয়োজনের ফিড ({filteredFeed.length})
          </button>
          <button
            onClick={() => setActiveTab('my_demands')}
            className={`px-3 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
              activeTab === 'my_demands'
                ? 'bg-teal-700 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            আমার প্রয়োজন ({myDemands.length})
          </button>
        </div>

        <button
          onClick={() => setIsCreateOpen(true)}
          className="flex items-center gap-1.5 bg-teal-700 hover:bg-teal-800 text-white px-3 py-1.5 rounded-xl text-xs font-bold shadow-xs transition cursor-pointer"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>নতুন প্রয়োজন</span>
        </button>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-4">
        {activeTab === 'feed' ? (
          <div>
            {/* Search & Filter Bar */}
            <div className="bg-white p-3 rounded-2xl border border-slate-200 shadow-xs mb-4 space-y-2.5">
              <div className="relative">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="প্রয়োজন খুঁজুন (e.g. ইলেকট্রিশিয়ান, ইট, পিকআপ)..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-teal-600 font-medium"
                />
              </div>

              <div className="flex items-center justify-between gap-2 text-xs">
                <div className="flex items-center gap-2 flex-1">
                  <span className="text-slate-500 font-medium text-[11px]">উপজেলা:</span>
                  <select
                    value={selectedUpazila}
                    onChange={e => setSelectedUpazila(e.target.value)}
                    className="bg-slate-50 border border-slate-200 text-slate-700 px-2 py-1 rounded-lg text-xs font-medium cursor-pointer"
                  >
                    <option value="all">সকল উপজেলা (৯টি)</option>
                    {UPAZILAS.map(u => (
                      <option key={u.id} value={u.id}>{u.name}</option>
                    ))}
                  </select>
                </div>

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => setUrgencyFilter(urgencyFilter === 'urgent' ? 'all' : 'urgent')}
                    className={`px-2.5 py-1 rounded-lg text-xs font-bold transition cursor-pointer ${
                      urgencyFilter === 'urgent'
                        ? 'bg-rose-100 text-rose-700 border border-rose-300'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {urgencyFilter === 'urgent' ? '✓ জরুরি প্রয়োজন' : 'জরুরি ফিল্টার'}
                  </button>
                </div>
              </div>
            </div>

            {/* List of Demands */}
            {filteredFeed.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-2xl border border-slate-200 p-6">
                <AlertCircle className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                <p className="text-sm font-bold text-slate-700">কোনো প্রকাশিত প্রয়োজন পাওয়া যায়নি</p>
                <p className="text-xs text-slate-500 mt-1">অন্য উপজেলা নির্বাচন করুন অথবা নতুন প্রয়োজন পোস্ট করুন</p>
              </div>
            ) : (
              <div className="space-y-3">
                {filteredFeed.map(d => (
                  <div
                    key={d.id}
                    onClick={() => setSelectedDemand(d)}
                    className="bg-white border border-slate-200 hover:border-teal-500/50 rounded-2xl p-4 shadow-xs transition hover:shadow-sm cursor-pointer"
                  >
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <DemandStatusBadge status={d.status} compact />
                        {d.priority === 'URGENT' && (
                          <span className="bg-rose-50 text-rose-700 border border-rose-200 px-2 py-0.5 rounded-full text-[10px] font-bold">
                            জরুরি
                          </span>
                        )}
                      </div>
                      <span className="text-[11px] text-slate-400 font-mono">
                        #{d.id} • {d.upazilaNameBn}
                      </span>
                    </div>

                    <h3 className="font-bold text-slate-900 text-sm mb-1 leading-snug">
                      {d.titleBn}
                    </h3>
                    <p className="text-xs text-slate-600 line-clamp-2 mb-3 leading-relaxed">
                      {d.descriptionBn}
                    </p>

                    <div className="flex items-center justify-between text-xs pt-2 border-t border-slate-100">
                      <div className="flex items-center gap-1.5 text-slate-600">
                        <MapPin className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                        <span className="text-[11px] truncate max-w-[180px]">{d.locationDisplayBn}</span>
                      </div>

                      <div className="font-bold text-teal-800 text-xs">
                        {d.budgetMin && d.budgetMax ? `৳${d.budgetMin} - ৳${d.budgetMax}` : (d.budgetMin ? `৳${d.budgetMin}+` : 'আলোচনা সাপেক্ষে')}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          /* My Demands View */
          <div>
            <div className="flex items-center justify-between mb-3">
              <div>
                <h2 className="text-sm font-bold text-slate-800">আমার পোস্ট করা প্রয়োজনসমূহ</h2>
                <p className="text-xs text-slate-500">আপনার পোস্ট করা সকল খসড়া, সক্রিয় ও সম্পন্ন প্রয়োজনের তালিকা</p>
              </div>
            </div>

            {myDemands.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-2xl border border-slate-200 p-6">
                <AlertCircle className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                <p className="text-sm font-bold text-slate-700">আপনার কোনো প্রয়োজন তালিকাভুক্ত নেই</p>
                <button
                  onClick={() => setIsCreateOpen(true)}
                  className="mt-3 inline-flex items-center gap-1.5 bg-teal-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>প্রথম প্রয়োজন পোস্ট করুন</span>
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                {myDemands.map(d => (
                  <div
                    key={d.id}
                    onClick={() => setSelectedDemand(d)}
                    className="bg-white border border-slate-200 hover:border-teal-500/50 rounded-2xl p-4 shadow-xs transition hover:shadow-sm cursor-pointer"
                  >
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <DemandStatusBadge status={d.status} />
                      <span className="text-[11px] text-slate-400 font-mono">
                        {d.upazilaNameBn}
                      </span>
                    </div>

                    <h3 className="font-bold text-slate-900 text-sm mb-1 leading-snug">
                      {d.titleBn}
                    </h3>
                    <p className="text-xs text-slate-600 line-clamp-2 mb-3 leading-relaxed">
                      {d.descriptionBn}
                    </p>

                    <div className="flex items-center justify-between text-xs pt-2 border-t border-slate-100">
                      <div className="flex items-center gap-1.5 text-slate-600">
                        <MapPin className="w-3.5 h-3.5 text-teal-600 shrink-0" />
                        <span className="text-[11px] truncate max-w-[180px]">{d.locationDisplayBn}</span>
                      </div>

                      <div className="font-bold text-teal-800 text-xs">
                        {d.budgetMin && d.budgetMax ? `৳${d.budgetMin} - ৳${d.budgetMax}` : (d.budgetMin ? `৳${d.budgetMin}+` : 'আলোচনা সাপেক্ষে')}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Demand Detail Modal */}
      {selectedDemand && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-3xl max-w-lg w-full max-h-[90vh] overflow-y-auto p-5 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
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

            <h2 className="text-base font-black text-slate-900 mb-2 leading-snug">
              {selectedDemand.titleBn}
            </h2>

            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 mb-4 space-y-2">
              <p className="text-xs text-slate-700 leading-relaxed font-medium">
                {selectedDemand.descriptionBn}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs mb-4">
              <div className="border border-slate-100 bg-white p-2.5 rounded-xl">
                <p className="text-[10px] text-slate-400 font-bold uppercase">স্থান / উপজেলা</p>
                <p className="font-bold text-slate-800 mt-0.5 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-teal-600" />
                  <span>{selectedDemand.locationDisplayBn}</span>
                </p>
              </div>

              <div className="border border-slate-100 bg-white p-2.5 rounded-xl">
                <p className="text-[10px] text-slate-400 font-bold uppercase">বাজেট পরিসীমা</p>
                <p className="font-bold text-teal-800 mt-0.5">
                  {selectedDemand.budgetMin && selectedDemand.budgetMax ? `৳${selectedDemand.budgetMin} - ৳${selectedDemand.budgetMax}` : (selectedDemand.budgetMin ? `৳${selectedDemand.budgetMin}+` : 'আলোচনা সাপেক্ষে')}
                </p>
              </div>
            </div>

            {/* Requester Profile & Privacy Policy */}
            <div className="border border-slate-200 rounded-xl p-3 bg-white mb-4">
              <p className="text-[10px] text-slate-400 font-bold uppercase mb-2">অনুরোধকারীর প্রোফাইল ও যোগাযোগ নীতি</p>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-full bg-teal-100 text-teal-800 flex items-center justify-center font-bold text-xs">
                    {selectedDemand.requesterName.charAt(0)}
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-900">{selectedDemand.requesterName}</p>
                    <p className="text-[11px] text-slate-500 font-mono">
                      {selectedDemand.isOwner ? selectedDemand.contactPhone : `${selectedDemand.contactPhone.slice(0, 6)}****${selectedDemand.contactPhone.slice(-4)}`}
                    </p>
                  </div>
                </div>
                <span className="text-[10px] font-semibold bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md">
                  {selectedDemand.contactPreference === 'IN_APP_ONLY' ? 'ইন-অ্যাপ চ্যাট' : 'সরাসরি ফোন'}
                </span>
              </div>
            </div>

            {/* Owner Lifecycle Actions */}
            {selectedDemand.isOwner && (
              <div className="border-t border-slate-100 pt-3">
                <p className="text-[10px] text-slate-500 font-bold uppercase mb-2">জীবনচক্র নিয়ন্ত্রণ (মালিকের অ্যাকশন)</p>
                <div className="flex flex-wrap gap-2">
                  {selectedDemand.status === 'DRAFT' && (
                    <button
                      onClick={() => {
                        onStatusChange(selectedDemand.id, 'PUBLISHED');
                        setSelectedDemand(prev => prev ? { ...prev, status: 'PUBLISHED' } : null);
                      }}
                      className="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold shadow-xs cursor-pointer"
                    >
                      এখনই প্রকাশ করুন (Publish)
                    </button>
                  )}

                  {selectedDemand.status === 'PUBLISHED' && (
                    <>
                      <button
                        onClick={() => {
                          onStatusChange(selectedDemand.id, 'FULFILLED');
                          setSelectedDemand(prev => prev ? { ...prev, status: 'FULFILLED' } : null);
                        }}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold shadow-xs cursor-pointer"
                      >
                        প্রয়োজন পূরণ হয়েছে (Fulfill)
                      </button>
                      <button
                        onClick={() => {
                          onStatusChange(selectedDemand.id, 'PAUSED');
                          setSelectedDemand(prev => prev ? { ...prev, status: 'PAUSED' } : null);
                        }}
                        className="bg-amber-600 hover:bg-amber-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold shadow-xs cursor-pointer"
                      >
                        সাময়িক বন্ধ (Pause)
                      </button>
                      <button
                        onClick={() => {
                          onStatusChange(selectedDemand.id, 'CANCELLED');
                          setSelectedDemand(prev => prev ? { ...prev, status: 'CANCELLED' } : null);
                        }}
                        className="bg-rose-600 hover:bg-rose-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold shadow-xs cursor-pointer"
                      >
                        বাতিল করুন (Cancel)
                      </button>
                    </>
                  )}

                  {selectedDemand.status === 'PAUSED' && (
                    <>
                      <button
                        onClick={() => {
                          onStatusChange(selectedDemand.id, 'PUBLISHED');
                          setSelectedDemand(prev => prev ? { ...prev, status: 'PUBLISHED' } : null);
                        }}
                        className="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold shadow-xs cursor-pointer"
                      >
                        পুনরায় প্রকাশ করুন (Resume)
                      </button>
                      <button
                        onClick={() => {
                          onStatusChange(selectedDemand.id, 'CANCELLED');
                          setSelectedDemand(prev => prev ? { ...prev, status: 'CANCELLED' } : null);
                        }}
                        className="bg-rose-600 hover:bg-rose-700 text-white px-3 py-1.5 rounded-xl text-xs font-bold shadow-xs cursor-pointer"
                      >
                        বাতিল করুন (Cancel)
                      </button>
                    </>
                  )}

                  {selectedDemand.status === 'FULFILLED' && (
                    <button
                      onClick={() => {
                        onStatusChange(selectedDemand.id, 'CLOSED');
                        setSelectedDemand(prev => prev ? { ...prev, status: 'CLOSED' } : null);
                      }}
                      className="bg-slate-700 hover:bg-slate-800 text-white px-3 py-1.5 rounded-xl text-xs font-bold shadow-xs cursor-pointer"
                    >
                      স্থায়ী বন্ধ করুন (Close)
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Create Demand Modal */}
      {isCreateOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-3xl max-w-lg w-full max-h-[90vh] overflow-y-auto p-5 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-100">
              <h2 className="text-base font-black text-slate-900">নতুন প্রয়োজন প্রকাশ করুন</h2>
              <button
                onClick={() => {
                  setIsCreateOpen(false);
                  setFormError(null);
                }}
                className="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center transition cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {formError && (
              <div className="mb-3 p-2.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-semibold">
                {formError}
              </div>
            )}

            <div className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">প্রয়োজনের শিরোনাম (বাংলা) *</label>
                <input
                  type="text"
                  placeholder="e.g. কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন"
                  value={formTitle}
                  onChange={e => setFormTitle(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-teal-600 font-medium text-xs"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">বিস্তারিত বিবরণ (বাংলা) *</label>
                <textarea
                  rows={3}
                  placeholder="কী সমস্যা বা সুনির্দিষ্ট কী সেবা প্রয়োজন তা বিস্তারিত লিখুন..."
                  value={formDesc}
                  onChange={e => setFormDesc(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:border-teal-600 font-medium text-xs"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">উপজেলা *</label>
                  <select
                    value={formUpazilaId}
                    onChange={e => setFormUpazilaId(Number(e.target.value))}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-xs cursor-pointer"
                  >
                    {UPAZILAS.map(u => (
                      <option key={u.id} value={u.id}>{u.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">জরুরিতা *</label>
                  <select
                    value={formPriority}
                    onChange={e => setFormPriority(e.target.value as any)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-xs cursor-pointer"
                  >
                    <option value="NORMAL">সাধারণ (Normal)</option>
                    <option value="URGENT">জরুরি (Urgent)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">নির্দিষ্ট এলাকা / ঠিকানা</label>
                <input
                  type="text"
                  placeholder="e.g. কলাতলী রোড, হোটেল মোটেল জোন"
                  value={formLocation}
                  onChange={e => setFormLocation(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-xs"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">সর্বনিম্ন বাজেট (৳)</label>
                  <input
                    type="number"
                    placeholder="500"
                    value={formBudgetMin}
                    onChange={e => setFormBudgetMin(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-xs"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">সর্বোচ্চ বাজেট (৳)</label>
                  <input
                    type="number"
                    placeholder="1500"
                    value={formBudgetMax}
                    onChange={e => setFormBudgetMax(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl font-medium text-xs"
                  />
                </div>
              </div>
            </div>

            <div className="flex gap-2 pt-4 mt-4 border-t border-slate-100">
              <button
                onClick={() => handleCreateSubmit(false)}
                className="flex-1 bg-slate-100 hover:bg-slate-200 text-slate-700 py-2 rounded-xl text-xs font-bold transition cursor-pointer"
              >
                খসড়া সংরক্ষণ (Save Draft)
              </button>
              <button
                onClick={() => handleCreateSubmit(true)}
                className="flex-1 bg-teal-700 hover:bg-teal-800 text-white py-2 rounded-xl text-xs font-bold shadow-xs transition cursor-pointer"
              >
                প্রকাশ করুন (Publish)
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
