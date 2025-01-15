from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('dispensing_operations_app.urls')),
]
