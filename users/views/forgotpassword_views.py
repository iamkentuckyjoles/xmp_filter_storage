import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import ForgotPasswordRequest

def forgot_password(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        verify = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = verify.json()

        if not result.get('success'):
            messages.error(request, 'reCAPTCHA verification failed. Please try again.')
            return redirect('users:forgot_password')

        # ✅ If passed reCAPTCHA, continue form logic
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
        return redirect('users:forgot_password')

    context = {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    }
    return render(request, 'user/forgot_password.html', context)
