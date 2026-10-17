from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from core.views import is_admin, is_patient, is_doctor
from adminpanel.utils import log_activity
from patients.models import Patient
from .models import Appointment
from .forms import AppointmentForm
from django.views.decorators.http import require_POST

@login_required
@user_passes_test(is_patient, login_url='login')
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            try:
                patient = request.user.patient
            except Patient.DoesNotExist:
                patient = Patient.objects.create(user=request.user)
            appointment.patient = patient
            appointment.save()
            log_activity(
                request.user, 'book', 'Appointment',
                f'{patient} booked an appointment with Dr. {appointment.doctor.name} on {appointment.date}.',
            )
            messages.success(request, 'Appointment booked successfully.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form, 'title': 'Book Appointment'})


@login_required
def appointment_list(request):
    if is_admin(request.user):
        appointments = Appointment.objects.all()
    elif is_doctor(request.user):
        appointments = request.user.doctor.appointments.all()
    else:
        try:
            patient = request.user.patient
            appointments = patient.appointments.all()
        except Patient.DoesNotExist:
            appointments = Appointment.objects.none()
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'status_filter': status_filter,
        'appointment_statuses': Appointment.STATUS_CHOICES,
    })


@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    doctor = getattr(request.user, 'doctor', None) if is_doctor(request.user) else None
    allowed = (
        is_admin(request.user)
        or (is_patient(request.user) and appointment.patient.user == request.user)
        or (doctor is not None and appointment.doctor == doctor)
    )
    if not allowed:
        messages.error(request, 'You are not allowed to do that.')
        return redirect('appointment_list')
    if appointment.status in ('completed', 'cancelled', 'rejected'):
        messages.error(request, 'This appointment can no longer be cancelled.')
        return redirect('appointment_list')
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        log_activity(
            request.user, 'cancel', 'Appointment',
            f'Cancelled appointment for {appointment.patient} with Dr. {appointment.doctor.name} on {appointment.date}.',
        )
        messages.success(request, 'Appointment cancelled.')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})


ALLOWED_TRANSITIONS = {
    'pending': {'confirmed', 'rejected'},
    'confirmed': {'completed', 'rejected'},
}

STATUS_ACTION = {
    'confirmed': 'confirm',
    'completed': 'complete',
    'rejected': 'reject',
}


@login_required
@require_POST
def appointment_update_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)
    doctor = getattr(request.user, 'doctor', None) if is_doctor(request.user) else None
    can_manage = is_admin(request.user) or (doctor is not None and appointment.doctor == doctor)
    if not can_manage:
        messages.error(request, 'You are not allowed to do that.')
        return redirect('appointment_list')
    if status in ALLOWED_TRANSITIONS.get(appointment.status, set()):
        appointment.status = status
        appointment.save()
        log_activity(
            request.user, STATUS_ACTION.get(status, 'update'), 'Appointment',
            f'{appointment.get_status_display()} appointment for {appointment.patient} with Dr. {appointment.doctor.name} on {appointment.date}.',
        )
        messages.success(request, f'Appointment marked as {appointment.get_status_display()}.')
    else:
        messages.error(request, 'Invalid status change.')
    if is_doctor(request.user):
        return redirect('doctor_dashboard')
    return redirect('appointment_list')