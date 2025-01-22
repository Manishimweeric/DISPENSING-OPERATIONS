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
from rest_framework.exceptions import NotFound

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
    serializer_class = CustomerSerializer
    def get_queryset(self):
        """
        Filters the queryset based on the user_id query parameter if provided.
        If no user_id is provided, it returns all customers.
        """
        user_id = self.request.query_params.get('user_id', None)

        # If a user_id is provided, filter the queryset by user_id
        if user_id:
            queryset = Customer.objects.filter(user_id=user_id)
            
            # If no customers are found for that user_id, raise a NotFound exception
            if not queryset.exists():
                raise NotFound(f"No customers found for user ID {user_id}")
            
            return queryset

        # If no user_id is provided, return all customers
        return Customer.objects.all()

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

