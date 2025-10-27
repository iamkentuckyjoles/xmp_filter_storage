# dashboard/forms.py

from django import forms  # Django form utilities
from users.models import CustomUser  # Custom user model (if used elsewhere)
from django.contrib.auth import get_user_model  # Dynamic user model retrieval
from event.models import Event, Filter  # Importing related models

User = get_user_model()  # Ensures compatibility with custom user models

# 🔐 Admin-only form for creating users with hashed passwords
class AdminUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Secure password input

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']  # Include role for access control

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password before saving
        if commit:
            user.save()
        return user

# 📁 Form for creating or editing Event instances
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'year']  # Basic event metadata

# 🧩 Form for uploading named filter files (.xmp) with duplicate-check logic per event
class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['file']  # File field for filter uploads

#
class FilterUploadForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['name', 'file']  # Adjust based on your Filter model


# 🧩 Form for editing user details (admin-only)
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # 🔧 Editable fields only

# 🔧 Form for updating user role (admin-only access)
class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']  # 🎯 Only expose the role field for editing
        widgets = {
            'role': forms.Select(choices=[
                ('admin', 'Admin'),
                ('senior', 'Senior'),
                ('junior', 'Junior'),
            ])  # 📋 Dropdown for selecting role
        }
