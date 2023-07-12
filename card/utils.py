# Standard library imports
from io import BytesIO

# Third-party imports
import qrcode
from django.core.files.base import ContentFile
from django.utils.text import slugify


def generate_qr_code(data):
    vcard = f"BEGIN:VCARD\nVERSION:3.0\n" \
            f"N:{data['last_name']};{data['first_name']}\n" \
            f"EMAIL:{data['email']}\n" \
            f"TEL:{data['phone_number']}\n" \
            f"ORG:{'AFEX'}\n" \
            f"TITLE:{data['role']}\n" \
            f"END:VCARD"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    png_io = BytesIO()
    qr_img.save(png_io, format='PNG')
    qr_code = ContentFile(png_io.getvalue(), f"{slugify(data['email'])}.png")
    return qr_code
