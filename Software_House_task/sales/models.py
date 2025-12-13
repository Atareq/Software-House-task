import uuid

from django.contrib.auth import get_user_model
from django.db import models
from safedelete.models import SafeDeleteModel

from customers.models import Customer
from products.models import Product

User = get_user_model()


def generate_order_number():
    return str(uuid.uuid4())[:20]


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"


class Order(SafeDeleteModel):
    order_number = models.CharField(max_length=20, unique=True,
                                    default=generate_order_number)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    @property
    def total_amount(self):
        return sum(item.total for item in self.items.all())


class OrderItem(SafeDeleteModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.qty * self.price
