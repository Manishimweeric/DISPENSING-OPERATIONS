from django.db import models
from datetime import datetime

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
class Customer(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    plate_number = models.CharField(max_length=50)
    created_at = models.CharField(max_length=20, default=get_default_datetime)  # Default value
    Method = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

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
    status = models.CharField(max_length=50, default="active")
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)

    def __str__(self):
        return f"Stock of {self.oil_type.name}"

# Maintenance Model
class Maintenance(models.Model):
    description = models.TextField()
    maintainer = models.CharField(max_length=150)
    created_at = models.CharField(max_length=20, default=get_default_datetime)  # Default value
    status = models.CharField(max_length=50, default="active")
    station = models.ForeignKey('Station', on_delete=models.CASCADE)

    def __str__(self):
        return f"Maintenance by {self.maintainer}"

# Order Model
class Order(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.CharField(max_length=20, default=get_default_datetime)  # Default value
    status = models.CharField(max_length=50, default="active")
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
