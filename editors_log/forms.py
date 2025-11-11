from django import forms
from .models import EditorLog
from django.utils import timezone
from django.core.validators import RegexValidator

class EditorLogForm(forms.ModelForm):
    date_field = forms.DateField(
        label="Select Date",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'border p-2 rounded-md w-full'
        }),
        initial=timezone.now
    )

    duration = forms.CharField(
        label="Duration (24-hours)",
        validators=[
            RegexValidator(
                regex=r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$',
                message="Enter time in 24-hour format (HH:MM:SS)"
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'HH:MM:SS',
            'class': 'border p-2 rounded-md w-full',
            'autocomplete': 'off',
            'pattern': '^(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d$',
            'title': '24-hour format: HH:MM:SS'
        }),
    )

    # Make these fields optional
    clip = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'border p-2 rounded-md w-full',
            'min': 0,
        })
    )
    
    teamedit = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'border p-2 rounded-md w-full',
            'min': 0,
        })
    )
    
    indiedit = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'border p-2 rounded-md w-full',
            'min': 0,
        })
    )
    
    build = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'border p-2 rounded-md w-full',
            'min': 0,
        })
    )

    class Meta:
        model = EditorLog
        fields = ['date_field', 'event', 'clip', 'teamedit', 'indiedit', 'build', 'duration', 'notes']
        widgets = {
            'event': forms.TextInput(attrs={
                'class': 'border p-2 rounded-md w-full',
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'border p-2 rounded-md w-full',
                'placeholder': 'Enter any additional notes...'
            }),
        }
        labels = {
            'teamedit': 'Team Edit',
            'indiedit': 'Independent Edit',
            'build': 'Build',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            try:
                initial_date = timezone.datetime(
                    year=self.instance.year,
                    month=self.instance.month,
                    day=self.instance.date
                ).date()
                self.fields['date_field'].initial = initial_date
            except (ValueError, TypeError):
                pass
            
            if self.instance.duration:
                self.fields['duration'].initial = self.instance.duration.strftime('%H:%M:%S')

    def clean_clip(self):
        """Convert empty clip value to 0"""
        return self.cleaned_data['clip'] or 0

    def clean_teamedit(self):
        """Convert empty teamedit value to 0"""
        return self.cleaned_data['teamedit'] or 0

    def clean_indiedit(self):
        """Convert empty indiedit value to 0"""
        return self.cleaned_data['indiedit'] or 0

    def clean_build(self):
        """Convert empty build value to 0"""
        return self.cleaned_data['build'] or 0

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        selected_date = self.cleaned_data['date_field']
        instance.year = selected_date.year
        instance.month = selected_date.month
        instance.date = selected_date.day
        
        duration_str = self.cleaned_data['duration']
        from datetime import datetime
        duration_obj = datetime.strptime(duration_str, '%H:%M:%S').time()
        instance.duration = duration_obj
        
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance