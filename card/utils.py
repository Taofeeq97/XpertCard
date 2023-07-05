import qrcode
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify

def generate_qr_code(data):
    qr_code_data = f"First Name: {data['first_name']}\n" \
                   f"Last Name: {data['last_name']}\n" \
                   f"Email: {data['email']}\n" \
                   f"City: {data['city']}\n" \
                   f"Country: {data['country']}\n" \
                   f"Phone Number: {data['phone_number']}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    png_io = BytesIO()
    qr_img.save(png_io, format='PNG')
    qr_code = ContentFile(png_io.getvalue(), f"{slugify(data['email'])}.png")
    return qr_code
