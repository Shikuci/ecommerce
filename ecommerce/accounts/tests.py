from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Account


class AccountAuthenticationTests(TestCase):
    def test_registration_creates_user_and_profile(self):
        response = self.client.post(reverse("register"), {
            "username": "labuser", "first_name": "Lab", "last_name": "User",
            "email": "lab@example.com", "phone_number": "001234567",
            "password1": "Strong-pass-927!", "password2": "Strong-pass-927!",
        })
        self.assertRedirects(response, reverse("signin"))
        user = get_user_model().objects.get(username="labuser")
        self.assertTrue(Account.objects.filter(user=user, phone_number="001234567").exists())

    def test_signin_with_email_and_logout(self):
        user = get_user_model().objects.create_user(
            username="labuser", email="lab@example.com", password="Strong-pass-927!"
        )
        response = self.client.post(reverse("signin"), {
            "email": user.email, "password": "Strong-pass-927!",
        })
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("signin"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_invalid_login_displays_error(self):
        response = self.client.post(reverse("signin"), {
            "email": "nobody@example.com", "password": "wrong",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email/username or password.")


class ProfileEditTests(TestCase):
    def test_profile_fields_can_be_updated(self):
        user = get_user_model().objects.create_user(username="profileuser", email="old@example.com", password="Strong-pass-927!")
        Account.objects.create(user=user, phone_number="123")
        self.client.force_login(user)
        response = self.client.post(reverse("profile"), {"first_name": "New", "last_name": "Name", "email": "new@example.com", "phone_number": "987654"})
        self.assertRedirects(response, reverse("profile"))
        user.refresh_from_db()
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.account.phone_number, "987654")


class PhoneLoginTests(TestCase):
    def test_signin_with_phone_number(self):
        user = get_user_model().objects.create_user(username="phoneuser", email="phone@example.com", password="Strong-pass-927!")
        Account.objects.create(user=user, phone_number="5550102")
        response = self.client.post(reverse("signin"), {"email": "5550102", "password": "Strong-pass-927!"})
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_profile_defaults_to_read_only_then_edit_form(self):
        user = get_user_model().objects.create_user(username="readuser", password="Strong-pass-927!")
        Account.objects.create(user=user, phone_number="555")
        self.client.force_login(user)
        response = self.client.get(reverse("profile"))
        self.assertContains(response, "Edit profile")
        self.assertNotContains(response, "Save changes")
        response = self.client.get(reverse("profile") + "?edit=1")
        self.assertContains(response, "Save changes")
