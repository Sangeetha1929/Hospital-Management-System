from django import forms
from django.contrib.auth.models import User
from .models import Doctor


class DoctorForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.order_by('username'),
        required=False,
        label='Linked user account',
        help_text='Optional. Link a login account so this doctor can manage their appointments.',
    )

    class Meta:
        model = Doctor
        fields = ['user', 'name', 'specialization', 'department', 'phone', 'email',
                  'experience_years', 'availability', 'bio']
        widgets = {
            'availability': forms.TextInput(attrs={'placeholder': 'e.g. Mon-Fri 9AM-5PM'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
