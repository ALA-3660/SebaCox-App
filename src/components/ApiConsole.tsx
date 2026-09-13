import React, { useState } from 'react';
import { Play, CheckCircle2, AlertCircle, Copy, Check, Terminal, ExternalLink, Code } from 'lucide-react';
import { StandardApiResponse } from '../types';

interface Preset {
  name: string;
  method: 'GET' | 'POST';
  endpoint: string;
  body?: string;
  auth?: boolean;
}

const PRESETS: Preset[] = [
  {
    name: '1. Health Check (Phase 1)',
    method: 'GET',
    endpoint: '/api/v1/health/',
  },
  {
    name: '2. Login: Request OTP (Valid BD)',
    method: 'POST',
    endpoint: '/api/v1/auth/login/request-otp/',
    body: JSON.stringify({ mobile_number: '01712345678' }, null, 2),
  },
  {
    name: '3. Login: Request OTP (Invalid)',
    method: 'POST',
    endpoint: '/api/v1/auth/login/request-otp/',
    body: JSON.stringify({ mobile_number: '+14155552671' }, null, 2),
  },
  {
    name: '4. Login: Verify OTP',
    method: 'POST',
    endpoint: '/api/v1/auth/login/verify-otp/',
    body: JSON.stringify({ mobile_number: '01712345678', otp_code: '123456' }, null, 2),
  },
  {
    name: '5. Register: Request OTP',
    method: 'POST',
    endpoint: '/api/v1/auth/register/request-otp/',
    body: JSON.stringify({ mobile_number: '01899112233' }, null, 2),
  },
  {
    name: '6. Register: Verify OTP',
    method: 'POST',
    endpoint: '/api/v1/auth/register/verify-otp/',
    body: JSON.stringify({ mobile_number: '01899112233', otp_code: '123456' }, null, 2),
  },
  {
    name: '7. Token Refresh',
    method: 'POST',
    endpoint: '/api/v1/auth/token/refresh/',
    body: JSON.stringify({ refresh_token: 'paste_refresh_token_here' }, null, 2),
  },
  {
    name: '8. Current User / Me (Unauth 401)',
    method: 'GET',
    endpoint: '/api/v1/auth/me/',
  },
  {
    name: '9. Locations: Countries',
    method: 'GET',
    endpoint: '/api/v1/locations/countries/',
  },
  {
    name: '10. Locations: Divisions',
    method: 'GET',
    endpoint: '/api/v1/locations/divisions/',
  },
  {
    name: '11. Locations: Districts (Chattogram)',
    method: 'GET',
    endpoint: '/api/v1/locations/districts/?division_id=1',
  },
  {
    name: '12. Locations: Upazilas (Cox\'s Bazar)',
    method: 'GET',
    endpoint: '/api/v1/locations/upazilas/?district_id=1',
  },
  {
    name: '13. Locations: Search ("কক্সবাজার" / "Teknaf")',
    method: 'GET',
    endpoint: '/api/v1/locations/search/?q=কক্সবাজার',
  },
  {
    name: '14. Locations: Context Profile (GET)',
    method: 'GET',
    endpoint: '/api/v1/locations/context/',
  },
  {
    name: '15. Locations: Set Selected Area (POST)',
    method: 'POST',
    endpoint: '/api/v1/locations/context/',
    body: JSON.stringify({
      location_type: 'SELECTED',
      address_text: 'কক্সবাজার সদর, কক্সবাজার',
      upazila_id: 1,
      district_id: 1,
      latitude: 21.4272,
      longitude: 92.0058
    }, null, 2)
  },
  {
    name: '16. Locations: Reverse Geocode (GPS)',
    method: 'GET',
    endpoint: '/api/v1/locations/reverse-geocode/?lat=21.4272&lon=92.0058',
  },
  {
    name: '17. Locations: Service Areas',
    method: 'GET',
    endpoint: '/api/v1/locations/service-areas/',
  },
  {
    name: '18. Categories: All Active List',
    method: 'GET',
    endpoint: '/api/v1/categories/',
  },
  {
    name: '19. Categories: Recursive Tree (Public)',
    method: 'GET',
    endpoint: '/api/v1/categories/tree/?kind=PUBLIC_SERVICE_CATEGORY',
  },
  {
    name: '20. Categories: Featured',
    method: 'GET',
    endpoint: '/api/v1/categories/featured/',
  },
  {
    name: '21. Categories: System Domains',
    method: 'GET',
    endpoint: '/api/v1/categories/?kind=SYSTEM_DOMAIN',
  },
  {
    name: '22. Services: All Services',
    method: 'GET',
    endpoint: '/api/v1/services/',
  },
  {
    name: '23. Services: Featured Services',
    method: 'GET',
    endpoint: '/api/v1/services/featured/',
  },
  {
    name: '24. Services: Search ("ডাক্তার" / "bricks")',
    method: 'GET',
    endpoint: '/api/v1/services/search/?q=ডাক্তার',
  },
  {
    name: '25. Services: By Category (Tourism & Travel)',
    method: 'GET',
    endpoint: '/api/v1/services/by-category/1/',
  },
  {
    name: '26. Demands: List Published Needs (Phase 6)',
    method: 'GET',
    endpoint: '/api/v1/demands/',
  },
  {
    name: '27. Demands: Search by Bangla Query & Upazila',
    method: 'GET',
    endpoint: '/api/v1/demands/?q=ইলেকট্রিশিয়ান&upazila_id=1',
  },
  {
    name: '28. Demands: Create Demand (Draft or Publish)',
    method: 'POST',
    endpoint: '/api/v1/demands/',
    body: JSON.stringify({
      title_bn: 'কক্সবাজার সদরে অভিজ্ঞ ইলেকট্রিশিয়ান প্রয়োজন',
      description_bn: 'বাসার মূল সার্কিট ব্রেকার মেরামত ও ওয়্যারিং চেক করার জন্য জরুরি প্রয়োজন।',
      demand_type: 'SERVICE',
      priority: 'URGENT',
      upazila_id: 1,
      location_display_bn: 'কলাতলী রোড, কক্সবাজার সদর',
      budget_min: 800,
      budget_max: 1500,
      publish_now: true,
      contact_preference: 'BOTH'
    }, null, 2),
  },
  {
    name: '29. Demands: Detail & Privacy Masking',
    method: 'GET',
    endpoint: '/api/v1/demands/1/',
  },
  {
    name: '30. Demands: Publish Draft',
    method: 'POST',
    endpoint: '/api/v1/demands/1/publish/',
    body: JSON.stringify({ reason: 'প্রকাশের জন্য প্রস্তুত' }, null, 2),
  },
  {
    name: '31. Demands: Fulfill Need',
    method: 'POST',
    endpoint: '/api/v1/demands/1/fulfill/',
    body: JSON.stringify({ reason: 'সেবা সফলভাবে পাওয়া গেছে' }, null, 2),
  },
  {
    name: '32. Demands: My Demands (Owner View)',
    method: 'GET',
    endpoint: '/api/v1/demands/my-demands/',
  },
  {
    name: '33. Invalid Route (Standard 404)',
    method: 'GET',
    endpoint: '/api/v1/invalid-route/',
  },
];

export const ApiConsole: React.FC = () => {
  const [endpoint, setEndpoint] = useState<string>('/api/v1/auth/login/request-otp/');
  const [method, setMethod] = useState<'GET' | 'POST'>('POST');
  const [requestBody, setRequestBody] = useState<string>(
    JSON.stringify({ mobile_number: '01712345678' }, null, 2)
  );
  const [tokenHeader, setTokenHeader] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<StandardApiResponse | null>(null);
  const [statusCode, setStatusCode] = useState<number | null>(null);
  const [responseTime, setResponseTime] = useState<number | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const applyPreset = (p: Preset) => {
    setMethod(p.method);
    setEndpoint(p.endpoint);
    setRequestBody(p.body || '');
  };

  const executeRequest = async () => {
    setLoading(true);
    setResponse(null);
    setStatusCode(null);
    const start = performance.now();

    try {
      const headers: Record<string, string> = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      };
      if (tokenHeader.trim()) {
        headers['Authorization'] = tokenHeader.startsWith('Bearer ')
          ? tokenHeader
          : `Bearer ${tokenHeader}`;
      }

      const options: RequestInit = {
        method,
        headers,
      };

      if (method === 'POST' && requestBody.trim()) {
        options.body = requestBody;
      }

      const res = await fetch(endpoint, options);
      const duration = Math.round(performance.now() - start);
      setResponseTime(duration);
      setStatusCode(res.status);

      const json = await res.json();
      setResponse(json);

      // Auto-populate token header if tokens returned
      if (json?.data?.tokens?.access_token) {
        setTokenHeader(`Bearer ${json.data.tokens.access_token}`);
      }
    } catch (err: any) {
      setStatusCode(500);
      setResponse({
        success: false,
        data: null,
        message: 'অনুরোধটি সম্পন্ন করা যায়নি',
        errors: { detail: err?.message || 'Network request failed' },
      });
    } finally {
      setLoading(false);
    }
  };

  const copyResponse = () => {
    if (response) {
      navigator.clipboard.writeText(JSON.stringify(response, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-teal-700" />
          <h2 className="font-bold text-slate-800 text-sm">SebaCox Phase 1 & 2 API Console</h2>
        </div>
        <div className="text-xs text-slate-500">
          Standard JSend-compliant contracts
        </div>
      </div>

      {/* Presets */}
      <div className="mb-4">
        <label className="block text-xs font-bold text-slate-600 mb-1.5">দ্রুত টেস্ট প্রিসেটস (Quick Presets):</label>
        <div className="flex flex-wrap gap-1.5">
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => applyPreset(p)}
              className="px-2.5 py-1 text-[11px] font-semibold bg-slate-100 hover:bg-teal-50 hover:text-teal-800 hover:border-teal-300 border border-slate-200 rounded-lg text-slate-700 transition cursor-pointer"
            >
              {p.name}
            </button>
          ))}
        </div>
      </div>

      {/* URL bar */}
      <div className="flex flex-col sm:flex-row gap-2 mb-3">
        <select
          value={method}
          onChange={(e) => setMethod(e.target.value as 'GET' | 'POST')}
          className="px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl text-xs font-bold text-teal-900 focus:outline-none"
        >
          <option value="GET">GET</option>
          <option value="POST">POST</option>
        </select>
        <div className="flex-1 flex rounded-xl border border-slate-300 bg-slate-50 overflow-hidden focus-within:border-teal-700">
          <input
            type="text"
            value={endpoint}
            onChange={(e) => setEndpoint(e.target.value)}
            className="flex-1 px-3 py-2 text-xs font-mono bg-transparent focus:outline-none text-slate-800 font-semibold"
            placeholder="/api/v1/auth/..."
          />
        </div>
        <button
          id="btn-execute-api"
          onClick={executeRequest}
          disabled={loading}
          className="px-5 py-2 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold transition flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50"
        >
          <Play className="w-3.5 h-3.5 fill-current" />
          <span>{loading ? 'পাঠানো হচ্ছে...' : 'অনুরোধ পাঠান'}</span>
        </button>
      </div>

      {/* Optional Auth Header & Body */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
        <div>
          <label className="block text-[11px] font-bold text-slate-600 mb-1">
            Authorization Header (Optional):
          </label>
          <input
            type="text"
            value={tokenHeader}
            onChange={(e) => setTokenHeader(e.target.value)}
            placeholder="Bearer <jwt_access_token>"
            className="w-full px-3 py-1.5 text-xs font-mono border border-slate-200 rounded-lg bg-slate-50 text-slate-700 focus:outline-none focus:border-teal-700"
          />
        </div>

        {method === 'POST' && (
          <div>
            <label className="block text-[11px] font-bold text-slate-600 mb-1">
              JSON Request Body:
            </label>
            <textarea
              rows={3}
              value={requestBody}
              onChange={(e) => setRequestBody(e.target.value)}
              className="w-full p-2 text-xs font-mono border border-slate-200 rounded-lg bg-slate-50 text-slate-700 focus:outline-none focus:border-teal-700"
            />
          </div>
        )}
      </div>

      {/* Response Box */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-700">প্রতিক্রিয়া (Response):</span>
            {statusCode !== null && (
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                  statusCode >= 200 && statusCode < 300
                    ? 'bg-emerald-100 text-emerald-800'
                    : statusCode === 404
                    ? 'bg-amber-100 text-amber-800'
                    : 'bg-rose-100 text-rose-800'
                }`}
              >
                HTTP {statusCode}
              </span>
            )}
            {responseTime !== null && (
              <span className="text-[11px] text-slate-400 font-mono">
                {responseTime} ms
              </span>
            )}
          </div>
          {response && (
            <button
              onClick={copyResponse}
              className="text-xs text-slate-500 hover:text-teal-700 flex items-center gap-1 cursor-pointer font-medium"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'কপি হয়েছে!' : 'কপি করুন'}</span>
            </button>
          )}
        </div>

        <div className="bg-slate-900 rounded-xl p-4 font-mono text-xs overflow-x-auto text-emerald-400 min-h-[160px] border border-slate-800">
          {loading ? (
            <div className="text-slate-500 italic">সার্ভার থেকে প্রতিক্রিয়া লোড হচ্ছে...</div>
          ) : response ? (
            <pre>{JSON.stringify(response, null, 2)}</pre>
          ) : (
            <div className="text-slate-600 italic">
              একটি প্রিসেট নির্বাচন করে 'অনুরোধ পাঠান' বাটনে চাপুন।
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
