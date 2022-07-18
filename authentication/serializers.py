from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError


from .models import User



class customTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        ctx={
            'RefreshToken': RefreshToken.for_user(user)
        }
        return ctx

    @classmethod
    def validate(self, attrs):
        data = {}
        email_or_username = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email_or_username, password=password)
        if email_or_username and password:
            if user:
                if not user.is_active:
                    msg = ('User account is disabled.')
                    raise exceptions.ValidationError(msg)
                if not user.email_verified:
                    msg = ('Please verify your email.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = ('Unable to log in with given credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = ('Must include "email" and "password"')
            raise exceptions.ValidationError(msg)
        data_get_token = self.get_token(user)
        refresh = data_get_token.get('RefreshToken', '')
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')