from django.db import models

class Workspace(models.Model):
    workspace_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class ClockifyUser(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    PROJECT_TYPES = [
        ('PHOTO_EDITING', 'Photo Editing'),
        ('CLIPPING', 'Clipping'),
        ('BUILDING', 'Building'),
        ('PRODUCTION', 'Production'),
    ]
    
    project_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    
    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    time_entry_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(ClockifyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    billable = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.name} - {self.description}"