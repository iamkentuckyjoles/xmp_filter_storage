"""
URL configuration for SIF project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ─── Django Core Imports ─────────────────────────────────────────────
from django.contrib import admin  # Default admin site (unused here)
from django.urls import path, include  # URL routing and app inclusion
from django.contrib.auth import views as auth_views  # Built-in auth views (e.g. LoginView)

# ─── Custom Admin ────────────────────────────────────────────────────
from users.admin import custom_admin_site  # Role-restricted admin site for 'admin' users

# ─── Static & Media Config (for development) ─────────────────────────
from django.conf import settings  # Access project settings
from django.conf.urls.static import static  # Serve media files in dev mode

# ─── URL Patterns ────────────────────────────────────────────────────
urlpatterns = [
    path('admin/', custom_admin_site.urls),  # Custom admin route
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),  # Login view using custom template
    path('user/', include(('users.urls', 'users'), namespace='users')),  # User-related routes
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),  # Dashboard routes with namespace
    path('clockify/', include('clockify_integration.urls', namespace='clockify_integration')), # Include clockify app URLs
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)