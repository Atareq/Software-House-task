from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions_helper import (AdminPermission,
                                     SalesCreateAndReadOnlyPermission)

from .models import Order
from .serializers import (DashboardSerializer, DateRangeSerializer,
                          OrderSerializer)
from .services import export_sales_orders_excel, get_dashboard_metrics


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, AdminPermission |
                          SalesCreateAndReadOnlyPermission)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'customer__name', 'created_by__username']
    search_fields = ['order_number', 'customer__name']
    ordering_fields = ['order_date', 'order_number', 'status']
    ordering = ['-order_date']


class SalesExcelExportAPIView(APIView):
    permission_classes = (IsAuthenticated, AdminPermission)

    def get(self, request):
        serializer = DateRangeSerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        return export_sales_orders_excel(
            start_date=data["start_date"],
            end_date=data["end_date"],
        )


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated, AdminPermission]

    def get(self, request):
        date_serializer = DateRangeSerializer(data=request.query_params)
        date_serializer.is_valid(raise_exception=True)
        data = get_dashboard_metrics(
            from_date=date_serializer.validated_data["start_date"],
            to_date=date_serializer.validated_data["end_date"],
        )

        serializer = DashboardSerializer(data)
        return Response(serializer.data)
