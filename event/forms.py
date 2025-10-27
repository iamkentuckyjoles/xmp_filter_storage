from django import forms

# 🔎 Form for searching events by name or year or both with two boxes
class EventSearchForm(forms.Form):
    name = forms.CharField(required=False, label="Event Name")
    year = forms.IntegerField(required=False, label="Year")