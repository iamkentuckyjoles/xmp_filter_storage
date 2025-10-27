# users/views/admin_views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from django.contrib import messages


# Helper: Only allow users with role='admin'
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_change_user_password(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if user.role not in ['senior', 'junior']:
        messages.error(request, "Password reset is only allowed for senior and junior users.")
        return redirect('dashboard:user_list')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        messages.success(request, f"Password for {user.username} has been successfully reset.")
        return redirect('dashboard:view_users_by_role', role=user.role)

    return render(request, 'dashboard/users/admin_change_password.html', {'user': user})

