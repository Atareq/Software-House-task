from rest_framework import serializers

from .models import StockMovement


class StockMovementReadOnlySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name", read_only=True
    )
    user_username = serializers.CharField(
        source="user.username", read_only=True
    )

    class Meta:
        model = StockMovement
        fields = [
            "id",
            "product",
            "product_name",
            "qty",
            "movement_type",
            "user",
            "user_username",
            "timestamp",
        ]
        read_only_fields = fields
