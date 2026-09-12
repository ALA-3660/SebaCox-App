import React, { useState, useEffect } from 'react';
import { 
  Smartphone, 
  Wifi, 
  RefreshCw, 
  CheckCircle2, 
  XCircle, 
  Lock, 
  LogOut, 
  ShieldCheck, 
  Phone, 
  KeyRound, 
  ArrowRight, 
  User as UserIcon,
  Sparkles,
  MapPin,
  Search,
  Navigation,
  ChevronRight,
  ArrowLeft,
  Compass,
  Check,
  Type,
  Grid,
  Layers,
  Home,
  Package,
  Activity,
  Ticket,
  Truck,
  Coffee,
  Wrench,
  Anchor,
  AlertTriangle,
  Book,
  Monitor,
  DollarSign,
  Briefcase,
  X,
  SlidersHorizontal,
  Info,
  Calendar,
  CreditCard,
  MessageCircle,
  HelpCircle,
  ShoppingBag,
  ExternalLink,
  Building2
} from 'lucide-react';
import { StandardApiResponse } from '../types';
import { 
  INITIAL_46_TAXONOMY_CATEGORIES, 
  INITIAL_SERVICES, 
  MockCategory, 
  MockService 
} from '../data/taxonomyMockData';

type FlutterScreen = 'auth' | 'otp' | 'home' | 'location' | 'categories' | 'health';
type AuthMode = 'login' | 'register';

interface SelectedArea {
  id: number;
  name_bn: string;
  name_en: string;
  district_bn: string;
  district_en: string;
  full_address_bn: string;
  latitude: number;
  longitude: number;
}

const BANGLADESH_DIVISIONS = [
  { id: 1, name_bn: 'চট্টগ্রাম', name_en: 'Chattogram' },
  { id: 2, name_bn: 'ঢাকা', name_en: 'Dhaka' },
];

const BANGLADESH_DISTRICTS: Record<number, Array<{ id: number; name_bn: string; name_en: string }>> = {
  1: [
    { id: 1, name_bn: 'কক্সবাজার', name_en: "Cox's Bazar" },
    { id: 2, name_bn: 'চট্টগ্রাম', name_en: 'Chattogram' },
  ],
  2: [
    { id: 3, name_bn: 'ঢাকা', name_en: 'Dhaka' },
  ]
};

const BANGLADESH_UPAZILAS: Record<number, Array<{ id: number; name_bn: string; name_en: string; lat: number; lon: number }>> = {
  1: [
    { id: 1, name_bn: 'কক্সবাজার সদর', name_en: "Cox's Bazar Sadar", lat: 21.4272, lon: 92.0058 },
    { id: 2, name_bn: 'চকোরিয়া', name_en: 'Chakaria', lat: 21.7866, lon: 92.0778 },
    { id: 3, name_bn: 'মহেশখালী', name_en: 'Maheshkhali', lat: 21.5500, lon: 91.9500 },
    { id: 4, name_bn: 'রামু', name_en: 'Ramu', lat: 21.4500, lon: 92.1000 },
    { id: 5, name_bn: 'টেকনাফ', name_en: 'Teknaf', lat: 20.8583, lon: 92.2975 },
    { id: 6, name_bn: 'উখিয়া', name_en: 'Ukhiya', lat: 21.2833, lon: 92.1500 },
    { id: 7, name_bn: 'কুতুবদিয়া', name_en: 'Kutubdia', lat: 21.8167, lon: 91.8500 },
    { id: 8, name_bn: 'পেকুয়া', name_en: 'Pekua', lat: 21.8833, lon: 91.9833 },
    { id: 9, name_bn: 'ঈদগাঁও', name_en: 'Eidgaon', lat: 21.5583, lon: 92.0583 },
  ],
  2: [
    { id: 10, name_bn: 'পটিয়া', name_en: 'Patiya', lat: 22.2961, lon: 91.9803 },
    { id: 11, name_bn: 'হাটহাজারী', name_en: 'Hathazari', lat: 22.5083, lon: 91.8083 },
  ],
  3: [
    { id: 12, name_bn: 'ধানমন্ডি', name_en: 'Dhanmondi', lat: 23.7465, lon: 90.3760 },
    { id: 13, name_bn: 'গুলশান', name_en: 'Gulshan', lat: 23.7925, lon: 90.4078 },
  ]
};

export const FlutterSimulator: React.FC = () => {
  // Navigation & Screen state
  const [activeScreen, setActiveScreen] = useState<FlutterScreen>('home');
  const [authMode, setAuthMode] = useState<AuthMode>('login');
  
  // Form state
  const [phone, setPhone] = useState<string>('01712345678');
  const [otp, setOtp] = useState<string>('123456');
  const [devOtp, setDevOtp] = useState<string | null>('123456');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [infoMessage, setInfoMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [countdown, setCountdown] = useState<number>(60);

  // Authenticated session state (pre-initialized to verified user for seamless testing)
  const [currentUser, setCurrentUser] = useState<{ id: number; mobile_number: string; is_verified: boolean } | null>({
    id: 1,
    mobile_number: '+8801712345678',
    is_verified: true
  });
  const [accessToken, setAccessToken] = useState<string | null>('mock_jwt_access_sebacox_active_session');
  const [refreshToken, setRefreshToken] = useState<string | null>('mock_jwt_refresh_sebacox_active_session');

  // Phase 3 Location State
  const [selectedArea, setSelectedArea] = useState<SelectedArea>({
    id: 1,
    name_bn: 'কক্সবাজার সদর',
    name_en: "Cox's Bazar Sadar",
    district_bn: 'কক্সবাজার',
    district_en: "Cox's Bazar",
    full_address_bn: 'কক্সবাজার সদর, কক্সবাজার',
    latitude: 21.4272,
    longitude: 92.0058
  });

  const [currentGps, setCurrentGps] = useState<{
    latitude: number;
    longitude: number;
    address_bn: string;
    distance_km: number;
  } | null>(null);
  const [gpsLoading, setGpsLoading] = useState<boolean>(false);
  const [locTab, setLocTab] = useState<'hierarchy' | 'search'>('hierarchy');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [showTypographyLabels, setShowTypographyLabels] = useState<boolean>(false);
  
  // Administrative selection drilldown
  const [selDivId, setSelDivId] = useState<number>(1);
  const [selDistId, setSelDistId] = useState<number>(1);

  // Health check state (Phase 1 retained)
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [healthLoading, setHealthLoading] = useState<boolean>(false);

  // Timer countdown
  useEffect(() => {
    let timer: any;
    if (activeScreen === 'otp' && countdown > 0) {
      timer = setInterval(() => {
        setCountdown((prev) => (prev > 0 ? prev - 1 : 0));
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [activeScreen, countdown]);

  // Request OTP
  const handleRequestOtp = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    setInfoMessage(null);

    const endpoint = authMode === 'login' 
      ? '/api/v1/auth/login/request-otp' 
      : '/api/v1/auth/register/request-otp';

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile_number: phone }),
      });
      const data: StandardApiResponse = await res.json();

      if (res.ok && data.success) {
        setDevOtp(data.data?.dev_otp || '123456');
        setOtp(data.data?.dev_otp || '123456');
        setCountdown(60);
        setActiveScreen('otp');
        setInfoMessage('ওটিপি পাঠানো হয়েছে');
      } else {
        setErrorMessage(data.message || 'ওটিপি পাঠাতে সমস্যা হয়েছে।');
      }
    } catch (err: any) {
      setErrorMessage('সার্ভার সংযোগ ত্রুটি: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Verify OTP
  const handleVerifyOtp = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    setInfoMessage(null);

    const endpoint = authMode === 'login' 
      ? '/api/v1/auth/login/verify-otp' 
      : '/api/v1/auth/register/verify-otp';

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile_number: phone, otp_code: otp }),
      });
      const data: StandardApiResponse = await res.json();

      if (res.ok && data.success) {
        setCurrentUser(data.data.user);
        setAccessToken(data.data.tokens.access_token);
        setRefreshToken(data.data.tokens.refresh_token);
        setActiveScreen('home');
      } else {
        setErrorMessage(data.message || 'ভুল ওটিপি কোড।');
      }
    } catch (err: any) {
      setErrorMessage('নেটওয়ার্ক সংযোগ ত্রুটি: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Token Refresh test
  const handleRefreshToken = async () => {
    if (!refreshToken) return;
    setIsLoading(true);
    try {
      const res = await fetch('/api/v1/auth/token/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setAccessToken(data.data.access_token);
        setInfoMessage('টোকেন সফলভাবে রিফ্রেশ হয়েছে!');
      } else {
        setErrorMessage('টোকেন রিফ্রেশ ব্যর্থ: ' + data.message);
      }
    } catch (e: any) {
      setErrorMessage('ত্রুটি: ' + e.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Logout
  const handleLogout = async () => {
    setIsLoading(true);
    try {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
    } catch (_) {
      // Ignored
    } finally {
      setCurrentUser(null);
      setAccessToken(null);
      setRefreshToken(null);
      setActiveScreen('auth');
      setIsLoading(false);
      setInfoMessage('লগআউট সম্পন্ন হয়েছে।');
    }
  };

  // Health check
  const runHealthCheck = async () => {
    setHealthLoading(true);
    try {
      const res = await fetch('/api/v1/health');
      const data = await res.json();
      setHealthStatus(data);
    } catch (e) {
      setHealthStatus({ success: false, message: 'সার্ভার অফলাইন' });
    } finally {
      setHealthLoading(false);
    }
  };

  // Phase 3 Location Handlers
  const handleDetectGps = async () => {
    setGpsLoading(true);
    setErrorMessage(null);
    try {
      const res = await fetch('/api/v1/locations/reverse-geocode?lat=21.4272&lon=92.0058');
      const json = await res.json();
      if (json.success) {
        setCurrentGps({
          latitude: json.data.latitude,
          longitude: json.data.longitude,
          address_bn: json.data.address_bn,
          distance_km: 1.2
        });
        setInfoMessage('জিপিএস অবস্থান সফলভাবে শনাক্ত হয়েছে!');
      } else {
        setErrorMessage('জিপিএস শনাক্ত ব্যর্থ হয়েছে।');
      }
    } catch (err: any) {
      setErrorMessage('জিপিএস নেটওয়ার্ক ত্রুটি: ' + err.message);
    } finally {
      setGpsLoading(false);
    }
  };

  const handleApplyGpsAsServiceArea = async () => {
    if (!currentGps) return;
    setSelectedArea({
      id: 99,
      name_bn: 'কলাতলী বিচ',
      name_en: 'Kolatoli Beach',
      district_bn: 'কক্সবাজার',
      district_en: "Cox's Bazar",
      full_address_bn: currentGps.address_bn,
      latitude: currentGps.latitude,
      longitude: currentGps.longitude
    });
    try {
      await fetch('/api/v1/locations/context', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location_type: 'SELECTED',
          address_text: currentGps.address_bn,
          latitude: currentGps.latitude,
          longitude: currentGps.longitude
        })
      });
    } catch (e) {
      // preview resilient
    }
    setActiveScreen('home');
    setInfoMessage('সেবা এলাকা হিসেবে জিপিএস অবস্থান নির্ধারিত হয়েছে!');
  };

  const handleSelectUpazila = async (upz: { id: number; name_bn: string; name_en: string; lat: number; lon: number }) => {
    const dist = (BANGLADESH_DISTRICTS[selDivId] || []).find(d => d.id === selDistId);
    const distName = dist ? dist.name_bn : 'কক্সবাজার';
    const distNameEn = dist ? dist.name_en : "Cox's Bazar";

    setSelectedArea({
      id: upz.id,
      name_bn: upz.name_bn,
      name_en: upz.name_en,
      district_bn: distName,
      district_en: distNameEn,
      full_address_bn: `${upz.name_bn}, ${distName}`,
      latitude: upz.lat,
      longitude: upz.lon
    });

    try {
      await fetch('/api/v1/locations/context', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location_type: 'SELECTED',
          address_text: `${upz.name_bn}, ${distName}`,
          upazila_id: upz.id,
          district_id: selDistId,
          latitude: upz.lat,
          longitude: upz.lon
        })
      });
    } catch (e) {
      // preview resilient
    }

    setActiveScreen('home');
    setInfoMessage(`সেবা এলাকা ${upz.name_bn} নির্ধারিত হয়েছে!`);
  };

  const allUpazilasForSearch = Object.values(BANGLADESH_UPAZILAS).flat();
  const searchResults = searchQuery.trim()
    ? allUpazilasForSearch.filter(u => 
        u.name_bn.toLowerCase().includes(searchQuery.toLowerCase()) ||
        u.name_en.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : [];

  // Helper for visualizing Global Bangla Typography Standard
  const TypoTag: React.FC<{ font: 'hind' | 'baloo' | 'tiro'; role: string }> = ({ font, role }) => {
    if (!showTypographyLabels) return null;
    const styles = {
      hind: 'bg-teal-700 text-white',
      baloo: 'bg-amber-600 text-white',
      tiro: 'bg-blue-600 text-white'
    };
    const names = {
      hind: 'Hind Siliguri',
      baloo: 'Baloo Da 2',
      tiro: 'Tiro Bangla'
    };
    return (
      <span className={`inline-block ml-1 px-1 py-0.2 rounded text-[7px] font-mono font-bold tracking-tight uppercase shadow-xs ${styles[font]}`}>
        {names[font]} • {role}
      </span>
    );
  };

  return (
    <div className="flex flex-col xl:flex-row gap-6 items-center justify-center p-2">
      {/* Mobile Device Mockup */}
      <div className="relative w-full max-w-[340px] bg-slate-950 rounded-[44px] p-3 shadow-2xl border-4 border-slate-800">
        {/* Dynamic Island / Speaker notch */}
        <div className="absolute top-5 left-1/2 -translate-x-1/2 w-28 h-5 bg-black rounded-full z-20 flex items-center justify-center">
          <div className="w-2.5 h-2.5 bg-slate-800 rounded-full mr-2"></div>
          <div className="w-10 h-1 bg-slate-800 rounded-full"></div>
        </div>

        {/* Screen Content */}
        <div className="w-full bg-slate-50 rounded-[34px] overflow-hidden flex flex-col min-h-[600px] max-h-[600px] text-slate-800 font-tiro select-none">
          {/* Mobile Status Bar */}
          <div className="pt-3 px-6 pb-2 flex justify-between items-center text-xs font-semibold text-slate-500 bg-white border-b border-slate-100 font-mono">
            <span>09:41</span>
            <div className="flex items-center gap-1.5">
              <Wifi className="w-3.5 h-3.5" />
              <div className="w-4 h-2.5 border border-slate-500 rounded-xs relative">
                <div className="h-full bg-slate-500 w-3/4"></div>
              </div>
            </div>
          </div>

          {/* App Header with LocationHeaderChip */}
          <div className="bg-white px-3 py-2 border-b border-slate-200 flex items-center justify-between gap-2">
            <div className="flex items-center gap-1.5 min-w-0">
              <div className="w-6 h-6 rounded-md bg-teal-700 text-white flex items-center justify-center text-[10px] font-black shrink-0 font-hind">
                SC
              </div>
              <div className="flex items-center">
                <h1 className="text-xs font-bold tracking-tight text-teal-900 shrink-0 font-hind">সেবাকক্স</h1>
                <TypoTag font="hind" role="Brand Title" />
              </div>
            </div>

            {/* Location Header Chip */}
            <button
              onClick={() => setActiveScreen(activeScreen === 'location' ? 'home' : 'location')}
              className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-teal-50 border border-teal-200 text-teal-900 text-[10px] font-bold hover:bg-teal-100 transition cursor-pointer max-w-[130px] truncate font-baloo"
              title="সেবা এলাকা পরিবর্তন করুন"
            >
              <MapPin className="w-3 h-3 text-teal-700 shrink-0" />
              <span className="truncate font-baloo">{selectedArea.name_bn}</span>
            </button>

            <div className="flex items-center gap-1 shrink-0">
              <button
                onClick={() => {
                  if (activeScreen === 'health') {
                    setActiveScreen(currentUser ? 'home' : 'auth');
                  } else {
                    setActiveScreen('health');
                    runHealthCheck();
                  }
                }}
                className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full border cursor-pointer font-baloo ${
                  activeScreen === 'health'
                    ? 'bg-teal-700 text-white border-teal-800'
                    : 'bg-slate-100 text-slate-600 border-slate-200'
                }`}
              >
                {activeScreen === 'health' ? 'হোম' : 'Health'}
              </button>
            </div>
          </div>

          {/* Screen Body */}
          <div className="flex-1 overflow-y-auto p-4 flex flex-col justify-between">
            {/* 1. HEALTH CHECK SCREEN (Phase 1 legacy preserved) */}
            {activeScreen === 'health' && (
              <div className="flex flex-col gap-4 py-4">
                <div className="text-center">
                  <h2 className="text-base font-bold text-slate-900">Phase 1 Health Status</h2>
                  <p className="text-xs text-slate-500">API Endpoint: /api/v1/health/</p>
                </div>
                <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-xs">
                  {healthLoading ? (
                    <div className="flex justify-center py-6 text-teal-700">
                      <RefreshCw className="w-6 h-6 animate-spin" />
                    </div>
                  ) : healthStatus ? (
                    <div className="space-y-2 text-xs">
                      <div className="flex items-center gap-2 text-emerald-600 font-bold">
                        <CheckCircle2 className="w-4 h-4" />
                        <span>Status: {healthStatus.data?.status || 'OK'}</span>
                      </div>
                      <div className="text-slate-600">Phase: {healthStatus.data?.phase || 'Active'}</div>
                      <div className="text-slate-500">{healthStatus.message}</div>
                    </div>
                  ) : (
                    <div className="text-xs text-slate-500 text-center py-4">পরীক্ষা করতে নিচে চাপুন</div>
                  )}
                </div>
                <button
                  onClick={runHealthCheck}
                  className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>পুনরায় স্বাস্থ্য পরীক্ষা করুন</span>
                </button>
              </div>
            )}

            {/* 2. AUTH SCREEN (Phone entry: Login / Register) */}
            {activeScreen === 'auth' && (
              <div className="flex flex-col gap-4">
                {/* Brand Banner */}
                <div className="text-center pt-2">
                  <span className="text-xs text-teal-700 font-bold bg-teal-50 px-2.5 py-0.5 rounded-full border border-teal-200 font-baloo">
                    Phase 2 — প্রমাণীকরণ
                  </span>
                  <div className="flex items-center justify-center mt-2">
                    <h2 className="text-lg font-black text-slate-900 font-hind">
                      {authMode === 'login' ? 'অ্যাকাউন্টে লগইন' : 'নতুন অ্যাকাউন্ট তৈরি'}
                    </h2>
                    <TypoTag font="hind" role="Large Heading" />
                  </div>
                  <p className="text-[11px] text-slate-500 italic mt-0.5 font-tiro">
                    “মানুষের প্রয়োজন থেকে সেবার সমাধান।”
                  </p>
                </div>

                {/* Mode Selector */}
                <div className="grid grid-cols-2 p-1 bg-slate-200/70 rounded-xl text-xs font-bold font-baloo">
                  <button
                    onClick={() => { setAuthMode('login'); setErrorMessage(null); }}
                    className={`py-1.5 rounded-lg transition cursor-pointer font-baloo ${
                      authMode === 'login' ? 'bg-white text-teal-800 shadow-xs' : 'text-slate-600'
                    }`}
                  >
                    লগইন
                  </button>
                  <button
                    onClick={() => { setAuthMode('register'); setErrorMessage(null); }}
                    className={`py-1.5 rounded-lg transition cursor-pointer font-baloo ${
                      authMode === 'register' ? 'bg-white text-teal-800 shadow-xs' : 'text-slate-600'
                    }`}
                  >
                    নতুন নিবন্ধন
                  </button>
                </div>

                {/* Form */}
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1 font-tiro">
                      মোবাইল নম্বর দিন
                      <TypoTag font="tiro" role="Form Label" />
                    </label>
                    <div className="flex rounded-xl border border-slate-300 bg-white overflow-hidden focus-within:border-teal-700 focus-within:ring-1 focus-within:ring-teal-700">
                      <div className="px-2.5 py-2 bg-slate-100 border-r border-slate-200 text-xs font-bold text-teal-800 flex items-center font-mono">
                        +88
                      </div>
                      <input
                        type="tel"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        placeholder="017XXXXXXXX"
                        className="w-full px-3 py-2 text-xs font-semibold focus:outline-none font-tiro"
                      />
                    </div>
                    <p className="text-[10px] text-slate-400 mt-1 font-tiro">
                      গ্রাহক, ড্রাইভার, হোটেল বা সেবা সরবরাহকারী সবার জন্য একটি নম্বর
                    </p>
                  </div>

                  {errorMessage && (
                    <div className="p-2.5 rounded-lg bg-rose-50 border border-rose-200 text-[11px] text-rose-700 font-medium font-tiro">
                      {errorMessage}
                    </div>
                  )}

                  {infoMessage && (
                    <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-[11px] text-emerald-700 font-medium font-tiro">
                      {infoMessage}
                    </div>
                  )}

                  <button
                    id="sim-request-otp"
                    onClick={handleRequestOtp}
                    disabled={isLoading}
                    className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold shadow-xs transition flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50 font-baloo"
                  >
                    {isLoading ? (
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <>
                        <span className="font-baloo">ওটিপি পাঠান</span>
                        <TypoTag font="baloo" role="Button" />
                        <ArrowRight className="w-3.5 h-3.5" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}

            {/* 3. OTP VERIFICATION SCREEN */}
            {activeScreen === 'otp' && (
              <div className="flex flex-col gap-4 font-tiro">
                <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl">
                  <div className="flex items-center gap-2 text-emerald-800 font-bold text-xs font-baloo">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span className="font-baloo">ওটিপি পাঠানো হয়েছে</span>
                    <TypoTag font="baloo" role="Card Heading" />
                  </div>
                  <div className="text-[11px] text-emerald-700 mt-0.5 font-tiro">
                    নম্বর: <span className="font-bold font-mono">{phone}</span>
                  </div>
                </div>

                {devOtp && (
                  <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-amber-800 flex items-center justify-between">
                    <span className="text-[11px] font-medium font-tiro">ডেভ টেস্ট কোড:</span>
                    <span className="font-mono font-bold text-xs bg-amber-200 px-2 py-0.5 rounded">
                      {devOtp}
                    </span>
                  </div>
                )}

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1 text-center font-tiro">
                    ওটিপি লিখুন (৬ অঙ্কের কোড)
                    <TypoTag font="tiro" role="Form Label" />
                  </label>
                  <input
                    type="text"
                    maxLength={6}
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    placeholder="123456"
                    className="w-full py-2 text-center text-xl font-mono tracking-widest font-black rounded-xl border border-slate-300 bg-white focus:outline-none focus:border-teal-700 focus:ring-1 focus:ring-teal-700"
                  />
                </div>

                {errorMessage && (
                  <div className="p-2.5 rounded-lg bg-rose-50 border border-rose-200 text-[11px] text-rose-700 font-medium font-tiro">
                    {errorMessage}
                  </div>
                )}

                <button
                  id="sim-verify-otp"
                  onClick={handleVerifyOtp}
                  disabled={isLoading}
                  className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold shadow-xs transition flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50 font-baloo"
                >
                  {isLoading ? (
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <>
                      <span className="font-baloo">যাচাই করুন</span>
                      <TypoTag font="baloo" role="Button" />
                    </>
                  )}
                </button>

                <div className="text-center font-tiro">
                  {countdown > 0 ? (
                    <p className="text-[11px] text-slate-500 font-tiro">
                      পুনরায় পাঠাতে অপেক্ষা করুন: <span className="font-bold font-mono">{countdown}</span> সেকেন্ড
                    </p>
                  ) : (
                    <button
                      onClick={handleRequestOtp}
                      className="text-[11px] font-bold text-teal-700 hover:underline cursor-pointer font-baloo"
                    >
                      আবার ওটিপি পাঠান
                    </button>
                  )}
                </div>

                <button
                  onClick={() => setActiveScreen('auth')}
                  className="text-[10px] text-slate-500 hover:text-slate-700 text-center cursor-pointer font-tiro"
                >
                  ← নম্বর পরিবর্তন করুন
                </button>
              </div>
            )}

            {/* 4. AUTHENTICATED SCREEN */}
            {activeScreen === 'home' && currentUser && (
              <div className="flex flex-col gap-3 font-tiro">
                {/* Location Selection Card (Phase 3 Core Integration) */}
                <div className="p-3 bg-teal-50/80 border border-teal-200 rounded-xl space-y-2 shadow-xs">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5">
                      <span className="p-1 bg-teal-600 text-white rounded-md">
                        <MapPin className="w-3.5 h-3.5" />
                      </span>
                      <span className="text-xs font-bold text-teal-900 font-baloo">নির্বাচিত সেবা এলাকা</span>
                      <TypoTag font="baloo" role="Card Heading" />
                    </div>
                    <span className="text-[9px] bg-teal-200/70 text-teal-900 font-bold px-1.5 py-0.5 rounded font-baloo">
                      সক্রিয় এলাকা
                    </span>
                  </div>

                  <div>
                    <div className="text-xs font-bold text-slate-800 font-tiro">
                      {selectedArea.full_address_bn}
                    </div>
                    <div className="text-[10px] text-slate-500 font-mono mt-0.5">
                      SRID 4326: {selectedArea.latitude.toFixed(4)}° N, {selectedArea.longitude.toFixed(4)}° E
                    </div>
                  </div>

                  <button
                    onClick={() => setActiveScreen('location')}
                    className="w-full py-1.5 bg-teal-700 hover:bg-teal-800 text-white rounded-lg text-[11px] font-bold transition flex items-center justify-center gap-1 cursor-pointer shadow-xs font-baloo"
                  >
                    <span className="font-baloo">অবস্থান বা উপজেলা পরিবর্তন করুন</span>
                    <TypoTag font="baloo" role="Button" />
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>

                {/* GPS Current Location (Decoupled Demonstration) */}
                {currentGps && (
                  <div className="p-2.5 bg-blue-50 border border-blue-200 rounded-xl text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-blue-900 flex items-center gap-1 text-[11px] font-baloo">
                        <Navigation className="w-3 h-3 text-blue-600" /> বর্তমান জিপিএস অবস্থান
                        <TypoTag font="baloo" role="Sub-heading" />
                      </span>
                      <span className="text-[9px] bg-blue-100 text-blue-800 px-1 py-0.5 rounded font-bold font-baloo">
                        পৃথক কনটেক্সট
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-700 font-tiro">{currentGps.address_bn}</div>
                    <div className="text-[10px] text-slate-500 font-tiro">
                      দূরত্ব: সেবা এলাকা হতে {currentGps.distance_km} কিমি (Haversine)
                    </div>
                  </div>
                )}

                {/* Profile Card */}
                <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-xs space-y-1.5">
                  <h4 className="text-xs font-bold text-slate-800 border-b border-slate-100 pb-1 flex items-center justify-between font-baloo">
                    <span className="flex items-center gap-1">
                      <UserIcon className="w-3.5 h-3.5 text-teal-700" />
                      <span className="font-baloo">প্রোফাইল সেশন</span>
                    </span>
                    <span className="text-[10px] text-emerald-700 font-bold bg-emerald-50 px-1.5 py-0.2 rounded border border-emerald-200">
                      Active
                    </span>
                  </h4>
                  <div className="flex justify-between text-[11px] font-tiro">
                    <span className="text-slate-500 font-tiro">মোবাইল:</span>
                    <span className="font-semibold text-slate-800 font-mono">{currentUser.mobile_number}</span>
                  </div>
                </div>

                {/* Security and Token testing controls */}
                <div className="bg-slate-100/80 p-2.5 rounded-xl space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-slate-600 flex items-center gap-1 font-baloo">
                      <KeyRound className="w-3 h-3" /> JWT সেশন
                    </span>
                    <span className="text-[9px] bg-teal-100 text-teal-800 px-1.5 py-0.5 rounded font-mono">
                      HMAC-SHA256
                    </span>
                  </div>
                  <button
                    onClick={handleRefreshToken}
                    disabled={isLoading}
                    className="w-full py-1 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-lg text-[10px] font-bold transition flex items-center justify-center gap-1 cursor-pointer font-baloo"
                  >
                    <RefreshCw className={`w-3 h-3 ${isLoading ? 'animate-spin' : ''}`} />
                    <span className="font-baloo">টোকেন রিফ্রেশ টেস্ট</span>
                  </button>
                </div>

                {/* Logout Button */}
                <button
                  id="sim-logout"
                  onClick={handleLogout}
                  className="w-full py-1.5 border border-rose-200 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer font-baloo"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span className="font-baloo">লগআউট</span>
                  <TypoTag font="baloo" role="Button" />
                </button>
              </div>
            )}

            {/* 5. LOCATION SELECTION SCREEN (Phase 3 Interactive) */}
            {activeScreen === 'location' && (
              <div className="flex flex-col gap-3 py-1 font-tiro">
                {/* Header */}
                <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                  <button
                    onClick={() => setActiveScreen(currentUser ? 'home' : 'auth')}
                    className="flex items-center gap-1 text-xs text-slate-600 hover:text-slate-900 font-bold cursor-pointer font-baloo"
                  >
                    <ArrowLeft className="w-3.5 h-3.5" />
                    <span className="font-baloo">ফিরে যান</span>
                  </button>
                  <div className="flex items-center">
                    <span className="text-xs font-bold text-slate-900 font-hind">অবস্থান নির্বাচন</span>
                    <TypoTag font="hind" role="Page Title" />
                  </div>
                </div>

                {/* GPS Detection Action Card */}
                <div className="p-2.5 bg-blue-50/70 border border-blue-200 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-blue-900 flex items-center gap-1 font-baloo">
                      <Navigation className="w-3.5 h-3.5 text-blue-600" />
                      <span className="font-baloo">জিপিএস অটো-ডিটেকশন</span>
                      <TypoTag font="baloo" role="Card Heading" />
                    </span>
                    <button
                      onClick={handleDetectGps}
                      disabled={gpsLoading}
                      className="px-2 py-0.5 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-[10px] font-bold transition flex items-center gap-1 cursor-pointer font-baloo"
                    >
                      {gpsLoading ? <RefreshCw className="w-3 h-3 animate-spin" /> : 'শনাক্ত করুন'}
                    </button>
                  </div>
                  {currentGps ? (
                    <div className="space-y-1 pt-1 border-t border-blue-200/60 font-tiro">
                      <div className="text-[11px] text-blue-900 font-medium font-tiro">
                        📍 {currentGps.address_bn}
                      </div>
                      <button
                        onClick={handleApplyGpsAsServiceArea}
                        className="w-full py-1 bg-blue-700 hover:bg-blue-800 text-white rounded text-[10px] font-bold transition cursor-pointer font-baloo"
                      >
                        ✓ এটি সেবা এলাকা হিসেবে সেট করুন
                      </button>
                    </div>
                  ) : (
                    <p className="text-[10px] text-blue-700 font-tiro">
                      ডিভাইসের বর্তমান জিপিএস অবস্থান নির্ণয় করতে বোতামে চাপুন।
                    </p>
                  )}
                </div>

                {/* Tab Switcher: Hierarchy vs Search */}
                <div className="flex bg-slate-200 p-0.5 rounded-lg text-xs font-bold font-baloo">
                  <button
                    onClick={() => setLocTab('hierarchy')}
                    className={`flex-1 py-1 rounded-md transition cursor-pointer font-baloo ${
                      locTab === 'hierarchy' ? 'bg-white text-teal-900 shadow-xs' : 'text-slate-600'
                    }`}
                  >
                    প্রশাসনিক স্তর
                  </button>
                  <button
                    onClick={() => setLocTab('search')}
                    className={`flex-1 py-1 rounded-md transition cursor-pointer font-baloo ${
                      locTab === 'search' ? 'bg-white text-teal-900 shadow-xs' : 'text-slate-600'
                    }`}
                  >
                    অনুসন্ধান
                  </button>
                </div>

                {/* Tab 1: Administrative Hierarchy Drilldown */}
                {locTab === 'hierarchy' && (
                  <div className="space-y-2 text-xs font-tiro">
                    {/* Country & Division Selectors */}
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <label className="text-[10px] text-slate-500 font-bold block mb-0.5 font-tiro">বিভাগ</label>
                        <select
                          value={selDivId}
                          onChange={(e) => {
                            const div = Number(e.target.value);
                            setSelDivId(div);
                            const firstDist = (BANGLADESH_DISTRICTS[div] || [])[0]?.id || 1;
                            setSelDistId(firstDist);
                          }}
                          className="w-full bg-white border border-slate-300 rounded-lg p-1.5 text-xs font-medium font-tiro"
                        >
                          {BANGLADESH_DIVISIONS.map(d => (
                            <option key={d.id} value={d.id}>{d.name_bn}</option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="text-[10px] text-slate-500 font-bold block mb-0.5 font-tiro">জেলা</label>
                        <select
                          value={selDistId}
                          onChange={(e) => setSelDistId(Number(e.target.value))}
                          className="w-full bg-white border border-slate-300 rounded-lg p-1.5 text-xs font-medium font-tiro"
                        >
                          {(BANGLADESH_DISTRICTS[selDivId] || []).map(d => (
                            <option key={d.id} value={d.id}>{d.name_bn}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    {/* Upazila Selection List */}
                    <div>
                      <label className="text-[10px] text-slate-500 font-bold block mb-1 font-tiro">
                        উপজেলা নির্বাচন করুন ({(BANGLADESH_UPAZILAS[selDistId] || []).length === 9 ? '৯টি' : (BANGLADESH_UPAZILAS[selDistId] || []).length + 'টি'} এলাকা উপলব্ধ)
                        <TypoTag font="tiro" role="Label" />
                      </label>
                      <div className="max-h-48 overflow-y-auto space-y-1 pr-1">
                        {(BANGLADESH_UPAZILAS[selDistId] || []).map((u) => {
                          const isSelected = selectedArea.id === u.id && selectedArea.name_bn === u.name_bn;
                          return (
                            <button
                              key={u.id}
                              onClick={() => handleSelectUpazila(u)}
                              className={`w-full p-2 rounded-xl text-left flex items-center justify-between border transition cursor-pointer ${
                                isSelected
                                  ? 'bg-teal-50 border-teal-500 text-teal-900 font-bold'
                                  : 'bg-white border-slate-200 hover:border-teal-300 text-slate-700'
                              }`}
                            >
                              <div>
                                <div className="text-xs font-tiro">{u.name_bn}</div>
                                <div className="text-[10px] text-slate-400 font-mono">{u.name_en}</div>
                              </div>
                              {isSelected ? (
                                <span className="p-0.5 bg-teal-600 text-white rounded-full">
                                  <Check className="w-3 h-3" />
                                </span>
                              ) : (
                                <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
                              )}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                )}

                {/* Tab 2: Live Location Search */}
                {locTab === 'search' && (
                  <div className="space-y-2 text-xs">
                    <div className="relative">
                      <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
                      <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="যেমন: ঈদগাঁও, চকোরিয়া, টেকনাফ, Sadar..."
                        className="w-full pl-8 pr-3 py-1.5 bg-white border border-slate-300 rounded-xl text-xs focus:outline-teal-700 font-tiro"
                      />
                    </div>

                    <div className="max-h-48 overflow-y-auto space-y-1">
                      {searchResults.length > 0 ? (
                        searchResults.map(u => (
                          <button
                            key={u.id}
                            onClick={() => handleSelectUpazila(u)}
                            className="w-full p-2 bg-white border border-slate-200 hover:border-teal-400 rounded-xl text-left flex items-center justify-between cursor-pointer"
                          >
                            <div>
                              <div className="text-xs font-bold text-slate-800 font-tiro">{u.name_bn}</div>
                              <div className="text-[10px] text-slate-400 font-mono">{u.name_en}</div>
                            </div>
                            <span className="text-[10px] bg-teal-50 text-teal-700 px-2 py-0.5 rounded font-bold font-tiro">
                              বাছাই করুন
                            </span>
                          </button>
                        ))
                      ) : (
                        <div className="text-center py-6 text-slate-400 text-xs">
                          {searchQuery ? 'কোনো এলাকা পাওয়া যায়নি' : 'উপজেলার নাম বাংলায় বা ইংরেজিতে খুঁজুন'}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Scope & Privacy Guarantee Footer */}
                <div className="p-2 bg-slate-100 rounded-lg text-[9px] text-slate-600 leading-tight">
                  🔒 <strong>নিরাপত্তা নীতি:</strong> জিপিএস অবস্থান এবং নির্বাচিত সেবা এলাকা পৃথক রাখা হয়। ব্যবহারকারীর সম্মতি ব্যতিরেকে সেবা এলাকা পরিবর্তন করা হয় না।
                </div>
              </div>
            )}

            {/* Bottom watermark */}
            <div className="pt-2 text-center text-[10px] text-slate-400">
              SebaCox Flutter Engine • SRID 4326 Geo-Foundation
            </div>
          </div>
        </div>
      </div>

      {/* Side Explanations & Controls */}
      <div className="flex-1 max-w-xl flex flex-col gap-4">
        {/* Phase 3 Status Banner */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2 text-teal-900 font-black text-base">
              <Compass className="w-5 h-5 text-teal-700" />
              <span>Phase 3 Location & Geographic Verification</span>
            </div>
            <span className="bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10px] font-bold px-2 py-0.5 rounded-full">
              Phase 3 Active
            </span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Test the complete location lifecycle: hierarchical drilldown (Country → Division → District → Upazila), live bilingual search, separate device GPS vs selected service area, and SRID 4326 geospatial storage.
          </p>

          <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="font-bold text-slate-800">Current GPS ≠ Service Area</div>
              <div className="text-[11px] text-slate-500 mt-1">
                Strict separation ensures moving users never have their selected service area overwritten without explicit consent.
              </div>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="font-bold text-slate-800">SRID 4326 Coordinates</div>
              <div className="text-[11px] text-slate-500 mt-1">
                WGS 84 global standard coordinates with Haversine great-circle distance & bounding box filters.
              </div>
            </div>
          </div>
        </div>

        {/* Phase 3 Location State Inspector */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-teal-700" />
              <span>Active Location Profile Inspector</span>
            </h4>
            <span className="text-[10px] font-mono bg-teal-50 text-teal-800 px-2 py-0.5 rounded border border-teal-200 font-bold">
              apps.locations.UserLocation
            </span>
          </div>

          <div className="space-y-2 text-xs">
            <div className="bg-slate-50 p-2.5 rounded-lg space-y-1">
              <div className="flex justify-between items-center text-slate-500">
                <span>Selected Service Area (type=SELECTED):</span>
                <span className="text-[9px] bg-emerald-100 text-emerald-800 px-1.5 py-0.2 rounded font-bold">Active</span>
              </div>
              <div className="font-bold text-slate-800 text-[11px]">
                {selectedArea.full_address_bn} ({selectedArea.name_en})
              </div>
              <div className="font-mono text-[10px] text-slate-500">
                Lat: {selectedArea.latitude.toFixed(6)}, Lon: {selectedArea.longitude.toFixed(6)} [SRID 4326]
              </div>
            </div>

            <div className="bg-slate-50 p-2.5 rounded-lg space-y-1">
              <div className="flex justify-between items-center text-slate-500">
                <span>Current GPS Position (type=CURRENT):</span>
                <span className={`text-[9px] px-1.5 py-0.2 rounded font-bold ${
                  currentGps ? 'bg-blue-100 text-blue-800' : 'bg-slate-200 text-slate-600'
                }`}>
                  {currentGps ? 'Detected' : 'Not Requested'}
                </span>
              </div>
              <div className="text-[11px] text-slate-700">
                {currentGps ? currentGps.address_bn : 'No GPS coordinate broadcasted'}
              </div>
            </div>
          </div>
        </div>

        {/* Global Bangla Typography Standard Inspector */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5 font-hind">
              <Type className="w-4 h-4 text-teal-700" />
              <span>গ্লোবাল বাংলা টাইপোগ্রাফি স্ট্যান্ডার্ড (Global Typography)</span>
            </h4>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-teal-100 text-teal-800 border border-teal-200">
              Enforced
            </span>
          </div>

          <p className="text-xs text-slate-600 mb-3 font-tiro leading-relaxed">
            SebaCox-এর সকল ইউজার ইন্টারফেসে ৩টি নির্ধারিত ফন্ট সুনির্দিষ্ট অনুক্রমে ব্যবহার করা বাধ্যতামূলক। নিচে লাইভ টগল করে সিমুলেটরে ফন্ট ট্যাগসমূহ পর্যবেক্ষণ করুন:
          </p>

          <div className="flex items-center justify-between p-3 bg-slate-50 border border-slate-200 rounded-xl mb-3">
            <div className="text-xs">
              <div className="font-bold text-slate-800 font-baloo">সিমুলেটরে ফন্ট ট্যাগ হাইলাইট</div>
              <div className="text-[11px] text-slate-500 font-tiro">প্রতিটি শিরোনাম ও টেক্সটের পাশে ফন্টের নাম দেখাবে</div>
            </div>
            <button
              onClick={() => setShowTypographyLabels(!showTypographyLabels)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition cursor-pointer font-baloo flex items-center gap-1.5 ${
                showTypographyLabels
                  ? 'bg-teal-700 text-white shadow-xs'
                  : 'bg-slate-200 hover:bg-slate-300 text-slate-700'
              }`}
            >
              <Type className="w-3.5 h-3.5" />
              <span>{showTypographyLabels ? 'ট্যাগ লুকান' : 'ট্যাগ দেখান'}</span>
            </button>
          </div>

          <div className="space-y-2 text-xs">
            <div className="p-2.5 rounded-xl border border-teal-200 bg-teal-50/50 flex items-start gap-2.5">
              <span className="px-2 py-0.5 rounded text-[10px] font-bold font-mono bg-teal-700 text-white shrink-0 mt-0.5">
                Hind Siliguri
              </span>
              <div className="min-w-0 font-tiro">
                <div className="font-bold text-teal-900 font-hind text-sm">বড় Heading ও Page Title</div>
                <div className="text-[11px] text-teal-800/80 mt-0.5 font-tiro">
                  অ্যাপ বার, স্ক্রিনের মূল শিরোনাম, প্রধান সেকশন শিরোনাম।
                </div>
              </div>
            </div>

            <div className="p-2.5 rounded-xl border border-amber-200 bg-amber-50/50 flex items-start gap-2.5">
              <span className="px-2 py-0.5 rounded text-[10px] font-bold font-mono bg-amber-600 text-white shrink-0 mt-0.5">
                Baloo Da 2
              </span>
              <div className="min-w-0 font-tiro">
                <div className="font-bold text-amber-900 font-baloo text-sm">মাঝারি Heading, কার্ড ও বাটন</div>
                <div className="text-[11px] text-amber-800/80 mt-0.5 font-tiro">
                  কার্ড টাইটেল, সাব-হেডিং, ট্যাব ও বাটনের মূল টেক্সট।
                </div>
              </div>
            </div>

            <div className="p-2.5 rounded-xl border border-blue-200 bg-blue-50/50 flex items-start gap-2.5">
              <span className="px-2 py-0.5 rounded text-[10px] font-bold font-mono bg-blue-600 text-white shrink-0 mt-0.5">
                Tiro Bangla
              </span>
              <div className="min-w-0 font-tiro">
                <div className="font-bold text-blue-900 font-tiro text-sm">বডি টেক্সট, লেবেল ও তথ্য</div>
                <div className="text-[11px] text-blue-800/80 mt-0.5 font-tiro">
                  ফর্ম লেবেল, ইনপুট টেক্সট, বর্ণনা, বার্তা, তালিকা ও সহায়ক নির্দেশিকা।
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Live Token Inspector */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-teal-700" />
              <span>Authentication State Inspector</span>
            </h4>
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
              currentUser ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
            }`}>
              {currentUser ? 'AUTHENTICATED' : 'UNAUTHENTICATED'}
            </span>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex justify-between items-center bg-slate-50 p-2 rounded-lg">
              <span className="text-slate-500">Access Token:</span>
              <span className="font-mono text-[10px] text-slate-700 max-w-[220px] truncate">
                {accessToken ? `${accessToken.substring(0, 24)}...` : 'None (Logged out)'}
              </span>
            </div>
            <div className="flex justify-between items-center bg-slate-50 p-2 rounded-lg">
              <span className="text-slate-500">Refresh Token:</span>
              <span className="font-mono text-[10px] text-slate-700 max-w-[220px] truncate">
                {refreshToken ? `${refreshToken.substring(0, 24)}...` : 'None (Logged out)'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
