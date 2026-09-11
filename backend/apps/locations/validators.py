"""
Validators for location fields and coordinates.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"
"""
import re
from django.core.exceptions import ValidationError
from .constants import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE


def validate_latitude(value):
    """Validate that latitude falls within legal bounds (-90.0 to +90.0)."""
    try:
        val = float(value)
    except (TypeError, ValueError):
        raise ValidationError('অক্ষাংশ (Latitude) অবশ্যই একটি সংখ্যা হতে হবে।')

    if val < MIN_LATITUDE or val > MAX_LATITUDE:
        raise ValidationError(
            f'অক্ষাংশ অবশ্যই {MIN_LATITUDE} এবং {MAX_LATITUDE} এর মধ্যে হতে হবে।'
        )


def validate_longitude(value):
    """Validate that longitude falls within legal bounds (-180.0 to +180.0)."""
    try:
        val = float(value)
    except (TypeError, ValueError):
        raise ValidationError('দ্রাঘিমাংশ (Longitude) অবশ্যই একটি সংখ্যা হতে হবে।')

    if val < MIN_LONGITUDE or val > MAX_LONGITUDE:
        raise ValidationError(
            f'দ্রাঘিমাংশ অবশ্যই {MIN_LONGITUDE} এবং {MAX_LONGITUDE} এর মধ্যে হতে হবে।'
        )


def validate_location_code(value):
    """Validate administrative or BBS geocode format."""
    if value is None:
        return

    if not str(value).strip():
        raise ValidationError('অবস্থান কোড খালি রাখা যাবে না।')

    cleaned = str(value).strip()
    if len(cleaned) > 20:
        raise ValidationError('অবস্থান কোড সর্বোচ্চ ২০ অক্ষরের হতে পারে।')

    if not re.match(r'^[A-Za-z0-9\-_]+$', cleaned):
        raise ValidationError('অবস্থান কোডে শুধুমাত্র বর্ণ, সংখ্যা, হাইফেন বা আন্ডারস্কোর ব্যবহার করা যাবে।')


def validate_radius(value):
    """Validate search radius in kilometers (0.1km to 500km)."""
    try:
        val = float(value)
    except (TypeError, ValueError):
        raise ValidationError('ব্যাসার্ধ (Radius) অবশ্যই একটি বৈধ সংখ্যা হতে হবে।')

    if val <= 0:
        raise ValidationError('ব্যাসার্ধ অবশ্যই ০ এর চেয়ে বেশি হতে হবে।')
    if val > 500.0:
        raise ValidationError('অনুসন্ধানের ব্যাসার্ধ সর্বোচ্চ ৫০০ কিলোমিটার হতে পারে।')
