"""
Sensitive Data Masking Filter for Python/Django Logging.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"

Ensures sensitive customer and system credentials never leak into server logs.
"""
import logging
import re

SENSITIVE_PATTERNS = [
    (re.compile(r'(password|passwd|pwd)[\s]*[=:]\s*[\'"]?([^\'"\s,]+)', re.IGNORECASE), r'\1=********'),
    (re.compile(r'(otp|pin|verification_code)[\s]*[=:]\s*[\'"]?([^\'"\s,]+)', re.IGNORECASE), r'\1=******'),
    (re.compile(r'(access_token|refresh_token|token|authorization)[\s]*[=:]\s*[\'"]?Bearer\s+([^\'"\s,]+)', re.IGNORECASE), r'\1=Bearer ********'),
    (re.compile(r'(api_key|secret_key|client_secret)[\s]*[=:]\s*[\'"]?([^\'"\s,]+)', re.IGNORECASE), r'\1=********'),
    (re.compile(r'(card_number|cvv|cvc)[\s]*[=:]\s*[\'"]?([^\'"\s,]+)', re.IGNORECASE), r'\1=************'),
]


class SensitiveDataFilter(logging.Filter):
    """Filter that masks sensitive tokens, passwords, and OTPs in log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            if isinstance(record.msg, str):
                message = record.msg
                for pattern, replacement in SENSITIVE_PATTERNS:
                    message = pattern.sub(replacement, message)
                record.msg = message

            if record.args:
                new_args = []
                for arg in record.args:
                    if isinstance(arg, str):
                        masked = arg
                        for pattern, replacement in SENSITIVE_PATTERNS:
                            masked = pattern.sub(replacement, masked)
                        new_args.append(masked)
                    else:
                        new_args.append(arg)
                record.args = tuple(new_args)
        except Exception:
            # Filtering must never break logging
            pass
        return True
