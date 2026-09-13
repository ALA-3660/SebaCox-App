import React, { useState, useMemo } from 'react';
import { 
  ArrowLeft, 
  Search, 
  Layers, 
  Check, 
  X, 
  Clock, 
  Truck, 
  CreditCard, 
  MessageCircle,
  HelpCircle,
  Sparkles
} from 'lucide-react';
import { 
  INITIAL_46_TAXONOMY_CATEGORIES, 
  INITIAL_SERVICES, 
  MockCategory, 
  MockService 
} from '../data/taxonomyMockData';

interface CategoriesSimulatorViewProps {
  onBack: () => void;
  onSelectService?: (service: MockService) => void;
  showTypoTag: (font: 'hind' | 'baloo' | 'tiro', role: string) => React.ReactNode;
}

export const CategoriesSimulatorView: React.FC<CategoriesSimulatorViewProps> = ({
  onBack,
  onSelectService,
  showTypoTag
}) => {
  const [filterKind, setFilterKind] = useState<'ALL' | 'PUBLIC_SERVICE_CATEGORY' | 'SYSTEM_DOMAIN'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<MockCategory | null>(null);

  // Filtered categories
  const filteredCategories = useMemo(() => {
    return INITIAL_46_TAXONOMY_CATEGORIES.filter(cat => {
      const matchesKind = filterKind === 'ALL' || cat.kind === filterKind;
      const q = searchQuery.toLowerCase().trim();
      const matchesSearch = !q || 
        cat.name_bn.toLowerCase().includes(q) || 
        cat.name_en.toLowerCase().includes(q) ||
        cat.slug.toLowerCase().includes(q);
      return matchesKind && matchesSearch;
    });
  }, [filterKind, searchQuery]);

  // Services under selected category
  const servicesForCategory = useMemo(() => {
    if (!selectedCategory) return [];
    return INITIAL_SERVICES.filter(s => s.category_id === selectedCategory.id);
  }, [selectedCategory]);

  return (
    <div className="flex flex-col gap-2.5 font-tiro py-1">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-2">
        <button
          onClick={selectedCategory ? () => setSelectedCategory(null) : onBack}
          className="flex items-center gap-1 text-xs text-slate-600 hover:text-slate-900 font-bold cursor-pointer font-baloo"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span className="font-baloo">{selectedCategory ? 'ক্যাটাগরি তালিকা' : 'হোমে ফিরুন'}</span>
        </button>
        <div className="flex items-center">
          <span className="text-xs font-bold text-slate-900 font-hind">
            {selectedCategory ? selectedCategory.name_bn : 'সেবা ক্যাটাগরি (৪৬টি)'}
          </span>
          {showTypoTag('hind', 'Page Title')}
        </div>
      </div>

      {!selectedCategory ? (
        <>
          {/* Slogan pill */}
          <div className="bg-teal-50 border border-teal-200 rounded-lg p-2 text-center">
            <p className="text-[11px] font-bold text-teal-900 font-hind">
              “প্রয়োজন থেকে সমাধান- এক অ্যাপেই”
            </p>
            <p className="text-[10px] text-teal-800 font-tiro">
              খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই
            </p>
          </div>

          {/* Search Box */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="ক্যাটাগরি খুঁজুন (বাংলা / English)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-white border border-slate-300 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-teal-600 font-tiro"
            />
          </div>

          {/* Filter Chips */}
          <div className="flex gap-1 overflow-x-auto text-[10px] font-baloo pb-1">
            <button
              onClick={() => setFilterKind('ALL')}
              className={`px-2 py-0.5 rounded-full border cursor-pointer whitespace-nowrap font-baloo ${
                filterKind === 'ALL'
                  ? 'bg-teal-700 text-white border-teal-800'
                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
              }`}
            >
              সকল ({INITIAL_46_TAXONOMY_CATEGORIES.length})
            </button>
            <button
              onClick={() => setFilterKind('PUBLIC_SERVICE_CATEGORY')}
              className={`px-2 py-0.5 rounded-full border cursor-pointer whitespace-nowrap font-baloo ${
                filterKind === 'PUBLIC_SERVICE_CATEGORY'
                  ? 'bg-teal-700 text-white border-teal-800'
                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
              }`}
            >
              পাবলিক সেবা (৩১)
            </button>
            <button
              onClick={() => setFilterKind('SYSTEM_DOMAIN')}
              className={`px-2 py-0.5 rounded-full border cursor-pointer whitespace-nowrap font-baloo ${
                filterKind === 'SYSTEM_DOMAIN'
                  ? 'bg-teal-700 text-white border-teal-800'
                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
              }`}
            >
              সিস্টেম ডোমেইন (১৫)
            </button>
          </div>

          {/* Categories List */}
          <div className="space-y-1.5 max-h-[380px] overflow-y-auto pr-0.5">
            {filteredCategories.map((cat) => (
              <div
                key={cat.id}
                onClick={() => setSelectedCategory(cat)}
                className="bg-white p-2.5 rounded-xl border border-slate-200 hover:border-teal-500 hover:shadow-xs transition cursor-pointer flex items-center justify-between gap-2"
              >
                <div className="flex items-center gap-2 min-w-0">
                  <div className="w-7 h-7 rounded-lg bg-teal-50 text-teal-800 flex items-center justify-center shrink-0">
                    <Layers className="w-3.5 h-3.5" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-1">
                      <span className="text-xs font-bold text-slate-900 truncate font-baloo">
                        {cat.name_bn}
                      </span>
                    </div>
                    <div className="text-[10px] text-slate-500 truncate font-mono">
                      {cat.name_en} • #{cat.slug}
                    </div>
                  </div>
                </div>

                <div className="shrink-0 flex items-center gap-1">
                  <span className={`text-[9px] px-1.5 py-0.5 rounded font-bold font-mono ${
                    cat.kind === 'PUBLIC_SERVICE_CATEGORY'
                      ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                      : 'bg-indigo-50 text-indigo-800 border border-indigo-200'
                  }`}>
                    {cat.kind === 'PUBLIC_SERVICE_CATEGORY' ? 'পাবলিক' : 'সিস্টেম'}
                  </span>
                </div>
              </div>
            ))}

            {filteredCategories.length === 0 && (
              <div className="text-center py-8 text-slate-400 text-xs">
                কোনো ক্যাটাগরি পাওয়া যায়নি
              </div>
            )}
          </div>
        </>
      ) : (
        /* Category Drilldown / Detail View */
        <div className="space-y-3">
          <div className="bg-teal-50/70 border border-teal-200 rounded-xl p-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-teal-900 font-hind">
                {selectedCategory.name_bn}
              </span>
              <span className="text-[10px] bg-teal-200/70 text-teal-900 font-mono px-1.5 py-0.5 rounded font-bold">
                {selectedCategory.slug}
              </span>
            </div>
            <p className="text-[11px] text-teal-800 font-tiro mt-1">
              English: {selectedCategory.name_en}
            </p>
            <p className="text-[10px] text-teal-700 font-mono mt-0.5">
              Kind: {selectedCategory.kind}
            </p>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs font-bold text-slate-800 font-baloo">
                এই ক্যাটাগরির সেবাসমূহ ({servicesForCategory.length})
              </span>
              {showTypoTag('baloo', 'Section Header')}
            </div>

            <div className="space-y-2">
              {servicesForCategory.map((srv) => (
                <div
                  key={srv.id}
                  className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-xs space-y-1.5"
                >
                  <div className="flex items-start justify-between gap-1">
                    <div>
                      <div className="text-xs font-bold text-slate-900 font-baloo">
                        {srv.name_bn}
                      </div>
                      <div className="text-[10px] text-slate-500 font-mono">
                        {srv.name_en} • Type: {srv.service_type}
                      </div>
                    </div>
                    {onSelectService && (
                      <button
                        onClick={() => onSelectService(srv)}
                        className="px-2 py-0.5 bg-teal-600 text-white rounded text-[10px] font-bold hover:bg-teal-700 cursor-pointer font-baloo"
                      >
                        নির্বাচন
                      </button>
                    )}
                  </div>

                  {/* Capability Matrix Badges */}
                  <div className="flex flex-wrap gap-1 pt-1 border-t border-slate-100">
                    <span className={`text-[8px] font-bold px-1.5 py-0.2 rounded font-mono ${
                      srv.requires_booking 
                        ? 'bg-amber-100 text-amber-900' 
                        : 'bg-slate-100 text-slate-500'
                    }`}>
                      Booking: {srv.requires_booking ? 'Yes' : 'No'}
                    </span>
                    <span className={`text-[8px] font-bold px-1.5 py-0.2 rounded font-mono ${
                      srv.supports_delivery 
                        ? 'bg-blue-100 text-blue-900' 
                        : 'bg-slate-100 text-slate-500'
                    }`}>
                      Delivery: {srv.supports_delivery ? 'Yes' : 'No'}
                    </span>
                    <span className={`text-[8px] font-bold px-1.5 py-0.2 rounded font-mono ${
                      srv.supports_negotiation 
                        ? 'bg-purple-100 text-purple-900' 
                        : 'bg-slate-100 text-slate-500'
                    }`}>
                      Negotiation: {srv.supports_negotiation ? 'Yes' : 'No'}
                    </span>
                  </div>
                </div>
              ))}

              {servicesForCategory.length === 0 && (
                <div className="p-4 bg-slate-50 rounded-xl text-center text-xs text-slate-500">
                  এই ক্যাটাগরিতে সরাসরি কনফিগার করা নমুনা সেবা নেই।
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
