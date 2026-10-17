from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from core.views import is_admin, is_patient
from adminpanel.utils import log_activity
from .models import Patient
from .forms import PatientForm


@login_required
@user_passes_test(is_patient, login_url='home')
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        patient = Patient.objects.create(user=request.user)
    appointments = patient.appointments.all()
    stats = {
        'total': appointments.count(),
        'upcoming': appointments.filter(
            status__in=['pending', 'confirmed'], date__gte=timezone.localdate()
        ).count(),
        'completed': appointments.filter(status='completed').count(),
    }
    return render(request, 'patients/patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
        'stats': stats,
    })


@login_required
@user_passes_test(is_patient, login_url='home')
def patient_update(request):
    try:
        patient = request.user.patient
    except Patient.DoesNotExist:
        patient = Patient.objects.create(user=request.user)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient, user=request.user)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            log_activity(
                request.user, 'update', 'Patient',
                f'{request.user.username} updated their profile.',
            )
            messages.success(request, 'Profile updated successfully.')
            return redirect('patient_dashboard')
    else:
        form = PatientForm(instance=patient, user=request.user)
        form.fields['first_name'].initial = request.user.first_name
        form.fields['last_name'].initial = request.user.last_name
        form.fields['email'].initial = request.user.email
    return render(request, 'patients/patient_form.html', {'form': form})


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def patient_list(request):
    patients = Patient.objects.all()
    query = request.GET.get('q', '')
    if query:
        patients = [p for p in patients if query.lower() in p.user.username.lower()
                    or query.lower() in (p.user.first_name + ' ' + p.user.last_name).lower().strip()]
    return render(request, 'patients/patient_list.html', {'patients': patients, 'query': query})


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.all()
    return render(request, 'patients/patient_detail.html', {'patient': patient, 'appointments': appointments})


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        user = patient.user
        username = user.username
        patient.delete()
        user.delete()
        log_activity(request.user, 'delete', 'Patient', f'Removed patient {username}.')
        messages.success(request, 'Patient removed successfully.')
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
