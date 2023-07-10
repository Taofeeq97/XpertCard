import re
from rest_framework.validators import ValidationError


def ValidateimageSize(file_obj):
    if file_obj.size > 10000000:
        raise ValidationError("File exceeds Size limit")  

def validate_image_extension(value):
    allowed_extensions = ['png', 'jpeg', 'jpg']
    pattern = r'^.+\.({})$'.format('|'.join(allowed_extensions))
    if not re.match(pattern, value.name):
        raise ValidationError("Invalid file extension. Allowed extensions are: {}.".format(", ".join(allowed_extensions)))
