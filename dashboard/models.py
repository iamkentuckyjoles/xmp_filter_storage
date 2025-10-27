from django.db import models  # Django model base
from event.models import Event, Filter  # Importing related models from event app
from django.shortcuts import render, get_object_or_404  # For rendering templates and safe object retrieval

# View function to display filters associated with a specific event
def event_filters(request, event_id):
    event = Event.objects.get(id=event_id)  # Fetch the event by ID
    filters = event.filters.all()  # Retrieve all filters linked to the event
    return render(request, 'dashboard/event_filters.html', {
        'event': event,
        'filters': filters
    })  # Render the template with event and its filters