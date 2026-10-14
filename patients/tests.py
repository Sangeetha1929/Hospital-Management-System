
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from core.models import Profile
from .models import Patient


class PatientTests(TestCase):

    def setUp(self):
        self.staff = User.objects.create_user(
            username="stafftest",
            password="SafeStaffPass123!"
        )
        self.staff.profile.user_type = "staff"
        self.staff.profile.save()

        self.patient_user = User.objects.create_user(
            username="patienttest",
            password="SafePatientPass123!"
        )
        self.patient = Patient.objects.create(user=self.patient_user)

    def test_patient_list_redirects_when_logged_out(self):
        response = self.client.get(reverse("patient_list"))
        self.assertEqual(response.status_code, 302)

    def test_patient_detail_redirects_when_logged_out(self):
        response = self.client.get(
            reverse("patient_detail", args=[self.patient.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_staff_can_view_patient_list(self):
        self.client.login(username="stafftest", password="SafeStaffPass123!")
        response = self.client.get(reverse("patient_list"))
        self.assertEqual(response.status_code, 200)

    def test_patient_cannot_view_staff_patient_list(self):
        self.client.login(
            username="patienttest",
            password="SafePatientPass123!"
        )
        response = self.client.get(reverse("patient_list"))
        self.assertEqual(response.status_code, 302)

    def test_patient_delete_requires_login(self):
        response = self.client.get(
            reverse("patient_delete", args=[self.patient.pk])
        )
        self.assertEqual(response.status_code, 302)
