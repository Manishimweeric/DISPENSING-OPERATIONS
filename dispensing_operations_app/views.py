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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

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
    """
    Handles both listing and creating customers.
    GET: Returns all customers or filters by user_id if provided.
    POST: Creates a new customer associated with the logged-in user.
    """
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """
        Filters the queryset based on the user_id query parameter if provided.
        If no user_id is provided, it returns all customers.
        """
        user_id = self.request.query_params.get('user_id', None)

        if user_id:
            queryset = Customer.objects.filter(user_id=user_id)
            if not queryset.exists():
                raise NotFound(f"No customers found for user ID {user_id}")
            return queryset

        return Customer.objects.all()

    def perform_create(self, serializer):
        """
        Automatically associates the created customer with the logged-in user.
        """
        serializer.save()
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

    def get_queryset(self):
        station_id = self.request.query_params.get('station_id', None)
        if station_id:
            return Maintenance.objects.filter(station_id=station_id)
        return Maintenance.objects.all()
    def post(self, serializer):
        calibration_id = self.request.data.get('Calibration')
        if Maintenance.objects.filter(Calibration=calibration_id).exists():
            return Response({
                'error': 'A maintenance record with this calibration already Schedured.'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

    def put(self, request, *args, **kwargs):
        maintenance_id = kwargs.get('pk')
        maintenance = get_object_or_404(Maintenance, pk=maintenance_id)
        serializer = self.serializer_class(maintenance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

# Order Views
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
@api_view(['GET'])
def get_dashboard_stats(request):
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)
    
    stats = {
        'total_customers': Customer.objects.filter(is_active=True).count(),
        'total_stations': Station.objects.filter(status='active').count(),
        'total_users': User.objects.filter(is_active=True).count(),
        'total_oil_types': OilType.objects.filter(status='active').count(),
        'total_stock': Stock.objects.filter(status='active').aggregate(total=Sum('quantity'))['total'] or 0,
        'sales_by_oil_type': list(Customer.objects.values('oil_type__name').annotate(total_sales=Sum('quantity')).order_by('-total_sales')),
        'recent_maintenance': Maintenance.objects.filter(status='active').order_by('-created_at')[:5].values(),
        'orders_by_station': list(Order.objects.values('station__name').annotate(total_orders=Count('id')).order_by('-total_orders')),
        'stock_by_oil_type': list(Stock.objects.filter(status='active').values('oil_type__name', 'quantity')),
        'recent_customers': list(Customer.objects.filter(is_active=True).order_by('-created_at')[:5].values('name', 'plate_number', 'quantity', 'oil_type__name')),
    }
    return Response(stats)


@api_view(['GET'])
def get_sales_trends(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_sales = Customer.objects.filter(
        created_at__gte=thirty_days_ago,
        is_active=True
    ).extra(select={'date': 'DATE(created_at)'}).values('date').annotate(total_quantity=Sum('quantity')).order_by('date')
    return Response(list(daily_sales))

class MonthlyDataView(APIView):
    def get(self, request):
        # Aggregate monthly data for customers
        customers = Customer.objects.values('created_at__month').annotate(
            total_quantity=Sum('quantity')
        )

        # Aggregate monthly data for stock
        stocks = Stock.objects.values('created_at__month').annotate(
            total_stock=Sum('quantity')
        )

        # Combine customer and stock data
        combined_data = []
        months = set([c['created_at__month'] for c in customers] + [s['created_at__month'] for s in stocks])
        for month in months:
            combined_data.append({
                'month': month,
                'Customers': next((c['total_quantity'] for c in customers if c['created_at__month'] == month), 0),
                'Inventory': next((s['total_stock'] for s in stocks if s['created_at__month'] == month), 0),
            })

        return Response(combined_data, status=status.HTTP_200_OK)


class CalibrationView(APIView):
    def get(self, request):
        station_id = request.query_params.get("station_id", None)
        if station_id:
            calibrations = Calibration.objects.filter(station_id=station_id)
            serializer = CalibrationSerializer(calibrations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        calibrations = Calibration.objects.all()
        serializer = CalibrationSerializer(calibrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CalibrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk=None):
        """ 
        Updates a specific calibration record.
        """
        calibration = get_object_or_404(Calibration, pk=pk)
        serializer = CalibrationSerializer(calibration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomerDetailListCreateView(generics.ListCreateAPIView):
    queryset = CustomerDetail.objects.all()
    serializer_class = CustomerDetailSerializer
    parser_classes = [MultiPartParser, FormParser]  # Allow file uploads

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    