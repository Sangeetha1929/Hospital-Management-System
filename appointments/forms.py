from django import forms
from doctors.models import Doctor
from .models import Appointment
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
    def clean(self):
        cleaned = super().clean()
        doctor = cleaned.get('doctor')
        date = cleaned.get('date')
        time = cleaned.get('time')

        if date and date < timezone.localdate():
            self.add_error('date', 'You cannot book an appointment in the past.')

        if doctor and date and time:
            taken = Appointment.objects.filter(
                doctor=doctor, date=date, time=time
            ).exclude(status='cancelled').exists()
            if taken:
                raise forms.ValidationError('This doctor is already booked at that time. Please choose another slot.')
        return cleaned