from rest_framework import serializers
from .models import ClockifyWorkspace, ClockifyUsers, ClockifyProjects, ClockifyTimeEntry

class ClockifyWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockifyWorkspace
        fields = ['workspace_id', 'name']

class ClockifyUserSerializer(serializers.ModelSerializer):
    workspace = serializers.CharField(source='workspace.name', read_only=True)
    class Meta:
        model = ClockifyUsers
        fields = ['workspace', 'user_id', 'name', 'email']

class ClockifyProjectSerializer(serializers.ModelSerializer):
    workspace = serializers.CharField(source='workspace.name', read_only=True)
    class Meta:
        model = ClockifyProjects
        fields = ['workspace', 'project_id', 'name']

class ClockifyTimeEntrySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    project = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ClockifyTimeEntry
        fields = ['time_entry_id', 'user', 'project', 'description', 'start', 'end', 'duration']