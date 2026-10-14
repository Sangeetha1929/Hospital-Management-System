
from datetime import date, time, timedelta

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from core.models import Profile
from patients.models import Patient
from doctors.models import Doctor
from .models import Appointment


class AppointmentTests(TestCase):

    def setUp(self):
        self.patient_user = User.objects.create_user(
            username="apptpatient",
            password="SafePatientPass123!"
        )
        self.patient = Patient.objects.create(user=self.patient_user)

        self.staff = User.objects.create_user(
            username="apptstaff",
            password="SafeStaffPass123!"
        )
        self.staff.profile.user_type = "staff"
        self.staff.profile.save()

        self.other_user = User.objects.create_user(
            username="otherpatient",
            password="SafeOtherPass123!"
        )
        self.other_patient = Patient.objects.create(user=self.other_user)

        self.doctor = Doctor.objects.create(
            name="Appointment Doctor",
            specialization="General Medicine",
            department="general",
            phone="9876543210",
            email="apptdoctor@example.com",
            experience_years=3,
        )

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=date.today() + timedelta(days=2),
            time=time(10, 30),
            reason="General checkup",
            status="pending",
        )

    def test_appointment_list_requires_login(self):
        response = self.client.get(reverse("appointment_list"))
        self.assertEqual(response.status_code, 302)

    def test_booking_page_requires_patient_login(self):
        response = self.client.get(reverse("appointment_create"))
        self.assertEqual(response.status_code, 302)

    def test_patient_can_open_booking_page(self):
        self.client.login(
            username="apptpatient",
            password="SafePatientPass123!"
        )
        response = self.client.get(reverse("appointment_create"))
        self.assertEqual(response.status_code, 200)

    def test_patient_can_view_own_appointments(self):
        self.client.login(
            username="apptpatient",
            password="SafePatientPass123!"
        )
        response = self.client.get(reverse("appointment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "General checkup")

    def test_staff_can_confirm_pending_appointment(self):
        self.client.login(
            username="apptstaff",
            password="SafeStaffPass123!"
        )
        response = self.client.post(
            reverse(
                "appointment_status",
                args=[self.appointment.pk, "confirmed"]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "confirmed")

    def test_patient_cannot_change_appointment_status(self):
        self.client.login(
            username="apptpatient",
            password="SafePatientPass123!"
        )
        response = self.client.post(
            reverse(
                "appointment_status",
                args=[self.appointment.pk, "confirmed"]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "pending")

    def test_patient_can_cancel_own_appointment(self):
        self.client.login(
            username="apptpatient",
            password="SafePatientPass123!"
        )
        response = self.client.post(
            reverse("appointment_cancel", args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "cancelled")

    def test_patient_cannot_cancel_another_patients_appointment(self):
        self.client.login(
            username="otherpatient",
            password="SafeOtherPass123!"
        )
        response = self.client.post(
            reverse("appointment_cancel", args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "pending")
