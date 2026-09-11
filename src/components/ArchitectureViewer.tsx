import React from 'react';
import { Layers, Database, ShieldCheck, Cpu, KeyRound, Smartphone, Lock, UserCheck, RefreshCw } from 'lucide-react';

export const ArchitectureViewer: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: User Identity */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <div className="w-9 h-9 rounded-xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700 mb-3">
            <UserCheck className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-800 text-sm mb-1">Unified User Identity</h3>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            Single account architecture. Mobile number is the unique primary identifier (+8801XXXXXXXXX).
          </p>
          <div className="text-[11px] font-mono bg-slate-50 text-slate-600 p-2 rounded-lg space-y-1">
            <div>• Model: apps.authentication.User</div>
            <div>• Sub-roles: Future extensibility</div>
            <div>• Canonical E.164 format</div>
          </div>
        </div>

        {/* Card 2: Cryptographic OTP */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <div className="w-9 h-9 rounded-xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-700 mb-3">
            <Lock className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-800 text-sm mb-1">Cryptographic OTP Engine</h3>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            No plain-text OTP storage. HMAC-SHA256 salted hashes, 5-minute expiry, and brute-force defenses.
          </p>
          <div className="text-[11px] font-mono bg-slate-50 text-slate-600 p-2 rounded-lg space-y-1">
            <div>• Code: 6-digit CSPRNG</div>
            <div>• Salt: 32-byte secure random</div>
            <div>• Max Attempts: 5 before lock</div>
          </div>
        </div>

        {/* Card 3: JWT Token Lifecycle */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <div className="w-9 h-9 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-700 mb-3">
            <KeyRound className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-800 text-sm mb-1">JWT Bearer Architecture</h3>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            Stateless authentication with short-lived access tokens and revocable refresh tokens.
          </p>
          <div className="text-[11px] font-mono bg-slate-50 text-slate-600 p-2 rounded-lg space-y-1">
            <div>• Access: 60 minutes expiry</div>
            <div>• Refresh: 30 days lifetime</div>
            <div>• Blacklist: Redis/Cache backed</div>
          </div>
        </div>

        {/* Card 4: Flutter Mobile Auth */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <div className="w-9 h-9 rounded-xl bg-purple-50 border border-purple-200 flex items-center justify-center text-purple-700 mb-3">
            <Smartphone className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-800 text-sm mb-1">Flutter Clean Architecture</h3>
          <p className="text-xs text-slate-500 mb-3 leading-relaxed">
            Repository pattern with FlutterSecureStorage, Stream-based AuthState, and auto-refresh interceptor.
          </p>
          <div className="text-[11px] font-mono bg-slate-50 text-slate-600 p-2 rounded-lg space-y-1">
            <div>• AuthRepository + StreamController</div>
            <div>• Automatic 401 token refresh</div>
            <div>• Secure Token Keystore / Keychain</div>
          </div>
        </div>
      </div>

      {/* Auth Data Flow Diagram */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
        <h3 className="font-bold text-slate-800 text-sm mb-3">Phase 2 Authentication & Identity Data Flow</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs">
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="font-bold text-teal-800 mb-1">1. OTP Request</div>
            <p className="text-slate-600 leading-relaxed text-[11px]">
              User inputs phone (e.g. 01711223344). Mobile normalizes to <code>+8801711223344</code>. Backend checks rate limit, creates salted OTP record, and dispatches SMS.
            </p>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="font-bold text-teal-800 mb-1">2. Verification</div>
            <p className="text-slate-600 leading-relaxed text-[11px]">
              User submits 6-digit code. Backend hashes with record salt, checks expiration and attempt count. On match, marks verified and invalidates OTP.
            </p>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="font-bold text-teal-800 mb-1">3. Token Issuance</div>
            <p className="text-slate-600 leading-relaxed text-[11px]">
              Backend signs Access & Refresh JWT tokens. Mobile client persists tokens in secure keychain/keystore and broadcasts authenticated state.
            </p>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="font-bold text-teal-800 mb-1">4. Session & Refresh</div>
            <p className="text-slate-600 leading-relaxed text-[11px]">
              Subsequent API requests attach <code>Authorization: Bearer &lt;token&gt;</code>. On 401 expiry, ApiClient automatically invokes refresh endpoint.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
