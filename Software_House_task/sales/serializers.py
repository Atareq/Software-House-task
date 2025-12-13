from datetime import date

from django.db import transaction
from rest_framework import serializers

from products.serializers import ProductSerializer
from sales.services import handle_order_stock_transition

from .models import Order, OrderItem, OrderStatus
from .services import check_order_update_allowed


class OrderItemSerializer(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "qty",
            "price",
            "total",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer",
            "order_date",
            "created_by",
            "status",
            "items",
            "total_amount",
        ]
        read_only_fields = ["order_number", "order_date", "created_by"]

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        request = self.context["request"]

        order = Order.objects.create(
            created_by=request.user,
            **validated_data
        )
        items = [
            OrderItem(order=order, **item)
            for item in items_data
        ]
        OrderItem.objects.bulk_create(items)

        if order.status == OrderStatus.CONFIRMED:
            handle_order_stock_transition(order,  OrderStatus.PENDING,
                                          order.status, request.user)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        old_status = instance.status
        validated_data.pop("items")

        new_status = check_order_update_allowed(
            old_status, validated_data.get("status", old_status))

        # The only allowed changes in case of order is confirmed/cancelled
        # Is status field
        if old_status != OrderStatus.PENDING:
            validated_data = {"status": new_status}

        instance = super().update(instance, validated_data)
        if old_status != new_status:
            handle_order_stock_transition(
                order=instance,
                old_status=old_status,
                new_status=new_status,
                user=self.context["request"].user,
            )

        return instance


class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField(
        format="%Y-%m-%d", input_formats=["%Y-%m-%d"], required=False
    )
    end_date = serializers.DateField(
        format="%Y-%m-%d", input_formats=["%Y-%m-%d"], required=False
    )

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")

        if start and end and start > end:
            raise serializers.ValidationError(
                "start_date must be before or equal to end_date"
            )

        if not start and not end:
            today = date.today()
            attrs["start_date"] = today
            attrs["end_date"] = today
        return attrs


class DashboardSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    total_customers = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    low_stock_products = ProductSerializer(many=True)
