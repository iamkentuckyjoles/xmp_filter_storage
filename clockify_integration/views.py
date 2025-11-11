from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import sync_clockify_workspaces, sync_clockify_users, sync_clockify_projects, sync_clockify_time_entries 
from .serializers import ClockifyWorkspaceSerializer, ClockifyUserSerializer, ClockifyProjectSerializer, ClockifyTimeEntrySerializer
from django.utils import timezone

class ClockifyWorkspaceListAPIView(APIView):
    """
    Fetch workspaces from Clockify API, save/update in DB, and return name/timezone list.
    """
    def get(self, request):
        api_key = settings.CLOCKIFY_API_KEY
        if not api_key:
            return Response({"error": "API key is required in settings."}, status=status.HTTP_400_BAD_REQUEST)

        workspaces = sync_clockify_workspaces()

        if isinstance(workspaces, dict) and workspaces.get("error"):
            return Response(workspaces, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ClockifyWorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ClockifyAllUsersAPIView(APIView):
    """
    Fetch users from all Clockify workspaces, save/update them in DB, and return list.
    """
    def get(self, request):
        users = sync_clockify_users()

        if isinstance(users, dict) and users.get("error"):
            return Response(users, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Custom serializer response to include workspace name
        data = [
            {
                "workspace": u.workspace.name if u.workspace else None,
                "user_id": u.user_id,
                "name": u.name,
                "email": u.email,
                
            }
            for u in users
        ]

        return Response(data, status=status.HTTP_200_OK)

class ClockifyProjectsListAPIView(APIView):
    """
    Fetch projects from all Clockify workspaces, save/update them in DB, and return list.
    """
    def get(self, request):
        projects = sync_clockify_projects()

        if isinstance(projects, dict) and projects.get("error"):
            return Response(projects, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serialize manually since each project has workspace info
        data = [
            {
                "workspace": p.workspace.name if p.workspace else None,
                "project_id": p.project_id,
                "name": p.name,
                
            }
            for p in projects
        ]

        return Response(data, status=status.HTTP_200_OK)
    
class ClockifyTimeEntriesAPIView(APIView):
    def get(self, request):
        entries = sorted(sync_clockify_time_entries(), key=lambda e: e.id, reverse=True)

        if isinstance(entries, dict) and entries.get("error"):
            return Response(entries, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = []
        for e in entries:
            # Localize and format start/end times
            start = e.start.astimezone(timezone.get_current_timezone()).strftime("%b %d, %Y %I:%M %p") if e.start else None
            end = e.end.astimezone(timezone.get_current_timezone()).strftime("%b %d, %Y %I:%M %p") if e.end else None

            data.append({
                "id": e.time_entry_id,
                "user": e.user.name if e.user else None,
                "project": e.project.name if e.project else None,
                "description": e.description,
                "start": start,
                "end": end,
                "duration": e.duration,
            })

        return Response(data, status=status.HTTP_200_OK)
    
