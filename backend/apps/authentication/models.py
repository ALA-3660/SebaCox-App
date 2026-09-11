import hashlib
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from .validators import normalize_mobile_number, validate_bd_mobile_number


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where mobile_number is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("ব্যবহারকারীর জন্য মোবাইল নম্বর আবশ্যক।")
        
        normalized_number = normalize_mobile_number(mobile_number)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', False)

        user = self.model(mobile_number=normalized_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(mobile_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    SebaCox Custom User Model.
    Designed for future expansion: A single user account that may later act as
    customer, service provider, seller, landlord, renter, job seeker, or employer.
    """
    id = models.BigAutoField(primary_key=True)
    mobile_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        validators=[validate_bd_mobile_number],
        help_text="Primary authentication identifier in canonical format (+8801XXXXXXXXX)."
    )
    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
        help_text="Optional contact and notification email address."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active."
    )
    is_verified = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Designates whether the user's mobile number has been verified via OTP."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into the admin site."
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time the user account was created."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mobile_number']),
            models.Index(fields=['is_active', 'is_verified']),
            models.Index(fields=['created_at']),
        ]

    def save(self, *args, **kwargs):
        if self.mobile_number:
            self.mobile_number = normalize_mobile_number(self.mobile_number)
        if self.email == '':
            self.email = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.mobile_number


class OTPVerification(models.Model):
    """
    OTP Verification Foundation.
    Stores cryptographic hashes of OTPs (never plaintext) along with expiry,
    purpose, rate limits, and verification status.
    """
    PURPOSE_REGISTRATION = 'REGISTRATION'
    PURPOSE_LOGIN = 'LOGIN'
    PURPOSE_PHONE_VERIFICATION = 'PHONE_VERIFICATION'
    PURPOSE_PASSWORD_RESET = 'PASSWORD_RESET'

    PURPOSE_CHOICES = [
        (PURPOSE_REGISTRATION, 'Registration'),
        (PURPOSE_LOGIN, 'Login'),
        (PURPOSE_PHONE_VERIFICATION, 'Phone Verification'),
        (PURPOSE_PASSWORD_RESET, 'Password Reset'),
    ]

    id = models.BigAutoField(primary_key=True)
    mobile_number = models.CharField(
        max_length=20,
        db_index=True,
        validators=[validate_bd_mobile_number]
    )
    otp_hash = models.CharField(
        max_length=128,
        help_text="SHA-256 cryptographic hash of salt + raw OTP. Never store plaintext."
    )
    salt = models.CharField(
        max_length=32,
        help_text="Random cryptographic salt for OTP hashing."
    )
    purpose = models.CharField(
        max_length=30,
        choices=PURPOSE_CHOICES,
        db_index=True
    )
    expires_at = models.DateTimeField(
        db_index=True
    )
    attempts = models.PositiveIntegerField(
        default=0,
        help_text="Number of incorrect verification attempts."
    )
    max_attempts = models.PositiveIntegerField(
        default=5,
        help_text="Maximum allowed attempts before invalidation."
    )
    is_consumed = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether this OTP has already been verified and used."
    )
    consumed_at = models.DateTimeField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'OTP Verification'
        verbose_name_plural = 'OTP Verifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mobile_number', 'purpose', 'is_consumed']),
            models.Index(fields=['expires_at']),
        ]

    @staticmethod
    def hash_otp(raw_otp: str, salt: str) -> str:
        """Computes SHA-256 hash of salt + OTP string."""
        combined = f"{salt}:{raw_otp}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    def verify_code(self, raw_code: str) -> bool:
        """Verifies if given raw code matches the stored secure hash."""
        expected_hash = self.hash_otp(str(raw_code).strip(), self.salt)
        return expected_hash == self.otp_hash

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    @property
    def can_attempt(self) -> bool:
        return (not self.is_consumed) and (not self.is_expired) and (self.attempts < self.max_attempts)

    def __str__(self):
        return f"OTP for {self.mobile_number} ({self.purpose}) - Consumed: {self.is_consumed}"


class AuthAuditLog(models.Model):
    """
    Audit Trail Foundation for Authentication Events.
    Tracks security events without ever logging passwords, secrets, or raw OTP values.
    """
    EVENT_OTP_REQUESTED = 'OTP_REQUESTED'
    EVENT_OTP_VERIFIED = 'OTP_VERIFIED'
    EVENT_LOGIN_SUCCESS = 'LOGIN_SUCCESS'
    EVENT_LOGIN_FAILED = 'LOGIN_FAILED'
    EVENT_LOGOUT = 'LOGOUT'
    EVENT_TOKEN_REFRESH_SUCCESS = 'TOKEN_REFRESH_SUCCESS'
    EVENT_TOKEN_REFRESH_FAILED = 'TOKEN_REFRESH_FAILED'
    EVENT_ACCOUNT_ACTIVATED = 'ACCOUNT_ACTIVATED'

    EVENT_CHOICES = [
        (EVENT_OTP_REQUESTED, 'OTP Requested'),
        (EVENT_OTP_VERIFIED, 'OTP Verified'),
        (EVENT_LOGIN_SUCCESS, 'Login Success'),
        (EVENT_LOGIN_FAILED, 'Login Failed'),
        (EVENT_LOGOUT, 'Logout'),
        (EVENT_TOKEN_REFRESH_SUCCESS, 'Token Refresh Success'),
        (EVENT_TOKEN_REFRESH_FAILED, 'Token Refresh Failed'),
        (EVENT_ACCOUNT_ACTIVATED, 'Account Activated'),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='auth_audit_logs'
    )
    mobile_number = models.CharField(
        max_length=20,
        db_index=True
    )
    event = models.CharField(
        max_length=40,
        choices=EVENT_CHOICES,
        db_index=True
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Non-sensitive event metadata (e.g. latency, reason). NEVER store secrets."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Auth Audit Log'
        verbose_name_plural = 'Auth Audit Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.created_at}] {self.event} - {self.mobile_number}"
