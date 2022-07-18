from django.urls import path

from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *
from .serializers import customTokenObtainPairSerializer

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(serializer_class=customTokenObtainPairSerializer)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', Signup.as_view(), name='signup'),
    path('verify-email/<str:token>/', VerifyEmail.as_view(), name='verify_email'),
    path('user/', UserAPI.as_view(), name='load_user'),
    
    
]
