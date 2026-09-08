from uuid import uuid4

from django.urls import reverse

from rest_framework.test import APITestCase

from .models import User
from .services import user_create


class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
        self.me_url = reverse('user-me')
        self.verify_email_url = reverse('user-verify-email')

        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'full_name': 'test user',
            'password': 'qwerty123',
        }


    def test_register_success(self):
        response = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()

        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])


    def test_register_duplicate_email(self):
        user_create(
            full_name='test user',
            email='test@example.com',
            username='testuser1',
            password='qwerty123'
        )

        response = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )

        self.assertEqual(response.status_code, 400)


    def test_register_duplicate_username(self):
        user_create(
            full_name='test user',
            email='test1@example.com',
            username='testuser',
            password='qwerty123'
        )

        response = self.client.post(
            self.register_url,
            self.user_data,
            format='json'
        )

        self.assertEqual(response.status_code, 400)


    def test_login_success(self):
        user_create(
            full_name='test user',
            email='test@example.com',
            username='testuser',
            password='qwerty123'
        )

        response = self.client.post(
            self.login_url,
            {
                'username': 'testuser',
                'password': 'qwerty123',
            },
            format='json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])


    def test_access_protected_endpoint_with_valid_token(self):
        user_create(
            full_name='test user',
            email='test@example.com',
            username='testuser',
            password='qwerty123'
        )

        login_response = self.client.post(
            self.login_url,
            {
                'username': 'testuser',
                'password': 'qwerty123',
            },
            format='json'
        )

        access_token = login_response.data['data']['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, 200)


    def test_access_protected_endpoint_with_invalid_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer asdasdasd'
        )

        response = self.client.get(self.me_url)

        self.assertEqual(
            response.status_code,
            401
        )


    def test_verify_email_success(self):
        user = user_create(
            full_name='test user',
            email='test@example.com',
            username='testuser',
            password='qwerty123'
        )

        response = self.client.get(
            self.verify_email_url,
            {
                'token': str(user.verification_token)
            }
        )

        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()

        self.assertTrue(user.is_verified)


    def test_verify_email_invalid_token(self):
        response = self.client.get(
            self.verify_email_url,
            {
                'token': str(uuid4())
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )
