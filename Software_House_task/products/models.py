from django.db import models
from safedelete.models import SafeDeleteModel


class Product(SafeDeleteModel):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, null=True)
    # pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    # inventory
    stock_qty = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sku} - {self.name}"
