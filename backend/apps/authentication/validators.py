import re
from django.core.exceptions import ValidationError

# Regex pattern for Bangladesh mobile numbers:
# Accepts:
# - Local 11 digits: 013XXXXXXXX to 019XXXXXXXX
# - With 88 country code: 8801XXXXXXXXX
# - With +88 country code: +8801XXXXXXXXX
# - With whitespace or dashes between groups: e.g. 01711-123456 or +88 01711 123456
BD_MOBILE_REGEX = re.compile(r'^(?:\+?88)?01[3-9]\d{8}$')

def clean_phone_number_string(raw_number: str) -> str:
    """Strip common formatting characters (spaces, dashes, parentheses)."""
    if not raw_number:
        return ''
    return re.sub(r'[\s\-\(\)\.]', '', str(raw_number).strip())

def normalize_mobile_number(raw_number: str) -> str:
    """
    Normalizes a mobile number to standard international E.164 format (+8801XXXXXXXXX).
    Ensures that '01711123456', '+8801711123456', and '8801711123456' resolve to the exact same canonical string.
    """
    cleaned = clean_phone_number_string(raw_number)
    if not cleaned:
        raise ValidationError("মোবাইল নম্বর প্রদান করা আবশ্যক।")

    # If starts with +8801...
    if cleaned.startswith('+8801') and len(cleaned) == 14:
        if BD_MOBILE_REGEX.match(cleaned):
            return cleaned

    # If starts with 8801...
    if cleaned.startswith('8801') and len(cleaned) == 13:
        canonical = '+' + cleaned
        if BD_MOBILE_REGEX.match(canonical):
            return canonical

    # If local 11 digits starting with 01...
    if cleaned.startswith('01') and len(cleaned) == 11:
        canonical = '+88' + cleaned
        if BD_MOBILE_REGEX.match(canonical):
            return canonical

    raise ValidationError("সঠিক বাংলাদেশি মোবাইল নম্বর দিন (যেমন: 017XXXXXXXX বা +88017XXXXXXXX)।")

def validate_bd_mobile_number(value: str) -> None:
    """Validator suitable for Django model fields and serializers."""
    normalize_mobile_number(value)
