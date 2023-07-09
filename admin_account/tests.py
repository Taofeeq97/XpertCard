
from django.test import TestCase, Client


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        # Prepare the data for the login request
        data = {
            'email': 'hbusari@afexnigeria.com',
            'password': 'admin12345',
        }
        print(data)
        # Send the login request
        response = self.client.post('http://127.0.0.1:8000/api/account/login/', data)
        print(response)

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'token')

        # Assert the response data
        response_data = response.json()
        self.assertEqual(response_data['email'], 'admin@afexnigeria.com')
        self.assertIn('token', response_data)