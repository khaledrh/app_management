from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# class UserRegistrationTest(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.register_url = reverse('users:register')  # Update this with your actual URL name for registration

#     def test_register_new_user(self):
#         """
#         Test registering a new user successfully.
#         """
#         response = self.client.post(self.register_url, {
#             'username': 'testuser',
#             'email': 'testuser@example.com',
#             'password1': 'TestPassword123',
#             'password2': 'TestPassword123'
#         })

#         # Check if the response indicates a redirect, which is typical after a successful registration
#         self.assertEqual(response.status_code, 302)
#         # Check if the user has been created in the database
#         self.assertTrue(User.objects.filter(username='testuser').exists())

#     def test_register_user_with_mismatched_passwords(self):
#         """
#         Test registering a user with mismatched passwords.
#         """
#         response = self.client.post(self.register_url, {
#             'username': 'testuser2',
#             'email': 'testuser2@example.com',
#             'password1': 'TestPassword123',
#             'password2': 'DifferentPassword123'
#         })

#         # Check if the response indicates a failure (e.g., form is not valid)
#         self.assertEqual(response.status_code, 200)
#         # Check that the user was not created
#         self.assertFalse(User.objects.filter(username='testuser2').exists())

#     def test_register_user_with_existing_username(self):
#         """
#         Test registering a user with a username that already exists.
#         """
#         User.objects.create_user(username='testuser', email='testuser@example.com', password='TestPassword123')

#         response = self.client.post(self.register_url, {
#             'username': 'testuser',  # Same username as above
#             'email': 'newemail@example.com',
#             'password1': 'TestPassword123',
#             'password2': 'TestPassword123'
#         })

#         # Check if the response indicates a failure
#         self.assertEqual(response.status_code, 200)
#         # Ensure no new user was created with the duplicate username
#         self.assertEqual(User.objects.filter(username='testuser').count(), 1)

# class UserAuthenticationTest(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.login_url = reverse('users:login')  # Update this with your actual URL name for login
#         self.logout_url = reverse('users:logout')  # Update this with your actual URL name for logout
#         # Create a test user
#         self.user = User.objects.create_user(username='testuser', password='TestPassword123')

#     def test_login_user(self):
#         """
#         Test logging in a user with correct credentials.
#         """
#         response = self.client.post(self.login_url, {
#             'username': 'testuser',
#             'password': 'TestPassword123'
#         })

#         # Check if the response indicates a redirect after successful login
#         self.assertEqual(response.status_code, 302)
#         # Check if the user is authenticated
#         self.assertTrue(response.wsgi_request.user.is_authenticated)

#     def test_login_user_with_wrong_credentials(self):
#         """
#         Test logging in a user with incorrect credentials.
#         """
#         response = self.client.post(self.login_url, {
#             'username': 'testuser',
#             'password': 'WrongPassword123'
#         })

#         # Check if the response indicates failure (e.g., re-rendering the login form)
#         self.assertEqual(response.status_code, 200)
#         # Check if the user is not authenticated
#         self.assertFalse(response.wsgi_request.user.is_authenticated)

#     def test_logout_user(self):
#         """
#         Test logging out a user.
#         """
#         # First, log the user in
#         self.client.login(username='testuser', password='TestPassword123')

#         # Then, log the user out
#         response = self.client.post(self.logout_url)

#         # Check if the response indicates a redirect after logout
#         self.assertEqual(response.status_code, 302)
#         # Check if the user is no longer authenticated
#         self.assertFalse(response.wsgi_request.user.is_authenticated)

# class UserManagementTest(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.login_url = reverse('users:login')
#         self.change_password_url = reverse('users:change_password')
#         self.delete_account_url = reverse('users:delete_account')

#         # Create a test user
#         self.user = User.objects.create_user(username='testuser', password='TestPassword123')

#     def test_change_password(self):
#         """
#         Test changing the user's password.
#         """
#         # Log in the user first
#         self.client.login(username='testuser', password='TestPassword123')

#         # Change the password
#         response = self.client.post(self.change_password_url, {
#             'old_password': 'TestPassword123',
#             'new_password1': 'NewTestPassword123',
#             'new_password2': 'NewTestPassword123'
#         })

#         # Check if the response indicates a redirect after password change
#         self.assertEqual(response.status_code, 302)

#         # Log out the user
#         self.client.logout()

#         # Attempt to log in with the old password (should fail)
#         login_old_password = self.client.login(username='testuser', password='TestPassword123')
#         self.assertFalse(login_old_password)

#         # Attempt to log in with the new password (should succeed)
#         login_new_password = self.client.login(username='testuser', password='NewTestPassword123')
#         self.assertTrue(login_new_password)

#     def test_delete_account(self):
#         """
#         Test deleting the user's account.
#         """
#         # Log in the user first
#         self.client.login(username='testuser', password='TestPassword123')

#         # Delete the account
#         response = self.client.post(self.delete_account_url)

#         # Check if the response indicates a redirect after account deletion
#         self.assertEqual(response.status_code, 302)

#         # Check if the user is no longer in the database
#         self.assertFalse(User.objects.filter(username='testuser').exists())

#         # Attempt to log in (should fail)
#         login_attempt = self.client.login(username='testuser', password='TestPassword123')
#         self.assertFalse(login_attempt)