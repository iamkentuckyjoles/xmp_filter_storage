# users/views/admin_views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



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

        # ✅ Send email notification automatically
        subject = "Your Account Password Has Been Reset"
        message = (
            f"Hi {user.username},\n\n"
            f"Your account password has been reset by the admin.\n\n"
            f"Here are your new login credentials:\n"
            f"Username: {user.username}\n"
            f"Password: {new_password}\n\n"
            f"Regards,\nSIF Admin"
        )

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Make sure this is set in settings.py
                [user.email],
                fail_silently=False,
            )
            messages.success(request, f"Password for {user.username} has been reset and sent via email.")
        except Exception as e:
            messages.warning(request, f"Password updated, but failed to send email: {e}")

        return redirect('dashboard:view_forgot_password_requests')

    return render(request, 'dashboard/users/admin_change_password.html', {'user': user})
