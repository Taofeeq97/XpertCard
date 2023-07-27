# from elasticsearch import Elasticsearch

# es = Elasticsearch(['http://localhost:9200'], http_auth=('elastic', '7PeMZZH7haepPZTxMBpP'))

# # Define the index settings and mappings
# index_settings = {
#     'settings': {
#         'number_of_shards': 1,
#         'number_of_replicas': 0
#     },
#     'mappings': {
#         'properties': {
#             'first_name': {'type': 'text'},
#             'last_name': {'type': 'text'},
#             'email': {'type': 'text'},
#             'profile_picture': {'type': 'keyword'},
#             'role': {'type': 'text'},
#             'qr_code': {'type': 'keyword'},
#             'tribe': {'type': 'text'},
#             'company_address': {'type': 'nested'},
#             'card_type' : {'type': 'text'},
#             'phone_number': {'type': 'text'},
# #             'is_active': {'type': 'boolean'},
# #             'is_deleted': {'type': 'boolean'}
# #         }
# #     }
# # }

# # # Create the index
# # response = es.indices.create(index='card_el_index', body=index_settings)

# # # Check if the index creation was successful
# # if response['acknowledged']:
# #     print(f"The index card_el_index was created successfully.")
# # else:
# #     print(f"Failed to create the index card_el_index.")
# import qrcode
# from io import BytesIO
# from django.core.files.base import ContentFile
# from django.utils.text import slugify


# import qrcode
# from io import BytesIO
# from django.core.files.base import ContentFile
# from django.utils.text import slugify

# def generate_qr_code():
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )

#     fiverr_url = "https://www.fiverr.com/s/DlAe1P"

#     qr.add_data(fiverr_url)
#     qr.make(fit=True)
#     qr_img = qr.make_image(fill_color="black", back_color="white")

#     # Save QR code image to a file
#     png_io = BytesIO()
#     qr_img.save(png_io, format='PNG')
   

#     # Print the QR code image
#     qr_img.show()
#     print('yess')

# generate_qr_code()

# give an array of k sort the array  by the least repeated integers if the multiple integer habve thesame numbr occurence  sort them in descendin order return the final array

# input  : k = [-1,1,-6,4,5, -6, 1,4,1]
# output : [5,-1,4,4, -6, -6, 1,1,1]

# 1 <= k.length <= 100
# -100 <= k[i] <= 100
# import typing

# def solution(k:[int]) -> [int]:
#     #write something here
#     res = []
#     return res

# # do not change the code bellow
# if __name__=='__main__':
#     line = input()
#     k =line.strip().split()
#     k = [int (x) for x in k]
#     output = solution(k)
#     if output == []:
#         print('[]')
#     else:
#         print('[%s]' % ','.join(map(str, output)))
