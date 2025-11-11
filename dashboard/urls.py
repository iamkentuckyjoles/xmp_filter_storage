from django.contrib.auth import views as auth_views  # built-in auth views
from django.urls import path, include  # for defining URL patterns
from dashboard import views  # local views
from dashboard.view_modules.event_views import delete_event, edit_event
from dashboard.view_modules.filter_views import delete_filter  # dashboard views
from . import views  # local views (redundant if already imported above)
from dashboard.view_modules.user_views import edit_user, delete_user, update_role # user management rules
from .views import view_users_by_role
from dashboard.view_modules import user_views   
from dashboard.view_modules.user_views import view_forgot_password_requests # forgot password requests view
from dashboard.view_modules.clockify_views import ClockifyReportsView

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_redirect, name='redirect'),  # role-based redirect
    path('admin/', views.admin_home, name='admin_home'),  # admin dashboard
    path('admin/create-user/', views.create_user, name='create_user'),  # admin user creation
    path('users/', views.view_users, name='view_users'),  # Admin-only route to view all registered users
    path('users/role/<str:role>/', view_users_by_role, name='view_users_by_role'), # Admin only route to view users by role
    path('senior/', views.senior_home, name='senior_home'),  # senior dashboard
    path('junior/', views.junior_home, name='junior_home'),  # junior dashboard
    path('default/', views.default_home, name='default_home'),  # fallback dashboard
    path('event/', views.event_folder_list, name='event_folder_list'),  # list of event folders
    path('events/<int:event_id>/filters/', views.event_filters, name='event_filters'),  # filters per event
    path('create-event/', views.create_event, name='create_event'),  # create new event
    path('event/<int:event_id>/upload-filter/', views.upload_filter, name='upload_filter'),  # upload filter to event
    # 🧭 Routes for editing and deleting users (admin-only)
    path('users/<int:user_id>/update_role/', views.update_role, name='update_role'),  # 🧭 Route for updating user role
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),  # ✏️ Edit user info
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),  # 🗑️ Confirm and delete user
    # 🧭 Routes for editing and deleting events(admin/senior access)
    path('events/edit/<int:event_id>/', edit_event, name='edit_event'), # ✏️ edit an existing event
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'), # ✏️ deleting an existing event
    # 🗑️ Route to delete a filter (admin/senior only)
    path('filters/delete/<int:filter_id>/', delete_filter, name='delete_filter'),
    # 📬 Route to view all forgot password requests (admin-only)
    path('forgot-password-requests/', user_views.view_forgot_password_requests, name='view_forgot_password_requests'),
    path('forgot-password-requests/<int:request_id>/handled/', user_views.mark_forgot_password_handled, name='mark_forgot_password_handled'),
    # ⏱️ Clockify Integration Dashboard
    path('clockify/', views.ClockifyReportsView, name = 'clockify_reports'),  # Clockify integration URLs
    path('clockify/', include('clockify_integration.urls')),  # Clockify integration URLs

    # 📝 Editors Log URLs
    path('', include('editors_log.urls')),
]