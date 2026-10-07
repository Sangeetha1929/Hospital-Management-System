from django import forms
from .models import Patient
from django.contrib.auth.models import User

class PatientForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'blood_group', 'phone', 'address',
                  'emergency_contact', 'medical_notes']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'medical_notes': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        patient = super().save(commit=False)
        if commit:
            patient.save()
        return patient
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        qs = User.objects.filter(email__iexact=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email