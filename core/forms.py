from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile
from patients.models import Patient


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'e.g. john_doe'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = user.profile
            profile.phone = self.cleaned_data['phone']
            profile.user_type = 'patient'      # always patient
            profile.save()
            Patient.objects.get_or_create(user=user)
        return user
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['phone', 'address']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        qs = User.objects.filter(email__iexact=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile


class AdminAuthenticationForm(AuthenticationForm):
    """Login form for the admin login page: superusers only."""

    error_messages = {
        **AuthenticationForm.error_messages,
        'not_admin': 'Access denied. Only administrators can log in here.',
    }

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_superuser:
            raise ValidationError(
                self.error_messages['not_admin'],
                code='not_admin',
            )


class StaffExcludedAuthenticationForm(AuthenticationForm):
    """Login form for the normal login page: patients and doctors only.

    Administrators (Django superusers/staff) must use the dedicated
    Admin Login page instead.
    """

    error_messages = {
        **AuthenticationForm.error_messages,
        'not_allowed': (
            'Access denied. Administrators must log in through the '
            'Admin Login page. Only patients and doctors can log in here.'
        ),
    }

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.is_superuser or user.is_staff:
            raise ValidationError(
                self.error_messages['not_allowed'],
                code='not_allowed',
            )