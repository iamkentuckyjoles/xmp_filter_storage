# users/views/auth_views.py

from django.contrib.auth import authenticate, login, logout  # 🔐 Auth system
from django.shortcuts import render, redirect                 # 🧭 Template rendering and redirects
from django.contrib import messages                          # 💬 Flash messages for feedback

# -------------------------------------------------------------------
# View: login_view
# Purpose: Authenticates user credentials and logs them in
# Behavior:
#   - On POST: attempts login and redirects to dashboard
#   - On GET: renders login form
# -------------------------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard:redirect')  # 🔁 Let dashboard_redirect handle role logic
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'user/login.html')  # ✅ Corrected template path

# -------------------------------------------------------------------
# View: logout_view
# Purpose: Logs out the current user and redirects to login page
# Behavior:
#   - Ends session
#   - Redirects to login page
# -------------------------------------------------------------------
def logout_view(request):
    logout(request)  # Terminate session
    messages.success(request, "You’ve been logged out.")  # Optional feedback

    return redirect('users:login')  #  Redirect to login page
