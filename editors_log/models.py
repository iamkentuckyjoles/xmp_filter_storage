from django.db import models
from django.conf import settings
from django.utils import timezone

class EditorLog(models.Model):
    # User information (linked to your CustomUser model)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='editor_logs'
    )
    
    # Date information
    year = models.PositiveIntegerField(default=timezone.now().year)
    month = models.PositiveIntegerField(default=timezone.now().month)
    date = models.PositiveIntegerField(help_text="Day of month (1-31)")  # This replaces "day 1", "day 2"
    
    # Event information
    event = models.CharField(max_length=255)
    clip = models.IntegerField(default=0)
    teamedit = models.IntegerField(default=0)
    indiedit = models.IntegerField(default=0)
    build = models.IntegerField(default=0)
    
    # Duration (stored as time)
    duration = models.TimeField()
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', '-month', '-date']
        unique_together = ['user', 'year', 'month', 'date',]
    
    def __str__(self):
        return f"{self.user.username} - {self.year}/{self.month}/{self.date}"
    
    def get_duration_24h(self):
        """Return duration in 24-hour format as string"""
        if self.duration:
            return self.duration.strftime('%H:%M:%S')
        return ''
    
    @property
    def user_role(self):
        """Convenience method to get user role"""
        return self.user.role
    
    @property
    def username(self):
        """Convenience method to get username"""
        return self.user.username