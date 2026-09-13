import React, { useState } from 'react';
import { 
  Type, 
  CheckCircle2, 
  Sparkles, 
  Smartphone, 
  Layers, 
  Copy, 
  Check, 
  Sliders, 
  ShieldCheck,
  BookOpen
} from 'lucide-react';
import { banglaTypography } from '../theme/banglaTypography';

export const TypographyStandardViewer: React.FC = () => {
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [customText, setCustomText] = useState<string>('সেবাকক্স — “প্রয়োজন থেকে সমাধান- এক অ্যাপেই” • “খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই”');

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="p-2 bg-teal-50 text-teal-800 rounded-xl border border-teal-200">
                <Type className="w-5 h-5" />
              </span>
              <h2 className="text-xl font-black text-slate-900 font-hind">
                GLOBAL BANGLA TYPOGRAPHY STANDARD
              </h2>
            </div>
            <p className="text-xs text-slate-600 max-w-2xl font-tiro leading-relaxed">
              SebaCox-এর সকল user-facing UI-তে বাংলা ফন্ট ব্যবহারের নিয়ম বাধ্যতামূলক। প্রতিটি screen-এ আলাদা আলাদা font manually define না করে Flutter ThemeData ও centralized TextStyle সিস্টেমের মাধ্যমে নিয়ন্ত্রিত।
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <span className="bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-bold px-3 py-1.5 rounded-xl flex items-center gap-1.5 font-baloo">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>বাধ্যতামূলক আর্কিটেকচারাল মানদণ্ড</span>
            </span>
          </div>
        </div>
      </div>

      {/* The 3 Mandatory Fonts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* 1. HIND SILIGURI */}
        <div className="bg-white rounded-2xl border border-teal-200 shadow-xs overflow-hidden flex flex-col justify-between">
          <div className="p-5 border-b border-teal-100 bg-teal-50/50">
            <div className="flex items-center justify-between mb-2">
              <span className="px-2 py-0.5 bg-teal-700 text-white rounded-md text-[10px] font-bold tracking-wider uppercase font-mono">
                1. Large Heading
              </span>
              <span className="text-[11px] font-bold text-teal-800 font-mono">
                Google Font
              </span>
            </div>
            <h3 className="text-2xl font-bold text-teal-950 font-hind">
              হিন্দ শিলিগুড়ি (Hind Siliguri)
            </h3>
            <p className="text-[11px] text-teal-700 font-tiro mt-1">
              পরিচ্ছন্ন জ্যামিতিক গঠন ও বলিষ্ঠ দূরদৃষ্টিসম্পন্ন ডিসপ্লে টাইপোগ্রাফি।
            </p>
          </div>

          <div className="p-5 space-y-4 flex-1">
            <div>
              <div className="text-[10px] font-bold uppercase text-slate-400 font-mono mb-1">
                অনুমোদিত ব্যবহারক্ষেত্র:
              </div>
              <ul className="space-y-1 text-xs text-slate-700 font-tiro">
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-600"></span>
                  <span>বড় Heading (Display Headings)</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-600"></span>
                  <span>Page Title & Screen Header</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-600"></span>
                  <span>প্রধান Section Heading</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-teal-600"></span>
                  <span>গুরুত্বপূর্ণ বড় শিরোনাম ও ব্র্যান্ডিং</span>
                </li>
              </ul>
            </div>

            {/* Visual Specimen */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
              <div className="text-[10px] text-slate-400 font-mono">লাইভ স্পেসিমেন (Live Specimen):</div>
              <div className="text-xl font-bold text-slate-900 font-hind">
                সেবাকক্স মোবাইল প্ল্যাটফর্ম
              </div>
              <div className="text-base font-semibold text-slate-800 font-hind">
                কক্সবাজারের সার্বিক স্থানীয় সেবা নেটওয়ার্ক
              </div>
            </div>
          </div>

          <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-mono text-[11px]">Flutter: AppTypography.largeHeading1</span>
            <span className="text-[10px] bg-teal-100 text-teal-800 font-bold px-2 py-0.5 rounded">Weight: 700</span>
          </div>
        </div>

        {/* 2. BALOO DA 2 */}
        <div className="bg-white rounded-2xl border border-amber-200 shadow-xs overflow-hidden flex flex-col justify-between">
          <div className="p-5 border-b border-amber-100 bg-amber-50/50">
            <div className="flex items-center justify-between mb-2">
              <span className="px-2 py-0.5 bg-amber-600 text-white rounded-md text-[10px] font-bold tracking-wider uppercase font-mono">
                2. Medium Heading
              </span>
              <span className="text-[11px] font-bold text-amber-800 font-mono">
                Google Font
              </span>
            </div>
            <h3 className="text-2xl font-bold text-amber-950 font-baloo">
              বালু দা ২ (Baloo Da 2)
            </h3>
            <p className="text-[11px] text-amber-700 font-tiro mt-1">
              বন্ধুত্বপূর্ণ গোলাকার প্রান্ত ও চমৎকার ভিজ্যুয়াল কনট্রাস্ট।
            </p>
          </div>

          <div className="p-5 space-y-4 flex-1">
            <div>
              <div className="text-[10px] font-bold uppercase text-slate-400 font-mono mb-1">
                অনুমোদিত ব্যবহারক্ষেত্র:
              </div>
              <ul className="space-y-1 text-xs text-slate-700 font-tiro">
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span>
                  <span>মাঝারি Heading ও সেকশন শিরোনাম</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span>
                  <span>Card Heading (সার্ভিস ও প্রোভাইডার কার্ড)</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span>
                  <span>Sub-heading ও মডিউল টাইটেল</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span>
                  <span>Button-এর গুরুত্বপূর্ণ শিরোনাম ও অ্যাকশন</span>
                </li>
              </ul>
            </div>

            {/* Visual Specimen */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
              <div className="text-[10px] text-slate-400 font-mono">লাইভ স্পেসিমেন (Live Specimen):</div>
              <div className="text-lg font-bold text-slate-900 font-baloo">
                নির্বাচিত সেবা এলাকা: চকোরিয়া
              </div>
              <button className="px-4 py-2 bg-teal-700 text-white rounded-lg text-xs font-bold font-baloo shadow-xs">
                অবস্থান পরিবর্তন করুন
              </button>
            </div>
          </div>

          <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-mono text-[11px]">Flutter: AppTypography.mediumHeading1</span>
            <span className="text-[10px] bg-amber-100 text-amber-800 font-bold px-2 py-0.5 rounded">Weight: 600, 700</span>
          </div>
        </div>

        {/* 3. TIRO BANGLA */}
        <div className="bg-white rounded-2xl border border-blue-200 shadow-xs overflow-hidden flex flex-col justify-between">
          <div className="p-5 border-b border-blue-100 bg-blue-50/50">
            <div className="flex items-center justify-between mb-2">
              <span className="px-2 py-0.5 bg-blue-700 text-white rounded-md text-[10px] font-bold tracking-wider uppercase font-mono">
                3. Body / Normal Text
              </span>
              <span className="text-[11px] font-bold text-blue-800 font-mono">
                Google Font
              </span>
            </div>
            <h3 className="text-2xl font-bold text-blue-950 font-tiro">
              তিরো বাংলা (Tiro Bangla)
            </h3>
            <p className="text-[11px] text-blue-700 font-tiro mt-1">
              উচ্চ রিড্যাবিলিটি, ভারসাম্যপূর্ণ স্পেসিং ও ঐতিহ্যবাহী বাংলা যুক্তাক্ষর রেন্ডারিং।
            </p>
          </div>

          <div className="p-5 space-y-4 flex-1">
            <div>
              <div className="text-[10px] font-bold uppercase text-slate-400 font-mono mb-1">
                অনুমোদিত ব্যবহারক্ষেত্র:
              </div>
              <ul className="space-y-1 text-xs text-slate-700 font-tiro">
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                  <span>সকল সাধারণ লেখা ও Body Text</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                  <span>Description, Label ও Helper Text</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                  <span>Form Field ও ইনপুট টেক্সট</span>
                </li>
                <li className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
                  <span>Error/Success message ও List items</span>
                </li>
              </ul>
            </div>

            {/* Visual Specimen */}
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-2">
              <div className="text-[10px] text-slate-400 font-mono">লাইভ স্পেসিমেন (Live Specimen):</div>
              <p className="text-xs text-slate-700 font-tiro leading-relaxed">
                যাচাইকরণের জন্য আপনার মোবাইল নম্বরে একটি ৬ অঙ্কের ওটিপি পাঠানো হয়েছে। সেবা এলাকা এবং ডিভাইসের জিপিএস অবস্থান সবসময় পৃথক সংরক্ষিত থাকে।
              </p>
              <div className="text-[11px] text-emerald-700 font-tiro font-semibold">
                ✓ টোকেন ভ্যালিডেশন সফল হয়েছে
              </div>
            </div>
          </div>

          <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs">
            <span className="text-slate-500 font-mono text-[11px]">Flutter: AppTypography.bodyMedium</span>
            <span className="text-[10px] bg-blue-100 text-blue-800 font-bold px-2 py-0.5 rounded">Weight: 400, 500</span>
          </div>
        </div>
      </div>

      {/* Interactive Typography Playground & Live Inspector */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-base font-bold text-slate-900 font-hind flex items-center gap-2">
              <Sliders className="w-4 h-4 text-teal-700" />
              <span>ইন্টারেক্টিভ টাইপোগ্রাফি তুলনা ও প্রিভিউ (Live Inspector)</span>
            </h3>
            <p className="text-xs text-slate-500 font-tiro mt-0.5">
              যেকোনো বাংলা বাক্য লিখে তিনটি ফন্টের রূপ ও ব্যবহারিক দৃশ্যমানতা পরীক্ষা করুন।
            </p>
          </div>

          <div className="flex items-center gap-2">
            <input 
              type="text"
              value={customText}
              onChange={(e) => setCustomText(e.target.value)}
              placeholder="এখানে বাংলা লিখুন..."
              className="px-3 py-1.5 text-xs border border-slate-300 rounded-xl bg-slate-50 focus:bg-white focus:outline-teal-700 w-64 font-tiro"
            />
          </div>
        </div>

        {/* 3 Font Comparison Cards */}
        <div className="space-y-4">
          {/* Hind Siliguri Row */}
          <div className="p-4 bg-teal-50/40 rounded-xl border border-teal-200">
            <div className="flex items-center justify-between text-[11px] font-bold text-teal-900 mb-2">
              <span className="font-hind">HIND SILIGURI (Large Heading / Page Title)</span>
              <span className="font-mono text-[10px] bg-teal-200/60 px-2 py-0.5 rounded text-teal-900">fontFamily: 'Hind Siliguri'</span>
            </div>
            <div className="text-xl md:text-2xl font-bold text-slate-900 font-hind">
              {customText}
            </div>
            <div className="text-[11px] text-slate-500 font-tiro mt-1">
              উপযুক্ত ক্ষেত্র: অ্যাপের প্রধান শিরোনাম, প্রতিটি স্ক্রিনের হেডার, সেকশনের প্রধান হেডিং।
            </div>
          </div>

          {/* Baloo Da 2 Row */}
          <div className="p-4 bg-amber-50/40 rounded-xl border border-amber-200">
            <div className="flex items-center justify-between text-[11px] font-bold text-amber-900 mb-2">
              <span className="font-baloo">BALOO DA 2 (Medium Heading / Card Title / Button)</span>
              <span className="font-mono text-[10px] bg-amber-200/60 px-2 py-0.5 rounded text-amber-900">fontFamily: 'Baloo Da 2'</span>
            </div>
            <div className="text-lg md:text-xl font-bold text-slate-900 font-baloo">
              {customText}
            </div>
            <div className="text-[11px] text-slate-500 font-tiro mt-1">
              উপযুক্ত ক্ষেত্র: কার্ডের শিরোনাম, সাব-হেডিং, বাটনের ভেতরের অ্যাকশন টেক্সট, ফিল্টার ট্যাবস।
            </div>
          </div>

          {/* Tiro Bangla Row */}
          <div className="p-4 bg-blue-50/40 rounded-xl border border-blue-200">
            <div className="flex items-center justify-between text-[11px] font-bold text-blue-900 mb-2">
              <span className="font-tiro">TIRO BANGLA (Body / Description / Label / Forms)</span>
              <span className="font-mono text-[10px] bg-blue-200/60 px-2 py-0.5 rounded text-blue-900">fontFamily: 'Tiro Bangla'</span>
            </div>
            <div className="text-sm md:text-base font-normal text-slate-800 font-tiro leading-relaxed">
              {customText}
            </div>
            <div className="text-[11px] text-slate-500 font-tiro mt-1">
              উপযুক্ত ক্ষেত্র: সকল বর্ণনামূলক অনুচ্ছেদ, ফর্মের ইনপুট ফিল্ড ও লেবেল, সিস্টেম মেসেজ ও লিস্ট আইটেম।
            </div>
          </div>
        </div>
      </div>

      {/* Code Architecture & Centralized ThemeData System */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-teal-700" />
            <h3 className="text-base font-bold text-slate-900 font-hind">
              সেন্ট্রালাইজড আর্কিটেকচার বাস্তবায়ন (Flutter AppTypography & AppTheme)
            </h3>
          </div>
          <span className="text-[11px] text-slate-500 font-mono">mobile/lib/core/theme/</span>
        </div>

        <p className="text-xs text-slate-600 font-tiro leading-relaxed">
          প্রতিটি screen-এ আলাদাভাবে ম্যানুয়াল ফন্ট ডিফাইন নিষিদ্ধ। সমস্ত ফন্ট এবং স্টাইল সেন্ট্রালাইজড <code className="font-mono text-teal-800 bg-teal-50 px-1 py-0.5 rounded">AppTypography</code> এবং Flutter <code className="font-mono text-teal-800 bg-teal-50 px-1 py-0.5 rounded">ThemeData</code>-র মাধ্যমে নিয়ন্ত্রিত:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 text-slate-100 p-4 rounded-xl font-mono text-xs overflow-x-auto">
            <div className="text-slate-400 text-[10px] mb-2">// 1. AppTypography Central Definitions</div>
            <pre className="text-[11px] leading-relaxed text-teal-300">
{`class AppTypography {
  static const fontHindSiliguri = 'Hind Siliguri';
  static const fontBalooDa2 = 'Baloo Da 2';
  static const fontTiroBangla = 'Tiro Bangla';

  // Large Heading (Hind Siliguri)
  static const largeHeading1 = TextStyle(
    fontFamily: fontHindSiliguri,
    fontSize: 28,
    fontWeight: FontWeight.w700,
  );

  // Medium Heading (Baloo Da 2)
  static const mediumHeading1 = TextStyle(
    fontFamily: fontBalooDa2,
    fontSize: 18,
    fontWeight: FontWeight.w700,
  );

  // Body & Labels (Tiro Bangla)
  static const bodyMedium = TextStyle(
    fontFamily: fontTiroBangla,
    fontSize: 14,
    fontWeight: FontWeight.w400,
  );
}`}
            </pre>
          </div>

          <div className="bg-slate-900 text-slate-100 p-4 rounded-xl font-mono text-xs overflow-x-auto">
            <div className="text-slate-400 text-[10px] mb-2">// 2. Flutter ThemeData TextTheme Mapping</div>
            <pre className="text-[11px] leading-relaxed text-amber-300">
{`ThemeData get lightTheme {
  return ThemeData(
    useMaterial3: true,
    fontFamily: AppTypography.fontTiroBangla,
    textTheme: const TextTheme(
      // Hind Siliguri for large headers
      displayLarge: AppTypography.largeHeading1,
      headlineLarge: AppTypography.largeHeading2,
      
      // Baloo Da 2 for medium headings
      titleLarge: AppTypography.mediumHeading1,
      titleMedium: AppTypography.mediumHeading2,

      // Tiro Bangla for body, labels, forms
      bodyLarge: AppTypography.bodyLarge,
      bodyMedium: AppTypography.bodyMedium,
      labelLarge: AppTypography.label,
    ),
  );
}`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};
