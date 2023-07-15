from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import CustomAdminUser


class CreateAccountAPITest(APITestCase):
    def setUp(self):
        self.create_account_url = reverse('create_account')
        self.valid_payload = {
            'first_name': 'John',
            'middle_name': 'Doe',
            'last_name': 'Smith',
            'email': 'testemail@afexnigeria.com',
            'username': 'testemail@afexnigeria.com',
            'password': 'test1234',
            'confirm_password':'test1234',
        }
    
    def test_create_account_success(self):
        response = self.client.post(self.create_account_url, data=self.valid_payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomAdminUser.objects.count(), 1)
        self.assertEqual(CustomAdminUser.objects.first().email, 'testemail@afexnigeria.com')


