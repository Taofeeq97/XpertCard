from django.test import TestCase, Client
from rest_framework.reverse import reverse
from .models import CustomAdminUser


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        number_of_users = 15

        for num in range(1, number_of_users + 1):
            data = {
                'first_name': 'jooo',
                'last_name': 'haay',
                'email': f'hbus{num}@afexnigeria.com',
                'password': 'admin12345',
            }
            CustomAdminUser.objects.create_user(**data)

    def test_login(self):
        # Prepare the data for the login request
        data = {
            'email': 'hbus@afexnigeria.com',
            'password': 'admin12345',
        }
        print(data)
        # Send the login request
        response = self.client.post(reverse('token_obtain_pair'), data)
        print(response.status_code)

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
