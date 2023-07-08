from rest_framework.validators import ValidationError
from django.utils.deconstruct import deconstructible



def ValidateimageSize(file_obj):
    if file_obj.size > 10000000:
        raise ValidationError("File exceeds Size limit")