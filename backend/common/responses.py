"""
Standard API Response Module for SebaCox.
"প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
"খুঁজুন, যোগাযোগ করুন, সেবা নিন- সহজেই"

Standardizes API response contracts across all future modules.
"""
from typing import Any, Optional, Dict
from rest_framework.response import Response
from rest_framework import status


class StandardResponse:
    """Helper factory for returning unified SebaCox API responses."""

    @staticmethod
    def success(
        data: Any = None,
        message: str = "সফলভাবে সম্পন্ন হয়েছে",
        status_code: int = status.HTTP_200_OK,
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """
        Standard Success Response:
        {
            "success": True,
            "data": data,
            "message": message
        }
        """
        payload = {
            "success": True,
            "data": data if data is not None else {},
            "message": message
        }
        return Response(payload, status=status_code, headers=headers)

    @staticmethod
    def error(
        message: str = "অনুরোধটি সম্পন্ন করা যায়নি",
        errors: Any = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """
        Standard Error Response:
        {
            "success": False,
            "data": None,
            "message": message,
            "errors": errors or {}
        }
        """
        payload = {
            "success": False,
            "data": None,
            "message": message,
            "errors": errors if errors is not None else {}
        }
        return Response(payload, status=status_code, headers=headers)
