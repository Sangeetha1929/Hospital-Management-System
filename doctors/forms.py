from django import forms
from .models import Doctor


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'department', 'phone', 'email',
                  'experience_years', 'availability', 'bio']
        widgets = {
            'availability': forms.TextInput(attrs={'placeholder': 'e.g. Mon-Fri 9AM-5PM'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
