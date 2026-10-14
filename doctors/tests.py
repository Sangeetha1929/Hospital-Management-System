
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Doctor


class DoctorTests(TestCase):

    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="Test Doctor",
            specialization="General Medicine",
            department="general",
            phone="9876543210",
            email="doctor@example.com",
            experience_years=5,
        )

        self.staff = User.objects.create_user(
            username="doctorstaff",
            password="SafeStaffPass123!"
        )
        self.staff.profile.user_type = "staff"
        self.staff.profile.save()

        self.patient = User.objects.create_user(
            username="doctorpatient",
            password="SafePatientPass123!"
        )

    def test_doctor_list_loads(self):
        response = self.client.get(reverse("doctor_list"))
        self.assertEqual(response.status_code, 200)

    def test_doctor_detail_loads(self):
        response = self.client.get(
            reverse("doctor_detail", args=[self.doctor.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_doctor_create_redirects_when_logged_out(self):
        response = self.client.get(reverse("doctor_create"))
        self.assertEqual(response.status_code, 302)

    def test_patient_cannot_create_doctor(self):
        self.client.login(
            username="doctorpatient",
            password="SafePatientPass123!"
        )
        response = self.client.get(reverse("doctor_create"))
        self.assertEqual(response.status_code, 302)

    def test_staff_can_open_doctor_create_page(self):
        self.client.login(
            username="doctorstaff",
            password="SafeStaffPass123!"
        )
        response = self.client.get(reverse("doctor_create"))
        self.assertEqual(response.status_code, 200)
