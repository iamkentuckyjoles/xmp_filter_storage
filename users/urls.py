from django.contrib.auth import views as auth_views  # Optional: built-in auth views (not used here)
from django.urls import path  # Defines URL patterns
from users.views import auth_views, forgotpassword_views  # Import custom views
from users.views.admin_views import admin_change_user_password


app_name = 'users'  # Namespace for reverse lookups

urlpatterns = [
    path('login/', auth_views.login_view, name='login'),        # 🔐 Login page
    path('logout/', auth_views.logout_view, name='logout'),     # 🚪 Logout route
    path('forgot-password/', forgotpassword_views.forgot_password, name='forgot_password'),    # 🔑 Forgot password
    path('admin/reset-password/<int:user_id>/', admin_change_user_password, name='admin_change_user_password'),
]