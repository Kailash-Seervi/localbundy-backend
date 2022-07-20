from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from .models import User
from .utils import Util
from .serializers import UserSerializer

class Signup(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('username',None)

        user  = User.objects.filter(email=email)
        if user.exists():
            return Response(
                {"success": False, "message": "User with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not name:
            name=email
        
        user = User.objects.create(email=email, password=password, username=name)
        user.set_password(password)
        user.save()
        current_site = settings.FRONTEND_URL
        relativeLink = settings.FRONTEND_EMAIL_VERIFY_URL
        
        token = RefreshToken.for_user(user).access_token
        absurl = 'http://'+current_site+relativeLink+str(token)+"/"
        print(absurl)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)

        return Response({"success": True, "message": "User successfully created!. Please check your email for verification "})

class VerifyEmail(APIView):

    def post(self, request):
        token = request.data.get('token','')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256", "HS384", "HS512"])
            print(payload)
            try:
                user = User.objects.get(id=payload['user_id'])
            except User.DoesNotExist:
                return Response({"success": False, "message": "User Doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
            if not user.email_verified:
                user.email_verified = True
                user.save()
            return Response({"success": True, "message": "Email verified"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({"success": False, "message": "Token Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({"success": False, "message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationToken(APIView):

    def post(self, request):
        email = request.data.get('email', None)
        if not email:
            return Response({"success": False, "message": "Please enter a valid email"})
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User not registered"})
        
        if not user.email_verified:
            current_site = settings.FRONTEND_URL
            relativeLink = settings.FRONTEND_EMAIL_VERIFY_URL
            
            token = RefreshToken.for_user(user).access_token
            absurl = 'http://'+current_site+relativeLink+str(token)+"/"
            print(absurl)
            email_body = 'Hi '+user.username + \
                ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_email(data)
            return Response({"success": True, "message": "Verification email sent!"})
        
        return Response({"success": True, "message": "Email already verified!"})


class UserAPI(RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user