from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('customers.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('products.urls')),
    path('api/', include('sales.urls')),
    path('api/', include('stock.urls')),
    path('admin/', admin.site.urls),
]
