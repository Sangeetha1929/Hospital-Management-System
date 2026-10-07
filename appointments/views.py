from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from core.views import is_staff, is_patient
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
            messages.success(request, 'Appointment booked successfully.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form, 'title': 'Book Appointment'})


@login_required
def appointment_list(request):
    if is_staff(request.user):
        appointments = Appointment.objects.all()
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
    if not (is_staff(request.user) or (is_patient(request.user) and appointment.patient.user == request.user)):
        messages.error(request, 'You are not allowed to do that.')
        return redirect('appointment_list')
    if appointment.status in ('completed', 'cancelled'):
        messages.error(request, 'This appointment can no longer be cancelled.')
        return redirect('appointment_list')
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled.')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})


ALLOWED_TRANSITIONS = {
    'pending': {'confirmed'},
    'confirmed': {'completed'},
}


@login_required
@user_passes_test(is_staff, login_url='home')
@require_POST
def appointment_update_status(request, pk, status):
    appointment = get_object_or_404(Appointment, pk=pk)
    if status in ALLOWED_TRANSITIONS.get(appointment.status, set()):
        appointment.status = status
        appointment.save()
        messages.success(request, f'Appointment marked as {appointment.get_status_display()}.')
    else:
        messages.error(request, 'Invalid status change.')
    return redirect('appointment_list')