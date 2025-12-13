from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from core.permissions_helper import (AdminPermission,
                                     SalesCreateAndReadOnlyPermission)

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,
                          SalesCreateAndReadOnlyPermission | AdminPermission)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer_code', 'name', 'phone']
    search_fields = ['customer_code', 'name', 'email', 'phone']
    ordering_fields = ['id', 'name', 'customer_code']
    ordering = ['id']
