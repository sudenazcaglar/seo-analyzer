from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456", email="test@example.com")
        self.register_url = "/api/register/"
        self.token_url = "/api/token/"
        self.profile_url = "/api/profile/"

    def test_register_user(self):
        data = {
            "username": "newuser",
            "password": "testpass123",
            "email": "newuser@example.com"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_login_user(self):
        data = {"username": "testuser", "password": "123456"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_invalid_credentials(self):
        data = {"username": "wronguser", "password": "wrongpass"}
        response = self.client.post(self.token_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_access_with_token(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        response = self.client.get(self.profile_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_profile_access_without_token(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        