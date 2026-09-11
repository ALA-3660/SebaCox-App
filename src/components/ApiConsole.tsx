import React, { useState } from 'react';
import { Play, CheckCircle2, AlertCircle, Copy, Check, Terminal, ExternalLink } from 'lucide-react';
import { StandardApiResponse } from '../types';

export const ApiConsole: React.FC = () => {
  const [endpoint, setEndpoint] = useState<string>('/api/v1/health/');
  const [method, setMethod] = useState<'GET'>('GET');
  const [loading, setLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<StandardApiResponse | null>(null);
  const [statusCode, setStatusCode] = useState<number | null>(null);
  const [responseTime, setResponseTime] = useState<number | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const executeRequest = async (targetEndpoint = endpoint) => {
    setLoading(true);
    setResponse(null);
    setStatusCode(null);
    const start = performance.now();

    try {
      const res = await fetch(targetEndpoint, {
        method,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      });
      const duration = Math.round(performance.now() - start);
      setResponseTime(duration);
      setStatusCode(res.status);

      const json = await res.json();
      setResponse(json);
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
          <h2 className="font-bold text-slate-800 text-sm">SebaCox Standard API Explorer</h2>
        </div>
        <span className="text-[11px] font-mono bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md">
          DRF /api/v1/
        </span>
      </div>

      {/* Quick Presets */}
      <div className="mb-4">
        <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide mb-2">
          Preset Endpoints:
        </p>
        <div className="flex flex-wrap gap-2">
          <button
            id="btn-preset-health"
            onClick={() => {
              setEndpoint('/api/v1/health/');
              executeRequest('/api/v1/health/');
            }}
            className="text-xs px-3 py-1.5 rounded-lg border border-emerald-300 bg-emerald-50 text-emerald-800 font-medium hover:bg-emerald-100 transition flex items-center gap-1.5 cursor-pointer"
          >
            <span className="font-bold text-[10px] bg-emerald-200 px-1 py-0.2 rounded">GET</span>
            <span>/api/v1/health/</span>
            <span className="text-[10px] text-emerald-600">(Success)</span>
          </button>

          <button
            id="btn-preset-404"
            onClick={() => {
              setEndpoint('/api/v1/invalid-route/');
              executeRequest('/api/v1/invalid-route/');
            }}
            className="text-xs px-3 py-1.5 rounded-lg border border-amber-300 bg-amber-50 text-amber-800 font-medium hover:bg-amber-100 transition flex items-center gap-1.5 cursor-pointer"
          >
            <span className="font-bold text-[10px] bg-amber-200 px-1 py-0.2 rounded">GET</span>
            <span>/api/v1/invalid-route/</span>
            <span className="text-[10px] text-amber-600">(Standard Error)</span>
          </button>
        </div>
      </div>

      {/* Endpoint URL Input */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xs font-bold bg-teal-700 text-white px-2.5 py-2 rounded-lg">
          {method}
        </span>
        <input
          type="text"
          value={endpoint}
          onChange={(e) => setEndpoint(e.target.value)}
          placeholder="/api/v1/health/"
          className="flex-1 text-xs font-mono bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-800 focus:outline-teal-600"
        />
        <button
          id="btn-send-request"
          onClick={() => executeRequest()}
          disabled={loading}
          className="bg-teal-700 hover:bg-teal-800 text-white font-medium text-xs py-2 px-4 rounded-lg flex items-center gap-1.5 transition disabled:opacity-60 cursor-pointer"
        >
          <Play className="w-3.5 h-3.5" />
          <span>{loading ? 'Sending...' : 'Send'}</span>
        </button>
      </div>

      {/* Response Box */}
      <div className="bg-slate-900 rounded-xl p-4 text-slate-200 font-mono text-xs">
        <div className="flex items-center justify-between pb-2 mb-3 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <span className="text-slate-400 font-sans text-xs">Response</span>
            {statusCode !== null && (
              <span
                className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${
                  statusCode >= 200 && statusCode < 300
                    ? 'bg-emerald-900/80 text-emerald-300 border border-emerald-700'
                    : 'bg-red-900/80 text-red-300 border border-red-700'
                }`}
              >
                HTTP {statusCode}
              </span>
            )}
            {responseTime !== null && (
              <span className="text-[11px] text-slate-400 font-mono">
                {responseTime}ms
              </span>
            )}
          </div>

          {response && (
            <button
              onClick={copyResponse}
              className="text-slate-400 hover:text-white flex items-center gap-1 text-[11px] font-sans cursor-pointer"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          )}
        </div>

        {loading ? (
          <div className="py-8 text-center text-slate-400">Executing request...</div>
        ) : response ? (
          <pre className="overflow-x-auto text-[12px] leading-relaxed text-emerald-400">
            {JSON.stringify(response, null, 2)}
          </pre>
        ) : (
          <div className="py-8 text-center text-slate-500 font-sans text-xs">
            Click "Send" or a Preset above to test the standard API responses.
          </div>
        )}
      </div>

      {/* Contract Verification Info */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-3">
          <p className="font-semibold text-slate-700 mb-1">Standard Success Contract:</p>
          <code className="text-[11px] text-slate-600 block">
            &#123; success: true, data: &#123;...&#125;, message: "সফলভাবে সম্পন্ন হয়েছে" &#125;
          </code>
        </div>
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-3">
          <p className="font-semibold text-slate-700 mb-1">Standard Error Contract:</p>
          <code className="text-[11px] text-slate-600 block">
            &#123; success: false, data: null, message: "অনুরোধটি সম্পন্ন করা যায়নি", errors: &#123;...&#125; &#125;
          </code>
        </div>
      </div>
    </div>
  );
};
