# Python standard library imports
import random
import string
import threading

# Django imports
from django.core.mail import send_mail

# Third-party imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView

# Local imports
from Expertcard.settings import EMAIL_HOST_USER
from .models import CustomAdminUser
from .serializers import (
    CreateCustomAdminUserSerializer,
    EmailResetPasswordSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
)
from .tasks import send_email_fun
from .utils import clear_verification_code



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
    

class ForgotPasswordApiView(APIView):
    """
    An endpoint to generate a verification code
    """
    serializer_class = EmailResetPasswordSerializer

    def clear_verification_code(self, user):
        user.verification_code = ''
        user.save()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if CustomAdminUser.objects.filter(email__exact=email).exists():
                user = CustomAdminUser.objects.get(email=email)

                verification_code = ''.join(random.choices(string.digits, k=6))
                print(verification_code)
                user.verification_code = int(verification_code)
                user.save()

                # Set a timer for 1 minute
                timer = threading.Timer(300, self.clear_verification_code, args=[user])
                timer.start()

                # Send the verification code to the user's email
                mail_subject = "Password Reset Verification Code"
                message = f"Hi {user.username},\n\n" \
                          f"Please use the following verification code to reset your password: {verification_code}"
                send_mail(subject=mail_subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[user.email])

                return Response({
                    "status": "success",
                    "message": "We have sent a password-reset verification code to the email you provided. Please check and reset, kindly do so within 3 minute as the OTP expires."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "error",
                    "message": "The email provided doesn't exist"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyVerificationCode(APIView):
    """
    An endpoint to verify the verification code

    """

    def post(self, request, *args, **kwargs):
        verification_code = request.data.get('verification_code')
        print(verification_code)
        try:
            user = CustomAdminUser.objects.get(verification_code=verification_code)
            print(user)
        except CustomAdminUser.DoesNotExist:
            return Response({"status": "fail", "message": "Invalid or Expired verification code"}, status=status.HTTP_400_BAD_REQUEST)
        # Reset the verification code after successful verification
        user.verification_code = ''
        user.save()
        return Response({"status": "success", "message": "Verification code is valid"}, status=status.HTTP_200_OK)


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
        print(user)
        user.save()   
        print(user)
        return Response({"status": "success", "message": "Password set successfully"}, status=status.HTTP_200_OK)

        
