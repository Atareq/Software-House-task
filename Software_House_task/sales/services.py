from rest_framework.exceptions import ValidationError

from sales.models import OrderStatus
from stock.models import MovementType, StockMovement


def check_order_update_allowed(old_status, new_status):
    allowed_transitions = {
        OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.CANCELLED],
        OrderStatus.CANCELLED: [],
    }

    if new_status not in allowed_transitions.get(old_status, []):
        raise ValidationError(
            f"Invalid status transition from {old_status} to {new_status}"
        )
    return new_status


def handle_order_stock_transition(order, old_status, new_status, user):
    if old_status == OrderStatus.PENDING and new_status == OrderStatus.CONFIRMED:
        _reduce_stock(order, user)

    elif old_status == OrderStatus.CONFIRMED and new_status ==\
            OrderStatus.CANCELLED:
        _restore_stock(order, user)

    elif old_status == new_status == OrderStatus.PENDING:
        pass

    else:
        raise ValidationError(
            f"Invalid status transition from {old_status} to {new_status}"
        )


def _reduce_stock(order, user):
    for item in order.items.select_related("product"):
        product = item.product

        if product.stock_qty < item.qty:
            raise ValidationError(
                f"Insufficient stock for product {product.name} SKU: "
                f"{product.sku}"
            )

        product.stock_qty -= item.qty
        product.save()
        StockMovement.objects.create(
            product=product,
            qty=-item.qty,
            user=user,
            movement_type=MovementType.ORDER_CONFIRMED,
        )


def _restore_stock(order, user):
    for item in order.items.select_related("product"):
        product = item.product

        product.stock_qty += item.qty
        product.save()

        StockMovement.objects.create(
            product=product,
            qty=item.qty,
            user=user,
            movement_type=MovementType.ORDER_CANCELLED,
        )
