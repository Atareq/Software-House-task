from django.db import transaction
from rest_framework import serializers

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
