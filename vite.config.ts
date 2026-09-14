import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import {defineConfig} from 'vite';
import { INITIAL_46_TAXONOMY_CATEGORIES, INITIAL_SERVICES } from './src/data/taxonomyMockData';
import { SEBACOX_MASTER_CATEGORIES, ALL_MASTER_SUB_CATEGORIES } from './src/data/categoryMasterData';
import { INITIAL_MOCK_DEMANDS, MockDemand } from './src/data/demandMockData';

export default defineConfig(() => {
  return {
    plugins: [
      react(),
      tailwindcss(),
      {
        name: 'sebacox-api-middleware',
        configureServer(server) {
          // In-memory mock store for Vite dev preview
          const users = new Map();
          const otps = new Map();
          const activeSessions = new Map();
          const demandsStore = [...INITIAL_MOCK_DEMANDS];
          let nextUserId = 101;

          // Normalize BD mobile helper
          const normalizeBD = (raw) => {
            const cleaned = String(raw || '').replace(/[\s\-\(\)\.]/g, '').trim();
            const bdRegex = /^(?:\+?88)?01[3-9]\d{8}$/;
            if (!cleaned) throw new Error('মোবাইল নম্বর প্রদান করা আবশ্যক।');
            if (cleaned.startsWith('+8801') && cleaned.length === 14 && bdRegex.test(cleaned)) return cleaned;
            if (cleaned.startsWith('8801') && cleaned.length === 13 && bdRegex.test('+' + cleaned)) return '+' + cleaned;
            if (cleaned.startsWith('01') && cleaned.length === 11 && bdRegex.test('+88' + cleaned)) return '+88' + cleaned;
            throw new Error('সঠিক বাংলাদেশি মোবাইল নম্বর দিন (যেমন: 017XXXXXXXX বা +88017XXXXXXXX)।');
          };

          const parseBody = (req: any): Promise<any> => {
            return new Promise((resolve) => {
              let body = '';
              req.on('data', (chunk: any) => { body += chunk; });
              req.on('end', () => {
                try {
                  resolve(body ? JSON.parse(body) : {});
                } catch {
                  resolve({});
                }
              });
            });
          };

          server.middlewares.use(async (req: any, res: any, next: any) => {
            const pathname = req.url ? req.url.split('?')[0].replace(/\/+$/, '') : '';
            res.setHeader('Content-Type', 'application/json');

            if (pathname === '/api/v1/health') {
              res.end(JSON.stringify({
                success: true,
                data: { status: 'healthy', phase: 'Phase 2: Authentication Foundation' },
                message: 'SebaCox API is running',
              }));
              return;
            }

            // Register: Request OTP
            if (pathname === '/api/v1/auth/register/request-otp' && req.method === 'POST') {
              const body = await parseBody(req);
              try {
                const mobile = normalizeBD(body.mobile_number);
                if (users.has(mobile) && users.get(mobile).is_verified) {
                  res.statusCode = 400;
                  res.end(JSON.stringify({
                    success: false,
                    data: null,
                    message: 'এই মোবাইল নম্বরটি দিয়ে ইতোমধ্যে একাউন্ট খোলা হয়েছে। অনুগ্রহ করে লগইন করুন।',
                    errors: { mobile_number: ['এই নম্বর দিয়ে ইতিমধ্যে একাউন্ট রয়েছে।'] }
                  }));
                  return;
                }
                otps.set(`${mobile}:register`, { code: '123456', expiresAt: Date.now() + 300000 });
                res.end(JSON.stringify({
                  success: true,
                  data: {
                    mobile_number: mobile,
                    expires_in: 300,
                    dev_otp: '123456',
                    purpose: 'registration'
                  },
                  message: 'ওটিপি সফলভাবে পাঠানো হয়েছে।'
                }));
              } catch (err) {
                res.statusCode = 400;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: err.message,
                  errors: { mobile_number: [err.message] }
                }));
              }
              return;
            }

            // Register: Verify OTP
            if (pathname === '/api/v1/auth/register/verify-otp' && req.method === 'POST') {
              const body = await parseBody(req);
              try {
                const mobile = normalizeBD(body.mobile_number);
                const code = String(body.otp_code || '').trim();
                const stored = otps.get(`${mobile}:register`);
                if (!stored || (stored.code !== code && code !== '123456')) {
                  res.statusCode = 400;
                  res.end(JSON.stringify({
                    success: false,
                    data: null,
                    message: 'ভুল ওটিপি কোড। অনুগ্রহ করে পুনরায় চেষ্টা করুন।',
                    errors: { otp_code: ['ভুল কোড'] }
                  }));
                  return;
                }
                otps.delete(`${mobile}:register`);
                const user = {
                  id: users.has(mobile) ? users.get(mobile).id : nextUserId++,
                  mobile_number: mobile,
                  email: null,
                  is_verified: true,
                  created_at: new Date().toISOString()
                };
                users.set(mobile, user);
                const token = 'mock_jwt_access_' + Math.random().toString(36).substring(2);
                const refreshToken = 'mock_jwt_refresh_' + Math.random().toString(36).substring(2);
                activeSessions.set(token, user);
                activeSessions.set(refreshToken, { user, type: 'refresh' });

                res.end(JSON.stringify({
                  success: true,
                  data: {
                    user,
                    tokens: {
                      access_token: token,
                      refresh_token: refreshToken,
                      token_type: 'Bearer',
                      expires_in: 3600
                    }
                  },
                  message: 'রেজিস্ট্রেশন এবং ওটিপি যাচাই সফল হয়েছে।'
                }));
              } catch (err) {
                res.statusCode = 400;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: err.message,
                  errors: { detail: err.message }
                }));
              }
              return;
            }

            // Login: Request OTP
            if (pathname === '/api/v1/auth/login/request-otp' && req.method === 'POST') {
              const body = await parseBody(req);
              try {
                const mobile = normalizeBD(body.mobile_number);
                otps.set(`${mobile}:login`, { code: '123456', expiresAt: Date.now() + 300000 });
                res.end(JSON.stringify({
                  success: true,
                  data: {
                    mobile_number: mobile,
                    expires_in: 300,
                    dev_otp: '123456',
                    purpose: 'login'
                  },
                  message: 'লগইন ওটিপি সফলভাবে পাঠানো হয়েছে।'
                }));
              } catch (err) {
                res.statusCode = 400;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: err.message,
                  errors: { mobile_number: [err.message] }
                }));
              }
              return;
            }

            // Login: Verify OTP
            if (pathname === '/api/v1/auth/login/verify-otp' && req.method === 'POST') {
              const body = await parseBody(req);
              try {
                const mobile = normalizeBD(body.mobile_number);
                const code = String(body.otp_code || '').trim();
                const stored = otps.get(`${mobile}:login`);
                if (!stored || (stored.code !== code && code !== '123456')) {
                  res.statusCode = 400;
                  res.end(JSON.stringify({
                    success: false,
                    data: null,
                    message: 'ভুল ওটিপি কোড। অনুগ্রহ করে পুনরায় চেষ্টা করুন।',
                    errors: { otp_code: ['ভুল কোড'] }
                  }));
                  return;
                }
                otps.delete(`${mobile}:login`);
                let user = users.get(mobile);
                if (!user) {
                  user = {
                    id: nextUserId++,
                    mobile_number: mobile,
                    email: null,
                    is_verified: true,
                    created_at: new Date().toISOString()
                  };
                  users.set(mobile, user);
                }
                const token = 'mock_jwt_access_' + Math.random().toString(36).substring(2);
                const refreshToken = 'mock_jwt_refresh_' + Math.random().toString(36).substring(2);
                activeSessions.set(token, user);
                activeSessions.set(refreshToken, { user, type: 'refresh' });

                res.end(JSON.stringify({
                  success: true,
                  data: {
                    user,
                    tokens: {
                      access_token: token,
                      refresh_token: refreshToken,
                      token_type: 'Bearer',
                      expires_in: 3600
                    }
                  },
                  message: 'লগইন সফল হয়েছে।'
                }));
              } catch (err) {
                res.statusCode = 400;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: err.message,
                  errors: { detail: err.message }
                }));
              }
              return;
            }

            // Token Refresh
            if (pathname === '/api/v1/auth/token/refresh' && req.method === 'POST') {
              const body = await parseBody(req);
              const rToken = body.refresh_token;
              const session = activeSessions.get(rToken);
              if (!session || session.type !== 'refresh') {
                res.statusCode = 401;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: 'রিফ্রেশ টোকেনটি অবৈধ বা এর মেয়াদ শেষ হয়ে গেছে।',
                  errors: { detail: 'অবৈধ রিফ্রেশ টোকেন' }
                }));
                return;
              }
              const newAccess = 'mock_jwt_access_' + Math.random().toString(36).substring(2);
              activeSessions.set(newAccess, session.user);
              res.end(JSON.stringify({
                success: true,
                data: {
                  access_token: newAccess,
                  token_type: 'Bearer',
                  expires_in: 3600
                },
                message: 'টোকেন সফলভাবে রিফ্রেশ করা হয়েছে।'
              }));
              return;
            }

            // Current User
            if (pathname === '/api/v1/auth/me' && req.method === 'GET') {
              const authHeader = req.headers['authorization'] || '';
              const token = authHeader.replace(/^Bearer\s+/i, '');
              const user = activeSessions.get(token);
              if (!user) {
                res.statusCode = 401;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: 'প্রমাণীকরণ আবশ্যক। অনুমোদন টোকেন প্রদান করুন।',
                  errors: { detail: 'প্রমাণীকরণ তথ্য প্রদান করা হয়নি।' }
                }));
                return;
              }
              res.end(JSON.stringify({
                success: true,
                data: user,
                message: 'ব্যবহারকারী প্রোফাইল সফলভাবে পাওয়া গেছে।'
              }));
              return;
            }

            // Logout
            if (pathname === '/api/v1/auth/logout' && req.method === 'POST') {
              const body = await parseBody(req);
              if (body.refresh_token) {
                activeSessions.delete(body.refresh_token);
              }
              const authHeader = req.headers['authorization'] || '';
              const token = authHeader.replace(/^Bearer\s+/i, '');
              if (token) {
                activeSessions.delete(token);
              }
              res.end(JSON.stringify({
                success: true,
                data: null,
                message: 'লগআউট সফলভাবে সম্পন্ন হয়েছে।'
              }));
              return;
            }

            // ==========================================
            // PHASE 3: LOCATION & GEOGRAPHIC FOUNDATION
            // ==========================================
            const locationStore = {
              countries: [
                { id: 1, name_bn: 'বাংলাদেশ', name_en: 'Bangladesh', code: 'BGD', is_active: true }
              ],
              divisions: [
                { id: 1, country_id: 1, name_bn: 'চট্টগ্রাম', name_en: 'Chattogram', code: 'CTG', is_active: true },
                { id: 2, country_id: 1, name_bn: 'ঢাকা', name_en: 'Dhaka', code: 'DHK', is_active: true }
              ],
              districts: [
                { id: 1, division_id: 1, name_bn: 'কক্সবাজার', name_en: "Cox's Bazar", code: 'CXB', is_active: true },
                { id: 2, division_id: 1, name_bn: 'চট্টগ্রাম', name_en: 'Chattogram', code: 'CHIT', is_active: true },
                { id: 3, division_id: 2, name_bn: 'ঢাকা', name_en: 'Dhaka', code: 'DHAK', is_active: true }
              ],
              upazilas: [
                { id: 1, district_id: 1, name_bn: 'কক্সবাজার সদর', name_en: "Cox's Bazar Sadar", code: 'CXB-SADAR', is_active: true },
                { id: 2, district_id: 1, name_bn: 'চকোরিয়া', name_en: 'Chakaria', code: 'CXB-CHAK', is_active: true },
                { id: 3, district_id: 1, name_bn: 'মহেশখালী', name_en: 'Maheshkhali', code: 'CXB-MAH', is_active: true },
                { id: 4, district_id: 1, name_bn: 'রামু', name_en: 'Ramu', code: 'CXB-RAM', is_active: true },
                { id: 5, district_id: 1, name_bn: 'টেকনাফ', name_en: 'Teknaf', code: 'CXB-TEK', is_active: true },
                { id: 6, district_id: 1, name_bn: 'উখিয়া', name_en: 'Ukhiya', code: 'CXB-UKH', is_active: true },
                { id: 7, district_id: 1, name_bn: 'কুতুবদিয়া', name_en: 'Kutubdia', code: 'CXB-KUT', is_active: true },
                { id: 8, district_id: 1, name_bn: 'পেকুয়া', name_en: 'Pekua', code: 'CXB-PEK', is_active: true },
                { id: 9, district_id: 1, name_bn: 'ঈদগাঁও', name_en: 'Eidgaon', is_active: true }
              ],
              unions: [
                { id: 1, upazila_id: 1, name_bn: 'ঝিলংজা', name_en: 'Jhilongja', code: 'CXB-JHIL', is_active: true },
                { id: 2, upazila_id: 1, name_bn: 'পিএমখালী', name_en: 'PM Khali', code: 'CXB-PMKH', is_active: true },
                { id: 3, upazila_id: 1, name_bn: 'খুরুশকুল', name_en: 'Khurushkul', code: 'CXB-KHUR', is_active: true },
                { id: 4, upazila_id: 1, name_bn: 'পাটলীমাউখালী', name_en: 'Patali Machhuakhali', code: 'CXB-PATM', is_active: true },
                { id: 5, upazila_id: 1, name_bn: 'ভারুয়াখালী', name_en: 'Bharuakhali', code: 'CXB-BHAR', is_active: true },
                { id: 6, upazila_id: 4, name_bn: 'ফতেখাঁরকুল', name_en: 'Fatekharkul', code: 'CXB-FATE', is_active: true },
                { id: 7, upazila_id: 4, name_bn: 'জোয়ারিয়ানালা', name_en: 'Joarianala', code: 'CXB-JOAR', is_active: true },
                { id: 8, upazila_id: 6, name_bn: 'রত্নাপালং', name_en: 'Ratnapalong', code: 'CXB-RATN', is_active: true },
                { id: 9, upazila_id: 6, name_bn: 'রাজাপালং', name_en: 'Rajapalong', code: 'CXB-RAJA', is_active: true },
                { id: 10, upazila_id: 5, name_bn: 'বাহারছড়া', name_en: 'Baharchhara', code: 'CXB-BAHA', is_active: true },
                { id: 11, upazila_id: 5, name_bn: 'সেন্টমার্টিন', name_en: 'Saint Martin', code: 'CXB-STM', is_active: true },
                { id: 12, upazila_id: 9, name_bn: 'ঈদগাঁও সদর', name_en: 'Eidgaon Sadar', code: 'CXB-EIDG', is_active: true },
                { id: 13, upazila_id: 9, name_bn: 'জালালাবাদ', name_en: 'Jalalabad', code: 'CXB-JALAL', is_active: true },
                { id: 14, upazila_id: 9, name_bn: 'ইসলামাবাদ', name_en: 'Islamabad', code: 'CXB-ISLAM', is_active: true }
              ],
              municipalities: [
                { id: 1, district_id: 1, upazila_id: 1, name_bn: 'কক্সবাজার পৌরসভা', name_en: "Cox's Bazar Pourashava", code: 'CXB-POUR-1', is_active: true },
                { id: 2, district_id: 1, upazila_id: 2, name_bn: 'চকোরিয়া পৌরসভা', name_en: 'Chakaria Pourashava', code: 'CXB-POUR-2', is_active: true },
                { id: 3, district_id: 1, upazila_id: 3, name_bn: 'মহেশখালী পৌরসভা', name_en: 'Maheshkhali Pourashava', code: 'CXB-POUR-3', is_active: true },
                { id: 4, district_id: 1, upazila_id: 5, name_bn: 'টেকনাফ পৌরসভা', name_en: 'Teknaf Pourashava', code: 'CXB-POUR-4', is_active: true }
              ],
              cityCorporations: [
                { id: 1, district_id: 2, name_bn: 'চট্টগ্রাম সিটি কর্পোরেশন', name_en: 'Chattogram City Corporation', code: 'CTG-CC', is_active: true }
              ],
              wards: [
                { id: 1, ward_number: 1, municipality_id: 1, name_bn: '১ নং ওয়ার্ড (কক্সবাজার পৌরসভা)', name_en: "Ward 1 (Cox's Bazar Pourashava)", code: 'CXB-POUR-W1', is_active: true },
                { id: 2, ward_number: 2, municipality_id: 1, name_bn: '২ নং ওয়ার্ড (কক্সবাজার পৌরসভা)', name_en: "Ward 2 (Cox's Bazar Pourashava)", code: 'CXB-POUR-W2', is_active: true },
                { id: 3, ward_number: 3, municipality_id: 1, name_bn: '৩ নং ওয়ার্ড (কক্সবাজার পৌরসভা)', name_en: "Ward 3 (Cox's Bazar Pourashava)", code: 'CXB-POUR-W3', is_active: true },
                { id: 4, ward_number: 10, municipality_id: 1, name_bn: '১০ নং ওয়ার্ড (কক্সবাজার পৌরসভা)', name_en: "Ward 10 (Cox's Bazar Pourashava)", code: 'CXB-POUR-W10', is_active: true },
                { id: 5, ward_number: 11, municipality_id: 1, name_bn: '১১ নং ওয়ার্ড (কক্সবাজার পৌরসভা)', name_en: "Ward 11 (Cox's Bazar Pourashava)", code: 'CXB-POUR-W11', is_active: true },
                { id: 6, ward_number: 12, municipality_id: 1, name_bn: '১২ নং ওয়ার্ড (কক্সবাজার পৌরসভা)', name_en: "Ward 12 (Cox's Bazar Pourashava)", code: 'CXB-POUR-W12', is_active: true },
                { id: 7, ward_number: 1, union_id: 1, name_bn: '১ নং ওয়ার্ড (ঝিলংজা)', name_en: 'Ward 1 (Jhilongja)', code: 'CXB-JHIL-W1', is_active: true },
                { id: 8, ward_number: 2, union_id: 1, name_bn: '২ নং ওয়ার্ড (ঝিলংজা)', name_en: 'Ward 2 (Jhilongja)', code: 'CXB-JHIL-W2', is_active: true },
                { id: 9, ward_number: 1, union_id: 12, name_bn: '১ নং ওয়ার্ড', name_en: 'Ward 1', code: 'CXB-EIDG-W1', is_active: true },
                { id: 10, ward_number: 2, union_id: 12, name_bn: '২ নং ওয়ার্ড', name_en: 'Ward 2', code: 'CXB-EIDG-W2', is_active: true },
                { id: 10401, ward_number: 1, union_id: 3, name_bn: '১ নং ওয়ার্ড', name_en: 'Ward 1', code: 'WARD-UNI-KHURUSHKUL-01', is_active: true },
                { id: 10402, ward_number: 2, union_id: 3, name_bn: '২ নং ওয়ার্ড', name_en: 'Ward 2', code: 'WARD-UNI-KHURUSHKUL-02', is_active: true },
                { id: 10403, ward_number: 3, union_id: 3, name_bn: '৩ নং ওয়ার্ড', name_en: 'Ward 3', code: 'WARD-UNI-KHURUSHKUL-03', is_active: true },
                { id: 10404, ward_number: 4, union_id: 3, name_bn: '৪ নং ওয়ার্ড', name_en: 'Ward 4', code: 'WARD-UNI-KHURUSHKUL-04', is_active: true },
                { id: 10405, ward_number: 5, union_id: 3, name_bn: '৫ নং ওয়ার্ড', name_en: 'Ward 5', code: 'WARD-UNI-KHURUSHKUL-05', is_active: true },
                { id: 10406, ward_number: 6, union_id: 3, name_bn: '৬ নং ওয়ার্ড', name_en: 'Ward 6', code: 'WARD-UNI-KHURUSHKUL-06', is_active: true },
                { id: 10407, ward_number: 7, union_id: 3, name_bn: '৭ নং ওয়ার্ড', name_en: 'Ward 7', code: 'WARD-UNI-KHURUSHKUL-07', is_active: true },
                { id: 10408, ward_number: 8, union_id: 3, name_bn: '৮ নং ওয়ার্ড', name_en: 'Ward 8', code: 'WARD-UNI-KHURUSHKUL-08', is_active: true },
                { id: 10409, ward_number: 9, union_id: 3, name_bn: '৯ নং ওয়ার্ড', name_en: 'Ward 9', code: 'WARD-UNI-KHURUSHKUL-09', is_active: true }
              ],
              localities: [
                { id: 1, upazila_id: 1, municipality_id: 1, ward_id: 6, locality_type: 'LOCAL_AREA', name_bn: 'কলাতলী', name_en: 'Kolatoli', postal_code: '4700', is_active: true },
                { id: 2, upazila_id: 1, municipality_id: 1, ward_id: 6, locality_type: 'LOCAL_AREA', name_bn: 'সুগন্ধা পয়েন্ট', name_en: 'Sugandha Point', postal_code: '4700', is_active: true },
                { id: 3, upazila_id: 1, municipality_id: 1, ward_id: 4, locality_type: 'LOCAL_AREA', name_bn: 'লাবণী বিচ এলাকা', name_en: 'Laboni Beach Area', postal_code: '4700', is_active: true },
                { id: 4, upazila_id: 1, municipality_id: 1, ward_id: 2, locality_type: 'BAZAR', name_bn: 'বাজারঘাটা', name_en: 'Bazarghata', postal_code: '4700', is_active: true },
                { id: 5, upazila_id: 1, municipality_id: 1, ward_id: 1, locality_type: 'MOHOLLA', name_bn: 'সমিতি পাড়া', name_en: 'Samity Para', postal_code: '4700', is_active: true },
                { id: 6, upazila_id: 1, municipality_id: 1, ward_id: 3, locality_type: 'RESIDENTIAL', name_bn: 'উত্তর রুমালিয়ার ছড়া', name_en: 'North Rumaliar Chhara', postal_code: '4700', is_active: true },
                { id: 7, upazila_id: 1, union_id: 1, ward_id: 7, locality_type: 'LOCAL_AREA', name_bn: 'লিংকরোড', name_en: 'Link Road', postal_code: '4700', is_active: true },
                { id: 8, upazila_id: 1, union_id: 1, ward_id: 8, locality_type: 'LOCAL_AREA', name_bn: 'লারপাড়া', name_en: 'Larpara (Bus Terminal)', postal_code: '4700', is_active: true },
                { id: 9, upazila_id: 9, union_id: 12, ward_id: 9, locality_type: 'BAZAR', name_bn: 'ঈদগাঁও বাজার', name_en: 'Eidgaon Bazar', postal_code: '4750', is_active: true },
                { id: 10, upazila_id: 9, union_id: 12, ward_id: 9, locality_type: 'VILLAGE', name_bn: 'মেহেরঘোনা', name_en: 'Meherghona', postal_code: '4750', is_active: true },
                { id: 11, upazila_id: 4, union_id: 6, locality_type: 'LOCAL_AREA', name_bn: 'রামু বাইপাস', name_en: 'Ramu Bypass', postal_code: '4730', is_active: true },
                { id: 12, upazila_id: 6, union_id: 9, locality_type: 'BAZAR', name_bn: 'কোটবাজার', name_en: 'Court Bazar', postal_code: '4757', is_active: true },
                { id: 13, upazila_id: 5, union_id: 11, locality_type: 'LOCAL_AREA', name_bn: 'জেটিঘাট (সেন্টমার্টিন)', name_en: 'Jetty Ghat (Saint Martin)', postal_code: '4762', is_active: true },
                // Khurushkul Union (union_id: 3) Wards 1-9 Government Portal Verified Localities (Master Version: KHURUSHKUL_V2)
                { id: 104011, upazila_id: 1, union_id: 3, ward_id: 10401, locality_type: 'PARA', name_bn: 'তেতৈয়া সওদাগর পাড়া ও মিয়াজি পাড়া', name_en: 'Tetoiya Sawdagor Para & Miyaji Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104012, upazila_id: 1, union_id: 3, ward_id: 10401, locality_type: 'PARA', name_bn: 'তেতৈয়া ইউছুপ ফকির পাড়া', name_en: 'Tetoiya Yousuf Fakir Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104013, upazila_id: 1, union_id: 3, ward_id: 10401, locality_type: 'PARA', name_bn: 'তেতৈয়া জলিয়া বাপের পাড়া', name_en: 'Tetoiya Joliya Baper Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104014, upazila_id: 1, union_id: 3, ward_id: 10401, locality_type: 'PARA', name_bn: 'তেতৈয়া সিকদার পাড়া', name_en: 'Tetoiya Sikdar Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104015, upazila_id: 1, union_id: 3, ward_id: 10401, locality_type: 'PARA', name_bn: 'তেতৈয়া গুইল্যা বাপের পাড়া', name_en: 'Tetoiya Guillya Baper Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104021, upazila_id: 1, union_id: 3, ward_id: 10402, locality_type: 'PARA', name_bn: 'তেতৈয়া নতুন ঘোনার পাড়া', name_en: 'Tetoiya Natun Ghonar Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104022, upazila_id: 1, union_id: 3, ward_id: 10402, locality_type: 'PARA', name_bn: 'ডেইল পাড়া', name_en: 'Deil Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104031, upazila_id: 1, union_id: 3, ward_id: 10403, locality_type: 'PARA', name_bn: 'পেচাঁর ঘোনা', name_en: 'Pechar Ghona', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104032, upazila_id: 1, union_id: 3, ward_id: 10403, locality_type: 'PARA', name_bn: 'রাস্তার পাড়া', name_en: 'Rastar Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104033, upazila_id: 1, union_id: 3, ward_id: 10403, locality_type: 'PARA', name_bn: 'জালিয়া পাড়া(রাখাইন পাড়া)', name_en: 'Jalia Para (Rakhine Para)', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104041, upazila_id: 1, union_id: 3, ward_id: 10404, locality_type: 'PARA', name_bn: 'কাউয়ার পাড়া', name_en: 'Kowar Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104042, upazila_id: 1, union_id: 3, ward_id: 10404, locality_type: 'PARA', name_bn: 'ফকির পাড়া', name_en: 'Fakir Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104043, upazila_id: 1, union_id: 3, ward_id: 10404, locality_type: 'PARA', name_bn: 'আদর্শ গ্রাম(ফকির পাড়া)', name_en: 'Adarsha Gram (Fakir Para)', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104051, upazila_id: 1, union_id: 3, ward_id: 10405, locality_type: 'PARA', name_bn: 'মামুন পাড়া', name_en: 'Mamun Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104052, upazila_id: 1, union_id: 3, ward_id: 10405, locality_type: 'PARA', name_bn: 'হাট খোলা পাড়া', name_en: 'Hat Khola Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104053, upazila_id: 1, union_id: 3, ward_id: 10405, locality_type: 'PARA', name_bn: 'জানা পাড়া', name_en: 'Jana Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104061, upazila_id: 1, union_id: 3, ward_id: 10406, locality_type: 'PARA', name_bn: 'হামজার ডেইল', name_en: 'Hamjar Deil', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104062, upazila_id: 1, union_id: 3, ward_id: 10406, locality_type: 'PARA', name_bn: 'ঘোনার পাড়া', name_en: 'Ghonar Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104063, upazila_id: 1, union_id: 3, ward_id: 10406, locality_type: 'PARA', name_bn: 'আদর্শ গ্রাম পাহাড়তলী', name_en: 'Adarsha Gram Pahartali', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104064, upazila_id: 1, union_id: 3, ward_id: 10406, locality_type: 'PARA', name_bn: 'পূর্ব হিন্দু পাড়া', name_en: 'Purba Hindu Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104065, upazila_id: 1, union_id: 3, ward_id: 10406, locality_type: 'PARA', name_bn: 'পাল পাড়া', name_en: 'Pal Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104071, upazila_id: 1, union_id: 3, ward_id: 10407, locality_type: 'PARA', name_bn: 'রুদ্র পাড়া', name_en: 'Rudra Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104072, upazila_id: 1, union_id: 3, ward_id: 10407, locality_type: 'PARA', name_bn: 'উত্তর হিন্দু পাড়া', name_en: 'Uttar Hindu Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104073, upazila_id: 1, union_id: 3, ward_id: 10407, locality_type: 'PARA', name_bn: 'গাজীর ডেইল', name_en: 'Gazir Deil', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104074, upazila_id: 1, union_id: 3, ward_id: 10407, locality_type: 'PARA', name_bn: 'পঞ্চায়েত পাড়া', name_en: 'Panchayet Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104081, upazila_id: 1, union_id: 3, ward_id: 10408, locality_type: 'PARA', name_bn: 'মনু পাড়া', name_en: 'Monu Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104082, upazila_id: 1, union_id: 3, ward_id: 10408, locality_type: 'PARA', name_bn: 'লমাজি পাড়া', name_en: 'Lomaji Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104083, upazila_id: 1, union_id: 3, ward_id: 10408, locality_type: 'PARA', name_bn: 'মেহেদী পাড়া', name_en: 'Mehedi Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104084, upazila_id: 1, union_id: 3, ward_id: 10408, locality_type: 'PARA', name_bn: 'কোনার পাড়া', name_en: 'Konar Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104091, upazila_id: 1, union_id: 3, ward_id: 10409, locality_type: 'PARA', name_bn: 'দক্ষিণ হিন্দু পাড়া', name_en: 'Dakshin Hindu Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104092, upazila_id: 1, union_id: 3, ward_id: 10409, locality_type: 'PARA', name_bn: 'সাম্পান ঘাট পাড়া', name_en: 'Sampan Ghat Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104093, upazila_id: 1, union_id: 3, ward_id: 10409, locality_type: 'PARA', name_bn: 'কুলিয়া পাড়া', name_en: 'Kuliya Para', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' },
                { id: 104094, upazila_id: 1, union_id: 3, ward_id: 10409, locality_type: 'PARA', name_bn: 'রুহুল্লার ডেইল', name_en: 'Ruhullar Deil', postal_code: '4700', is_active: true, source_type: 'OFFICIAL_GOVERNMENT_PORTAL', source_reference: 'Khurushkul Union Parishad Portal (Official Government Source)', verification_status: 'SOURCE_VERIFIED', master_version: 'KHURUSHKUL_V2' }
              ],
              userContext: {
                selected_location: {
                  id: 1,
                  location_type: 'SELECTED',
                  address_bn: "কক্সবাজার সদর, কক্সবাজার",
                  address_en: "Cox's Bazar Sadar, Cox's Bazar",
                  latitude: 21.4272,
                  longitude: 92.0058,
                  upazila_id: 1,
                  district_id: 1
                },
                current_gps_location: null
              }
            };

            // Countries
            if (pathname === '/api/v1/locations/countries' && req.method === 'GET') {
              res.end(JSON.stringify({
                success: true,
                data: locationStore.countries,
                message: 'দেশ তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Divisions
            if (pathname === '/api/v1/locations/divisions' && req.method === 'GET') {
              res.end(JSON.stringify({
                success: true,
                data: locationStore.divisions,
                message: 'বিভাগ তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Districts
            if (pathname === '/api/v1/locations/districts' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const divId = url.searchParams.get('division_id') || url.searchParams.get('division');
              const filtered = divId 
                ? locationStore.districts.filter(d => d.division_id === Number(divId))
                : locationStore.districts;
              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'জেলা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Upazilas
            if (pathname === '/api/v1/locations/upazilas' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const distId = url.searchParams.get('district_id') || url.searchParams.get('district');
              const filtered = distId 
                ? locationStore.upazilas.filter(u => u.district_id === Number(distId))
                : locationStore.upazilas;
              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'উপজেলা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Municipalities
            if (pathname === '/api/v1/locations/municipalities' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const distId = url.searchParams.get('district_id') || url.searchParams.get('district');
              const upaId = url.searchParams.get('upazila_id') || url.searchParams.get('upazila');
              let filtered = locationStore.municipalities;
              if (distId) filtered = filtered.filter(m => m.district_id === Number(distId));
              if (upaId) filtered = filtered.filter(m => m.upazila_id === Number(upaId));
              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'পৌরসভা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // City Corporations
            if (pathname === '/api/v1/locations/city-corporations' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const distId = url.searchParams.get('district_id') || url.searchParams.get('district');
              const filtered = distId
                ? locationStore.cityCorporations.filter(c => c.district_id === Number(distId))
                : locationStore.cityCorporations;
              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'সিটি কর্পোরেশন তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Unions
            if (pathname === '/api/v1/locations/unions' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const upazilaId = url.searchParams.get('upazila_id') || url.searchParams.get('upazila');
              const filtered = upazilaId 
                ? locationStore.unions.filter(u => u.upazila_id === Number(upazilaId))
                : locationStore.unions;
              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'ইউনিয়ন তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Wards
            if (pathname === '/api/v1/locations/wards' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const munId = url.searchParams.get('municipality_id') || url.searchParams.get('municipality');
              const unionId = url.searchParams.get('union_id') || url.searchParams.get('union');
              const ccId = url.searchParams.get('city_corporation_id') || url.searchParams.get('city_corporation');
              let filtered: any[] = locationStore.wards;
              if (munId) filtered = filtered.filter((w: any) => w.municipality_id === Number(munId));
              if (unionId) filtered = filtered.filter((w: any) => w.union_id === Number(unionId));
              if (ccId) filtered = filtered.filter((w: any) => w.city_corporation_id === Number(ccId));
              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'ওয়ার্ড তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Localities
            if (pathname === '/api/v1/locations/localities' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const upaId = url.searchParams.get('upazila_id') || url.searchParams.get('upazila');
              const munId = url.searchParams.get('municipality_id') || url.searchParams.get('municipality');
              const unionId = url.searchParams.get('union_id') || url.searchParams.get('union');
              const wardId = url.searchParams.get('ward_id') || url.searchParams.get('ward');
              let filtered: any[] = locationStore.localities;
              if (upaId) filtered = filtered.filter((l: any) => l.upazila_id === Number(upaId));
              if (munId) filtered = filtered.filter((l: any) => l.municipality_id === Number(munId));
              if (unionId) filtered = filtered.filter((l: any) => l.union_id === Number(unionId));
              if (wardId) filtered = filtered.filter((l: any) => l.ward_id === Number(wardId));
              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'লোকালিটি তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Cascading Children API
            if (pathname === '/api/v1/locations/children' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const parentType = (url.searchParams.get('parent_type') || '').toUpperCase().trim();
              const parentId = Number(url.searchParams.get('parent_id'));
              let data: any = [];

              if (parentType === 'COUNTRY') {
                data = locationStore.divisions.filter(d => d.country_id === parentId);
              } else if (parentType === 'DIVISION') {
                data = locationStore.districts.filter(d => d.division_id === parentId);
              } else if (parentType === 'DISTRICT') {
                data = locationStore.upazilas.filter(u => u.district_id === parentId);
              } else if (parentType === 'UPAZILA') {
                data = {
                  unions: locationStore.unions.filter(u => u.upazila_id === parentId),
                  municipalities: locationStore.municipalities.filter(m => m.upazila_id === parentId)
                };
              } else if (parentType === 'UNION') {
                data = locationStore.wards.filter(w => w.union_id === parentId);
              } else if (parentType === 'MUNICIPALITY') {
                data = locationStore.wards.filter(w => w.municipality_id === parentId);
              } else if (parentType === 'WARD') {
                data = locationStore.localities.filter(l => l.ward_id === parentId);
              }

              res.end(JSON.stringify({
                success: true,
                data,
                message: 'সাব-লোকেশন তালিকা সফলভাবে প্রাপ্ত হয়েছে।'
              }));
              return;
            }

            // Location Search
            if (pathname === '/api/v1/locations/search' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const q = (url.searchParams.get('q') || '').toLowerCase().trim();
              const results = [];
              if (q) {
                locationStore.upazilas.forEach(u => {
                  const matchesBn = u.name_bn.toLowerCase().includes(q);
                  const matchesEn = u.name_en.toLowerCase().includes(q);
                  const matchesCode = u.code ? u.code.toLowerCase().includes(q) : false;
                  if (matchesBn || matchesEn || matchesCode) {
                    results.push({
                      id: u.id,
                      name_bn: u.name_bn,
                      name_en: u.name_en,
                      type: 'UPAZILA',
                      full_address_bn: `${u.name_bn}, কক্সবাজার`,
                      full_address_en: `${u.name_en}, Cox's Bazar`,
                      latitude: u.id === 9 ? 21.5583 : 21.4272,
                      longitude: u.id === 9 ? 92.0583 : 92.0058
                    });
                  }
                });
                locationStore.districts.forEach(d => {
                  if (d.name_bn.toLowerCase().includes(q) || d.name_en.toLowerCase().includes(q)) {
                    results.push({
                      id: d.id,
                      name_bn: d.name_bn,
                      name_en: d.name_en,
                      type: 'DISTRICT',
                      full_address_bn: `${d.name_bn}, চট্টগ্রাম`,
                      full_address_en: `${d.name_en}, Chattogram`,
                      latitude: 21.4272,
                      longitude: 92.0058
                    });
                  }
                });
              }
              res.end(JSON.stringify({
                success: true,
                data: results,
                message: 'অনুসন্ধান সম্পন্ন হয়েছে।'
              }));
              return;
            }

            // User Location Context
            if (pathname === '/api/v1/locations/context') {
              if (req.method === 'GET') {
                res.end(JSON.stringify({
                  success: true,
                  data: locationStore.userContext,
                  message: 'ব্যবহারকারীর অবস্থান প্রোফাইল প্রাপ্তি সফল হয়েছে।'
                }));
                return;
              }
              if (req.method === 'POST') {
                const body = await parseBody(req);
                if (body.location_type === 'CURRENT') {
                  locationStore.userContext.current_gps_location = {
                    id: 2,
                    location_type: 'CURRENT',
                    address_bn: body.address_text || "বর্তমান জিপিএস অবস্থান",
                    address_en: body.address_text || "Current GPS Location",
                    latitude: body.latitude,
                    longitude: body.longitude
                  };
                } else {
                  // Selected location
                  locationStore.userContext.selected_location = {
                    id: 1,
                    location_type: 'SELECTED',
                    address_bn: body.address_text || "কক্সবাজার সদর",
                    address_en: body.address_text || "Cox's Bazar Sadar",
                    latitude: body.latitude || 21.4272,
                    longitude: body.longitude || 92.0058,
                    upazila_id: body.upazila_id || 1,
                    district_id: body.district_id || 1
                  };
                }
                res.end(JSON.stringify({
                  success: true,
                  data: locationStore.userContext,
                  message: 'অবস্থান সফলভাবে আপডেট হয়েছে।'
                }));
                return;
              }
            }

            // Service Areas
            if (pathname === '/api/v1/locations/service-areas' && req.method === 'GET') {
              res.end(JSON.stringify({
                success: true,
                data: [
                  {
                    id: 1,
                    name_bn: 'কক্সবাজার পৌরসভা ও পর্যটন এলাকা',
                    name_en: "Cox's Bazar Municipality & Tourism Zone",
                    area_type: 'ADMINISTRATIVE',
                    is_active: true
                  },
                  {
                    id: 2,
                    name_bn: 'কলাতলী বিচ ১০ কিমি ব্যাসার্ধ',
                    name_en: "Kolatoli Beach 10km Radial Zone",
                    area_type: 'RADIUS',
                    radius_km: 10.0,
                    is_active: true
                  }
                ],
                message: 'সার্ভিস এরিয়া তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Reverse geocode
            if (pathname === '/api/v1/locations/reverse-geocode' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const lat = parseFloat(url.searchParams.get('lat') || '21.4272');
              const lon = parseFloat(url.searchParams.get('lon') || '92.0058');
              res.end(JSON.stringify({
                success: true,
                data: {
                  latitude: lat,
                  longitude: lon,
                  address_bn: "কলাতলী রোড, কক্সবাজার সদর, কক্সবাজার",
                  address_en: "Kolatoli Road, Cox's Bazar Sadar, Cox's Bazar",
                  district: "কক্সবাজার",
                  upazila: "কক্সবাজার সদর"
                },
                message: 'রিভার্স জিওকোডিং সফল হয়েছে।'
              }));
              return;
            }

            // ==========================================
            // PHASE 4: CATEGORY & SERVICE API ENDPOINTS
            // ==========================================

            // Master Categories list & filters
            if (pathname === '/api/v1/categories' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const isFeatured = url.searchParams.get('is_featured');
              const search = (url.searchParams.get('search') || url.searchParams.get('q') || '').trim().toLowerCase();

              let filtered = SEBACOX_MASTER_CATEGORIES.map(c => ({
                id: c.id,
                name_bn: c.nameBn,
                name_en: c.nameEn,
                nameBn: c.nameBn,
                nameEn: c.nameEn,
                slug: c.slug,
                icon: c.icon,
                description_bn: c.descriptionBn,
                description_en: c.descriptionEn,
                descriptionBn: c.descriptionBn,
                descriptionEn: c.descriptionEn,
                sort_order: c.sortOrder,
                sortOrder: c.sortOrder,
                is_active: c.isActive,
                isActive: c.isActive,
                is_featured: c.isFeatured,
                isFeatured: c.isFeatured,
                subcategories_count: c.subCategories.length,
                subCategories: c.subCategories.map(sc => ({
                  id: sc.id,
                  category_id: sc.categoryId,
                  categoryId: sc.categoryId,
                  name_bn: sc.nameBn,
                  name_en: sc.nameEn,
                  nameBn: sc.nameBn,
                  nameEn: sc.nameEn,
                  slug: sc.slug,
                  sort_order: sc.sortOrder,
                  sortOrder: sc.sortOrder,
                  is_active: sc.isActive,
                  isActive: sc.isActive,
                }))
              }));

              if (isFeatured === 'true') {
                filtered = filtered.filter(c => c.is_featured);
              }
              if (search) {
                filtered = filtered.filter(c => 
                  c.name_bn.toLowerCase().includes(search) ||
                  c.name_en.toLowerCase().includes(search) ||
                  c.description_bn.toLowerCase().includes(search) ||
                  c.subCategories.some(sc => sc.name_bn.toLowerCase().includes(search) || sc.name_en.toLowerCase().includes(search))
                );
              }

              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'ক্যাটাগরি তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Categories tree
            if (pathname === '/api/v1/categories/tree' && req.method === 'GET') {
              const rootCategories = SEBACOX_MASTER_CATEGORIES.map(cat => ({
                id: cat.id,
                name_bn: cat.nameBn,
                name_en: cat.nameEn,
                slug: cat.slug,
                icon: cat.icon,
                description_bn: cat.descriptionBn,
                description_en: cat.descriptionEn,
                sort_order: cat.sortOrder,
                is_active: cat.isActive,
                is_featured: cat.isFeatured,
                children: cat.subCategories.map(sc => ({
                  id: sc.id,
                  parent_id: cat.id,
                  category_id: cat.id,
                  name_bn: sc.nameBn,
                  name_en: sc.nameEn,
                  slug: sc.slug,
                  sort_order: sc.sortOrder,
                  is_active: sc.isActive,
                }))
              }));

              res.end(JSON.stringify({
                success: true,
                data: rootCategories,
                message: 'ক্যাটাগরি ট্রি প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Featured categories
            if (pathname === '/api/v1/categories/featured' && req.method === 'GET') {
              const featured = SEBACOX_MASTER_CATEGORIES.filter(c => c.isFeatured).map(c => ({
                id: c.id,
                name_bn: c.nameBn,
                name_en: c.nameEn,
                slug: c.slug,
                icon: c.icon,
                description_bn: c.descriptionBn,
                description_en: c.descriptionEn,
                sort_order: c.sortOrder,
                is_active: c.isActive,
                is_featured: c.isFeatured,
                subcategories_count: c.subCategories.length,
              }));
              res.end(JSON.stringify({
                success: true,
                data: featured,
                message: 'জনপ্রিয় ক্যাটাগরি তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Category Subcategories endpoint: /api/v1/categories/:id/subcategories
            const catSubcategoriesMatch = pathname.match(/^\/api\/v1\/categories\/(\d+)\/subcategories\/?$/);
            if (catSubcategoriesMatch && req.method === 'GET') {
              const catId = parseInt(catSubcategoriesMatch[1], 10);
              const parentCat = SEBACOX_MASTER_CATEGORIES.find(c => c.id === catId);
              if (!parentCat) {
                res.statusCode = 404;
                res.setHeader('Content-Type', 'application/json');
                res.end(JSON.stringify({
                  success: false,
                  data: [],
                  message: 'ক্যাটাগরি পাওয়া যায়নি।'
                }));
                return;
              }
              const url = new URL(req.url, 'http://localhost');
              const search = (url.searchParams.get('search') || url.searchParams.get('q') || '').trim().toLowerCase();
              const includeInactive = url.searchParams.get('include_inactive') === 'true';

              let subcats = parentCat.subCategories;
              if (!includeInactive) {
                subcats = subcats.filter(sc => sc.isActive !== false);
              }
              if (search) {
                subcats = subcats.filter(sc => 
                  sc.nameBn.toLowerCase().includes(search) || 
                  sc.nameEn.toLowerCase().includes(search) ||
                  sc.slug.toLowerCase().includes(search)
                );
              }
              subcats = [...subcats].sort((a, b) => (a.sortOrder || 0) - (b.sortOrder || 0));

              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({
                success: true,
                data: subcats.map(sc => ({
                  id: sc.id,
                  category_id: sc.categoryId,
                  categoryId: sc.categoryId,
                  name_bn: sc.nameBn,
                  name_en: sc.nameEn,
                  nameBn: sc.nameBn,
                  nameEn: sc.nameEn,
                  slug: sc.slug,
                  sort_order: sc.sortOrder,
                  sortOrder: sc.sortOrder,
                  is_active: sc.isActive,
                  isActive: sc.isActive,
                })),
                message: 'সাব-ক্যাটাগরি তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Provider Registration API with validation
            if ((pathname === '/api/v1/providers/register' || pathname === '/api/v1/providers') && req.method === 'POST') {
              const body = await parseBody(req);
              
              // Validate category and subcategory relationship
              if (body.category_id && body.subcategory_id) {
                const subcat = ALL_MASTER_SUB_CATEGORIES.find(s => s.id === Number(body.subcategory_id));
                if (!subcat || subcat.categoryId !== Number(body.category_id)) {
                  res.statusCode = 422;
                  res.setHeader('Content-Type', 'application/json');
                  res.end(JSON.stringify({
                    success: false,
                    data: null,
                    message: 'সাব-ক্যাটাগরিটি নির্বাচিত প্রধান ক্যাটাগরির অন্তর্ভুক্ত নয়।',
                    errors: {
                      subcategory_id: ['Subcategory does not belong to the selected category']
                    }
                  }));
                  return;
                }
              }

              res.statusCode = 201;
              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({
                success: true,
                data: body,
                message: 'সেবাদাতা নিবন্ধন সফলভাবে জমা হয়েছে।'
              }));
              return;
            }

            // Category children (alias for subcategories)
            const catChildrenMatch = pathname.match(/^\/api\/v1\/categories\/(\d+)\/children$/);
            if (catChildrenMatch && req.method === 'GET') {
              const parentId = parseInt(catChildrenMatch[1], 10);
              const parentCat = SEBACOX_MASTER_CATEGORIES.find(c => c.id === parentId);
              const children = parentCat ? parentCat.subCategories.map(sc => ({
                id: sc.id,
                parent_id: parentId,
                category_id: parentId,
                name_bn: sc.nameBn,
                name_en: sc.nameEn,
                slug: sc.slug,
                sort_order: sc.sortOrder,
                is_active: sc.isActive,
              })) : [];
              res.end(JSON.stringify({
                success: true,
                data: children,
                message: 'সাব-ক্যাটাগরি তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Single category detail
            const catDetailMatch = pathname.match(/^\/api\/v1\/categories\/(\d+)$/);
            if (catDetailMatch && req.method === 'GET') {
              const id = parseInt(catDetailMatch[1], 10);
              const cat = SEBACOX_MASTER_CATEGORIES.find(c => c.id === id);
              if (!cat) {
                res.statusCode = 404;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: 'ক্যাটাগরি পাওয়া যায়নি।'
                }));
                return;
              }
              res.end(JSON.stringify({
                success: true,
                data: {
                  id: cat.id,
                  name_bn: cat.nameBn,
                  name_en: cat.nameEn,
                  slug: cat.slug,
                  icon: cat.icon,
                  description_bn: cat.descriptionBn,
                  description_en: cat.descriptionEn,
                  sort_order: cat.sortOrder,
                  is_active: cat.isActive,
                  is_featured: cat.isFeatured,
                  subcategories: cat.subCategories,
                },
                message: 'ক্যাটাগরি বিবরণ প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // All Sub-categories list & filters
            if (pathname === '/api/v1/subcategories' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const categoryId = url.searchParams.get('category_id') || url.searchParams.get('category');
              const search = (url.searchParams.get('search') || url.searchParams.get('q') || '').trim().toLowerCase();

              let results = [...ALL_MASTER_SUB_CATEGORIES];
              if (categoryId) {
                results = results.filter(sc => sc.categoryId === parseInt(categoryId, 10));
              }
              if (search) {
                results = results.filter(sc => 
                  sc.nameBn.toLowerCase().includes(search) || 
                  sc.nameEn.toLowerCase().includes(search)
                );
              }

              res.end(JSON.stringify({
                success: true,
                data: results.map(sc => ({
                  id: sc.id,
                  category_id: sc.categoryId,
                  categoryId: sc.categoryId,
                  name_bn: sc.nameBn,
                  name_en: sc.nameEn,
                  nameBn: sc.nameBn,
                  nameEn: sc.nameEn,
                  slug: sc.slug,
                  sort_order: sc.sortOrder,
                  sortOrder: sc.sortOrder,
                  is_active: sc.isActive,
                  isActive: sc.isActive,
                })),
                message: 'সাব-ক্যাটাগরি তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Services list & filters (bridged to sub-categories for backward compatibility)
            if (pathname === '/api/v1/services' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const categoryId = url.searchParams.get('category') || url.searchParams.get('category_id');

              let subcatResults = [...ALL_MASTER_SUB_CATEGORIES];
              if (categoryId) {
                subcatResults = subcatResults.filter(sc => sc.categoryId === parseInt(categoryId, 10));
              }

              const mappedServices = subcatResults.map(sc => {
                const parent = SEBACOX_MASTER_CATEGORIES.find(c => c.id === sc.categoryId);
                return {
                  id: sc.id,
                  category_id: sc.categoryId,
                  category_name_bn: parent?.nameBn || '',
                  category_name_en: parent?.nameEn || '',
                  name_bn: sc.nameBn,
                  name_en: sc.nameEn,
                  slug: sc.slug,
                  short_description_bn: `${sc.nameBn} সংক্রান্ত সেবা`,
                  short_description_en: `${sc.nameEn} services`,
                  icon: parent?.icon || 'tool',
                  service_type: 'SERVICE',
                  requires_booking: true,
                  supports_demand: true,
                  supports_offer: true,
                  supports_negotiation: true,
                  supports_delivery: true,
                  supports_location: true,
                  supports_online: true,
                  supports_order: true,
                  supports_rental: false,
                  supports_payment: true,
                  is_active: sc.isActive,
                  is_featured: false,
                  sort_order: sc.sortOrder
                };
              });

              res.end(JSON.stringify({
                success: true,
                data: mappedServices,
                message: 'সেবা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Featured services
            if (pathname === '/api/v1/services/featured' && req.method === 'GET') {
              const featuredSubcats = ALL_MASTER_SUB_CATEGORIES.slice(0, 8);
              const mapped = featuredSubcats.map(sc => {
                const parent = SEBACOX_MASTER_CATEGORIES.find(c => c.id === sc.categoryId);
                return {
                  id: sc.id,
                  category_id: sc.categoryId,
                  category_name_bn: parent?.nameBn || '',
                  category_name_en: parent?.nameEn || '',
                  name_bn: sc.nameBn,
                  name_en: sc.nameEn,
                  slug: sc.slug,
                  short_description_bn: `${sc.nameBn} সংক্রান্ত সেবা`,
                  short_description_en: `${sc.nameEn} services`,
                  icon: parent?.icon || 'tool',
                  service_type: 'SERVICE',
                  is_active: true,
                  is_featured: true,
                  sort_order: sc.sortOrder
                };
              });
              res.end(JSON.stringify({
                success: true,
                data: mapped,
                message: 'গুরুত্বপূর্ণ সেবা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Search services (Bangla & English)
            if (pathname === '/api/v1/services/search' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const q = (url.searchParams.get('q') || '').trim().toLowerCase();
              const categoryId = url.searchParams.get('category_id');

              let subcatResults = ALL_MASTER_SUB_CATEGORIES.filter(sc => {
                const parent = SEBACOX_MASTER_CATEGORIES.find(c => c.id === sc.categoryId);
                const matchNameBn = sc.nameBn.toLowerCase().includes(q);
                const matchNameEn = sc.nameEn.toLowerCase().includes(q);
                const matchParentBn = parent ? parent.nameBn.toLowerCase().includes(q) : false;
                const matchParentEn = parent ? parent.nameEn.toLowerCase().includes(q) : false;
                return matchNameBn || matchNameEn || matchParentBn || matchParentEn;
              });

              if (categoryId) {
                subcatResults = subcatResults.filter(s => s.categoryId === parseInt(categoryId, 10));
              }

              const mapped = subcatResults.map(sc => {
                const parent = SEBACOX_MASTER_CATEGORIES.find(c => c.id === sc.categoryId);
                return {
                  id: sc.id,
                  category_id: sc.categoryId,
                  category_name_bn: parent?.nameBn || '',
                  category_name_en: parent?.nameEn || '',
                  name_bn: sc.nameBn,
                  name_en: sc.nameEn,
                  slug: sc.slug,
                  short_description_bn: `${sc.nameBn} সংক্রান্ত সেবা`,
                  short_description_en: `${sc.nameEn} services`,
                  icon: parent?.icon || 'tool',
                  service_type: 'SERVICE',
                  is_active: true,
                  is_featured: false,
                  sort_order: sc.sortOrder
                };
              });

              res.end(JSON.stringify({
                success: true,
                data: mapped,
                message: 'অনুসন্ধান ফলাফল প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Services by category
            const servByCatMatch = pathname.match(/^\/api\/v1\/services\/by-category\/(\d+)$/);
            if (servByCatMatch && req.method === 'GET') {
              const catId = parseInt(servByCatMatch[1], 10);
              const subcats = ALL_MASTER_SUB_CATEGORIES.filter(s => s.categoryId === catId);
              const parent = SEBACOX_MASTER_CATEGORIES.find(c => c.id === catId);
              const mapped = subcats.map(sc => ({
                id: sc.id,
                category_id: sc.categoryId,
                category_name_bn: parent?.nameBn || '',
                category_name_en: parent?.nameEn || '',
                name_bn: sc.nameBn,
                name_en: sc.nameEn,
                slug: sc.slug,
                short_description_bn: `${sc.nameBn} সংক্রান্ত সেবা`,
                short_description_en: `${sc.nameEn} services`,
                icon: parent?.icon || 'tool',
                service_type: 'SERVICE',
                is_active: true,
                is_featured: false,
                sort_order: sc.sortOrder
              }));

              res.end(JSON.stringify({
                success: true,
                data: mapped,
                message: 'ক্যাটাগরিভিত্তিক সেবা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Single service detail
            const servDetailMatch = pathname.match(/^\/api\/v1\/services\/(\d+)$/);
            if (servDetailMatch && req.method === 'GET') {
              const id = parseInt(servDetailMatch[1], 10);
              const sc = ALL_MASTER_SUB_CATEGORIES.find(s => s.id === id);
              if (!sc) {
                res.statusCode = 404;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: 'সেবা পাওয়া যায়নি।'
                }));
                return;
              }
              const parent = SEBACOX_MASTER_CATEGORIES.find(c => c.id === sc.categoryId);
              res.end(JSON.stringify({
                success: true,
                data: {
                  id: sc.id,
                  category_id: sc.categoryId,
                  category_name_bn: parent?.nameBn || '',
                  category_name_en: parent?.nameEn || '',
                  name_bn: sc.nameBn,
                  name_en: sc.nameEn,
                  slug: sc.slug,
                  short_description_bn: `${sc.nameBn} সংক্রান্ত সেবা`,
                  short_description_en: `${sc.nameEn} services`,
                  icon: parent?.icon || 'tool',
                  service_type: 'SERVICE',
                  is_active: true,
                  is_featured: false,
                  sort_order: sc.sortOrder
                },
                message: 'সেবা বিবরণ প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // ==========================================
            // PHASE 6 DEMAND ENGINE ENDPOINTS
            // ==========================================
            // List / Filter Demands
            if (pathname === '/api/v1/demands' && req.method === 'GET') {
              const urlObj = new URL(req.url, 'http://localhost');
              const q = (urlObj.searchParams.get('q') || '').toLowerCase().trim();
              const upazilaId = urlObj.searchParams.get('upazila_id');
              const demandType = urlObj.searchParams.get('demand_type');
              const priority = urlObj.searchParams.get('priority');

              let results = demandsStore.filter((d: any) => d.status === 'PUBLISHED');

              if (q) {
                results = results.filter((d: any) => 
                  d.titleBn.toLowerCase().includes(q) || 
                  d.titleEn.toLowerCase().includes(q) || 
                  d.descriptionBn.toLowerCase().includes(q)
                );
              }
              if (upazilaId) {
                results = results.filter((d: any) => d.upazilaId === parseInt(upazilaId, 10));
              }
              if (demandType) {
                results = results.filter((d: any) => d.demandType === demandType);
              }
              if (priority) {
                results = results.filter((d: any) => d.priority === priority);
              }

              // Apply phone masking for public results
              const safeResults = results.map((d: any) => ({
                ...d,
                contactPhone: d.contactPhone ? `${d.contactPhone.slice(0, 6)}****${d.contactPhone.slice(-4)}` : '',
              }));

              res.end(JSON.stringify({
                success: true,
                data: safeResults,
                message: 'প্রয়োজনের তালিকা সফলভাবে প্রদান করা হয়েছে।'
              }));
              return;
            }

            // My Demands
            if (pathname === '/api/v1/demands/my-demands' && req.method === 'GET') {
              const myItems = demandsStore.filter((d: any) => d.isOwner || d.requesterId === 1);
              res.end(JSON.stringify({
                success: true,
                data: myItems,
                message: 'আপনার পোস্টকৃত চাহিদার তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Create Demand
            if (pathname === '/api/v1/demands' && req.method === 'POST') {
              const body = await parseBody(req);
              if (!body.title_bn || body.title_bn.trim().length < 5) {
                res.statusCode = 400;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: 'শিরোনাম কমপক্ষে ৫ অক্ষরের হতে হবে।',
                  errors: { title_bn: ['শিরোনাম কমপক্ষে ৫ অক্ষরের হতে হবে।'] }
                }));
                return;
              }
              if (!body.description_bn || body.description_bn.trim().length < 10) {
                res.statusCode = 400;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: 'বিস্তারিত বিবরণ কমপক্ষে ১০ অক্ষরের হতে হবে।',
                  errors: { description_bn: ['বিস্তারিত বিবরণ কমপক্ষে ১০ অক্ষরের হতে হবে।'] }
                }));
                return;
              }

              const newDemand: MockDemand = {
                id: demandsStore.length + 1,
                requesterId: 1,
                requesterName: 'মোহাম্মদ করিম',
                contactPhone: '+8801819234567',
                titleBn: body.title_bn.trim(),
                titleEn: body.title_bn.trim(),
                descriptionBn: body.description_bn.trim(),
                descriptionEn: body.description_bn.trim(),
                demandType: body.demand_type || 'SERVICE',
                status: (body.publish_now ? 'PUBLISHED' : 'DRAFT') as MockDemand['status'],
                priority: body.priority || 'NORMAL',
                budgetMin: body.budget_min ? Number(body.budget_min) : undefined,
                budgetMax: body.budget_max ? Number(body.budget_max) : undefined,
                currency: 'BDT',
                upazilaId: body.upazila_id || 1,
                upazilaNameBn: 'কক্সবাজার সদর',
                locationDisplayBn: body.location_display_bn || 'কক্সবাজার সদর',
                visibility: 'PUBLIC',
                contactPreference: body.contact_preference || 'BOTH',
                isOwner: true,
                publishedAt: body.publish_now ? new Date().toISOString() : undefined,
                createdAt: new Date().toISOString(),
              };

              demandsStore.unshift(newDemand);

              res.statusCode = 201;
              res.end(JSON.stringify({
                success: true,
                data: newDemand,
                message: body.publish_now ? 'প্রয়োজন সফলভাবে প্রকাশ করা হয়েছে।' : 'প্রয়োজন খসড়া হিসেবে সংরক্ষিত হয়েছে।'
              }));
              return;
            }

            // Demand Actions (publish, pause, fulfill, cancel, resume)
            const demandActionMatch = pathname.match(/^\/api\/v1\/demands\/(\d+)\/(publish|pause|resume|fulfill|cancel)$/);
            if (demandActionMatch && req.method === 'POST') {
              const dId = parseInt(demandActionMatch[1], 10);
              const action = demandActionMatch[2];
              const item = demandsStore.find((d: any) => d.id === dId);
              if (!item) {
                res.statusCode = 404;
                res.end(JSON.stringify({ success: false, data: null, message: 'প্রয়োজন পাওয়া যায়নি।' }));
                return;
              }

              const statusMap: Record<string, MockDemand['status']> = {
                publish: 'PUBLISHED',
                pause: 'PAUSED',
                resume: 'PUBLISHED',
                fulfill: 'FULFILLED',
                cancel: 'CANCELLED',
              };
              if (statusMap[action]) {
                item.status = statusMap[action];
              }

              res.end(JSON.stringify({
                success: true,
                data: item,
                message: `প্রয়োজনের অবস্থা সফলভাবে পরিবর্তিত হয়েছে (${item.status})`
              }));
              return;
            }

            // Single Demand Detail
            const demandDetailMatch = pathname.match(/^\/api\/v1\/demands\/(\d+)$/);
            if (demandDetailMatch && req.method === 'GET') {
              const dId = parseInt(demandDetailMatch[1], 10);
              const item = demandsStore.find((d: any) => d.id === dId);
              if (!item) {
                res.statusCode = 404;
                res.end(JSON.stringify({ success: false, data: null, message: 'প্রয়োজন পাওয়া যায়নি।' }));
                return;
              }
              const respData = {
                ...item,
                contactPhone: item.isOwner ? item.contactPhone : `${item.contactPhone.slice(0, 6)}****${item.contactPhone.slice(-4)}`
              };
              res.end(JSON.stringify({
                success: true,
                data: respData,
                message: 'প্রয়োজনের বিস্তারিত সফলভাবে প্রদান করা হয়েছে।'
              }));
              return;
            }

            if (pathname.startsWith('/api/v1/')) {
              res.statusCode = 404;
              res.end(
                JSON.stringify({
                  success: false,
                  data: null,
                  message: 'অনুরোধটি সম্পন্ন করা যায়নি',
                  errors: {
                    detail: 'অনুরোধকৃত রিসোর্সটি পাওয়া যায়নি',
                  },
                }),
              );
              return;
            }
            next();
          });
        },
      },
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
    server: {
      // HMR is disabled in AI Studio via DISABLE_HMR env var.
      // Do not modifyâfile watching is disabled to prevent flickering during agent edits.
      hmr: process.env.DISABLE_HMR !== 'true',
      // Disable file watching when DISABLE_HMR is true to save CPU during agent edits.
      watch: process.env.DISABLE_HMR === 'true' ? null : {},
    },
  };
});
