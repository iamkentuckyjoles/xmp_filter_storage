from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # Add this import
from dashboard.utils import admin_or_senior_required
from dashboard.form_modules.event_forms import EventForm
from event.models import Event



# Edit event (admin/senior only)
@admin_or_senior_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, f'Event "{event.name}" was successfully updated.')
        return redirect('dashboard:event_folder_list')
    return render(request, 'dashboard/events/edit_event.html', {'form': form, 'event': event})


# Delete event (admin/senior only)
@admin_or_senior_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event_name = event.name  # Store name before deletion
        event.delete()
        messages.success(request, f'Event "{event_name}" was successfully deleted.')
        return redirect('dashboard:event_folder_list')

    # Render confirmation page before deletion
    return render(request, 'dashboard/events/confirm_delete.html', {'event': event})

