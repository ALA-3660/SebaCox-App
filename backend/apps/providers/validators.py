"""
Validators for Provider Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
import re
from django.core.exceptions import ValidationError
from .constants import VALID_STATUS_TRANSITIONS, ProviderStatus


def validate_slug(value: str):
    """
    Validates that a provider slug only contains lowercase alphanumeric characters and hyphens.
    Strictly forbids whitespace, underscores, uppercase letters, or special characters.
    """
    if not value:
        raise ValidationError("স্লাগ (slug) ফাঁকা হতে পারে না।")

    pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    if not re.match(pattern, value):
        raise ValidationError(
            f"অবৈধ স্লাগ বিন্যাস: '{value}'। শুধুমাত্র ছোট হাতের ইংরেজি অক্ষর, সংখ্যা এবং হাইফেন প্রযোজ্য।"
        )


def validate_status_transition(current_status: str, new_status: str):
    """
    Enforces valid state transition according to ProviderStatus transition table.
    """
    if current_status == new_status:
        return

    allowed_targets = VALID_STATUS_TRANSITIONS.get(current_status, [])
    if new_status not in allowed_targets:
        raise ValidationError(
            f"অবৈধ স্ট্যাটাস পরিবর্তন: '{current_status}' থেকে '{new_status}' অনুমোদনযোগ্য নয়। "
            f"অনুমোদিত লক্ষ্য: {allowed_targets}"
        )
