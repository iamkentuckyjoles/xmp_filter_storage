from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages  # Add this import
from dashboard.utils import admin_or_senior_required
from event.models import Filter


# 🗑️ Delete filter (admin/senior only)
@admin_or_senior_required
def delete_filter(request, filter_id):
    filter_obj = get_object_or_404(Filter, id=filter_id)

    if request.method == 'POST':
        filter_name = filter_obj.name  # Store name before deletion
        event_id = filter_obj.event.id  # Store event_id before deletion
        filter_obj.delete()
        messages.success(request, f'Filter "{filter_name}" was successfully deleted.')
        return redirect('dashboard:event_filters', event_id=event_id)

    return render(request, 'dashboard/filters/delete_filter.html', {'filter': filter_obj})

