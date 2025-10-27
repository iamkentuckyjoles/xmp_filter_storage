from django.core.exceptions import PermissionDenied  # 🚫 Raise error if unauthorized

# 🔐 Utility function to check if user is an admin
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


# 🔐 Restrict view access to admin users only
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

# Decorator for admin/senior-only access
def admin_or_senior_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ['admin', 'senior']:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

