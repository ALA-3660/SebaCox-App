"""
Custom Unified Exception Handler for SebaCox REST API.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"

Ensures all exceptions (validation, 401, 403, 404, 500) return the standard JSON structure:
{
    "success": false,
    "data": null,
    "message": "...",
    "errors": {...}
}
"""
import logging
from django.conf import settings
from django.http import Http404
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    MethodNotAllowed,
)

logger = logging.getLogger('sebacox.exceptions')


def custom_exception_handler(exc, context) -> Response:
    """
    Unified exception handler mapping all framework and custom exceptions
    to standard SebaCox error responses.
    """
    # Call REST framework's default exception handler first to get standard response
    response = exception_handler(exc, context)

    # Convert Django native exceptions
    if isinstance(exc, Http404):
        exc = NotFound("অনুরোধকৃত রিসোর্সটি পাওয়া যায়নি")
        response = Response(status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, DjangoPermissionDenied):
        exc = PermissionDenied("আপনার এই সেবাটির অনুমতি নেই")
        response = Response(status=status.HTTP_403_FORBIDDEN)

    # If an unhandled exception occurred (e.g. 500 Internal Server Error)
    if response is None:
        logger.exception("Unhandled server exception in request", exc_info=exc)
        
        message = "সার্ভারে একটি অভ্যন্তরীণ ত্রুটি ঘটেছে। দয়া করে কিছুক্ষণ পরে আবার চেষ্টা করুন।"
        error_details = {}
        
        # Only expose traceback in development mode if explicitly enabled
        if getattr(settings, 'DEBUG', False):
            error_details = {
                "type": exc.__class__.__name__,
                "detail": str(exc),
            }

        return Response(
            {
                "success": False,
                "data": None,
                "message": message,
                "errors": error_details,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Handle standard DRF exceptions
    error_message = "অনুরোধটি সম্পন্ন করা যায়নি"
    errors = {}

    if isinstance(exc, ValidationError):
        error_message = "প্রদত্ত তথ্যে ত্রুটি রয়েছে"
        if isinstance(exc.detail, dict):
            errors = exc.detail
        elif isinstance(exc.detail, list):
            errors = {"non_field_errors": exc.detail}
        else:
            errors = {"detail": str(exc.detail)}
    elif isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        error_message = "অনুরোধটির জন্য প্রমাণীকরণ প্রয়োজন"
        errors = {"detail": str(exc.detail)}
    elif isinstance(exc, PermissionDenied):
        error_message = "আপনার এই অনুরোধটি সম্পাদন করার অনুমতি নেই"
        errors = {"detail": str(exc.detail)}
    elif isinstance(exc, NotFound):
        error_message = "অনুরোধকৃত রিসোর্সটি পাওয়া যায়নি"
        errors = {"detail": str(exc.detail)}
    elif isinstance(exc, MethodNotAllowed):
        error_message = f"অনুরোধ পদ্ধতি '{context['request'].method}' সমর্থিত নয়"
        errors = {"detail": str(exc.detail)}
    elif hasattr(exc, 'detail'):
        errors = {"detail": str(exc.detail)}

    return Response(
        {
            "success": False,
            "data": None,
            "message": error_message,
            "errors": errors,
        },
        status=response.status_code
    )
