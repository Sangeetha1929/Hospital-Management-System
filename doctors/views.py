from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from core.views import is_admin, is_doctor
from adminpanel.utils import log_activity
from .models import Doctor
from .forms import DoctorForm


def _sync_doctor_role(doctor):
    if doctor.user_id:
        profile = doctor.user.profile
        if profile.user_type != 'doctor':
            profile.user_type = 'doctor'
            profile.save()


@login_required
@user_passes_test(is_doctor, login_url='login')
def doctor_dashboard(request):
    doctor = request.user.doctor
    appointments = (
        doctor.appointments
        .select_related('patient__user')
        .order_by('date', 'time')
    )
    stats = {
        'total': appointments.count(),
        'pending': appointments.filter(status='pending').count(),
        'confirmed': appointments.filter(status='confirmed').count(),
        'completed': appointments.filter(status='completed').count(),
    }
    return render(request, 'doctors/doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
        'stats': stats,
    })


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
@user_passes_test(is_admin, login_url='admin_login')
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            _sync_doctor_role(doctor)
            log_activity(request.user, 'create', 'Doctor', f'Added doctor Dr. {doctor.name}.')
            messages.success(request, 'Doctor added successfully.')
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Add Doctor'})


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            _sync_doctor_role(doctor)
            log_activity(request.user, 'update', 'Doctor', f'Updated doctor Dr. {doctor.name}.')
            messages.success(request, 'Doctor updated successfully.')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/doctor_form.html', {'form': form, 'doctor': doctor, 'title': 'Edit Doctor'})


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        name = doctor.name
        doctor.delete()
        log_activity(request.user, 'delete', 'Doctor', f'Deleted doctor Dr. {name}.')
        messages.success(request, 'Doctor deleted successfully.')
        return redirect('doctor_list')
    return render(request, 'doctors/doctor_confirm_delete.html', {'doctor': doctor})
