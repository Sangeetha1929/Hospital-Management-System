
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from patients.models import Patient
from .models import Profile


class CoreTests(TestCase):

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_registration_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_new_user_gets_profile(self):
        user = User.objects.create_user(
            username="testpatient",
            password="TestPass123!"
        )
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_registration_creates_patient(self):
        response = self.client.post(reverse("register"), {
            "username": "newpatient",
            "first_name": "Test",
            "last_name": "Patient",
            "email": "newpatient@example.com",
            "phone": "9876543210",
            "password1": "SafeTestPass123!",
            "password2": "SafeTestPass123!",
        })

        self.assertTrue(
            User.objects.filter(username="newpatient").exists()
        )
        self.assertTrue(
            Patient.objects.filter(user__username="newpatient").exists()
        )
