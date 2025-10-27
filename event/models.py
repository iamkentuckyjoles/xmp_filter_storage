from django.db import models  # Base class for Django models
import os  # File and folder operations
import shutil
from django.conf import settings  # Access project settings like MEDIA_ROOT
from django.core.exceptions import ValidationError  # Raise validation errors

# -------------------------------------------------------------------
# Model: Event
# Purpose: Represents an event folder with a unique name and year
# -------------------------------------------------------------------
class Event(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Folder name, must be unique
    year = models.PositiveIntegerField()  # For filtering, deletion, search
    created_at = models.DateTimeField(auto_now_add=True)  # Add timestamp for sorting
    updated_at = models.DateTimeField(auto_now=True)  # Track modifications

    class Meta:
        ordering = ['-year', 'name']  # Default ordering
        indexes = [
            models.Index(fields=['-year', 'name']),  # Optimize queries for pagination
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save to DB first

        # Create folder after saving (e.g., filters/Jomanji_Festival)
        folder_name = self.name.replace(" ", "_")
        folder_path = os.path.join(settings.MEDIA_ROOT, 'filters', folder_name)
        os.makedirs(folder_path, exist_ok=True)

    def delete(self, *args, **kwargs):
        # First delete the physical folder
        folder_name = self.name.replace(" ", "_")
        folder_path = os.path.join(settings.MEDIA_ROOT, 'filters', folder_name)
        
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Deleted folder: {folder_path}")
            except Exception as e:
                print(f"Error deleting folder: {e}")
        
        # Then delete the database record
        super().delete(*args, **kwargs)

# -------------------------------------------------------------------
# Function: filter_upload_path
# Purpose: Define dynamic upload path based on event name
# -------------------------------------------------------------------
def filter_upload_path(instance, filename):
    folder = instance.event.name.replace(" ", "_")  # Clean folder name
    return f"filters/{folder}/{filename}"  # e.g., filters/Jomanji_Festival/vintage.xmp


# -------------------------------------------------------------------
# Function: validate_filters_file
# Purpose: Restrict uploads to .xmp files only
# -------------------------------------------------------------------
def validate_filters_file(file):
    if not file.name.lower().endswith('.xmp'):
        raise ValidationError("Only .xmp extension files are allowed.")


# -------------------------------------------------------------------
# Model: Filter
# Purpose: Represents a filter file linked to a specific event
# -------------------------------------------------------------------
class Filter(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='filters')  # Link to event
    name = models.CharField(max_length=255)  # e.g., "vintage"
    file = models.FileField(
        upload_to=filter_upload_path,  # Dynamic path based on event
        validators=[validate_filters_file]  # Restrict to .xmp files
    )
    tags = models.CharField(max_length=255, blank=True)  # Optional tags for search/filtering

    class Meta:
        unique_together = ('event', 'name')  # ✅ Allows same filter name across different events

    def __str__(self):
        return f"{self.name} [{self.event.name}]"