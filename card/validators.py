from rest_framework.validators import ValidationError
from django.utils.deconstruct import deconstructible


def ValidateImageFileExtension(file_obj):
        valid_extensions = ['.jpg', '.jpeg', '.png']
        extension = file_obj.name.split('.')[-1].lower()
        if extension not in valid_extensions:
            raise ValidationError("Only JPG, JPEG, and PNG files are allowed.")

def ValidateimageSize(file_obj):
    if file_obj.size > 10000000:
        raise ValidationError("File exceeds Size limit")