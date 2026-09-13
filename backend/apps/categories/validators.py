"""
Validators for Categories & Services.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"
"""
import re
from django.core.exceptions import ValidationError


def validate_slug(value: str):
    """Ensure slug matches lowercase alphanumeric with hyphens."""
    if not value or not str(value).strip():
        raise ValidationError('স্লাগ (Slug) খালি রাখা যাবে না।')
    
    cleaned = str(value).strip()
    if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', cleaned):
        raise ValidationError('স্লাগ শুধুমাত্র ছোট হাতের ইংরেজি বর্ণ, সংখ্যা এবং হাইফেনযুক্ত হতে পারে।')


def validate_no_circular_parent(category_id, parent_id, CategoryModel):
    """
    Ensures that setting parent_id does not introduce circular ancestry.
    A -> B -> C -> A is strictly rejected.
    """
    if not parent_id or not category_id:
        return

    if category_id == parent_id:
        raise ValidationError('একটি ক্যাটাগরি নিজেই নিজের প্যারেন্ট হতে পারে না।')

    current_parent_id = parent_id
    visited = {category_id}

    # Climb up the ancestry tree
    while current_parent_id:
        if current_parent_id in visited:
            raise ValidationError('ক্যাটাগরি হায়ারারকিতে চক্রাকার (Circular dependency) সম্পর্ক তৈরি করা যাবে না।')
        visited.add(current_parent_id)

        try:
            parent_obj = CategoryModel.objects.only('parent_id').get(id=current_parent_id)
            current_parent_id = parent_obj.parent_id
        except CategoryModel.DoesNotExist:
            break
