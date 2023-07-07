from django.db import models
from base import constants
from base.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_image_size
from django.core.validators import validate_image_file_extension
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from admin_account.models import CustomAdminUser
from django.utils.timesince import timesince
from django.utils import timezone


# Create your models here.

nigeria = constants.NIGERIA
kenya = constants.KENYA
uganda = constants.UGANDA
COUNTRY_CHOICES = (
        ('Nigeria', nigeria),
        ('Kenya', kenya),
        ('uganda', uganda)
    )

class ExpertCard(BaseModel):
    first_name=models.CharField(max_length=225)
    middle_name = models.CharField(max_length=225, null=True, blank=True)
    last_name= models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='media', validators=[validate_image_size, validate_image_file_extension])
    role = models.CharField(max_length=100, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_code', null=True, blank=True)
    tribe = models.CharField(max_length=100, null=True, blank=True)
    company_address = models.ForeignKey('CompanyAddress', on_delete=models.SET_NULL, null=True, blank=False)
    city = models.CharField(max_length=225)
    country = models.CharField(max_length=30,choices=COUNTRY_CHOICES)
    phone_number = PhoneNumberField(null=True, blank=True)
    

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
        return f" {timesince(self.action_time, timezone.now())} ago"





