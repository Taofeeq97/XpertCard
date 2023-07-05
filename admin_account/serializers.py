from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomAdminUser
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.encoding import force_str

class CreateCustomAdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomAdminUser
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'profile_picture', 'password']

    def validate_email(self, value):
        if not value.endswith(('afexafricaexchange.com', 'afexafrica', 'afexnigeria.com')):
            raise serializers.ValidationError('Invalid email format')
        return value

    def validate(self, data):
        password = data['password']
        confirm_password = self.context['request'].data['password2']
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['username'] = validated_data['email']
        user = CustomAdminUser(**validated_data)
        user.set_password(password)
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return token

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = CustomAdminUser.objects.filter(email=email).first()
        
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Invalid login credentials')
        
        token = self.get_token(user)
        response = {
            'email': email,
            'token': token,
        }
        return response
    

class EmailResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate_email(self, value):
        lower_email = value.lower()
        return lower_email
    

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs



    


