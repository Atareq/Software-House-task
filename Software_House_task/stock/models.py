from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product

User = get_user_model()


class MovementType(models.TextChoices):
    ORDER_CONFIRMED = "ORDER_CONFIRMED", "Order Confirmed"
    ORDER_CANCELLED = "ORDER_CANCELLED", "Order Cancelled"


class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()  # positive or negative in case of order returns

    movement_type = models.CharField(
        max_length=50,
        choices=MovementType.choices
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.sku} - {self.qty} ({self.movement_type})"
