from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/', include('customers.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('products.urls')),
    path('api/', include('sales.urls')),
    path('api/', include('stock.urls')),
    path('admin/', admin.site.urls),

    # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),

]
