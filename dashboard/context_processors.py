# dashboard/context_processors.py
from users.models import ForgotPasswordRequest

def forgot_password_requests_count(request):
    # Only count if user is authenticated (optional)
    if request.user.is_authenticated and request.user.is_staff:  # Only for admin users
        pending_count = ForgotPasswordRequest.objects.filter(status='Pending').count()
        return {'pending_requests_count': pending_count}
    return {'pending_requests_count': 0}  # Default value