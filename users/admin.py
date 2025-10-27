from django.contrib import admin  # Default admin site registration
from django.contrib.auth.admin import UserAdmin  # Base admin config for user model
from django.contrib.admin import AdminSite  # Allows custom admin site behavior
from django.core.exceptions import PermissionDenied  # Used for access control (not triggered here)
from .models import CustomUser  # Import custom user model

# -------------------------------------------------------------------
# Custom Admin Site: Restricts access to users with 'admin' role only
# -------------------------------------------------------------------
class CustomAdminSite(AdminSite):
    def has_permission(self, request):
        user = request.user
        return user.is_active and user.is_staff and getattr(user, 'role', None) == 'admin'


# Instantiate the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')


# -------------------------------------------------------------------
# CustomUserAdmin: Extends default UserAdmin with role-based display
# -------------------------------------------------------------------
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active')  # Columns in list view
    list_filter = ('role', 'is_active')  # Sidebar filters
    search_fields = ('username', 'email')  # Searchable fields

    # Add 'role' field to existing fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )


# Register CustomUser with the custom admin site
custom_admin_site.register(CustomUser, CustomUserAdmin)