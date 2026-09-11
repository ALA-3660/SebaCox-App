from django.urls import path
from .views import (
    RegisterRequestOTPView,
    RegisterVerifyOTPView,
    LoginRequestOTPView,
    LoginVerifyOTPView,
    TokenRefreshView,
    LogoutView,
    CurrentUserView,
)

app_name = 'authentication'

urlpatterns = [
    # Registration Flow
    path('register/request-otp/', RegisterRequestOTPView.as_view(), name='register-request-otp'),
    path('register/verify-otp/', RegisterVerifyOTPView.as_view(), name='register-verify-otp'),

    # Login Flow
    path('login/request-otp/', LoginRequestOTPView.as_view(), name='login-request-otp'),
    path('login/verify-otp/', LoginVerifyOTPView.as_view(), name='login-verify-otp'),

    # Token Lifecycle
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Current User Identity
    path('me/', CurrentUserView.as_view(), name='current-user'),
]
