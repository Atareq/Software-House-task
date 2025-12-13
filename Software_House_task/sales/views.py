from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions_helper import (AdminPermission,
                                     SalesCreateAndReadOnlyPermission)

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, AdminPermission |
                          SalesCreateAndReadOnlyPermission)
