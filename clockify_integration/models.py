from django.db import models
from datetime import timedelta

class ClockifyWorkspace(models.Model):
    # use Clockify's workspace id (string) as the primary key
    workspace_id = models.CharField(max_length=255, primary_key=True )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} ({self.workspace_id})"
    
class ClockifyUsers(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    workspace = models.ForeignKey(
        ClockifyWorkspace,
        on_delete=models.CASCADE,
        related_name="users"  # makes it easy to access workspace.users.all()
    )

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"
    
class ClockifyProjects(models.Model):
    project_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200,)
    workspace = models.ForeignKey(
        ClockifyWorkspace,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"
    

class ClockifyTimeEntry(models.Model):
    time_entry_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey("ClockifyUsers", on_delete=models.CASCADE)
    project = models.ForeignKey("ClockifyProjects", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    # These match the Clockify timeInterval structure
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.name} - {self.description or 'No Description'}"

    class Meta:
        verbose_name = "Time Entry"
        verbose_name_plural = "Time Entries"
