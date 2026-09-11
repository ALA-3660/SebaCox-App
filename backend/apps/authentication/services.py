import hmac
import hashlib
import base64
import json
import secrets
import time
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import User, OTPVerification, AuthAuditLog
from .validators import normalize_mobile_number


class OTPService:
    """
    Centralized OTP management service.
    Implements rate limiting, secure salted hashing, attempt tracking,
    and safe development-only inspection.
    """
    @classmethod
    def get_expiry_seconds(cls) -> int:
        return getattr(settings, 'OTP_EXPIRY_SECONDS', 300)

    @classmethod
    def get_max_attempts(cls) -> int:
        return getattr(settings, 'OTP_MAX_ATTEMPTS', 5)

    @classmethod
    def get_resend_cooldown_seconds(cls) -> int:
        return getattr(settings, 'OTP_RESEND_COOLDOWN_SECONDS', 60)

    @classmethod
    def is_dev_otp_allowed(cls) -> bool:
        # Development OTP is strictly forbidden in production!
        if getattr(settings, 'DEBUG', False) or getattr(settings, 'ALLOW_DEV_OTP', False):
            # Double check production settings
            if getattr(settings, 'IS_PRODUCTION', False):
                return False
            return True
        return False

    @classmethod
    def request_otp(cls, raw_mobile_number: str, purpose: str, ip_address: str = None, user_agent: str = '') -> tuple[OTPVerification, str | None]:
        mobile = normalize_mobile_number(raw_mobile_number)
        cooldown = cls.get_resend_cooldown_seconds()
        cutoff_time = timezone.now() - timedelta(seconds=cooldown)

        # Check resend cooldown
        recent_otp = OTPVerification.objects.filter(
            mobile_number=mobile,
            purpose=purpose,
            created_at__gte=cutoff_time
        ).first()

        if recent_otp:
            time_left = int((recent_otp.created_at + timedelta(seconds=cooldown) - timezone.now()).total_seconds())
            if time_left > 0:
                raise ValidationError(f"অনুগ্রহ করে পুনরায় ওটিপি চাওয়ার পূর্বে {time_left} সেকেন্ড অপেক্ষা করুন।")

        # Invalidate any older unconsumed OTPs for this purpose
        OTPVerification.objects.filter(
            mobile_number=mobile,
            purpose=purpose,
            is_consumed=False
        ).update(is_consumed=True)

        # Generate 6-digit cryptographic random code
        # In dev mode, deterministic code 123456 or random can be used
        if cls.is_dev_otp_allowed():
            raw_code = "123456"
        else:
            raw_code = f"{secrets.randbelow(900000) + 100000:06d}"

        salt = secrets.token_hex(16)
        otp_hash = OTPVerification.hash_otp(raw_code, salt)
        expires_at = timezone.now() + timedelta(seconds=cls.get_expiry_seconds())

        verification = OTPVerification.objects.create(
            mobile_number=mobile,
            otp_hash=otp_hash,
            salt=salt,
            purpose=purpose,
            expires_at=expires_at,
            max_attempts=cls.get_max_attempts(),
            is_consumed=False,
        )

        # Audit event (NEVER store raw_code in details or logs)
        AuthAuditLog.objects.create(
            mobile_number=mobile,
            event=AuthAuditLog.EVENT_OTP_REQUESTED,
            ip_address=ip_address,
            user_agent=user_agent[:255],
            details={'purpose': purpose, 'expires_in_sec': cls.get_expiry_seconds()}
        )

        # Only return dev_otp if explicitly allowed in development
        dev_code = raw_code if cls.is_dev_otp_allowed() else None
        return verification, dev_code

    @classmethod
    def verify_otp(cls, raw_mobile_number: str, raw_code: str, purpose: str, ip_address: str = None, user_agent: str = '') -> bool:
        mobile = normalize_mobile_number(raw_mobile_number)
        code_str = str(raw_code).strip()

        if not code_str:
            raise ValidationError("ওটিপি কোড প্রদান করা আবশ্যক।")

        verification = OTPVerification.objects.filter(
            mobile_number=mobile,
            purpose=purpose,
            is_consumed=False
        ).order_by('-created_at').first()

        if not verification:
            raise ValidationError("কোন সক্রিয় ওটিপি অনুরোধ পাওয়া যায়নি। অনুগ্রহ করে নতুন ওটিপি অনুরোধ করুন।")

        if verification.is_expired:
            raise ValidationError("ওটিপির মেয়াদ শেষ হয়ে গেছে। অনুগ্রহ করে নতুন ওটিপি অনুরোধ করুন।")

        if verification.attempts >= verification.max_attempts:
            raise ValidationError("সর্বোচ্চ ভেরিফিকেশন চেষ্টার সীমা অতিক্রম করেছে। নতুন ওটিপি অনুরোধ করুন।")

        # Verify hash
        if not verification.verify_code(code_str):
            verification.attempts += 1
            verification.save(update_fields=['attempts'])

            AuthAuditLog.objects.create(
                mobile_number=mobile,
                event=AuthAuditLog.EVENT_LOGIN_FAILED,
                ip_address=ip_address,
                user_agent=user_agent[:255],
                details={'purpose': purpose, 'reason': 'incorrect_code', 'attempts': verification.attempts}
            )

            remaining = verification.max_attempts - verification.attempts
            if remaining > 0:
                raise ValidationError(f"ভুল ওটিপি কোড। আপনার অবশিষ্ট চেষ্টা: {remaining} বার।")
            else:
                raise ValidationError("সর্বোচ্চ ভেরিফিকেশন চেষ্টার সীমা অতিক্রম করেছে। নতুন ওটিপি অনুরোধ করুন।")

        # Code matched successfully
        verification.is_consumed = True
        verification.consumed_at = timezone.now()
        verification.save(update_fields=['is_consumed', 'consumed_at'])

        AuthAuditLog.objects.create(
            mobile_number=mobile,
            event=AuthAuditLog.EVENT_OTP_VERIFIED,
            ip_address=ip_address,
            user_agent=user_agent[:255],
            details={'purpose': purpose}
        )
        return True


class TokenService:
    """
    Secure JWT-compatible Token Engine.
    Uses HMAC-SHA256 with project SECRET_KEY to sign and verify Access and Refresh tokens.
    Guarantees no tokens in URL query strings and no token logging.
    """
    ALGORITHM = "HS256"

    # In-memory or cache-based blacklist for revoked refresh tokens
    _revoked_tokens = set()

    @classmethod
    def _b64url_encode(cls, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

    @classmethod
    def _b64url_decode(cls, s: str) -> bytes:
        padding = '=' * (-len(s) % 4)
        return base64.urlsafe_b64decode(s + padding)

    @classmethod
    def _get_signing_key(cls) -> bytes:
        key = getattr(settings, 'SECRET_KEY', 'sebacox-secret-key')
        return key.encode('utf-8')

    @classmethod
    def encode_jwt(cls, payload: dict) -> str:
        header = {"alg": cls.ALGORITHM, "typ": "JWT"}
        header_b64 = cls._b64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
        payload_b64 = cls._b64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
        
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        signature = hmac.new(cls._get_signing_key(), signing_input, hashlib.sha256).digest()
        signature_b64 = cls._b64url_encode(signature)
        return f"{header_b64}.{payload_b64}.{signature_b64}"

    @classmethod
    def decode_jwt(cls, token: str) -> dict:
        parts = token.strip().split('.')
        if len(parts) != 3:
            raise ValidationError("অবৈধ টোকেন ফরম্যাট।")
        
        header_b64, payload_b64, signature_b64 = parts
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(cls._get_signing_key(), signing_input, hashlib.sha256).digest()
        
        try:
            actual_sig = cls._b64url_decode(signature_b64)
            if not hmac.compare_digest(expected_sig, actual_sig):
                raise ValidationError("টোকেন সিগনেচার যাচাইকরণ ব্যর্থ হয়েছে।")
            
            payload_data = json.loads(cls._b64url_decode(payload_b64).decode('utf-8'))
        except Exception:
            raise ValidationError("টোকেন ডিকোড করা সম্ভব হয়নি।")

        exp = payload_data.get('exp')
        if exp and exp < time.time():
            raise ValidationError("টোকেনের মেয়াদ শেষ হয়ে গেছে।")

        return payload_data

    @classmethod
    def generate_tokens_for_user(cls, user: User) -> dict:
        now = int(time.time())
        access_lifetime = getattr(settings, 'JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 60) * 60
        refresh_lifetime = getattr(settings, 'JWT_REFRESH_TOKEN_LIFETIME_DAYS', 30) * 86400

        access_payload = {
            'user_id': user.id,
            'mobile_number': user.mobile_number,
            'token_type': 'access',
            'iat': now,
            'exp': now + access_lifetime,
            'jti': secrets.token_hex(8)
        }

        refresh_payload = {
            'user_id': user.id,
            'mobile_number': user.mobile_number,
            'token_type': 'refresh',
            'iat': now,
            'exp': now + refresh_lifetime,
            'jti': secrets.token_hex(16)
        }

        return {
            'access_token': cls.encode_jwt(access_payload),
            'refresh_token': cls.encode_jwt(refresh_payload),
            'token_type': 'Bearer',
            'expires_in': access_lifetime
        }

    @classmethod
    def refresh_access_token(cls, refresh_token_string: str) -> dict:
        if not refresh_token_string:
            raise ValidationError("রিফ্রেশ টোকেন প্রদান করা আবশ্যক।")

        payload = cls.decode_jwt(refresh_token_string)
        if payload.get('token_type') != 'refresh':
            raise ValidationError("প্রদত্ত টোকেনটি রিফ্রেশ টোকেন নয়।")

        jti = payload.get('jti')
        if jti in cls._revoked_tokens:
            raise ValidationError("রিফ্রেশ টোকেনটি বাতিল করা হয়েছে।")

        user_id = payload.get('user_id')
        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise ValidationError("ব্যবহারকারী সক্রিয় নয় অথবা পাওয়া যায়নি।")

        # Rotate access token
        now = int(time.time())
        access_lifetime = getattr(settings, 'JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 60) * 60
        access_payload = {
            'user_id': user.id,
            'mobile_number': user.mobile_number,
            'token_type': 'access',
            'iat': now,
            'exp': now + access_lifetime,
            'jti': secrets.token_hex(8)
        }

        return {
            'access_token': cls.encode_jwt(access_payload),
            'token_type': 'Bearer',
            'expires_in': access_lifetime
        }

    @classmethod
    def revoke_refresh_token(cls, refresh_token_string: str) -> bool:
        try:
            payload = cls.decode_jwt(refresh_token_string)
            jti = payload.get('jti')
            if jti:
                cls._revoked_tokens.add(jti)
            return True
        except Exception:
            return False
