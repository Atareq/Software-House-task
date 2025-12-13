from rest_framework import viewsets
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