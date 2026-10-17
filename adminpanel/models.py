from django.conf import settings
from django.db import models


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Registered'),
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('book', 'Booked'),
        ('confirm', 'Confirmed'),
        ('complete', 'Completed'),
        ('cancel', 'Cancelled'),
        ('reject', 'Rejected'),
        ('role', 'Role Changed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    category = models.CharField(max_length=30)          # e.g. Doctor, Appointment
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Activity log'
        verbose_name_plural = 'Activity logs'

    def __str__(self):
        return f'[{self.created_at:%Y-%m-%d %H:%M}] {self.user} {self.action} {self.category}'

    @property
    def actor(self):
        if not self.user:
            return 'System'
        return self.user.get_full_name() or self.user.username
