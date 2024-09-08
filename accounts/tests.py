from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()



User = get_user_model()


class UserAuthTests(APITestCase):
    def setUp(self):
        self.url = reverse('user_auth')  # Use the name of your URL pattern
        self.user_email = 'existing@example.com'
        self.inactive_user_email = 'inactive@example.com'
        
        # Create an active user
        self.active_user = User.objects.create_user(email=self.user_email, password='password123', is_active=True)
        
        # Create an inactive user
        self.inactive_user = User.objects.create_user(email=self.inactive_user_email, password='password123', is_active=False)

    def test_successful_login_with_existing_active_user(self):
        """Test a successful login with an existing active user."""
        data = {'email': self.user_email, 'password': 'password123'}
        with patch('accounts.views.generate_otp', return_value='123456'):
            response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('code', response.data)
        self.assertEqual(response.data['message'], 'authentication successfull')

    def test_attempt_login_with_inactive_user(self):
        """Test login with an inactive user."""
        data = {'email': self.inactive_user_email, 'password': 'password123'}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'user is not active')

    def test_login_with_nonexistent_user(self):
        """Test login with a non-existent user (new user creation)."""
        new_user_email = 'newuser@example.com'
        data = {'email': new_user_email, 'password': 'password123'}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('code', response.data)

        # Check if user was created
        self.assertTrue(User.objects.filter(email=new_user_email).exists())

    def test_invalid_request_data(self):
        """Test with invalid request data."""
        data = {'email': ''}  # Invalid data
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_post_method(self):
        """Test with a non-POST method."""
        response = self.client.get(self.url)  # Use GET instead of POST
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)



class OTPVerificationTests(APITestCase):
    def setUp(self):
        self.url = reverse('otp_verification')  # Use the name of your URL pattern
        self.valid_otp_data = {
            'email': 'user@example.com',
            'otp': '123456'
        }
        self.invalid_otp_data = {
            'email': 'user@example.com',
            'otp': '654321'
        }

    @patch('accounts.serializers.OTPVerifySerializer.verify_otp')
    def test_successful_otp_verification(self, mock_verify_otp):
        """Test successful OTP verification."""
        mock_verify_otp.return_value = {'message': 'OTP verified successfully'}
        
        response = self.client.post(self.url, self.valid_otp_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP verified successfully')

    # @patch('accounts.serializers.OTPVerifySerializer.verify_otp')
    # def test_failed_otp_verification(self, mock_verify_otp):
    #     """Test failed OTP verification due to invalid OTP."""
    #     # mock_verify_otp.side_effect = ValueError('Invalid OTP')
        
    #     response = self.client.post(self.url, self.invalid_otp_data)
        
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_request_data(self):
        """Test OTP verification with invalid request data."""
        invalid_data = {'email': ''}  # Missing OTP field
        
        response = self.client.post(self.url, invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('otp', response.data)

    def test_non_post_method(self):
        """Test OTP verification with a non-POST method."""
        response = self.client.get(self.url)  # Use GET instead of POST
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)










class TeamsViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('teams_view')  # Use the name of your URL pattern
        self.user = User.objects.create_user(email='user@example.com', password='password123')
        self.team_data = {'name': 'New Team'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(AccessToken.for_user(self.user)))

    # def test_successful_team_creation(self):
    #     """Test a successful team creation when the user is authenticated and eligible."""
    #     response = self.client.post(self.url, self.team_data)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'success')
    #     self.assertTrue(Teams.objects.filter(slug='new-team').exists())
    #     self.user.refresh_from_db()
    #     self.assertEqual(self.user.teams, 1)

    def test_team_already_exists(self):
        """Test team creation failure when a team with the same name already exists."""
        Teams.objects.create(name='New Team', slug='new-team')  # Pre-create a team with the same slug
        response = self.client.post(self.url, self.team_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'team with this name already exists')

    def test_user_exceeds_team_limit(self):
        """Test team creation failure when the user is already part of two teams."""
        self.user.teams = 2
        self.user.save()

        response = self.client.post(self.url, self.team_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "you can't be in more than two teams")

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the endpoint."""
        self.client.credentials()  # Remove authentication
        response = self.client.post(self.url, self.team_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_non_post_method(self):
        """Test accessing the endpoint with a non-POST method."""
        response = self.client.get(self.url)  # Use GET instead of POST

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method "GET" not allowed.')