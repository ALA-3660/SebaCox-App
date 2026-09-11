import React, { useState, useEffect } from 'react';
import { RefreshCw, CheckCircle2, AlertTriangle, XCircle, Smartphone, Wifi, Server, Clock } from 'lucide-react';
import { ConnectionState, StandardApiResponse } from '../types';

export const FlutterSimulator: React.FC = () => {
  const [connectionState, setConnectionState] = useState<ConnectionState>('loading');
  const [statusMessage, setStatusMessage] = useState<string>('সংযোগ পরীক্ষা হচ্ছে...');
  const [details, setDetails] = useState<string | null>(null);
  const [latency, setLatency] = useState<number | null>(null);
  const [apiUrl, setApiUrl] = useState<string>('/api/v1/health/');
  const [simulateMode, setSimulateMode] = useState<'real' | 'timeout' | 'error'>('real');

  const checkConnection = async (mode: 'real' | 'timeout' | 'error' = simulateMode) => {
    setConnectionState('loading');
    setStatusMessage('সংযোগ পরীক্ষা হচ্ছে...');
    setDetails(null);
    setLatency(null);

    const startTime = performance.now();

    if (mode === 'timeout') {
      setTimeout(() => {
        setConnectionState('failure');
        setStatusMessage('সার্ভারের সাথে সংযোগ ব্যর্থ');
        setDetails('অনুরোধের সময়সীমা অতিক্রম করেছে (HTTP 408 Timeout)');
        setLatency(10000);
      }, 1200);
      return;
    }

    if (mode === 'error') {
      setTimeout(() => {
        setConnectionState('failure');
        setStatusMessage('সার্ভারের সাথে সংযোগ ব্যর্থ');
        setDetails('ইন্টারনেট সংযোগ পাওয়া যায়নি অথবা সার্ভার অনুপলব্ধ (500 Server Error)');
        setLatency(null);
      }, 800);
      return;
    }

    try {
      const res = await fetch(apiUrl, {
        headers: { 'Accept': 'application/json' },
      });
      const duration = Math.round(performance.now() - startTime);
      setLatency(duration);

      const json: StandardApiResponse = await res.json();

      if (res.ok && json.success) {
        setConnectionState('success');
        setStatusMessage('সার্ভারের সাথে সংযোগ সফল');
        setDetails(`API: ${json.message} • ল্যাটেন্সি: ${duration}ms`);
      } else {
        setConnectionState('failure');
        setStatusMessage('সার্ভারের সাথে সংযোগ ব্যর্থ');
        setDetails(json.message || 'সার্ভার থেকে ত্রুটি প্রতিক্রিয়া এসেছে');
      }
    } catch (err: any) {
      setConnectionState('failure');
      setStatusMessage('সার্ভারের সাথে সংযোগ ব্যর্থ');
      setDetails(err?.message || 'নেটওয়ার্ক সংযোগ স্থাপন করা যায়নি');
    }
  };

  useEffect(() => {
    checkConnection('real');
  }, []);

  return (
    <div className="flex flex-col xl:flex-row gap-6 items-center justify-center p-2">
      {/* Mobile Device Mockup */}
      <div className="relative w-full max-w-[340px] bg-slate-900 rounded-[44px] p-3 shadow-2xl border-4 border-slate-700">
        {/* Dynamic Island / Speaker notch */}
        <div className="absolute top-5 left-1/2 -translate-x-1/2 w-28 h-5 bg-black rounded-full z-20 flex items-center justify-center">
          <div className="w-2.5 h-2.5 bg-slate-800 rounded-full mr-2"></div>
          <div className="w-10 h-1 bg-slate-800 rounded-full"></div>
        </div>

        {/* Screen Content */}
        <div className="w-full bg-slate-50 rounded-[34px] overflow-hidden flex flex-col min-h-[580px] text-slate-800 font-sans">
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
          <div className="bg-white px-5 py-3 border-b border-slate-200 flex items-center justify-between">
            <h1 className="text-lg font-bold tracking-tight text-teal-900">SebaCox</h1>
            <span className="text-[11px] font-medium bg-teal-50 text-teal-700 px-2 py-0.5 rounded-full border border-teal-200">
              Flutter v1.0
            </span>
          </div>

          {/* Mobile Body */}
          <div className="p-4 flex-1 flex flex-col items-center justify-between">
            <div className="w-full space-y-4">
              {/* Product Principle Tagline */}
              <div className="bg-teal-50/80 border border-teal-200/80 rounded-xl p-2.5 text-center">
                <p className="text-xs font-medium text-teal-800">
                  “মানুষের প্রয়োজন থেকে সেবার সমাধান।”
                </p>
                <p className="text-[10px] text-teal-600 mt-0.5">
                  Phase 1 — Project Foundation
                </p>
              </div>

              {/* Status Section Title */}
              <div>
                <p className="text-[11px] uppercase tracking-wider font-semibold text-slate-400 mb-1.5">
                  Backend Connection Status
                </p>

                {/* Status Card based on state */}
                {connectionState === 'loading' && (
                  <div className="w-full bg-blue-50/80 border border-blue-200 rounded-2xl p-5 flex flex-col items-center text-center">
                    <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mb-3" />
                    <p className="font-bold text-slate-800 text-sm">{statusMessage}</p>
                    <p className="text-xs text-slate-500 mt-1">GET /api/v1/health/ কল করা হচ্ছে...</p>
                  </div>
                )}

                {connectionState === 'success' && (
                  <div className="w-full bg-emerald-50 border border-emerald-300 rounded-2xl p-5 flex flex-col items-center text-center shadow-xs">
                    <div className="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center mb-2.5">
                      <CheckCircle2 className="w-6 h-6 text-emerald-600" />
                    </div>
                    <p className="font-bold text-emerald-950 text-sm">{statusMessage}</p>
                    {details && (
                      <p className="text-xs text-emerald-700 mt-1 whitespace-pre-line leading-relaxed">
                        {details}
                      </p>
                    )}
                    {latency !== null && (
                      <div className="mt-3 inline-flex items-center gap-1 text-[11px] font-mono bg-emerald-100/60 text-emerald-800 px-2.5 py-0.5 rounded-md">
                        <Clock className="w-3 h-3" />
                        <span>{latency} ms response</span>
                      </div>
                    )}
                  </div>
                )}

                {connectionState === 'failure' && (
                  <div className="w-full bg-red-50 border border-red-300 rounded-2xl p-5 flex flex-col items-center text-center shadow-xs">
                    <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mb-2.5">
                      <XCircle className="w-6 h-6 text-red-600" />
                    </div>
                    <p className="font-bold text-red-950 text-sm">{statusMessage}</p>
                    {details && (
                      <p className="text-xs text-red-700 mt-1 leading-relaxed">
                        {details}
                      </p>
                    )}
                  </div>
                )}
              </div>

              {/* Re-check Button inside Flutter Screen */}
              <button
                id="btn-flutter-recheck"
                onClick={() => checkConnection(simulateMode)}
                disabled={connectionState === 'loading'}
                className="w-full bg-teal-700 hover:bg-teal-800 active:bg-teal-900 text-white font-medium text-xs py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition shadow-xs disabled:opacity-60 cursor-pointer"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${connectionState === 'loading' ? 'animate-spin' : ''}`} />
                <span>পুনরায় সংযোগ পরীক্ষা করুন</span>
              </button>

              {/* In-App URL Config Box */}
              <div className="bg-white border border-slate-200 rounded-xl p-3 text-left">
                <label className="text-[10px] font-semibold text-slate-500 uppercase tracking-wide block mb-1">
                  Configured API Endpoint
                </label>
                <input
                  type="text"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  className="w-full text-xs font-mono bg-slate-50 border border-slate-200 rounded-lg px-2 py-1.5 text-slate-700 focus:outline-teal-600"
                />
              </div>
            </div>

            {/* Flutter footer badge */}
            <div className="pt-2 text-center text-[10px] text-slate-400">
              SebaCox Flutter Core • mobile/lib/main.dart
            </div>
          </div>
        </div>
      </div>

      {/* Simulator Control Panel */}
      <div className="flex-1 max-w-lg bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
        <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
          <Smartphone className="w-5 h-5 text-teal-700" />
          <h2 className="font-bold text-slate-800 text-sm">Flutter Mobile Client State Inspector</h2>
        </div>

        <p className="text-xs text-slate-600 leading-relaxed mb-4">
          Test the Flutter application's connection states as defined in <strong>mobile/lib/features/home/home_screen.dart</strong>.
          The mobile client communicates through the centralized <strong>ApiClient</strong> with unified timeout, network error, and standard response parsing.
        </p>

        <div className="space-y-3 mb-5">
          <p className="text-xs font-semibold text-slate-700">Test Scenarios:</p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            <button
              id="test-real-connection"
              onClick={() => {
                setSimulateMode('real');
                checkConnection('real');
              }}
              className={`p-2.5 rounded-xl border text-xs font-medium flex flex-col items-center gap-1.5 transition cursor-pointer ${
                simulateMode === 'real'
                  ? 'border-emerald-500 bg-emerald-50/50 text-emerald-900 font-semibold'
                  : 'border-slate-200 hover:bg-slate-50 text-slate-700'
              }`}
            >
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Real Live API</span>
              <span className="text-[10px] text-slate-500">200 OK</span>
            </button>

            <button
              id="test-timeout-scenario"
              onClick={() => {
                setSimulateMode('timeout');
                checkConnection('timeout');
              }}
              className={`p-2.5 rounded-xl border text-xs font-medium flex flex-col items-center gap-1.5 transition cursor-pointer ${
                simulateMode === 'timeout'
                  ? 'border-amber-500 bg-amber-50/50 text-amber-900 font-semibold'
                  : 'border-slate-200 hover:bg-slate-50 text-slate-700'
              }`}
            >
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Timeout Error</span>
              <span className="text-[10px] text-slate-500">408 Timeout</span>
            </button>

            <button
              id="test-failure-scenario"
              onClick={() => {
                setSimulateMode('error');
                checkConnection('error');
              }}
              className={`p-2.5 rounded-xl border text-xs font-medium flex flex-col items-center gap-1.5 transition cursor-pointer ${
                simulateMode === 'error'
                  ? 'border-red-500 bg-red-50/50 text-red-900 font-semibold'
                  : 'border-slate-200 hover:bg-slate-50 text-slate-700'
              }`}
            >
              <XCircle className="w-4 h-4 text-red-600" />
              <span>Server Failure</span>
              <span className="text-[10px] text-slate-500">500 Offline</span>
            </button>
          </div>
        </div>

        {/* State Verification Checklist */}
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
          <p className="text-xs font-semibold text-slate-800 mb-2">Flutter UI State Specifications:</p>
          <ul className="text-xs space-y-1.5 text-slate-600">
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
              <span><strong>Loading:</strong> “সংযোগ পরীক্ষা হচ্ছে...” (Spinner Active)</span>
            </li>
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              <span><strong>Success:</strong> “সার্ভারের সাথে সংযোগ সফল” (Green Badge)</span>
            </li>
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
              <span><strong>Failure:</strong> “সার্ভারের সাথে সংযোগ ব্যর্থ” (Error & Retry)</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
