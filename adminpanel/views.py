from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from appointments.models import Appointment
from core.views import is_admin
from doctors.models import Doctor
from patients.models import Patient
from .models import ActivityLog
from .utils import log_activity


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    stats = {
        'users': User.objects.count(),
        'staff': User.objects.filter(profile__user_type='staff').count(),
        'patients': Patient.objects.count(),
        'doctors': Doctor.objects.count(),
        'appointments': Appointment.objects.count(),
        'pending': Appointment.objects.filter(status='pending').count(),
    }
    recent_appointments = (
        Appointment.objects
        .select_related('patient__user', 'doctor')
        .order_by('-created_at')[:8]
    )
    recent_activities = ActivityLog.objects.select_related('user')[:8]
    return render(request, 'adminpanel/dashboard.html', {
        'stats': stats,
        'recent_appointments': recent_appointments,
        'recent_activities': recent_activities,
    })


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_activity_list(request):
    activities = ActivityLog.objects.select_related('user')
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    action = request.GET.get('action', '')
    if query:
        activities = activities.filter(
            Q(description__icontains=query)
            | Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
        )
    if category:
        activities = activities.filter(category=category)
    if action:
        activities = activities.filter(action=action)
    categories = (
        ActivityLog.objects.exclude(category='')
        .values_list('category', flat=True)
        .distinct()
        .order_by('category')
    )
    return render(request, 'adminpanel/activity_list.html', {
        'activities': activities,
        'query': query,
        'category_filter': category,
        'action_filter': action,
        'categories': categories,
        'action_choices': ActivityLog.ACTION_CHOICES,
    })


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_user_list(request):
    users = User.objects.select_related('profile').order_by('-date_joined')
    query = request.GET.get('q', '')
    role = request.GET.get('role', '')
    if query:
        users = users.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
    if role in ('patient', 'staff'):
        users = users.filter(profile__user_type=role)
    return render(request, 'adminpanel/user_list.html', {
        'users': users,
        'query': query,
        'role_filter': role,
    })


@login_required
@user_passes_test(is_admin, login_url='admin_login')
@require_POST
def admin_user_toggle_admin(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target == request.user:
        messages.error(request, 'You cannot change your own admin access.')
        return redirect('admin_user_list')
    target.is_superuser = not target.is_superuser
    target.is_staff = target.is_superuser
    target.save()
    state = 'granted' if target.is_superuser else 'revoked'
    log_activity(
        request.user, 'role', 'User',
        f'Admin access {state} for {target.username}.',
    )
    messages.success(request, f'Admin access {state} for {target.username}.')
    return redirect('admin_user_list')


@login_required
@user_passes_test(is_admin, login_url='admin_login')
def admin_user_delete(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_user_list')
    if target.is_superuser:
        messages.error(request, 'Admin accounts cannot be deleted from here. Revoke admin access first.')
        return redirect('admin_user_list')
    if request.method == 'POST':
        target.delete()
        log_activity(request.user, 'delete', 'User', f'Deleted user {target.username}.')
        messages.success(request, 'User deleted successfully.')
        return redirect('admin_user_list')
    return render(request, 'adminpanel/user_confirm_delete.html', {'target_user': target})
