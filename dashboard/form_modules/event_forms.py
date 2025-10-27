from django import forms  # Django form utilities
from event.models import Event  # Event model

# 📁 Form for editing Event name and year (admin/senior only)
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'year']  # Basic event metadata

    def clean_name(self):
        name = self.cleaned_data['name']
        if Event.objects.exclude(id=self.instance.id).filter(name=name).exists():
            raise forms.ValidationError("Event name must be unique.")
        return name

    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 2000 or year > 2100:
            raise forms.ValidationError("Year must be between 2000 and 2100.")
        return year