# Django imports
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail

# Third-party imports
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView

# Local imports
from .serializers import (
    LoginSerializer,
    CreateCustomAdminUserSerializer,
    EmailResetPasswordSerializer,
    ResetPasswordSerializer,
)
from .models import CustomAdminUser
from .tasks import send_email_fun

# Python standard library imports
import random
import string
import base64



# Create your views here.

class ObtainTokenPairApiView(TokenObtainPairView):
    """
    An endpoint to obtain Access token

    """
    serializer_class = LoginSerializer


class UserLoggoutApiView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, ):
        request.user.auth_token.delete()
        response = {
            "message": "User Logged Out Successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


class CreateAdminUserApiView(generics.CreateAPIView):
    """
    An endpoint to Create an Admin User

    """
    serializer_class = CreateCustomAdminUserSerializer
    queryset = CustomAdminUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer=serializer)
        response = {
            "message": "User Created Successfully"
        }
        return Response(response, status=status.HTTP_201_CREATED)
    

# class ForgotPasswordApiView(APIView):
#     serializer_class = ResetPasswordSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data= request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             if CustomAdminUser.objects.filter(email__exact=email).exists():
#                 user = CustomAdminUser.objects.get(email = email)
#                 uuidb64 = urlsafe_base64_encode(str(user.id).encode('utf-8'))
#                 generator = PasswordResetTokenGenerator()
#                 token = generator.make_token(user)
#                 current_site = get_current_site(request=request).domain
#                 relative_path = reverse("reset_password", kwargs={"uuidb64": uuidb64, "token": token})
#                 abs_url = request.scheme + "://" + current_site + relative_path
#                 mail_subject = "Please Reset your Account Password"
#                 message = "Hi" + user.username + "," + \
#                           " Please Use the Link below to reset your account password:" + "" + abs_url
#                 from_email = 'otutaiwo1@gmail.com'
#                 recipient_list = [user.email]
#                 send_mail(mail_subject, message, from_email, recipient_list)
#                 # Utils.send_email.delay(mail_subject, message, user.email)
#                 return Response({"status": "success",
#                                  "message": "We have sent a password-reset link to the email you provided. Please check and reset  "},status=status.HTTP_200_OK)
#             else:
#                 return Response({"status": "error", "message": "The email provided doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordApiView(APIView):

    """
    An endpoint to generate verification code

    """
    serializer_class = EmailResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if CustomAdminUser.objects.filter(email__exact=email).exists():
                user = CustomAdminUser.objects.get(email=email)
                
                # Generate a 6-character verification code
                verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                print(verification_code)
                user.verification_code =verification_code
                
                # Send the verification code to the user's email
                mail_subject = "Password Reset Verification Code"
                message = f"Hi {user.username},\n\n" \
                          f"Please use the following verification code to reset your password: {verification_code}"
                send_email_fun(subject=mail_subject, message = message, sender='otutaiwo1@gmail.com', receiver=user.email)
                return Response({"status": "success", "message": "We have sent a password-reset verification code to the email you provided. Please check and reset  "},status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "message": "The email provided doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# class ForgotPasswordApiView(APIView):

#     """
#     An endpoint to generate verification code

#     """
#     serializer_class = EmailResetPasswordSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             if CustomAdminUser.objects.filter(email__exact=email).exists():
#                 user = CustomAdminUser.objects.get(email=email)
                
#                 # Generate a 6-character verification code
#                 verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#                 print(verification_code)

#                 # Encode the user object to the verification code
#                 user_data = {
#                     'user_id': user.id,
#                     'verification_code': verification_code
#                 }
#                 encoded_user_data = base64.urlsafe_b64encode(str(user_data).encode()).decode()

#                 # Save the encoded verification code in the user model
#                 user.verification_code = verification_code
#                 user.encoded_user_data = encoded_user_data
#                 user.save()

                
#                 # Send the verification code to the user's email
#                 mail_subject = "Password Reset Verification Code"
#                 message = f"Hi {user.username},\n\n" \
#                           f"Please use the following verification code to reset your password: {verification_code}"
#                 send_email_fun(subject=mail_subject, message = message, sender='otutaofeeqi@gmail.com', receiver=user.email)
#                 return Response({"status": "success", "message": "We have sent a password-reset verification code to the email you provided. Please check and reset  "},status=status.HTTP_200_OK)
#             else:
#                 return Response({"status": "error", "message": "The email provided doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class VerifyVerificationCode(APIView):
#     """
#     An endpoint to verify the verification code

#     """

#     def post(self, request, *args, **kwargs):
#         verification_code = request.data.get('verification_code')
#         try:
#             user = CustomAdminUser.objects.get(verification_code=verification_code)
#         except CustomAdminUser.DoesNotExist:
#             return Response({"status": "fail", "message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
#         # Reset the verification code after successful verification
#         encoded_data = user.encoded_user_data
#         decoded_user_data = base64.urlsafe_b64decode(encoded_data).decode()
#         user_id = eval(decoded_user_data)
#         user.verification_code = ''
#         user.encoded_user_data = ''
#         user.save()
#         return Response({"status": "success", "message": "Verification code is valid"}, status=status.HTTP_200_OK)


class VerifyVerificationCode(APIView):
    """
    An endpoint to verify the verification code

    """

    def post(self, request, *args, **kwargs):
        verification_code = request.data.get('verification_code')
        try:
            user = CustomAdminUser.objects.get(verification_code=verification_code)
        except CustomAdminUser.DoesNotExist:
            return Response({"status": "fail", "message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
        # Reset the verification code after successful verification
        user.verification_code = ''
        user.save()
        return Response({"status": "success", "message": "Verification code is valid"}, status=status.HTTP_200_OK)


class SetPasswordApiView(generics.UpdateAPIView):
    serializer_class = ResetPasswordSerializer

    def update(self, request, *args, **kwargs):
        email = self.get_serializer['email']
        password = self.get_serializer['password']
        user = CustomAdminUser.objects.get(email = email)
        self.perform_update(user.set_password(password))
        response = {
            "message":"new password set successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


class SetPasswordApiView(generics.UpdateAPIView):

    """
    An endpoint to set new password

    """
    serializer_class = ResetPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        user = CustomAdminUser.objects.get(email=email)
        user.set_password(new_password)
        user.save()   
        return Response({"status": "success", "message": "Password set successfully"}, status=status.HTTP_200_OK)

        
