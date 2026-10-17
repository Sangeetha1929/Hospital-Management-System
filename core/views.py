from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse

from adminpanel.utils import log_activity
from doctors.models import Doctor
from .forms import (
    RegisterForm,
    ProfileForm,
    AdminAuthenticationForm,
    StaffExcludedAuthenticationForm,
)


def is_admin(user):
    return user.is_superuser


def is_doctor(user):
    return (
        not user.is_superuser
        and hasattr(user, 'profile') and user.profile.user_type == 'doctor'
        and hasattr(user, 'doctor')
    )


def is_patient(user):
    return (
        not user.is_superuser
        and hasattr(user, 'profile') and user.profile.user_type == 'patient'
    )


class RoleLoginView(LoginView):
    """Normal login page: only patients and doctors may sign in here."""

    template_name = 'login.html'
    authentication_form = StaffExcludedAuthenticationForm

    def get_success_url(self):
        user = self.request.user
        if is_doctor(user):
            return reverse('doctor_dashboard')
        if is_patient(user):
            return reverse('patient_dashboard')
        return reverse('home')


class AdminLoginView(LoginView):
    """Dedicated admin login: only Django superusers may sign in here."""

    template_name = 'admin_login.html'
    authentication_form = AdminAuthenticationForm

    def get_success_url(self):
        return reverse('admin_dashboard')


def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'home.html', {'doctors': doctors})


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            log_activity(
                user,
                'register',
                'Authentication',
                f'New account registered: {user.username}.',
            )

            messages.success(
                request,
                'Registration successful! Welcome to CityCare Hospital.'
            )

            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            instance=request.user.profile,
            user=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profile updated successfully.'
            )

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=request.user.profile,
            user=request.user
        )

    return render(request, 'profile.html', {'form': form})
