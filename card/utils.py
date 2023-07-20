# import qrcode
# from io import BytesIO
# from django.core.files.base import ContentFile
# from django.utils.text import slugify


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
from rest_framework.reverse import reverse


def generate_qr_code(expert_card_id, request):
    vcard_url = request.build_absolute_uri(reverse('vcard_view', kwargs={'pk': expert_card_id}))
    print(vcard_url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard_url)  # Use the URL of the vCard view as the QR code data
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to a file
    png_io = BytesIO()
    qr_img.save(png_io, format='PNG')
    qr_code_image = ContentFile(png_io.getvalue(), f"qr_code_{expert_card_id}.png")

    return qr_code_image


