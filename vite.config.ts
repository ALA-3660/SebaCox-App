import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import {defineConfig} from 'vite';

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
