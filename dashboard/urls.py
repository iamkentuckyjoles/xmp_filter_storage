from django.urls import path, include
from dashboard import views
from dashboard.view_modules.user_views import (
    edit_user, delete_user, update_role,
    view_forgot_password_requests, mark_forgot_password_handled
)
from dashboard.view_modules.event_views import edit_event, delete_event
from dashboard.view_modules.filter_views import delete_filter
from dashboard.view_modules.clockify_views import ClockifyReportsView
from .views import view_users_by_role

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_redirect, name='redirect'),

    path('dashboard/', include([
        path('', views.admin_home, name='admin_home'),
        path('senior/', views.senior_home, name='senior_home'),
        path('junior/', views.junior_home, name='junior_home'),
        path('default/', views.default_home, name='default_home'),
    ])),

    path('users/', include([
        path('', views.view_users, name='view_users'),
        path('create/', views.create_user, name='create_user'),
        path('role/<str:role>/', view_users_by_role, name='view_users_by_role'),
        path('<int:user_id>/update_role/', update_role, name='update_role'),
        path('edit/<int:user_id>/', edit_user, name='edit_user'),
        path('delete/<int:user_id>/', delete_user, name='delete_user'),
    ])),

    path('events/', include([
        path('', views.event_folder_list, name='event_folder_list'),
        path('create/', views.create_event, name='create_event'),
        path('<int:event_id>/filters/', views.event_filters, name='event_filters'),
        path('<int:event_id>/upload-filter/', views.upload_filter, name='upload_filter'),
        path('edit/<int:event_id>/', edit_event, name='edit_event'),
        path('delete/<int:event_id>/', delete_event, name='delete_event'),
    ])),

    path('filters/', include([
        path('delete/<int:filter_id>/', delete_filter, name='delete_filter'),
    ])),

    path('forgot-password-requests/', include([
        path('', view_forgot_password_requests, name='view_forgot_password_requests'),
        path('<int:request_id>/handled/', mark_forgot_password_handled, name='mark_forgot_password_handled'),
    ])),

    path('clockify/', include([
        path('', views.ClockifyReportsView, name='clockify_reports'),
        path('', include('clockify_integration.urls')),
    ])),

    path('', include('editors_log.urls')),
]
