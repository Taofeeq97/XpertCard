# Django imports
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import FileExtensionValidator
from django.utils.timesince import timesince
from django.utils import timezone
from rest_framework.serializers import ValidationError

# Third-party imports
from phonenumber_field.modelfields import PhoneNumberField

# Local imports
from base import constants
from base.models import BaseModel
from .validators import ValidateimageSize
from admin_account.models import CustomAdminUser

# Create your models here.

nigeria = constants.NIGERIA
kenya = constants.KENYA
uganda = constants.UGANDA
landscape1 =constants.LANDSCAPE1
landscape2 = constants.LANDSCAPE2
portrait1 = constants.PORTRAIT1
portrait2 = constants.PORTRAIT2


COUNTRY_CHOICES = (
        ('Nigeria', nigeria),
        ('Kenya', kenya),
        ('uganda', uganda)
    )


CARD_TYPE_CHOICES = (
        ('Landscape1', landscape1),
        ('Landscape2', landscape2),
        ('Portrait1', portrait1),
        ('Portrait2', portrait2)
    )

class ExpertCard(BaseModel):
    first_name = models.CharField(max_length=225)
    middle_name = models.CharField(max_length=225, null=True, blank=True)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='media', validators=[ValidateimageSize])
    role = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_code', null=True, blank=True)
    tribe = models.CharField(max_length=100)
    card_vcf = models.FileField(null=True,blank=True, validators=[FileExtensionValidator(allowed_extensions=['vcf']),], upload_to='media')
    company_address = models.ForeignKey('CompanyAddress', on_delete=models.SET_NULL, null=True)
    address_title = models.CharField(max_length=255, blank=True, null=True)
    card_type = models.CharField(max_length=100, choices=CARD_TYPE_CHOICES, null=True, blank=True)
    phone_number = PhoneNumberField()

    def clean(self):
        super().clean()
        if self.pk:  # Check if the instance already exists (updating)
            old_instance = ExpertCard.objects.get(pk=self.pk)
            if self.email != old_instance.email:  # Check if the email is being updated
                email_exists = ExpertCard.objects.filter(email=self.email).exists()
                if email_exists:
                    raise ValidationError("Email already exists.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Run clean() method before saving
        super().save(*args, **kwargs)


    class Meta:
        indexes = [ models.Index(fields=['email'])]
        
    def __str__(self) -> str:
        return f"{self.email}'s Expert Card"


class CompanyAddress(BaseModel):
    address_title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    company_address  = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=30)
    latitude = models.CharField(max_length=15)
    longitude = models.CharField(max_length=15)

    def __str__(self) -> str:
        return f"{self.address_title}'s address"
    

CREATE, READ, UPDATE, DELETE = 'Create','Read', 'Update', 'Delete'
LOGIN, LOGOUT, LOGIN_FAILED = 'Login', 'Logout', 'Login Failed'

ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]


class ActivityLog(models.Model):
    actor = models.ForeignKey(CustomAdminUser, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    data = models.JSONField(default=dict, blank=True,null=True)

    # for generic relations
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    class Meta:
        ordering = ['-id']
    
    def __str__(self) -> str:
        return f"{self.action_type}, {self.content_type}, by {self.actor} on {self.action_time}"
    
    def time_since(self):
        time_difference = timezone.now() - self.action_time
        if time_difference.total_seconds() < 60:
            return "now"
        elif time_difference.total_seconds() < 3600:  # Less than 1 hour (60 minutes)
            return f"{int(time_difference.total_seconds() / 60)} minutes ago"
        elif time_difference.total_seconds() < 86400:  # Less than 1 day (24 hours)
            hours = int(time_difference.total_seconds() / 3600)
            if hours == 1:
                return "1 hour ago"
            else:
                return f"{hours} hours ago"
        else:
            days = int(time_difference.total_seconds() / 86400)
            if days == 1:
                return "1 day ago"
            else:
                return f"{days} days ago"




