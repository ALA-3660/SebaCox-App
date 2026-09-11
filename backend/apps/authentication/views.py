from rest_framework import views, status, permissions
from django.utils import timezone
from django.core.exceptions import ValidationError
from common.responses import StandardResponse
from .models import User, OTPVerification, AuthAuditLog
from .services import OTPService, TokenService
from .serializers import (
    UserSerializer,
    RegisterRequestOTPSerializer,
    RegisterVerifyOTPSerializer,
    LoginRequestOTPSerializer,
    LoginVerifyOTPSerializer,
    TokenRefreshSerializer,
    LogoutSerializer,
)


def get_client_ip(request) -> str:
    """Extract client IP address safely considering proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


class RegisterRequestOTPView(views.APIView):
    """
    POST /api/v1/auth/register/request-otp/
    Requests an OTP for new user registration.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterRequestOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="প্রদত্ত তথ্যে ত্রুটি রয়েছে",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        mobile_number = serializer.validated_data['mobile_number']
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            verification, dev_otp = OTPService.request_otp(
                raw_mobile_number=mobile_number,
                purpose=OTPVerification.PURPOSE_REGISTRATION,
                ip_address=ip,
                user_agent=user_agent
            )
        except ValidationError as e:
            return StandardResponse.error(
                message=str(e.message if hasattr(e, 'message') else e),
                errors={"mobile_number": [str(e)]},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS if 'অপেক্ষা' in str(e) else status.HTTP_400_BAD_REQUEST
            )

        response_data = {
            "mobile_number": mobile_number,
            "purpose": OTPVerification.PURPOSE_REGISTRATION,
            "expires_in": OTPService.get_expiry_seconds(),
        }
        if dev_otp:
            # Clearly labeled development-only mechanism
            response_data["dev_otp"] = dev_otp
            response_data["_dev_note"] = "DEVELOPMENT ONLY: Never exposed in production environments."

        return StandardResponse.success(
            data=response_data,
            message="নিবন্ধন ওটিপি কোড পাঠানো হয়েছে।"
        )


class RegisterVerifyOTPView(views.APIView):
    """
    POST /api/v1/auth/register/verify-otp/
    Verifies OTP and creates/activates the User account.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterVerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="প্রদত্ত তথ্যে ত্রুটি রয়েছে",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        mobile_number = serializer.validated_data['mobile_number']
        otp_code = serializer.validated_data['otp_code']
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            OTPService.verify_otp(
                raw_mobile_number=mobile_number,
                raw_code=otp_code,
                purpose=OTPVerification.PURPOSE_REGISTRATION,
                ip_address=ip,
                user_agent=user_agent
            )
        except ValidationError as e:
            return StandardResponse.error(
                message=str(e.message if hasattr(e, 'message') else e),
                errors={"otp_code": [str(e)]},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user, created = User.objects.get_or_create(
            mobile_number=mobile_number,
            defaults={'is_active': True, 'is_verified': True}
        )
        if not created:
            user.is_verified = True
            user.save(update_fields=['is_verified'])

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        AuthAuditLog.objects.create(
            user=user,
            mobile_number=mobile_number,
            event=AuthAuditLog.EVENT_ACCOUNT_ACTIVATED if created else AuthAuditLog.EVENT_LOGIN_SUCCESS,
            ip_address=ip,
            user_agent=user_agent[:255],
            details={'method': 'registration_otp'}
        )

        tokens = TokenService.generate_tokens_for_user(user)

        return StandardResponse.success(
            data={
                "user": UserSerializer(user).data,
                "tokens": tokens
            },
            message="নিবন্ধন ও ওটিপি যাচাই সফল হয়েছে।",
            status_code=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class LoginRequestOTPView(views.APIView):
    """
    POST /api/v1/auth/login/request-otp/
    Requests an OTP for user login.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginRequestOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="প্রদত্ত তথ্যে ত্রুটি রয়েছে",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        mobile_number = serializer.validated_data['mobile_number']
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            verification, dev_otp = OTPService.request_otp(
                raw_mobile_number=mobile_number,
                purpose=OTPVerification.PURPOSE_LOGIN,
                ip_address=ip,
                user_agent=user_agent
            )
        except ValidationError as e:
            return StandardResponse.error(
                message=str(e.message if hasattr(e, 'message') else e),
                errors={"mobile_number": [str(e)]},
                status_code=status.HTTP_429_TOO_MANY_REQUESTS if 'অপেক্ষা' in str(e) else status.HTTP_400_BAD_REQUEST
            )

        response_data = {
            "mobile_number": mobile_number,
            "purpose": OTPVerification.PURPOSE_LOGIN,
            "expires_in": OTPService.get_expiry_seconds(),
        }
        if dev_otp:
            response_data["dev_otp"] = dev_otp
            response_data["_dev_note"] = "DEVELOPMENT ONLY: Never exposed in production environments."

        return StandardResponse.success(
            data=response_data,
            message="লগইন ওটিপি কোড পাঠানো হয়েছে।"
        )


class LoginVerifyOTPView(views.APIView):
    """
    POST /api/v1/auth/login/verify-otp/
    Verifies OTP and authenticates the user, returning Access & Refresh tokens.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginVerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="প্রদত্ত তথ্যে ত্রুটি রয়েছে",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        mobile_number = serializer.validated_data['mobile_number']
        otp_code = serializer.validated_data['otp_code']
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            OTPService.verify_otp(
                raw_mobile_number=mobile_number,
                raw_code=otp_code,
                purpose=OTPVerification.PURPOSE_LOGIN,
                ip_address=ip,
                user_agent=user_agent
            )
        except ValidationError as e:
            return StandardResponse.error(
                message=str(e.message if hasattr(e, 'message') else e),
                errors={"otp_code": [str(e)]},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(mobile_number=mobile_number, is_active=True).first()
        if not user:
            return StandardResponse.error(
                message="ব্যবহারকারী অ্যাকাউন্ট পাওয়া যায়নি।",
                status_code=status.HTTP_404_NOT_FOUND
            )

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        AuthAuditLog.objects.create(
            user=user,
            mobile_number=mobile_number,
            event=AuthAuditLog.EVENT_LOGIN_SUCCESS,
            ip_address=ip,
            user_agent=user_agent[:255],
            details={'method': 'login_otp'}
        )

        tokens = TokenService.generate_tokens_for_user(user)

        return StandardResponse.success(
            data={
                "user": UserSerializer(user).data,
                "tokens": tokens
            },
            message="লগইন সফল হয়েছে।"
        )


class TokenRefreshView(views.APIView):
    """
    POST /api/v1/auth/token/refresh/
    Exchanges a valid Refresh token for a new Access token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if not serializer.is_valid():
            return StandardResponse.error(
                message="প্রদত্ত তথ্যে ত্রুটি রয়েছে",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        refresh_token = serializer.validated_data['refresh_token']
        try:
            token_data = TokenService.refresh_access_token(refresh_token)
        except ValidationError as e:
            return StandardResponse.error(
                message=str(e.message if hasattr(e, 'message') else e),
                errors={"refresh_token": [str(e)]},
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return StandardResponse.success(
            data=token_data,
            message="টোকেন সফলভাবে নবায়ন করা হয়েছে।"
        )


class LogoutView(views.APIView):
    """
    POST /api/v1/auth/logout/
    Revokes the provided refresh token and audits the logout event.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid()
        refresh_token = serializer.validated_data.get('refresh_token')

        if refresh_token:
            TokenService.revoke_refresh_token(refresh_token)

        user = request.user if hasattr(request, 'user') and request.user and request.user.is_authenticated else None
        mobile = user.mobile_number if user else 'anonymous'
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        AuthAuditLog.objects.create(
            user=user if user else None,
            mobile_number=mobile,
            event=AuthAuditLog.EVENT_LOGOUT,
            ip_address=ip,
            user_agent=user_agent[:255],
            details={'action': 'logout'}
        )

        return StandardResponse.success(
            data=None,
            message="সফলভাবে লগআউট হয়েছে।"
        )


class CurrentUserView(views.APIView):
    """
    GET /api/v1/auth/me/
    Returns basic authentication identity information for the current user.
    Requires valid Access token. Never returns passwords or secrets.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return StandardResponse.success(
            data=serializer.data,
            message="ব্যবহারকারীর তথ্য পাওয়া গেছে"
        )
