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
  Sparkles
} from 'lucide-react';
import { StandardApiResponse } from '../types';

type FlutterScreen = 'auth' | 'otp' | 'home' | 'health';
type AuthMode = 'login' | 'register';

export const FlutterSimulator: React.FC = () => {
  // Navigation & Screen state
  const [activeScreen, setActiveScreen] = useState<FlutterScreen>('auth');
  const [authMode, setAuthMode] = useState<AuthMode>('login');
  
  // Form state
  const [phone, setPhone] = useState<string>('01712345678');
  const [otp, setOtp] = useState<string>('123456');
  const [devOtp, setDevOtp] = useState<string | null>('123456');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [infoMessage, setInfoMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [countdown, setCountdown] = useState<number>(60);

  // Authenticated session state
  const [currentUser, setCurrentUser] = useState<{ id: number; mobile_number: string; is_verified: boolean } | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);

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
        <div className="w-full bg-slate-50 rounded-[34px] overflow-hidden flex flex-col min-h-[600px] max-h-[600px] text-slate-800 font-sans select-none">
          {/* Mobile Status Bar */}
          <div className="pt-3 px-6 pb-2 flex justify-between items-center text-xs font-semibold text-slate-500 bg-white border-b border-slate-100">
            <span>09:41</span>
            <div className="flex items-center gap-1.5">
              <Wifi className="w-3.5 h-3.5" />
              <div className="w-4 h-2.5 border border-slate-500 rounded-xs relative">
                <div className="h-full bg-slate-500 w-3/4"></div>
              </div>
            </div>
          </div>

          {/* App Header */}
          <div className="bg-white px-4 py-2.5 border-b border-slate-200 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-md bg-teal-700 text-white flex items-center justify-center text-[10px] font-black">
                SC
              </div>
              <h1 className="text-sm font-bold tracking-tight text-teal-900">সেবাকক্স</h1>
            </div>
            <div className="flex items-center gap-1">
              <button
                onClick={() => {
                  if (activeScreen === 'health') {
                    setActiveScreen(currentUser ? 'home' : 'auth');
                  } else {
                    setActiveScreen('health');
                    runHealthCheck();
                  }
                }}
                className={`text-[10px] font-bold px-2 py-0.5 rounded-full border cursor-pointer ${
                  activeScreen === 'health'
                    ? 'bg-teal-700 text-white border-teal-800'
                    : 'bg-teal-50 text-teal-700 border-teal-200'
                }`}
              >
                {activeScreen === 'health' ? 'Auth এ ফিরুন' : 'Health Check'}
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
                  <span className="text-xs text-teal-700 font-bold bg-teal-50 px-2.5 py-0.5 rounded-full border border-teal-200">
                    Phase 2 — প্রমাণীকরণ
                  </span>
                  <h2 className="text-lg font-black text-slate-900 mt-2">
                    {authMode === 'login' ? 'অ্যাকাউন্টে লগইন' : 'নতুন অ্যাকাউন্ট তৈরি'}
                  </h2>
                  <p className="text-[11px] text-slate-500 italic mt-0.5">
                    “মানুষের প্রয়োজন থেকে সেবার সমাধান।”
                  </p>
                </div>

                {/* Mode Selector */}
                <div className="grid grid-cols-2 p-1 bg-slate-200/70 rounded-xl text-xs font-bold">
                  <button
                    onClick={() => { setAuthMode('login'); setErrorMessage(null); }}
                    className={`py-1.5 rounded-lg transition cursor-pointer ${
                      authMode === 'login' ? 'bg-white text-teal-800 shadow-xs' : 'text-slate-600'
                    }`}
                  >
                    লগইন
                  </button>
                  <button
                    onClick={() => { setAuthMode('register'); setErrorMessage(null); }}
                    className={`py-1.5 rounded-lg transition cursor-pointer ${
                      authMode === 'register' ? 'bg-white text-teal-800 shadow-xs' : 'text-slate-600'
                    }`}
                  >
                    নতুন নিবন্ধন
                  </button>
                </div>

                {/* Form */}
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">
                      মোবাইল নম্বর দিন
                    </label>
                    <div className="flex rounded-xl border border-slate-300 bg-white overflow-hidden focus-within:border-teal-700 focus-within:ring-1 focus-within:ring-teal-700">
                      <div className="px-2.5 py-2 bg-slate-100 border-r border-slate-200 text-xs font-bold text-teal-800 flex items-center">
                        +88
                      </div>
                      <input
                        type="tel"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        placeholder="017XXXXXXXX"
                        className="w-full px-3 py-2 text-xs font-semibold focus:outline-none"
                      />
                    </div>
                    <p className="text-[10px] text-slate-400 mt-1">
                      গ্রাহক, ড্রাইভার, হোটেল বা সেবা সরবরাহকারী সবার জন্য একটি নম্বর
                    </p>
                  </div>

                  {errorMessage && (
                    <div className="p-2.5 rounded-lg bg-rose-50 border border-rose-200 text-[11px] text-rose-700 font-medium">
                      {errorMessage}
                    </div>
                  )}

                  {infoMessage && (
                    <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-[11px] text-emerald-700 font-medium">
                      {infoMessage}
                    </div>
                  )}

                  <button
                    id="sim-request-otp"
                    onClick={handleRequestOtp}
                    disabled={isLoading}
                    className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold shadow-xs transition flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50"
                  >
                    {isLoading ? (
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                      <>
                        <span>ওটিপি পাঠান</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}

            {/* 3. OTP VERIFICATION SCREEN */}
            {activeScreen === 'otp' && (
              <div className="flex flex-col gap-4">
                <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl">
                  <div className="flex items-center gap-2 text-emerald-800 font-bold text-xs">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>ওটিপি পাঠানো হয়েছে</span>
                  </div>
                  <div className="text-[11px] text-emerald-700 mt-0.5">
                    নম্বর: <span className="font-bold">{phone}</span>
                  </div>
                </div>

                {devOtp && (
                  <div className="p-2.5 bg-amber-50 border border-amber-200 rounded-lg text-amber-800 flex items-center justify-between">
                    <span className="text-[11px] font-medium">ডেভ টেস্ট কোড:</span>
                    <span className="font-mono font-bold text-xs bg-amber-200 px-2 py-0.5 rounded">
                      {devOtp}
                    </span>
                  </div>
                )}

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1 text-center">
                    ওটিপি লিখুন (৬ অঙ্কের কোড)
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
                  <div className="p-2.5 rounded-lg bg-rose-50 border border-rose-200 text-[11px] text-rose-700 font-medium">
                    {errorMessage}
                  </div>
                )}

                <button
                  id="sim-verify-otp"
                  onClick={handleVerifyOtp}
                  disabled={isLoading}
                  className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold shadow-xs transition flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50"
                >
                  {isLoading ? (
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <span>যাচাই করুন</span>
                  )}
                </button>

                <div className="text-center">
                  {countdown > 0 ? (
                    <p className="text-[11px] text-slate-500">
                      পুনরায় পাঠাতে অপেক্ষা করুন: <span className="font-bold">{countdown}</span> সেকেন্ড
                    </p>
                  ) : (
                    <button
                      onClick={handleRequestOtp}
                      className="text-[11px] font-bold text-teal-700 hover:underline cursor-pointer"
                    >
                      আবার ওটিপি পাঠান
                    </button>
                  )}
                </div>

                <button
                  onClick={() => setActiveScreen('auth')}
                  className="text-[10px] text-slate-500 hover:text-slate-700 text-center cursor-pointer"
                >
                  ← নম্বর পরিবর্তন করুন
                </button>
              </div>
            )}

            {/* 4. AUTHENTICATED SCREEN */}
            {activeScreen === 'home' && currentUser && (
              <div className="flex flex-col gap-4">
                <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center">
                    <CheckCircle2 className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-xs font-bold text-emerald-900">লগইন সফল হয়েছে</h3>
                    <p className="text-[10px] text-emerald-700">সেশন সক্রিয় ও সুরক্ষিত</p>
                  </div>
                </div>

                {/* Profile Card */}
                <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-xs space-y-2">
                  <h4 className="text-xs font-bold text-slate-800 border-b border-slate-100 pb-1 flex items-center gap-1.5">
                    <UserIcon className="w-3.5 h-3.5 text-teal-700" />
                    <span>ব্যবহারকারীর পরিচয়</span>
                  </h4>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-500">আইডি:</span>
                    <span className="font-mono font-bold text-slate-800">#{currentUser.id}</span>
                  </div>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-500">মোবাইল:</span>
                    <span className="font-semibold text-slate-800">{currentUser.mobile_number}</span>
                  </div>
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-500">অবস্থা:</span>
                    <span className="font-bold text-emerald-700">যাচাইকৃত (Verified)</span>
                  </div>
                </div>

                {/* Security and Token testing controls */}
                <div className="bg-slate-100/80 p-3 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-slate-600 flex items-center gap-1">
                      <KeyRound className="w-3 h-3" /> JWT সেশন টোকেন
                    </span>
                    <span className="text-[9px] bg-teal-100 text-teal-800 px-1.5 py-0.5 rounded font-mono">
                      HMAC-SHA256
                    </span>
                  </div>
                  <p className="text-[10px] text-slate-500">
                    অ্যাক্সেস টোকেন শুধুমাত্র মেমোরি ও সিকিউর স্টোরেজে সংরক্ষিত।
                  </p>
                  <button
                    onClick={handleRefreshToken}
                    disabled={isLoading}
                    className="w-full py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-lg text-[10px] font-bold transition flex items-center justify-center gap-1 cursor-pointer"
                  >
                    <RefreshCw className={`w-3 h-3 ${isLoading ? 'animate-spin' : ''}`} />
                    <span>টোকেন রিফ্রেশ টেস্ট</span>
                  </button>
                </div>

                {/* Logout Button */}
                <button
                  id="sim-logout"
                  onClick={handleLogout}
                  className="w-full py-2 border border-rose-200 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>লগআউট</span>
                </button>
              </div>
            )}

            {/* Bottom watermark */}
            <div className="pt-2 text-center text-[10px] text-slate-400">
              SebaCox Flutter Engine • Cox's Bazar
            </div>
          </div>
        </div>
      </div>

      {/* Side Explanations & Controls */}
      <div className="flex-1 max-w-xl flex flex-col gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center gap-2 text-teal-900 font-black text-base">
            <Smartphone className="w-5 h-5 text-teal-700" />
            <span>Flutter Phase 2 Interactive Simulator</span>
          </div>
          <p className="text-xs text-slate-600 mt-1">
            Test the live Bangladeshi mobile authentication flow with OTP verification, JWT token lifecycle, session checks, and secure logout.
          </p>

          <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="font-bold text-slate-800">Phone Normalization</div>
              <div className="text-[11px] text-slate-500 mt-1">
                Converts 017..., 8801... and formatted numbers to canonical <code>+8801XXXXXXXXX</code>.
              </div>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
              <div className="font-bold text-slate-800">OTP Cryptography</div>
              <div className="text-[11px] text-slate-500 mt-1">
                SHA-256 salted hashes, 5-min expiration, 60s resend cooldown, 5-attempt brute-force protection.
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
