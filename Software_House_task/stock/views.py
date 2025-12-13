from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from core.permissions_helper import AdminPermission, SalesReadOnly

from .models import StockMovement
from .serializers import StockMovementReadOnlySerializer


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockMovement.objects.select_related("product", "user").all()
    serializer_class = StockMovementReadOnlySerializer
    permission_classes = (IsAuthenticated, AdminPermission | SalesReadOnly)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product__sku', 'movement_type', 'user__username']
    search_fields = ['product__name', 'product__sku', 'user__username']
    ordering_fields = ['timestamp', 'product__sku', 'user__username']
    ordering = ['-timestamp']
