from django.conf import settings
from django.conf.urls.static import static
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
    path('dashboard/stats/', views.get_dashboard_stats, name='get_dashboard_stats'),
    path('dashboard/sales-trends/', views.get_sales_trends, name='get_sales_trends'),
    path('calibrations/', CalibrationView.as_view(), name='calibration-list-create'),
    path('calibrations/<int:pk>/', CalibrationView.as_view(), name='calibration-detail'),
    path('maintenance/<int:pk>/', MaintenanceListCreateView.as_view(), name='maintenance-detail'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('customersdata/<int:pk>/', CustomerListCreateView.as_view(), name='customer-update'),
    path('Stocks/<int:pk>/', StockListCreateView.as_view(), name='Stocks-update'),







    path('customer-details/', CustomerDetailListCreateView.as_view(), name='customer-detail-list-create'),
    path('customer-details/', CustomerDetailListCreateView.as_view(), name='customer-detail-list-by_customer'),
    # path('customer-details/<int:pk>/', CustomerDetailRetrieveUpdateView.as_view(), name='customer-detail-retrieve-update'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    