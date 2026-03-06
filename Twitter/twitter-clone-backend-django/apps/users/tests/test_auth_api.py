from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class AuthApiTests(APITestCase):
    def test_register_creates_user(self):
        url = "/api/v1/auth/register/"
        payload = {
            "email": "user1@example.com",
            "username": "user1",
            "password": "strong-pass-123",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=payload["email"]).exists())

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(
            email="dupe@example.com",
            username="dupe1",
            password="strong-pass-123",
        )

        response = self.client.post(
            "/api/v1/auth/register/",
            {
                "email": "dupe@example.com",
                "username": "dupe2",
                "password": "strong-pass-456",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_rejects_duplicate_username(self):
        User.objects.create_user(
            email="dupeuser1@example.com",
            username="dupeuser",
            password="strong-pass-123",
        )

        response = self.client.post(
            "/api/v1/auth/register/",
            {
                "email": "dupeuser2@example.com",
                "username": "dupeuser",
                "password": "strong-pass-456",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_token_and_me_flow(self):
        user = User.objects.create_user(
            email="user2@example.com",
            username="user2",
            password="strong-pass-456",
        )

        token_url = "/api/v1/auth/token/"
        token_payload = {"email": user.email, "password": "strong-pass-456"}
        token_response = self.client.post(token_url, token_payload, format="json")

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        access = token_response.data.get("access")
        self.assertTrue(access)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        me_url = "/api/v1/auth/me/"
        me_response = self.client.get(me_url)

        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data.get("email"), user.email)

    def test_token_rejects_wrong_password(self):
        user = User.objects.create_user(
            email="wrongpass@example.com",
            username="wrongpass",
            password="strong-pass-123",
        )

        token_url = "/api/v1/auth/token/"
        response = self.client.post(
            token_url,
            {"email": user.email, "password": "bad-pass"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        detail = str(response.data.get("detail", ""))
        self.assertIn("credentials", detail.lower())
