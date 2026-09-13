import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import {defineConfig} from 'vite';
import { INITIAL_46_TAXONOMY_CATEGORIES, INITIAL_SERVICES } from './src/data/taxonomyMockData';
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
                { id: 3, upazila_id: 1, name_bn: 'খুরুশকুল', name_en: 'Khurushkul', code: 'CXB-KHUR', is_active: true }
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
              const divId = url.searchParams.get('division_id');
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
              const distId = url.searchParams.get('district_id');
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

            // Unions
            if (pathname === '/api/v1/locations/unions' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const upazilaId = url.searchParams.get('upazila_id');
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

            // Categories list & filters
            if (pathname === '/api/v1/categories' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const kind = url.searchParams.get('kind');
              const level = url.searchParams.get('level');
              const parent = url.searchParams.get('parent');
              const isFeatured = url.searchParams.get('is_featured');

              let filtered = [...INITIAL_46_TAXONOMY_CATEGORIES];
              if (kind) {
                filtered = filtered.filter(c => c.kind === kind);
              }
              if (level !== null && level !== undefined) {
                filtered = filtered.filter(c => c.level === parseInt(level, 10));
              }
              if (parent !== null && parent !== undefined) {
                filtered = filtered.filter(c => c.parent_id === parseInt(parent, 10));
              }
              if (isFeatured === 'true') {
                filtered = filtered.filter(c => c.is_featured);
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
              const url = new URL(req.url, 'http://localhost');
              const kind = url.searchParams.get('kind') || 'PUBLIC_SERVICE_CATEGORY';

              const rootCategories = INITIAL_46_TAXONOMY_CATEGORIES
                .filter(c => c.kind === kind && c.parent_id === null)
                .map(root => ({
                  ...root,
                  children: INITIAL_46_TAXONOMY_CATEGORIES.filter(c => c.parent_id === root.id)
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
              const featured = INITIAL_46_TAXONOMY_CATEGORIES.filter(c => c.is_featured && c.kind === 'PUBLIC_SERVICE_CATEGORY');
              res.end(JSON.stringify({
                success: true,
                data: featured,
                message: 'জনপ্রিয় ক্যাটাগরি তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Category children
            const catChildrenMatch = pathname.match(/^\/api\/v1\/categories\/(\d+)\/children$/);
            if (catChildrenMatch && req.method === 'GET') {
              const parentId = parseInt(catChildrenMatch[1], 10);
              const children = INITIAL_46_TAXONOMY_CATEGORIES.filter(c => c.parent_id === parentId);
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
              const cat = INITIAL_46_TAXONOMY_CATEGORIES.find(c => c.id === id);
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
                data: cat,
                message: 'ক্যাটাগরি বিবরণ প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Services list & filters
            if (pathname === '/api/v1/services' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const categoryId = url.searchParams.get('category');
              const serviceType = url.searchParams.get('service_type');
              const isFeatured = url.searchParams.get('is_featured');

              let filtered = [...INITIAL_SERVICES];
              if (categoryId) {
                filtered = filtered.filter(s => s.category_id === parseInt(categoryId, 10));
              }
              if (serviceType) {
                filtered = filtered.filter(s => s.service_type === serviceType);
              }
              if (isFeatured === 'true') {
                filtered = filtered.filter(s => s.is_featured);
              }

              res.end(JSON.stringify({
                success: true,
                data: filtered,
                message: 'সেবা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Featured services
            if (pathname === '/api/v1/services/featured' && req.method === 'GET') {
              const featured = INITIAL_SERVICES.filter(s => s.is_featured);
              res.end(JSON.stringify({
                success: true,
                data: featured,
                message: 'গুরুত্বপূর্ণ সেবা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Search services (Bangla & English)
            if (pathname === '/api/v1/services/search' && req.method === 'GET') {
              const url = new URL(req.url, 'http://localhost');
              const q = (url.searchParams.get('q') || '').trim().toLowerCase();
              const categoryId = url.searchParams.get('category_id');

              let results = INITIAL_SERVICES.filter(s => {
                const matchNameBn = s.name_bn.toLowerCase().includes(q);
                const matchNameEn = s.name_en.toLowerCase().includes(q);
                const matchDescBn = s.short_description_bn.toLowerCase().includes(q);
                const matchDescEn = s.short_description_en.toLowerCase().includes(q);
                const matchCatBn = s.category_name_bn.toLowerCase().includes(q);
                const matchCatEn = s.category_name_en.toLowerCase().includes(q);
                return matchNameBn || matchNameEn || matchDescBn || matchDescEn || matchCatBn || matchCatEn;
              });

              if (categoryId) {
                results = results.filter(s => s.category_id === parseInt(categoryId, 10));
              }

              res.end(JSON.stringify({
                success: true,
                data: results,
                message: 'অনুসন্ধান ফলাফল প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Services by category
            const servByCatMatch = pathname.match(/^\/api\/v1\/services\/by-category\/(\d+)$/);
            if (servByCatMatch && req.method === 'GET') {
              const catId = parseInt(servByCatMatch[1], 10);
              const services = INITIAL_SERVICES.filter(s => s.category_id === catId);
              res.end(JSON.stringify({
                success: true,
                data: services,
                message: 'ক্যাটাগরিভিত্তিক সেবা তালিকা প্রাপ্তি সফল হয়েছে।'
              }));
              return;
            }

            // Single service detail
            const servDetailMatch = pathname.match(/^\/api\/v1\/services\/(\d+)$/);
            if (servDetailMatch && req.method === 'GET') {
              const id = parseInt(servDetailMatch[1], 10);
              const service = INITIAL_SERVICES.find(s => s.id === id);
              if (!service) {
                res.statusCode = 404;
                res.end(JSON.stringify({
                  success: false,
                  data: null,
                  message: 'সেবা পাওয়া যায়নি।'
                }));
                return;
              }
              res.end(JSON.stringify({
                success: true,
                data: service,
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
