from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # Add this import
from dashboard.forms import UserEditForm, RoleUpdateForm
from django.contrib.auth import get_user_model
from dashboard.utils import admin_required
from django.contrib.auth.decorators import login_required, user_passes_test
from dashboard.utils import is_admin
from users.models import ForgotPasswordRequest  

User = get_user_model()

# 🔄 View to update a user's role (admin-only)
@admin_required
def update_role(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = RoleUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Role for user "{user.username}" was successfully updated.')
            return redirect('dashboard:view_users_by_role', role=user.role)
    else:
        form = RoleUpdateForm(instance=user)

    return render(request, 'dashboard/users/update_role.html', {
        'form': form,
        'user': user
    })

# ✏️ Edit user info (admin-only)
@admin_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = UserEditForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        messages.success(request, f'User "{user.username}" was successfully updated.')
        return redirect('dashboard:view_users_by_role', role=user.role)

    return render(request, 'dashboard/users/edit_user.html', {'form': form, 'user': user})

# 🗑️ Delete user (admin-only)
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = user.username  # Store username before deletion
        role = user.role  # Store role before deletion
        user.delete()
        messages.success(request, f'User "{username}" was successfully deleted.')
        return redirect('dashboard:view_users_by_role', role=role)

    return render(request, 'dashboard/users/delete_user.html', {'user': user})


# 📬 View all forgot password requests (admin-only)
@admin_required
def view_forgot_password_requests(request):
    requests = ForgotPasswordRequest.objects.all().order_by('-created_at')
    return render(request, 'dashboard/forgot_password_request.html', {'requests': requests})


# ✅ Mark a forgot password request as handled (admin-only)
@admin_required
def mark_forgot_password_handled(request, request_id):
    req = get_object_or_404(ForgotPasswordRequest, id=request_id)
    req.status = 'Handled'
    req.save()
    messages.success(request, f'Request from {req.name} marked as handled.')
    return redirect('dashboard:view_forgot_password_requests')