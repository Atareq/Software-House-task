from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions_helper import AdminPermission, SalesReadOnly

from .models import StockMovement
from .serializers import StockMovementReadOnlySerializer


class StockMovementViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = StockMovement.objects.select_related("product", "user").all()
    serializer_class = StockMovementReadOnlySerializer
    permission_classes = (IsAuthenticated, AdminPermission | SalesReadOnly)
