from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from core.views import is_staff
from .models import Doctor
from .forms import DoctorForm


def doctor_list(request):
    doctors = Doctor.objects.all()
    query = request.GET.get('q', '')
    if query:
        doctors = doctors.filter(name__icontains=query) | doctors.filter(specialization__icontains=query)
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors, 'query': query})


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})


@login_required
@user_passes_test(is_staff, login_url='home')
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully.')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Add Doctor'})


@login_required
@user_passes_test(is_staff, login_url='home')
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully.')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/doctor_form.html', {'form': form, 'doctor': doctor, 'title': 'Edit Doctor'})


@login_required
@user_passes_test(is_staff, login_url='home')
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, 'Doctor deleted successfully.')
        return redirect('doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})
