from django.urls import path, include
from . import views

urlpatterns = [
    path('workspaces/', include('clockify_integration.workspace_urls')),
]