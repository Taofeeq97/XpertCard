from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from base.manager import UserManager
from card.validators import ValidateimageSize


# Create your models here.

class CustomAdminUser(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, verbose_name='Email Address')
    profile_picture = models.ImageField(upload_to='media', validators=[ ValidateimageSize], blank=True, null=True)
    is_trusted = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=100, null=True, blank=True)
    encoded_user_data = models.CharField(max_length=100, null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        indexes = [ models.Index(fields=['email'])]
       

    def __str__(self):
        return self.email


