from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from doctors.models import Doctor
from .forms import RegisterForm, ProfileForm


def is_staff(user):
    return hasattr(user, 'profile') and user.profile.user_type == 'staff'


def is_patient(user):
    return hasattr(user, 'profile') and user.profile.user_type == 'patient'


def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'home.html', {'doctors': doctors})


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

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
