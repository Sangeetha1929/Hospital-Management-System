from django.contrib.auth.models import User
from django.db import models


class Doctor(models.Model):
    DEPARTMENTS = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('pediatrics', 'Pediatrics'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('general', 'General Medicine'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doctor',
    )
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENTS, default='general')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    experience_years = models.PositiveIntegerField(default=0)
    availability = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
