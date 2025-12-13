import uuid

from django.db import models
from safedelete.models import SafeDeleteModel


class Customer(SafeDeleteModel):
    customer_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField()

    opening_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    def save(self, *args, **kwargs):
        if not self.customer_code:
            self.customer_code = f"CUST-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} - {self.customer_code}"
