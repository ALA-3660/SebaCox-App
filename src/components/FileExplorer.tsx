import React, { useState } from 'react';
import { Folder, FileText, Code2, Copy, Check } from 'lucide-react';
import { ProjectFileItem } from '../types';

const PROJECT_FILES: ProjectFileItem[] = [
  {
    path: 'backend/config/settings/base.py',
    name: 'base.py',
    category: 'backend',
    description: 'Shared Django settings with PostgreSQL, Redis, DRF, and sensitive data logging filter.',
    content: `BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        ...
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL'),
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'common.exceptions.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}`
  },
  {
    path: 'backend/config/settings/production.py',
    name: 'production.py',
    category: 'backend',
    description: 'Production settings strictly enforcing DEBUG=False, non-wildcard CORS, and SSL/HSTS hardening.',
    content: `from .base import *

# HARD REQUIREMENT: DEBUG must never be True in production
DEBUG = False

if not os.environ.get('SECRET_KEY') or 'django-insecure' in os.environ.get('SECRET_KEY'):
    raise ValueError("Production SECRET_KEY environment variable is missing or insecure!")

# Strict CORS: Wildcard is strictly forbidden
CORS_ALLOW_ALL_ORIGINS = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000`
  },
  {
    path: 'backend/common/responses.py',
    name: 'responses.py',
    category: 'backend',
    description: 'Unified StandardResponse factory for consistent success and error API contracts.',
    content: `class StandardResponse:
    @staticmethod
    def success(data=None, message="সফলভাবে সম্পন্ন হয়েছে", status_code=200):
        return Response({
            "success": True,
            "data": data or {},
            "message": message
        }, status=status_code)

    @staticmethod
    def error(message="অনুরোধটি সম্পন্ন করা যায়নি", errors=None, status_code=400):
        return Response({
            "success": False,
            "data": None,
            "message": message,
            "errors": errors or {}
        }, status=status_code)`
  },
  {
    path: 'backend/common/health.py',
    name: 'health.py',
    category: 'backend',
    description: 'GET /api/v1/health/ view returning standard health status without leaking internal secrets.',
    content: `class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return StandardResponse.success(
            data={"status": "healthy"},
            message="SebaCox API is running"
        )`
  },
  {
    path: 'backend/common/filters.py',
    name: 'filters.py',
    category: 'backend',
    description: 'Logging filter that automatically redacts passwords, OTPs, tokens, and credentials.',
    content: `class SensitiveDataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Masks passwords, OTPs, auth bearer tokens, and credit card numbers
        ...`
  },
  {
    path: 'mobile/lib/core/network/api_client.dart',
    name: 'api_client.dart',
    category: 'mobile',
    description: 'Reusable Flutter HTTP client handling timeouts, network exceptions, and standard JSON decoding.',
    content: `class ApiClient {
  Future<ApiResponse<T>> get<T>(String endpoint, { ... }) async {
    try {
      final response = await _client.get(uri).timeout(EnvConfig.connectTimeout);
      return _processResponse<T>(response, fromJson);
    } on TimeoutException {
      throw const TimeoutNetworkException();
    } on SocketException {
      throw const NoInternetNetworkException();
    }
  }
}`
  },
  {
    path: 'mobile/lib/features/home/home_screen.dart',
    name: 'home_screen.dart',
    category: 'mobile',
    description: 'Flutter Phase 1 foundation screen demonstrating the 3 backend connection states in Bengali.',
    content: `// 3 Connection States:
// 1. সংযোগ পরীক্ষা হচ্ছে...
// 2. সার্ভারের সাথে সংযোগ সফল
// 3. সার্ভারের সাথে সংযোগ ব্যর্থ

final response = await _apiClient.get<HealthStatus>(
  ApiConstants.healthEndpoint,
  fromJson: (json) => HealthStatus.fromJson(json),
);`
  },
  {
    path: 'infrastructure/docker-compose.yml',
    name: 'docker-compose.yml',
    category: 'infrastructure',
    description: 'Local development orchestration for Django, PostgreSQL 16, Redis 7, and Celery worker.',
    content: `services:
  postgres:
    image: postgres:16-alpine
  redis:
    image: redis:7-alpine
  backend:
    build:
      dockerfile: infrastructure/docker/Dockerfile.backend
    command: python manage.py runserver 0.0.0.0:8000
  celery_worker:
    command: celery -A workers.celery worker --loglevel=info`
  },
  {
    path: 'README.md',
    name: 'README.md',
    category: 'root',
    description: 'Comprehensive project README covering architecture, run instructions, and endpoints.',
    content: `# SebaCox (সেবাকক্স) — Phase 1 Foundation
Product Principle: “মানুষের প্রয়োজন থেকে সেবার সমাধান।”
...`
  }
];

export const FileExplorer: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<ProjectFileItem>(PROJECT_FILES[0]);
  const [copied, setCopied] = useState<boolean>(false);

  const copyCode = () => {
    navigator.clipboard.writeText(selectedFile.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-xs grid grid-cols-1 md:grid-cols-12">
      {/* File List Column */}
      <div className="md:col-span-4 border-r border-slate-200 bg-slate-50/70 p-4">
        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">
          Phase 1 Architecture Files
        </h3>
        <div className="space-y-1">
          {PROJECT_FILES.map((file) => (
            <button
              key={file.path}
              onClick={() => setSelectedFile(file)}
              className={`w-full text-left px-3 py-2 rounded-xl text-xs font-mono flex items-center justify-between transition cursor-pointer ${
                selectedFile.path === file.path
                  ? 'bg-teal-700 text-white font-bold shadow-xs'
                  : 'text-slate-700 hover:bg-slate-200/60'
              }`}
            >
              <div className="flex items-center gap-2 truncate">
                <FileText className="w-3.5 h-3.5 shrink-0" />
                <span className="truncate">{file.name}</span>
              </div>
              <span
                className={`text-[9px] uppercase px-1.5 py-0.5 rounded font-sans ${
                  selectedFile.path === file.path
                    ? 'bg-teal-800 text-teal-100'
                    : 'bg-slate-200 text-slate-600'
                }`}
              >
                {file.category}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Code Preview Column */}
      <div className="md:col-span-8 p-4 flex flex-col bg-slate-900 text-slate-200">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
          <div>
            <p className="text-xs font-mono font-bold text-teal-400">{selectedFile.path}</p>
            <p className="text-[11px] text-slate-400 mt-0.5">{selectedFile.description}</p>
          </div>
          <button
            onClick={copyCode}
            className="text-xs text-slate-400 hover:text-white flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 px-2.5 py-1.5 rounded-lg transition cursor-pointer"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>

        <pre className="text-xs font-mono text-slate-300 overflow-x-auto leading-relaxed p-2 bg-slate-950/60 rounded-xl flex-1">
          {selectedFile.content}
        </pre>
      </div>
    </div>
  );
};
