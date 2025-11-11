from django.shortcuts import render
from clockify_integration.models import ClockifyWorkspace, ClockifyUsers, ClockifyProjects, ClockifyTimeEntry
from dashboard.utils import admin_required
from django.contrib.auth import get_user_model

User = get_user_model()


@admin_required
def ClockifyReportsView(request):

     # Fetch all time entries with related user, project, and workspace
    entries = ClockifyTimeEntry.objects.select_related(
        'user', 'project', 'user__workspace', 'project__workspace', 'updated_at'
    ).order_by('-updated_at')

    context = {
        'entries': entries
    }
    return render(request, 'dashboard/clockify/clockify_reports.html', context)