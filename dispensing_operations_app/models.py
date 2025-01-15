from django.db import models

# Station Model
class Station(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# User Model
class User(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=30, blank=True, null=True,default="user")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    plate_number = models.CharField(max_length=50)
    date = models.DateField()
    status = models.CharField(max_length=50)
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# OilType Model
class OilType(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Stock Model
class Stock(models.Model):
    quantity = models.IntegerField()
    price_per_litre = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=50)
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)

    def __str__(self):
        return f"Stock of {self.oil_type.name}"

# Maintenance Model
class Maintenance(models.Model):
    description = models.TextField()
    maintainer = models.CharField(max_length=150)
    date = models.DateField()
    status = models.CharField(max_length=50)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)

    def __str__(self):
        return f"Maintenance by {self.maintainer}"

# Order Model
class Order(models.Model):
    name = models.CharField(max_length=150)
    date = models.DateField()
    status = models.CharField(max_length=50)
    oil_type = models.ForeignKey('OilType', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
