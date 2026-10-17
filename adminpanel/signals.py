from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

from .utils import log_activity


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    log_activity(user, 'login', 'Authentication', f'{user.get_full_name() or user.username} logged in.')


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if user:
        log_activity(user, 'logout', 'Authentication', f'{user.get_full_name() or user.username} logged out.')


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request=None, **kwargs):
    username = credentials.get('username', 'unknown')
    log_activity(None, 'login', 'Authentication', f'Failed login attempt for "{username}".')
