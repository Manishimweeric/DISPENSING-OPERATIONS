from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import AccessToken

class StationListCreateView(generics.ListCreateAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):

        email = serializer.validated_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        password = serializer.validated_data.get('password')
        hashed_password = make_password(password)

        user = serializer.save(password=hashed_password)  
        user.save()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_serializer = UserSerializer(user)
            access_token = AccessToken.for_user(user)

            return Response({
                "message": "Login successful",
                "user": user_serializer.data,
                "access_token": str(access_token),  # Return the access token
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# OilType Views
class OilTypeListCreateView(generics.ListCreateAPIView):
    queryset = OilType.objects.all()
    serializer_class = OilTypeSerializer

# Stock Views
class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

# Maintenance Views
class MaintenanceListCreateView(generics.ListCreateAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

# Order Views
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

