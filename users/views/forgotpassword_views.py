from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import ForgotPasswordRequest

def forgot_password(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        message = request.POST.get('message')

        ForgotPasswordRequest.objects.create(
            name=name,
            email=email,
            role=role,
            message=message,
        )

        messages.success(request, 'Your request has been submitted successfully. Please check your email within the day. Thank you!')
        return redirect('users:forgot_password')  # Redirects to login page

    return render(request, 'user/forgot_password.html')
