from django.contrib import admin
from .models import Workspace, ClockifyUser, Project, TimeEntry

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace_id')
    search_fields = ('name',)

@admin.register(ClockifyUser)
class ClockifyUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'workspace')
    list_filter = ('workspace',)
    search_fields = ('name', 'email')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_type', 'workspace')
    list_filter = ('project_type', 'workspace')
    search_fields = ('name',)

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'description', 'start_time', 'duration')
    list_filter = ('project', 'start_time')
    search_fields = ('user__name', 'description')