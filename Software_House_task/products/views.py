from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions_helper import AdminPermission, SalesReadOnly

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, SalesReadOnly | AdminPermission)
