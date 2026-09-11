from rest_framework import authentication
from rest_framework import exceptions
from django.core.exceptions import ValidationError
from .services import TokenService
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT Authentication for SebaCox API.
    Inspects standard 'Authorization: Bearer <token>' header.
    Never accepts tokens in query parameters.
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if auth_header[0].decode('utf-8').lower() != self.keyword.lower():
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed("অবৈধ Authorization হেডার: টোকেন অনুপস্থিত।")
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed("অবৈধ Authorization হেডার: টোকেন ফরম্যাট ত্রুটিপূর্ণ।")

        token_str = auth_header[1].decode('utf-8')

        try:
            payload = TokenService.decode_jwt(token_str)
        except ValidationError as e:
            raise exceptions.AuthenticationFailed(str(e.message if hasattr(e, 'message') else e))

        if payload.get('token_type') != 'access':
            raise exceptions.AuthenticationFailed("প্রদত্ত টোকেনটি এক্সেস টোকেন নয়।")

        user_id = payload.get('user_id')
        if not user_id:
            raise exceptions.AuthenticationFailed("টোকেনে ব্যবহারকারীর পরিচয় অনুপস্থিত।")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("ব্যবহারকারী পাওয়া যায়নি।")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("ব্যবহারকারীর অ্যাকাউন্টটি নিষ্ক্রিয়।")

        return (user, token_str)

    def authenticate_header(self, request):
        return self.keyword
