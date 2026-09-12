import React, { useState } from 'react';
import { 
  Smartphone, 
  Terminal, 
  Layers, 
  FolderTree, 
  CheckCircle2, 
  BookOpen, 
  ExternalLink,
  ShieldCheck,
  Server
} from 'lucide-react';
import { FlutterSimulator } from './components/FlutterSimulator';
import { ApiConsole } from './components/ApiConsole';
import { ArchitectureViewer } from './components/ArchitectureViewer';
import { FileExplorer } from './components/FileExplorer';
import { TestResultsView } from './components/TestResultsView';

type TabType = 'simulator' | 'api' | 'architecture' | 'files' | 'tests' | 'run';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabType>('simulator');

  return (
    <div className="min-h-screen bg-slate-100/70 text-slate-800 flex flex-col font-sans">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3.5 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-700 text-white flex items-center justify-center font-black text-lg shadow-xs">
              SC
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-black tracking-tight text-slate-900">SebaCox (সেবাকক্স)</h1>
                <span className="text-[11px] font-bold bg-teal-50 text-teal-800 px-2 py-0.5 rounded-full border border-teal-200">
                  Phase 4 — Category & Service Foundation
                </span>
              </div>
              <p className="text-xs text-teal-800 font-medium">
                “মানুষের প্রয়োজন থেকে সেবার সমাধান।”
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>46 Master Taxonomy Modules • Live</span>
            </div>
            <span className="text-slate-400">|</span>
            <span className="text-slate-500 font-medium">Cox's Bazar, Bangladesh</span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex gap-1 overflow-x-auto border-t border-slate-100 pt-1">
          <button
            id="tab-flutter-simulator"
            onClick={() => setActiveTab('simulator')}
            className={`px-3.5 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 cursor-pointer whitespace-nowrap ${
              activeTab === 'simulator'
                ? 'border-b-2 border-teal-700 text-teal-900 bg-teal-50/50'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span>Flutter App & States</span>
          </button>

          <button
            id="tab-api-console"
            onClick={() => setActiveTab('api')}
            className={`px-3.5 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 cursor-pointer whitespace-nowrap ${
              activeTab === 'api'
                ? 'border-b-2 border-teal-700 text-teal-900 bg-teal-50/50'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>API & Responses</span>
          </button>

          <button
            id="tab-architecture"
            onClick={() => setActiveTab('architecture')}
            className={`px-3.5 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 cursor-pointer whitespace-nowrap ${
              activeTab === 'architecture'
                ? 'border-b-2 border-teal-700 text-teal-900 bg-teal-50/50'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Architecture & Security</span>
          </button>

          <button
            id="tab-file-explorer"
            onClick={() => setActiveTab('files')}
            className={`px-3.5 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 cursor-pointer whitespace-nowrap ${
              activeTab === 'files'
                ? 'border-b-2 border-teal-700 text-teal-900 bg-teal-50/50'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <FolderTree className="w-3.5 h-3.5" />
            <span>File Structure</span>
          </button>

          <button
            id="tab-tests"
            onClick={() => setActiveTab('tests')}
            className={`px-3.5 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 cursor-pointer whitespace-nowrap ${
              activeTab === 'tests'
                ? 'border-b-2 border-teal-700 text-teal-900 bg-teal-50/50'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            <span>Verification Matrix</span>
          </button>

          <button
            id="tab-run-guide"
            onClick={() => setActiveTab('run')}
            className={`px-3.5 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 cursor-pointer whitespace-nowrap ${
              activeTab === 'run'
                ? 'border-b-2 border-teal-700 text-teal-900 bg-teal-50/50'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>Run Instructions</span>
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 flex-1 w-full">
        {activeTab === 'simulator' && <FlutterSimulator />}
        {activeTab === 'api' && <ApiConsole />}
        {activeTab === 'architecture' && <ArchitectureViewer />}
        {activeTab === 'files' && <FileExplorer />}
        {activeTab === 'tests' && <TestResultsView />}
        {activeTab === 'run' && (
          <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-6">
            <div>
              <h2 className="text-base font-bold text-slate-900 mb-1">Execution & Deployment Guide</h2>
              <p className="text-xs text-slate-500">
                Step-by-step instructions to run Django REST API, PostgreSQL, Redis, and Flutter client.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Backend Instructions */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 pb-2 border-b border-slate-200">
                  <Server className="w-4 h-4 text-blue-600" />
                  <h3 className="text-sm font-bold text-slate-800">1. How to Run Backend</h3>
                </div>

                <div className="space-y-2 text-xs">
                  <p className="font-semibold text-slate-700">Option A: Direct Python</p>
                  <pre className="bg-slate-900 text-emerald-400 p-3 rounded-xl font-mono text-[11px] overflow-x-auto leading-relaxed">
{`cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000`}
                  </pre>
                </div>

                <div className="space-y-2 text-xs">
                  <p className="font-semibold text-slate-700">Option B: Docker Compose (All Services)</p>
                  <pre className="bg-slate-900 text-emerald-400 p-3 rounded-xl font-mono text-[11px] overflow-x-auto leading-relaxed">
{`cd infrastructure
docker compose up --build`}
                  </pre>
                </div>
              </div>

              {/* Flutter Instructions */}
              <div className="space-y-4">
                <div className="flex items-center gap-2 pb-2 border-b border-slate-200">
                  <Smartphone className="w-4 h-4 text-teal-600" />
                  <h3 className="text-sm font-bold text-slate-800">2. How to Run Flutter</h3>
                </div>

                <div className="space-y-2 text-xs">
                  <p className="font-semibold text-slate-700">Mobile Device / Simulator / Chrome</p>
                  <pre className="bg-slate-900 text-emerald-400 p-3 rounded-xl font-mono text-[11px] overflow-x-auto leading-relaxed">
{`cd mobile
flutter pub get

# Run on connected device/emulator
flutter run

# Or run in Chrome browser
flutter run -d chrome`}
                  </pre>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-xs space-y-2">
                  <p className="font-semibold text-slate-800">Health Endpoint Verification:</p>
                  <p className="text-slate-600">
                    Once the backend is started, verify with curl:
                  </p>
                  <pre className="bg-slate-900 text-slate-200 p-2 rounded-lg font-mono text-[11px] overflow-x-auto">
                    curl http://localhost:8000/api/v1/health/
                  </pre>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-4 px-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>SebaCox • লোকেশন ও ক্যাটাগরি-ভিত্তিক মাল্টি-সার্ভিস প্ল্যাটফর্ম • Phase 1–4 Verified (107 Tests)</span>
          <span className="font-medium text-slate-700">“মানুষের প্রয়োজন থেকে সেবার সমাধান।”</span>
        </div>
      </footer>
    </div>
  );
}
