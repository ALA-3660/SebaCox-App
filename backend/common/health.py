"""
Health Check View for SebaCox API v1.
"মানুষের প্রয়োজন থেকে সেবার সমাধান।"

GET /api/v1/health/
Returns standard response indicating service operational state without leaking sensitive infrastructure details.
"""
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from common.responses import StandardResponse


class HealthCheckView(APIView):
    """
    Health check endpoint for SebaCox API v1.
    Allows clients, mobile apps, load balancers, and monitoring systems
    to verify server responsiveness.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        """
        Returns health status adhering to standard response format:
        {
            "success": true,
            "data": {
                "status": "healthy"
            },
            "message": "SebaCox API is running"
        }
        """
        data = {
            "status": "healthy"
        }
        return StandardResponse.success(
            data=data,
            message="SebaCox API is running"
        )
