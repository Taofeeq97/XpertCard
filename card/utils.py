import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify


# def generate_qr_code(data):
#     vcard = f"BEGIN:VCARD\nVERSION:3.0\n" \
#             f"N:{data['last_name']};{data['first_name']}\n" \
#             f"EMAIL:{data['email']}\n" \
#             f"TEL:{data['phone_number']}\n" \
#             f"ORG:{'AFEX,' + data['address_title']}\n" \
#             f"TITLE:{data['role']}\n" \
#             f"END:VCARD"
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(vcard)
#     qr.make(fit=True)
#     qr_img = qr.make_image(fill_color="black", back_color="white")
#     png_io = BytesIO()
#     qr_img.save(png_io, format='PNG')
#     qr_code = ContentFile(png_io.getvalue(), f"{slugify(data['email'])}.png")
#     return qr_code


import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify

def create_vcf_file(data):
    vcard = f"BEGIN:VCARD\nVERSION:3.0\n" \
            f"N:{data['last_name']};{data['first_name']}\n" \
            f"EMAIL:{data['email']}\n" \
            f"TEL:{data['phone_number']}\n" \
            f"ORG:AFEX,{data['address_title']}\n" \
            f"TITLE:{data['role']}\n" \
            f"END:VCARD"
    return vcard.encode('utf-8')  # Encode the string as bytes

def generate_qr_code(data):
    vcard_content = create_vcf_file(data)

    # Save the vCard (.vcf) data to a file
    vcard_file = ContentFile(vcard_content, f"{slugify(data['email'])}.vcf")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Get the full absolute URL for the .vcf file
    vcf_url = f"https://xpertcards-bucket.s3.amazonaws.com/media/{slugify(data['email'])}.vcf"

    qr.add_data(vcf_url)  # Use the full absolute URL as the QR code data
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to a file
    png_io = BytesIO()
    qr_img.save(png_io, format='PNG')
    qr_code_image = ContentFile(png_io.getvalue(), f"{slugify(data['email'])}.png")

    return qr_code_image, vcard_file



