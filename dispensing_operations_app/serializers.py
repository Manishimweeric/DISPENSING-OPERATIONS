from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:            
            try:                    
                    user = User.objects.get(email=email)
            except User.DoesNotExist:
                    raise ValidationError("Invalid email or password.")
            if not check_password(password, user.password):
                raise ValidationError("Invalid email or password.")
        else:
            raise ValidationError("Both email or phone number and password are required.")
        
        data['user'] = user
        return data
    
class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class OilTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OilType
        fields = '__all__'       

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

        
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CalibrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calibration
        fields = '__all__'

class CustomerDetailSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomerDetail
        fields = '__all__'

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None