from django.test import TestCase
from django.utils.text import slugify
from .models import CompanyAddress, ExpertCard


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
        self.address_2 = CompanyAddress.objects.create(
            address_title='Company Address 2',
            slug='company-address-2',
            company_address='456 Main St',
            city='Abuja',
            country='Nigeria',
            latitude='12.345 W',
            longitude='67.890 E',
        )

        self.expertcard = ExpertCard.objects.create(
            first_name='taofeeq',
            last_name='otu',
            email='example@email.com',
            profile_pictue='',
            tribe='Innovation',
            company=self.address_1,
            card_type='Portrait1',
            phone_number='+2347066609555'
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.address_1),
            "Company Address 1's address"
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
