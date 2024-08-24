from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import App
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class AppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='TestPassword123')
        self.client.login(username='testuser', password='TestPassword123')
        self.create_app_url = reverse('apps:new-app')
        self.update_app_url = lambda slug: reverse('apps:update', args=[slug])
        self.run_test_url = lambda app_id: reverse('apps:run_appium_test', args=[app_id])
        self.delete_app_url = lambda slug: reverse('apps:delete', args=[slug])

        # Define the path to the sample APK file
        self.apk_path = os.path.join('media', 'test', 'sample.apk')

        # Ensure the file exists before running the tests
        self.assertTrue(os.path.exists(self.apk_path), f"APK file does not exist at {self.apk_path}")

    def test_create_app(self):
        with open(self.apk_path, 'rb') as apk_file:
            apk_file_mock = SimpleUploadedFile(apk_file.name, apk_file.read(), content_type='application/vnd.android.package-archive')
            response = self.client.post(self.create_app_url, {
                'name': 'Test App',
                'apk_file_path': apk_file_mock,
            })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(App.objects.filter(name='Test App').exists())

    def test_update_app(self):
        with open(self.apk_path, 'rb') as apk_file:
            apk_file_mock = SimpleUploadedFile(apk_file.name, apk_file.read(), content_type='application/vnd.android.package-archive')
            self.client.post(self.create_app_url, {
                'name': 'Test App',
                'apk_file_path': apk_file_mock,
            })

        app = App.objects.get(name='Test App')
        update_url = self.update_app_url(app.slug)

        with open(self.apk_path, 'rb') as new_apk_file:
            new_apk_file_mock = SimpleUploadedFile(new_apk_file.name, new_apk_file.read(), content_type='application/vnd.android.package-archive')
            response = self.client.post(update_url, {
                'name': 'Updated Test App',
                'apk_file_path': new_apk_file_mock,
            })

        self.assertEqual(response.status_code, 302)
        app.refresh_from_db()
        self.assertEqual(app.name, 'Updated Test App')

    def test_run_appium_test(self):
        with open(self.apk_path, 'rb') as apk_file:
            apk_file_mock = SimpleUploadedFile(apk_file.name, apk_file.read(), content_type='application/vnd.android.package-archive')
            self.client.post(self.create_app_url, {
                'name': 'Test App',
                'apk_file_path': apk_file_mock,
            })

        app = App.objects.get(name='Test App')
        response = self.client.post(self.run_test_url(app.id))

        self.assertEqual(response.status_code, 302)
        app.refresh_from_db()
        self.assertIsNotNone(app.first_screen_screenshot_path)
        self.assertIsNotNone(app.second_screen_screenshot_path)
        self.assertIsNotNone(app.video_recording_path)
        self.assertIsNotNone(app.ui_hierarchy)
        self.assertIsNotNone(app.screen_changed)

    def test_delete_app(self):
        """
        Test deleting an app.
        """
        # Create the app
        with open(self.apk_path, 'rb') as apk_file:
            apk_file_mock = SimpleUploadedFile(apk_file.name, apk_file.read(), content_type='application/vnd.android.package-archive')
            self.client.post(self.create_app_url, {
                'name': 'Test App',
                'apk_file_path': apk_file_mock,
            })

        app = App.objects.get(name='Test App')
        delete_url = self.delete_app_url(app.slug)

        # Simulate deleting the app
        response = self.client.post(delete_url)

        # Check if the response indicates a redirect after deleting the app
        self.assertEqual(response.status_code, 302)

        # Verify that the app has been deleted
        self.assertFalse(App.objects.filter(name='Test App').exists())