from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('stations/', StationListCreateView.as_view(), name='station-list-create'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('oiltypes/', OilTypeListCreateView.as_view(), name='oiltype-list-create'),
    path('stocks/', StockListCreateView.as_view(), name='stock-list-create'),
    path('maintenance/', MaintenanceListCreateView.as_view(), name='maintenance-list-create'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
<<<<<<< HEAD
    path('dashboard/stats/', views.get_dashboard_stats, name='get_dashboard_stats'),
    path('dashboard/sales-trends/', views.get_sales_trends, name='get_sales_trends'),
    
=======
    path('monthly-data/', MonthlyDataView.as_view(), name='monthly-data'),
>>>>>>> 0d47ed615e2d7243eafbabb3fe517c5e73c77309
]

    