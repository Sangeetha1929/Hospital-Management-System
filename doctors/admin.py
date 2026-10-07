from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'department', 'phone', 'experience_years')
    search_fields = ('name', 'specialization', 'department')
    list_filter = ('department',)
