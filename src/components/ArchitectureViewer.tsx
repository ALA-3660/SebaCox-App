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

        {/* Card 5: Geographic & Location Engine */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs md:col-span-2 lg:col-span-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-9 h-9 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-800 text-sm">Phase 3 — Location & Geographic Foundation (SRID 4326)</h3>
              <p className="text-xs text-slate-500">“কক্সবাজার দিয়ে শুরু, সমগ্র বাংলাদেশ ও আন্তর্জাতিক সীমানায় সম্প্রসারণযোগ্য।”</p>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 mt-3 text-xs">
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
              <span className="font-bold text-teal-800">1. Global SRID 4326</span>
              <p className="text-slate-600 text-[11px]">
                Global standard coordinates (Decimal 10,7). Validated for latitude [-90, +90] and longitude [-180, +180].
              </p>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
              <span className="font-bold text-teal-800">2. 9-Tier Hierarchy</span>
              <p className="text-slate-600 text-[11px]">
                Country → Division → District → Upazila → Municipality/City Corp → Union → Ward → Locality.
              </p>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
              <span className="font-bold text-teal-800">3. Context Separation</span>
              <p className="text-slate-600 text-[11px]">
                Strict decoupling: <code>CURRENT</code> GPS location never automatically overwrites <code>SELECTED</code> service area.
              </p>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
              <span className="font-bold text-teal-800">4. Haversine & Search</span>
              <p className="text-slate-600 text-[11px]">
                Accurate spherical distance & bounding box queries. Bilingual search engine with Bangla NFC Unicode normalization.
              </p>
            </div>
          </div>
        </div>
        {/* Card 6: Category & Service Engine Foundation */}
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs md:col-span-2 lg:col-span-4">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-9 h-9 rounded-xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-slate-800 text-sm">Phase 4 — Universal Category & Service Foundation</h3>
              <p className="text-xs text-slate-500">“মানুষের প্রয়োজন থেকে সেবার সমাধান — কোনো হার্ডকোডেড বিজনেস মডিউল নয়।”</p>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 mt-3 text-xs">
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
              <span className="font-bold text-teal-800">1. Taxonomy Separation</span>
              <p className="text-slate-600 text-[11px]">
                Strict division between <code>PUBLIC_SERVICE_CATEGORY</code> (31 public categories) and <code>SYSTEM_DOMAIN</code> (15 operational domains). Recursive parent-child tree.
              </p>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
              <span className="font-bold text-teal-800">2. Single Source of Truth</span>
              <p className="text-slate-600 text-[11px]">
                Service model acts as single capability authority: 10 operational flags drive dynamic frontend workflows (booking, demand, offer, negotiation, delivery, etc.).
              </p>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
              <span className="font-bold text-teal-800">3. Integrity & Circular Defense</span>
              <p className="text-slate-600 text-[11px]">
                Strict slug validation (alphanumeric & hyphens) and recursive graph cycle detection preventing direct self-parenting and transitive circular loops.
              </p>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
              <span className="font-bold text-teal-800">4. Global Bangla Typography</span>
              <p className="text-slate-600 text-[11px]">
                Hind Siliguri for large headings, Baloo Da 2 for medium headings, and Tiro Bangla for body text across all screens and cards.
              </p>
            </div>
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
