from django.test import TestCase
from .models import CompanyAddress
from django.utils.text import slugify
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response

class CompanyAddressModelTest(TestCase):
    def setUp(self):
        
        self.address_1 = CompanyAddress.objects.create(
            address_title='Company Address 1',
            slug='company-address-1',
            company_address='123 Main St',
            city='Ibadan',
            country='Nigeria',
            latitude='12.345 N',
            longitude='67.890 W',
        )
        self.assertEqual(Response.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyAddress.objects.count(), 1)

        self.address_2 = CompanyAddress.objects.create(
            address_title='Company Address 2',
            slug='company-address-2',
            company_address='456 Main St',
            city='Abuja',
            country='Nigeria',
            latitude='12.345 W',
            longitude='67.890 E',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyAddress.objects.count(), 2)

    def test_str_representation(self):
        self.assertEqual(
            str(self.address_1),
            "Company Address 1's address"
        )
        self.assertEqual(
            str(self.address_2),
            "Company Address 2's address"
        )

    def test_unique_slug(self):
        slug_1 = slugify(self.address_1.address_title)
        slug_2 = slugify(self.address_2.address_title)
        self.assertEqual(
            self.address_1.slug,
            slug_1
        )
        self.assertEqual(
            self.address_2.slug,
            slug_2
        )
        self.assertNotEqual(
            self.address_1.slug,
            self.address_2.slug
        )
