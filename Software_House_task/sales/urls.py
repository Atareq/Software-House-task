from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DashboardAPIView, OrderViewSet, SalesExcelExportAPIView

router = DefaultRouter()
router.register(r'sales/orders', OrderViewSet, basename='sales-order')


urlpatterns = [
    path("sales/orders/export/", SalesExcelExportAPIView.as_view(),
                                            name="export-sales-excel"),
    path("sales/dashboard/", DashboardAPIView.as_view(), name="dashboard"),

]

urlpatterns += router.urls
