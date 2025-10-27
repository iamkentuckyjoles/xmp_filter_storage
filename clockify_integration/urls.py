# clockify_app/urls.py
from django.urls import path
from . import views

app_name = 'clockify_integration'

urlpatterns = [
    path('sync/', views.SyncDataView.as_view(), name='sync_data'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('refresh-data/', views.RefreshDataView.as_view(), name='refresh_data'),
    path('test-api/', views.TestAPIView.as_view(), name='test_api'),
]