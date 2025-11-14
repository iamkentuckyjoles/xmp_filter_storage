from django.urls import path
from . import views

urlpatterns = [
    path('editors-log/', views.editor_log_list, name='editor_log_list'),
    path('editors-log/add/', views.add_editor_log, name='add_editor_log'),
    path('editors-log/<int:pk>/edit/', views.edit_editor_log, name='edit_editor_log'),
    path('editors-log/<int:user_id>/', views.user_editor_logs, name='user_editor_logs'),

]
