# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import EditorLog
from .forms import EditorLogForm
from django.core.paginator import Paginator  

@login_required
def editor_log_list(request):
    user = request.user
    role = getattr(user, 'role', None)

    if role == 'admin':
        logs = EditorLog.objects.all()
    elif role == 'senior':
        logs = EditorLog.objects.filter(user__role='senior')
    elif role == 'junior':
        logs = EditorLog.objects.filter(user__role='junior')
    else:
        logs = EditorLog.objects.filter(user=user)

    # Date filtering: If 'filter_date' is provided (e.g., '2023-10-15'), filter by year, month, date
    filter_date = request.GET.get('filter_date')
    if filter_date:
        try:
            year, month, date = map(int, filter_date.split('-'))
            logs = logs.filter(year=year, month=month, date=date)
        except ValueError:
            pass  # Ignore invalid dates

    # Order by recency: newest first (adjust if you have a 'created_at' field)
    logs = logs.order_by('-year', '-month', '-date', '-id')  # '-id' ensures stable ordering for same dates

    # Paginate: 25 logs per page
    paginator = Paginator(logs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Group the paginated logs by day (for display)
    grouped_logs = {}
    for log in page_obj.object_list:  # Use the current page's logs
        day_key = f"{log.year}-{log.month:02d}-{log.date:02d}"
        grouped_logs.setdefault(day_key, []).append(log)

    # Pass both page_obj (for pagination) and grouped_logs (for display), plus filter_date for form prepopulation
    context = {
        'grouped_logs': grouped_logs,
        'page_obj': page_obj,
        'filter_date': filter_date,  # To prepopulate the form
    }
    return render(request, 'dashboard/editors_log/log_list.html', context)

@login_required
def add_editor_log(request):
    if request.method == 'POST':
        form = EditorLogForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('dashboard:editor_log_list')
    else:
        form = EditorLogForm()
    return render(request, 'dashboard/editors_log/add_log.html', {'form': form})


@login_required
def edit_editor_log(request, pk):
    log = get_object_or_404(EditorLog, pk=pk)
    # Only allow edit by the user who inputted the data
    if request.user != log.user:
        return redirect('dashboard:editor_log_list')

    # Prepopulate the date picker
    initial = {'date_field': f"{log.year}-{log.month:02d}-{log.date:02d}"}
    if request.method == 'POST':
        form = EditorLogForm(request.POST, instance=log, initial=initial)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('dashboard:editor_log_list')
    else:
        form = EditorLogForm(instance=log, initial=initial)

    return render(request, 'dashboard/editors_log/edit_log.html', {'form': form, 'log': log})
