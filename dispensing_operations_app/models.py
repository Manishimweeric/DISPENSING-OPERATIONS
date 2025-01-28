from django.db import models
from datetime import datetime
import random

# Function to get the current date and time as a string
def get_default_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Station Model
class Station(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    created_at = models.CharField(max_length=20, default=get_default_datetime)  # Default value
    status = models.CharField(max_length=50, default="active")
    def __str__(self):
        return self.name

# User Model
class User(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=30, blank=True, null=True, default="user")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    station  = models.ForeignKey('Station', on_delete=models.CASCADE,null=True)
    created_at = models.CharField(max_length=20, default=get_default_datetime)

    def __str__(self):
        return self.name


def generate_random_id():
    # Generate a random 5-digit ID
    return str(random.randint(10000, 99999))

class Customer(models.Model):
    id = models.CharField(
        max_length=5,
        primary_key=True,
        default=generate_random_id,
        editable=False,  # Prevent users from editing this field
        unique=True
    )
    name = models.CharField(max_length=150)
    Phonenumber = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    quantity = models.IntegerField(null=True)
    created_at = models.CharField(max_length=20, default=get_default_datetime) 
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="1")

    def __str__(self):
        return self.name
    
class CustomerDetail(models.Model):
    Customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    plate_number = models.CharField(max_length=50, null=True)
    created_at = models.CharField(max_length=20, default=get_default_datetime)  # Default value
    Method = models.CharField(max_length=50, null=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="1")
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Customer} - {self.plate_number}"


    def __str__(self):
        return self.name    

# OilType Model
class OilType(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    status = models.CharField(max_length=50, default="active")

    def __str__(self):
        return self.name

# Stock Model
class Stock(models.Model):
    quantity = models.IntegerField()
    price_per_litre = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.CharField(max_length=20, default=get_default_datetime)  # Default value
    status = models.CharField(max_length=50, default="In Stock")
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)

    def __str__(self):
        return f"Stock of {self.oil_type.name}"

# Maintenance Model
class Maintenance(models.Model):
    report=models.CharField(max_length=255,null=True, blank=True)
    maintainer = models.CharField(max_length=150)
    Date= models.DateField()
    Time=models.TimeField(blank=True, null=True,max_length=30)    
    created_at = models.CharField(max_length=20, default=get_default_datetime) 
    status = models.CharField(max_length=50, default="active")
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    Calibration = models.ForeignKey('Calibration', on_delete=models.CASCADE)

    def __str__(self):
        return f"Maintenance by {self.maintainer}"

# Order Model
class Order(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.CharField(max_length=20, default=get_default_datetime)  
    status = models.CharField(max_length=50, default="active")
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Calibration(models.Model):
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    Date  = models.DateField(max_length=200)
    Time=models.TimeField(blank=True, null=True,max_length=30)
    report=models.CharField(max_length=255,null=True, blank=True)
    status = models.CharField(max_length=50,default="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
