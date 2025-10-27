from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
from django.db import models

from .models import Workspace, ClockifyUser, Project, TimeEntry
from .services.clockify_api import ClockifyAPI
from django.conf import settings

class SyncDataView(View):
    def get(self, request):
        # Initialize API
        api = ClockifyAPI(settings.CLOCKIFY_API_KEY)
        
        # Sync workspaces
        workspaces_data = api.get_workspaces()
        for workspace_data in workspaces_data:
            Workspace.objects.update_or_create(
                workspace_id=workspace_data['id'],
                defaults={'name': workspace_data['name']}
            )
        
        # Sync users and projects for each workspace
        for workspace in Workspace.objects.all():
            users_data = api.get_users(workspace.workspace_id)
            for user_data in users_data:
                ClockifyUser.objects.update_or_create(
                    user_id=user_data['id'],
                    defaults={
                        'name': user_data['name'],
                        'email': user_data['email'],
                        'workspace': workspace
                    }
                )
            
            projects_data = api.get_projects(workspace.workspace_id)
            for project_data in projects_data:
                # Map project names to types
                project_type = 'PRODUCTION'  # default
                project_name = project_data['name'].lower()
                
                if 'photo' in project_name or 'editing' in project_name:
                    project_type = 'PHOTO_EDITING'
                elif 'clip' in project_name:
                    project_type = 'CLIPPING'
                elif 'build' in project_name:
                    project_type = 'BUILDING'
                
                Project.objects.update_or_create(
                    project_id=project_data['id'],
                    defaults={
                        'name': project_data['name'],
                        'workspace': workspace,
                        'project_type': project_type
                    }
                )
        
        return redirect('clockify_integration:reports')

class ReportsView(View):
    def get(self, request):
        # Get filter parameters
        period = request.GET.get('period', 'week')
        search_query = request.GET.get('search', '')
        project_type = request.GET.get('project_type', '')
        
        # Calculate date range based on period
        end_date = timezone.now()
        if period == 'day':
            start_date = end_date - timedelta(days=1)
        elif period == 'week':
            start_date = end_date - timedelta(weeks=1)
        elif period == 'month':
            start_date = end_date - relativedelta(months=1)
        else:
            start_date = end_date - timedelta(weeks=1)  # default to week
        
        # Get time entries based on filters
        time_entries = TimeEntry.objects.filter(
            start_time__gte=start_date,
            end_time__lte=end_date
        )
        
        # Apply search filter
        if search_query:
            time_entries = time_entries.filter(
                models.Q(user__name__icontains=search_query) |
                models.Q(description__icontains=search_query)
            )
        
        # Apply project type filter
        if project_type:
            time_entries = time_entries.filter(project__project_type=project_type)
        
        # Group data for display
        report_data = []
        for entry in time_entries:
            report_data.append({
                'user_name': entry.user.name,
                'user_email': entry.user.email,
                'workspace': entry.user.workspace.name,
                'project': entry.project.name,
                'project_type': entry.project.get_project_type_display(),
                'description': entry.description,
                'duration': entry.duration,
                'start_time': entry.start_time,
                'end_time': entry.end_time
            })
        
        context = {
            'report_data': report_data,
            'period': period,
            'search_query': search_query,
            'project_type': project_type,
            'project_types': dict(Project.PROJECT_TYPES)
        }
        
        return render(request, 'dashboard/clockify_reports.html', context)

class RefreshDataView(View):
    def post(self, request):
        api = ClockifyAPI(settings.CLOCKIFY_API_KEY)
        
        # Get the date range from the request or use default
        date_range_start = timezone.now() - timedelta(weeks=4)
        date_range_end = timezone.now()
        
        # For each workspace, get detailed report
        for workspace in Workspace.objects.all():
            report_data = api.get_detailed_report(
                workspace.workspace_id, 
                date_range_start, 
                date_range_end
            )
            
            # Process and save time entries
            for entry_data in report_data.get('timeentries', []):
                user, _ = ClockifyUser.objects.get_or_create(
                    user_id=entry_data['userId'],
                    defaults={
                        'name': entry_data.get('userName', 'Unknown'),
                        'email': '',  # You might need to get this elsewhere
                        'workspace': workspace
                    }
                )
                
                project, _ = Project.objects.get_or_create(
                    project_id=entry_data.get('projectId', ''),
                    defaults={
                        'name': entry_data.get('projectName', 'Unknown'),
                        'workspace': workspace,
                        'project_type': 'PRODUCTION'
                    }
                )
                
                # Parse time data
                start_time = datetime.fromisoformat(entry_data['timeInterval']['start'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(entry_data['timeInterval']['end'].replace('Z', '+00:00')) if entry_data['timeInterval']['end'] else None
                
                duration_seconds = entry_data['timeInterval']['duration'] or 0
                duration = timedelta(seconds=int(duration_seconds))
                
                TimeEntry.objects.update_or_create(
                    time_entry_id=entry_data['id'],
                    defaults={
                        'user': user,
                        'project': project,
                        'description': entry_data.get('description', ''),
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': duration,
                        'billable': entry_data.get('billable', False)
                    }
                )
        
        return JsonResponse({'status': 'success'})
    

# Add this to your views.py
class TestAPIView(View):
    def get(self, request):
        api = ClockifyAPI(settings.CLOCKIFY_API_KEY)
        
        # Test workspaces
        workspaces = api.get_workspaces()
        
        # Test users for first workspace
        if workspaces:
            users = api.get_users(workspaces[0]['id'])
            
        return JsonResponse({
            'workspaces_count': len(workspaces),
            'users_count': len(users) if workspaces else 0,
            'workspaces': workspaces,
            'users': users if workspaces else []
        })