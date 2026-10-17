from .models import ActivityLog


def log_activity(user, action, category, description):
    """Record an action performed on the site for the admin activity feed."""
    if user is not None and not getattr(user, 'is_authenticated', False):
        user = None
    return ActivityLog.objects.create(
        user=user,
        action=action,
        category=category,
        description=description,
    )
