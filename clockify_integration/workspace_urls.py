from django.urls import path
from .views import (
    ClockifyWorkspaceListAPIView,
    ClockifyAllUsersAPIView,
    ClockifyProjectsListAPIView,
    ClockifyTimeEntriesAPIView,
)

urlpatterns = [
    path('', ClockifyWorkspaceListAPIView.as_view(), name='clockify_workspace_list'),
    path('users/', ClockifyAllUsersAPIView.as_view(), name='clockify_all_users'),
    path('projects/', ClockifyProjectsListAPIView.as_view(), name='clockify_projects_list'),
    path('time_entries/', ClockifyTimeEntriesAPIView.as_view(), name='clockify_time_entries'),
]