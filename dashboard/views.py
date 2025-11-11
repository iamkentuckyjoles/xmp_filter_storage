# dashboard/views.py
from django.db.models import Q  # for complex queries
from django.contrib import messages  # for flash messages
from django.shortcuts import render, redirect, get_object_or_404  # for rendering and redirects
from django.contrib.auth.decorators import login_required, user_passes_test  # for access control
from .forms import AdminUserCreationForm  # form for creating users
from event.models import Event, Filter  # models for events and filters
from dashboard.forms import EventForm  # form for creating events
from dashboard.forms import FilterForm  # form for uploading filters
from .forms import FilterUploadForm
from django.contrib.auth import get_user_model  # 🔄 Dynamically fetch the active user model (CustomUser)
from event.forms import EventSearchForm  # 🧾 Import search form from event app and handles search input from user
from django.db.models import Q  # 🔍 Enables complex OR-based query filtering
from dashboard.view_modules.user_views import edit_user, delete_user, update_role # Re-export modular views
from django.core.paginator import Paginator 
from clockify_integration.models import ClockifyWorkspace, ClockifyUsers, ClockifyProjects, ClockifyTimeEntry


User = get_user_model()  # 🎯 Reference the CustomUser model defined in the users app


# redirect user to role-specific dashboard
@login_required
def dashboard_redirect(request):
    role = getattr(request.user, 'role', None)
    if role == 'admin':
        return redirect('dashboard:admin_home')
    elif role == 'senior':
        return redirect('dashboard:senior_home')
    elif role == 'junior':
        return redirect('dashboard:junior_home')
    else:
        return redirect('dashboard:default_home')  # fallback


# admin dashboard view
@login_required
@user_passes_test(lambda u: u.role == 'admin')
def admin_home(request):
    return render(request, 'dashboard/admin_home.html')


# senior dashboard view
@login_required
@user_passes_test(lambda u: u.role == 'senior')
def senior_home(request):
    return render(request, 'dashboard/senior_home.html')


# junior dashboard view
@login_required
@user_passes_test(lambda u: u.role == 'junior')
def junior_home(request):
    return render(request, 'dashboard/junior_home.html')


# fallback dashboard view
@login_required
def default_home(request):
    return render(request, 'dashboard/default_home.html')


# check if user is admin
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


# view to create user (admin only)
@login_required
@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ User added successfully!')
            return redirect('dashboard:view_users')
    else:
        form = AdminUserCreationForm()
    return render(request, 'dashboard/create_user.html', {'form': form})

# Restrict access to logged-in admins only
@login_required
@user_passes_test(is_admin)
def view_users(request):
    users = User.objects.all().order_by('role', 'username')

    # 🧩 Define role-label pairs for template looping
    role_labels = [
        ('admin', 'Admins'),
        ('senior', 'Seniors'),
        ('junior', 'Juniors'),
    ]

    return render(request, 'dashboard/view_users.html', {
        'users': users,
        'role_labels': role_labels,
    })
# Role-based View 
@login_required
@user_passes_test(is_admin)
def view_users_by_role(request, role):
    search_query = request.GET.get('search_email', '')
    users = User.objects.filter(role=role).order_by('username' or 'email')
    
    # Apply search filter if query exists
    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) | 
            Q(username__icontains=search_query)
        )
    
    label_map = {
        'admin': 'Admins',
        'senior': 'Seniors',
        'junior': 'Juniors',
    }
    label = label_map.get(role, role.title())
    
    return render(request, 'dashboard/users_by_role.html', {
        'users': users,
        'role': role,
        'label': label,
        'search_query': search_query,  # Pass search query back to template
    })

# List all event folders with optional search
def event_folder_list(request):
    form = EventSearchForm(request.GET or None)
    events = Event.objects.all()

    # Filter logic
    if form.is_valid():
        name = form.cleaned_data.get('name')
        year = form.cleaned_data.get('year')

        if name:
            events = events.filter(name__icontains=name)
        if year:
            events = events.filter(year=year)

    # Autocomplete data
    name_list = Event.objects.values_list('name', flat=True).distinct()
    year_list = Event.objects.values_list('year', flat=True).distinct()

    # Pagination - Add these lines
    paginator = Paginator(events, 10)  # Show 10 events per page
    page_number = request.GET.get('page', 1)
    events_page = paginator.get_page(page_number)

    context = {
        'form': form,
        'events': events_page,  # Change this from events to events_page
        'name_list': name_list,
        'year_list': year_list,
    }
    return render(request, 'dashboard/event_folders.html', context)

# list filters for a specific event
def event_filters(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    filters = Filter.objects.filter(event=event)
    return render(request, 'dashboard/event_filters.html', {
        'event': event,
        'filters': filters
    })


# check if user is admin or senior
def is_admin_or_senior(user):
    return user.is_authenticated and user.role in ['admin', 'senior']


# view to create event (admin and senior)
@login_required
@user_passes_test(is_admin_or_senior)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('dashboard:event_filters', event.id)
    else:
        form = EventForm()
    return render(request, 'dashboard/create_event.html', {'form': form})


# view to upload filter (admin and senior)
@login_required
@user_passes_test(is_admin_or_senior)
def upload_filter(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = FilterUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Check for duplicate filter name for this event
            filter_name = form.cleaned_data['name']
            duplicate = Filter.objects.filter(event=event, name=filter_name).exists()

            if duplicate:
                form.add_error('name', f"A filter named '{filter_name}' already exists for this event.")
            else:
                new_filter = form.save(commit=False)
                new_filter.event = event
                new_filter.save()
                messages.success(request, f"✅ Filter '{filter_name}' uploaded successfully.")
                return redirect('dashboard:event_filters', event_id=event.id)

    else:
        form = FilterUploadForm()

    return render(request, 'dashboard/filters/upload_filter.html', {
        'form': form,
        'event': event
    })

#clockify
@user_passes_test(is_admin)
def ClockifyReportsView(request):

     # Fetch all time entries with related user, project, and workspace
    entries = ClockifyTimeEntry.objects.select_related(
        'user', 'project', 'user__workspace', 'project__workspace'
    ).all()

    context = {
        'entries': entries
    }
    return render(request, 'dashboard/clockify/clockify_reports.html', context)
