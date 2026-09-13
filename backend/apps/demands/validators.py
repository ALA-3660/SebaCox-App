"""
Validation functions for SebaCox Demand Engine.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"""
from decimal import Decimal
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from .constants import (
    DemandStatus,
    VALID_DEMAND_STATUS_TRANSITIONS,
    LOCKED_HISTORICAL_STATUSES,
)


def validate_demand_status_transition(current_status: str, new_status: str) -> None:
    """
    Validate that transitioning from current_status to new_status is strictly allowed.
    Raises ValidationError if transition is invalid or attempt is made to edit a terminal state.
    """
    if current_status == new_status:
        return

    allowed = VALID_DEMAND_STATUS_TRANSITIONS.get(current_status, [])
    if new_status not in allowed:
        current_label = dict(DemandStatus.choices).get(current_status, current_status)
        new_label = dict(DemandStatus.choices).get(new_status, new_status)
        raise ValidationError(
            f"অবস্থা পরিবর্তন সম্ভব নয়: '{current_label}' থেকে '{new_label}' অনুমোদিত নয়।"
        )


def validate_demand_budget(budget_min=None, budget_max=None) -> None:
    """
    Validate budget range integrity.
    """
    if budget_min is not None:
        if Decimal(str(budget_min)) < 0:
            raise ValidationError("সর্বনিম্ন বাজেট ঋণাত্মক হতে পারে না।")

    if budget_max is not None:
        if Decimal(str(budget_max)) < 0:
            raise ValidationError("সর্বোচ্চ বাজেট ঋণাত্মক হতে পারে না।")

    if budget_min is not None and budget_max is not None:
        if Decimal(str(budget_min)) > Decimal(str(budget_max)):
            raise ValidationError("সর্বনিম্ন বাজেট সর্বোচ্চ বাজেটের চেয়ে বড় হতে পারে না।")


def validate_demand_quantity(quantity=None, unit=None) -> None:
    """
    Validate quantity is strictly positive when specified.
    """
    if quantity is not None:
        if Decimal(str(quantity)) <= 0:
            raise ValidationError("পরিমাণ অবশ্যই শূন্যের চেয়ে বড় হতে হবে।")


def validate_demand_for_publish(
    title_bn: str,
    description_bn: str,
    expires_at,
    budget_min=None,
    budget_max=None,
    quantity=None,
    unit=None,
    upazila_id=None,
    district_id=None,
    location_display_bn=None,
    current_time=None
) -> None:
    """
    Strict server-side validation executed before a Demand can transition to PUBLISHED.
    """
    errors = {}

    if not title_bn or not title_bn.strip():
        errors['title_bn'] = "প্রয়োজনের বাংলা শিরোনাম প্রদান করা আবশ্যক।"
    elif len(title_bn.strip()) < 5:
        errors['title_bn'] = "শিরোনাম কমপক্ষে ৫ অক্ষরের হতে হবে।"

    if not description_bn or not description_bn.strip():
        errors['description_bn'] = "প্রয়োজনের বিস্তারিত বিবরণ প্রদান করা আবশ্যক।"
    elif len(description_bn.strip()) < 10:
        errors['description_bn'] = "বিবরণ কমপক্ষে ১০ অক্ষরের হতে হবে।"

    # Location requirement: must have either upazila, district, or explicit location display
    if not upazila_id and not district_id and not (location_display_bn and location_display_bn.strip()):
        errors['location'] = "প্রয়োজনের সুনির্দিষ্ট এলাকা বা উপজেলা নির্বাচন আবশ্যক।"

    # Expiration validation
    if not expires_at:
        errors['expires_at'] = "প্রয়োজনের মেয়াদ উত্তীর্ণের তারিখ ও সময় নির্ধারণ আবশ্যক।"
    else:
        now = current_time or timezone.now()
        if expires_at <= now:
            errors['expires_at'] = "মেয়াদ উত্তীর্ণের সময় অবশ্যই বর্তমান সময়ের পরবর্তী হতে হবে।"

    # Budget validation
    try:
        validate_demand_budget(budget_min, budget_max)
    except ValidationError as e:
        errors['budget'] = str(e.message if hasattr(e, 'message') else e)

    # Quantity validation
    try:
        validate_demand_quantity(quantity, unit)
    except ValidationError as e:
        errors['quantity'] = str(e.message if hasattr(e, 'message') else e)

    if errors:
        raise ValidationError(errors)
