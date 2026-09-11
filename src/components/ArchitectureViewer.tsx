import React from 'react';
import { Layers, Database, ShieldCheck, Cpu, GitBranch, CheckCircle2 } from 'lucide-react';

export const ArchitectureViewer: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* 4 Pillars Architecture Diagram */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Layer 1: Flutter */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <div className="w-9 h-9 rounded-xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700 mb-3">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-800 text-sm mb-1">Flutter Mobile App</h3>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            Clean architecture client with decoupled ApiClient, EnvConfig base URL, and Material 3 theme.
          </p>
          <div className="text-[11px] font-mono bg-slate-50 text-slate-600 p-2 rounded-lg space-y-1">
            <div>• Core: network/api_client.dart</div>
            <div>• Feature: home/home_screen.dart</div>
            <div>• Theme: Coastal Teal & Slate</div>
          </div>
        </div>

        {/* Layer 2: Django REST */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <div className="w-9 h-9 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-700 mb-3">
            <Cpu className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-800 text-sm mb-1">Django REST API</h3>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            Modular backend with versioned routing (/api/v1/), unified exception handler, and strict settings.
          </p>
          <div className="text-[11px] font-mono bg-slate-50 text-slate-600 p-2 rounded-lg space-y-1">
            <div>• Endpoint: /api/v1/health/</div>
            <div>• Common: responses & exceptions</div>
            <div>• Settings: base, dev, prod</div>
          </div>
        </div>

        {/* Layer 3: PostgreSQL */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <div className="w-9 h-9 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-700 mb-3">
            <Database className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-800 text-sm mb-1">PostgreSQL 16+</h3>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            Relational storage managed via DATABASE_URL with connection pooling. Zero hardcoded passwords.
          </p>
          <div className="text-[11px] font-mono bg-slate-50 text-slate-600 p-2 rounded-lg space-y-1">
            <div>• Engine: psycopg3 binary</div>
            <div>• Pooling: CONN_MAX_AGE 600</div>
            <div>• No Phase 2 models yet</div>
          </div>
        </div>

        {/* Layer 4: Redis & Celery */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <div className="w-9 h-9 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-700 mb-3">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-800 text-sm mb-1">Redis & Workers</h3>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            High performance in-memory caching and Celery message broker configured via REDIS_URL.
          </p>
          <div className="text-[11px] font-mono bg-slate-50 text-slate-600 p-2 rounded-lg space-y-1">
            <div>• Cache: django-redis backend</div>
            <div>• Broker: Celery workers</div>
            <div>• Rate limiting & OTP ready</div>
          </div>
        </div>
      </div>

      {/* Security & Production Hardening Checklist */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
        <h3 className="font-bold text-slate-800 text-sm mb-3 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Production Security Baseline (Requirement 13)</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div className="flex items-start gap-2.5 p-2.5 rounded-xl bg-slate-50">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-slate-800">DEBUG=False Strictly Enforced</p>
              <p className="text-slate-500 text-[11px]">
                config/settings/production.py raises an exception if DEBUG=True or if SECRET_KEY is default.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-2.5 p-2.5 rounded-xl bg-slate-50">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-slate-800">Sensitive Data Log Masking</p>
              <p className="text-slate-500 text-[11px]">
                SensitiveDataFilter redacts passwords, OTPs, tokens, cards, and secrets from server logs.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-2.5 p-2.5 rounded-xl bg-slate-50">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-slate-800">Strict CORS Separation</p>
              <p className="text-slate-500 text-[11px]">
                Wildcard origins (*) are disabled in production; only explicit origins in CORS_ALLOWED_ORIGINS are accepted.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-2.5 p-2.5 rounded-xl bg-slate-50">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-slate-800">Production Security Headers</p>
              <p className="text-slate-500 text-[11px]">
                Includes HSTS (31536000s), SSL Redirect, nosniff, DENY X-Frame-Options, and secure cookies.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
