from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import User, OTPVerification
from .validators import normalize_mobile_number, validate_bd_mobile_number


class UserSerializer(serializers.ModelSerializer):
    """
    Safe User Serializer.
    Exposes only non-sensitive authentication identity fields.
    Never exposes passwords, OTPs, or internal tokens.
    """
    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'email', 'is_verified', 'created_at']
        read_only_fields = ['id', 'mobile_number', 'is_verified', 'created_at']


class RegisterRequestOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)

    def validate_mobile_number(self, value):
        try:
            normalized = normalize_mobile_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e.message if hasattr(e, 'message') else e))

        # Check if already registered and verified
        if User.objects.filter(mobile_number=normalized, is_verified=True).exists():
            raise serializers.ValidationError("এই মোবাইল নম্বরে ইতিমধ্যে অ্যাকাউন্ট বিদ্যমান। অনুগ্রহ করে লগইন করুন।")

        return normalized


class RegisterVerifyOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)
    otp_code = serializers.CharField(max_length=10)

    def validate_mobile_number(self, value):
        try:
            return normalize_mobile_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e.message if hasattr(e, 'message') else e))

    def validate_otp_code(self, value):
        cleaned = value.strip()
        if not cleaned.isdigit() or len(cleaned) != 6:
            raise serializers.ValidationError("ওটিপি কোডটি অবশ্যই ৬ অঙ্কের সংখ্যা হতে হবে।")
        return cleaned


class LoginRequestOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)

    def validate_mobile_number(self, value):
        try:
            normalized = normalize_mobile_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e.message if hasattr(e, 'message') else e))

        user = User.objects.filter(mobile_number=normalized).first()
        if not user:
            raise serializers.ValidationError("এই মোবাইল নম্বরে কোন অ্যাকাউন্ট খুঁজে পাওয়া যায়নি। অনুগ্রহ করে প্রথমে নিবন্ধন করুন।")

        if not user.is_active:
            raise serializers.ValidationError("আপনার অ্যাকাউন্টটি নিষ্ক্রিয় অবস্থায় রয়েছে। সহায়তার জন্য যোগাযোগ করুন।")

        return normalized


class LoginVerifyOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=20)
    otp_code = serializers.CharField(max_length=10)

    def validate_mobile_number(self, value):
        try:
            return normalize_mobile_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e.message if hasattr(e, 'message') else e))

    def validate_otp_code(self, value):
        cleaned = value.strip()
        if not cleaned.isdigit() or len(cleaned) != 6:
            raise serializers.ValidationError("ওটিপি কোডটি অবশ্যই ৬ অঙ্কের সংখ্যা হতে হবে।")
        return cleaned


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=False, allow_blank=True)
